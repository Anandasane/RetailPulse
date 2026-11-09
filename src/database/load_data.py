
import pandas as pd
from pathlib import Path
from sqlalchemy import text

from config.database import get_engine


# ============================================
# 1. CONFIGURATION
# ============================================

DATASETS = {
    "fact_sales": "data/processed/cleaned_transactions.csv",
    "fact_returns": "data/processed/returns.csv",
    "fact_cancelled": "data/processed/cancelled_transactions.csv",
    "rejected_records": "data/processed/rejected_records.csv"
}

CHUNK_SIZE = 5000

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


# ============================================
# 2. LOAD AND PREPARE DATA
# ============================================

def prepare_chunk(chunk):

    # Rename CSV columns to match MySQL schema
    chunk = chunk.rename(columns=COLUMN_MAPPING)

    # Convert date
    if "invoice_date" in chunk.columns:
        chunk["invoice_date"] = pd.to_datetime(
            chunk["invoice_date"],
            errors="coerce"
        )

    # Convert numeric fields
    for column in ["quantity", "unit_price", "revenue"]:
        if column in chunk.columns:
            chunk[column] = pd.to_numeric(
                chunk[column],
                errors="coerce"
            )

    # Customer ID must remain a string
    if "customer_id" in chunk.columns:
        chunk["customer_id"] = (
            chunk["customer_id"]
            .astype("string")
            .replace("<NA>", None)
        )

    # Convert invoice and stock codes to strings
    for column in ["invoice_no", "stock_code"]:
        if column in chunk.columns:
            chunk[column] = (
                chunk[column]
                .astype("string")
                .replace("<NA>", None)
            )

    # Replace pandas missing values with None for SQL
    chunk = chunk.astype(object).where(
        pd.notna(chunk),
        None
    )

    return chunk


# ============================================
# 3. LOAD CSV INTO MYSQL
# ============================================

def load_csv_to_mysql(engine, table_name, file_path):

    file_path = Path(file_path)

    if not file_path.exists():
        raise FileNotFoundError(
            f"Dataset not found: {file_path}"
        )

    print(f"\nLoading table: {table_name}")

    # Clear old records before full reload
    with engine.begin() as connection:
        connection.execute(
            text(f"DELETE FROM `{table_name}`")
        )

    total_rows = 0
    first_chunk = True

    for chunk in pd.read_csv(
        file_path,
        chunksize=CHUNK_SIZE,
        dtype={
            "InvoiceNo": "string",
            "StockCode": "string",
            "CustomerID": "string"
        }
    ):

        chunk = prepare_chunk(chunk)

        # Check that CSV columns match the target table
        expected_columns = set(COLUMN_MAPPING.values())
        actual_columns = set(chunk.columns)

        if actual_columns != expected_columns:
            raise ValueError(
                f"Column mismatch in {table_name}. "
                f"Expected: {expected_columns}. "
                f"Found: {actual_columns}"
            )

        chunk.to_sql(
            name=table_name,
            con=engine,
            if_exists="append",
            index=False,
            method=None,
            chunksize=1000
        )

        total_rows += len(chunk)
        first_chunk = False

        print(f"Inserted {total_rows:,} records")

    print(
        f"Completed {table_name}: {total_rows:,} rows"
    )

    return total_rows


# ============================================
# 4. VERIFY MYSQL RECORD COUNTS
# ============================================

def verify_database(engine, expected_counts):

    print("\n========== DATABASE VERIFICATION ==========")

    all_passed = True

    with engine.connect() as connection:

        for table_name, expected in expected_counts.items():

            result = connection.execute(
                text(
                    f"SELECT COUNT(*) FROM `{table_name}`"
                )
            )

            actual = result.scalar()

            passed = actual == expected

            print(
                f"{table_name}: "
                f"Expected={expected:,}, "
                f"Actual={actual:,}, "
                f"Status={'PASS' if passed else 'FAIL'}"
            )

            if not passed:
                all_passed = False

    if not all_passed:
        raise ValueError(
            "Database row count verification failed."
        )

    print("\nSUCCESS: All database counts verified!")


# ============================================
# 5. MAIN EXECUTION
# ============================================

def main():

    print("\n======================================")
    print(" RETAILPULSE - MYSQL DATA LOADER")
    print("======================================")

    engine = get_engine()

    expected_counts = {}

    try:

        for table_name, file_path in DATASETS.items():

            loaded_rows = load_csv_to_mysql(
                engine,
                table_name,
                file_path
            )

            expected_counts[table_name] = loaded_rows

        verify_database(
            engine,
            expected_counts
        )

    except Exception as error:

        print("\nDATABASE LOADING FAILED!")
        print("Error:", repr(error))

        raise

    finally:
        engine.dispose()

    print("\nRetailPulse database loading completed!")


if __name__ == "__main__":
    main()
