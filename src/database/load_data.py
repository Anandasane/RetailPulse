
import logging
from pathlib import Path

import pandas as pd
from sqlalchemy import text

from config.database import get_engine


# ============================================
# 1. PROJECT CONFIGURATION
# ============================================

DATASETS = {
    "fact_sales": Path("data/processed/cleaned_transactions.csv"),
    "fact_returns": Path("data/processed/returns.csv"),
    "fact_cancelled": Path(
        "data/processed/cancelled_transactions.csv"
    ),
    "rejected_records": Path(
        "data/processed/rejected_records.csv"
    )
}

CHUNK_SIZE = 5000
INSERT_CHUNK_SIZE = 1000

REPORT_DIR = Path("reports")
REPORT_DIR.mkdir(parents=True, exist_ok=True)

REPORT_FILE = REPORT_DIR / "database_load_report.csv"


# ============================================
# 2. COLUMN MAPPING
# ============================================

COLUMN_MAPPING = {
    "InvoiceNo": "invoice_no",
    "StockCode": "stock_code",
    "Description": "description",
    "Quantity": "quantity",
    "InvoiceDate": "invoice_date",
    "UnitPrice": "unit_price",
    "CustomerID": "customer_id",
    "Country": "country",
    "Revenue": "revenue"
}

EXPECTED_SOURCE_COLUMNS = set(COLUMN_MAPPING.keys())

EXPECTED_DB_COLUMNS = set(COLUMN_MAPPING.values())


# ============================================
# 3. LOGGING CONFIGURATION
# ============================================

logger = logging.getLogger("RetailPulse.Database")


# ============================================
# 4. CSV FILE VALIDATION
# ============================================

def validate_csv(file_path):
    """
    Validate CSV existence, file size,
    and expected column structure.
    """

    file_path = Path(file_path)

    if not file_path.exists():
        raise FileNotFoundError(
            f"CSV file not found: {file_path}"
        )

    if file_path.stat().st_size == 0:
        raise ValueError(
            f"CSV file is empty: {file_path}"
        )

    try:
        actual_columns = set(
            pd.read_csv(file_path, nrows=0).columns
        )

    except Exception as error:
        raise ValueError(
            f"Unable to read CSV file: {file_path}"
        ) from error

    if actual_columns != EXPECTED_SOURCE_COLUMNS:

        missing_columns = (
            EXPECTED_SOURCE_COLUMNS - actual_columns
        )

        unexpected_columns = (
            actual_columns - EXPECTED_SOURCE_COLUMNS
        )

        raise ValueError(
            f"Invalid CSV schema: {file_path}\n"
            f"Missing columns: {missing_columns}\n"
            f"Unexpected columns: {unexpected_columns}"
        )

    logger.info("CSV validation passed: %s", file_path)

    return True


# ============================================
# 5. DATA PREPARATION
# ============================================

def prepare_chunk(chunk):
    """
    Rename columns and convert values
    into database-compatible data types.
    """

    chunk = chunk.rename(
        columns=COLUMN_MAPPING
    ).copy()

    # Convert invoice date.
    chunk["invoice_date"] = pd.to_datetime(
        chunk["invoice_date"],
        errors="coerce"
    )

    # Convert numeric columns.
    for column in [
        "quantity",
        "unit_price",
        "revenue"
    ]:

        chunk[column] = pd.to_numeric(
            chunk[column],
            errors="coerce"
        )

    # Preserve identifiers as strings.
    for column in [
        "invoice_no",
        "stock_code",
        "customer_id"
    ]:

        chunk[column] = (
            chunk[column]
            .astype("string")
        )

    # Normalize text columns.
    for column in [
        "description",
        "country"
    ]:

        chunk[column] = (
            chunk[column]
            .astype("string")
        )

    # Convert pandas missing values to None
    # for text and identifier fields.
    for column in [
        "invoice_no",
        "stock_code",
        "customer_id",
        "description",
        "country"
    ]:

        chunk[column] = (
            chunk[column]
            .astype(object)
            .where(chunk[column].notna(), None)
        )

    return chunk


# ============================================
# 6. LOAD CSV INTO MYSQL
# ============================================

def load_csv_to_mysql(engine, table_name, file_path):
    """
    Load a CSV file into MySQL in chunks.

    Existing table data is replaced using
    a transactional full refresh.
    """

    file_path = Path(file_path)

    # Validate before modifying the table.
    validate_csv(file_path)

    logger.info(
        "Starting database load: %s",
        table_name
    )

    total_rows = 0

    # One transaction per table.
    with engine.begin() as connection:

        # Full refresh.
        connection.execute(
            text(f"DELETE FROM `{table_name}`")
        )

        # Read CSV in chunks.
        for chunk_number, chunk in enumerate(
            pd.read_csv(
                file_path,
                chunksize=CHUNK_SIZE,
                dtype={
                    "InvoiceNo": "string",
                    "StockCode": "string",
                    "CustomerID": "string"
                }
            ),
            start=1
        ):

            prepared_chunk = prepare_chunk(chunk)

            actual_columns = set(
                prepared_chunk.columns
            )

            if actual_columns != EXPECTED_DB_COLUMNS:

                raise ValueError(
                    f"Database column mismatch "
                    f"for table {table_name}"
                )

            prepared_chunk.to_sql(
                name=table_name,
                con=connection,
                if_exists="append",
                index=False,
                method=None,
                chunksize=INSERT_CHUNK_SIZE
            )

            rows_loaded = len(prepared_chunk)

            total_rows += rows_loaded

            logger.info(
                "%s | Chunk %s | Loaded %s rows",
                table_name,
                chunk_number,
                rows_loaded
            )

    logger.info(
        "Completed database load: %s | Total rows: %s",
        table_name,
        total_rows
    )

    return total_rows


# ============================================
# 7. DATABASE ROW COUNT VERIFICATION
# ============================================

def verify_database(engine, expected_counts):
    """
    Compare expected CSV row counts
    with actual MySQL table row counts.
    """

    logger.info("=" * 55)
    logger.info("DATABASE RECONCILIATION")
    logger.info("=" * 55)

    results = []

    with engine.connect() as connection:

        for table_name, expected_count in (
            expected_counts.items()
        ):

            actual_count = connection.execute(
                text(
                    f"SELECT COUNT(*) FROM `{table_name}`"
                )
            ).scalar_one()

            passed = actual_count == expected_count

            status = "PASS" if passed else "FAIL"

            results.append({
                "table_name": table_name,
                "expected_rows": expected_count,
                "actual_rows": actual_count,
                "status": status
            })

            logger.info(
                "%s | Expected: %s | Actual: %s | %s",
                table_name,
                expected_count,
                actual_count,
                status
            )

            if not passed:
                raise RuntimeError(
                    f"Row count mismatch for {table_name}: "
                    f"expected {expected_count}, "
                    f"found {actual_count}"
                )

    logger.info(
        "SUCCESS: All database counts verified!"
    )

    return results


# ============================================
# 8. GENERATE DATABASE LOAD REPORT
# ============================================

def generate_load_report(results):
    """
    Save database loading and reconciliation
    results into a CSV report.
    """

    report = pd.DataFrame(results)

    report.to_csv(
        REPORT_FILE,
        index=False
    )

    logger.info(
        "Database load report saved: %s",
        REPORT_FILE
    )

    return report


# ============================================
# 9. MAIN DATABASE LOADING PROCESS
# ============================================

def main():

    logger.info("=" * 60)
    logger.info("RETAILPULSE DATABASE LOADING STARTED")
    logger.info("=" * 60)

    engine = None

    try:

        engine = get_engine()

        expected_counts = {}

        # Load all four datasets.
        for table_name, file_path in DATASETS.items():

            loaded_rows = load_csv_to_mysql(
                engine,
                table_name,
                file_path
            )

            expected_counts[table_name] = loaded_rows

        # Verify database counts.
        verification_results = verify_database(
            engine,
            expected_counts
        )

        # Generate report.
        generate_load_report(
            verification_results
        )

        logger.info("=" * 60)
        logger.info(
            "RETAILPULSE DATABASE LOADING COMPLETED!"
        )
        logger.info("=" * 60)

    except Exception:

        logger.exception(
            "DATABASE LOADING FAILED"
        )

        raise

    finally:

        if engine is not None:

            engine.dispose()

            logger.info(
                "Database connection closed."
            )


# ============================================
# 10. SCRIPT ENTRY POINT
# ============================================

if __name__ == "__main__":
    main()
