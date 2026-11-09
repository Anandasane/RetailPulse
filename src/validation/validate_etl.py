
import sys
from pathlib import Path

import pandas as pd


# ============================================
# 1. PROJECT PATHS
# ============================================

RAW_FILE = Path("data/raw/Online Retail.xlsx")

CLEAN_FILE = Path("data/processed/cleaned_transactions.csv")
RETURNS_FILE = Path("data/processed/returns.csv")
CANCELLED_FILE = Path("data/processed/cancelled_transactions.csv")
REJECTED_FILE = Path("data/processed/rejected_records.csv")

REPORT_DIR = Path("reports")
REPORT_DIR.mkdir(parents=True, exist_ok=True)

REPORT_PATH = REPORT_DIR / "etl_reconciliation.csv"


# ============================================
# 2. LOAD DATASETS
# ============================================

def load_datasets():
    """Load raw Excel data and processed CSV datasets."""

    required_files = [
        RAW_FILE,
        CLEAN_FILE,
        RETURNS_FILE,
        CANCELLED_FILE,
        REJECTED_FILE
    ]

    for file_path in required_files:
        if not file_path.exists():
            raise FileNotFoundError(
                f"Required file not found: {file_path}"
            )

    print("\nLoading datasets...")

    raw = pd.read_excel(RAW_FILE)

    clean = pd.read_csv(
        CLEAN_FILE,
        dtype={"InvoiceNo": "string", "StockCode": "string"}
    )

    returns = pd.read_csv(
        RETURNS_FILE,
        dtype={"InvoiceNo": "string", "StockCode": "string"}
    )

    cancelled = pd.read_csv(
        CANCELLED_FILE,
        dtype={"InvoiceNo": "string", "StockCode": "string"}
    )

    rejected = pd.read_csv(
        REJECTED_FILE,
        dtype={"InvoiceNo": "string", "StockCode": "string"}
    )

    datasets = [clean, returns, cancelled, rejected]

    for dataset in datasets:
        for column in ["Quantity", "UnitPrice", "Revenue"]:
            if column in dataset.columns:
                dataset[column] = pd.to_numeric(
                    dataset[column],
                    errors="coerce"
                )

        if "InvoiceDate" in dataset.columns:
            dataset["InvoiceDate"] = pd.to_datetime(
                dataset["InvoiceDate"],
                errors="coerce"
            )

    print("All datasets loaded successfully.")

    return raw, clean, returns, cancelled, rejected


# ============================================
# 3. INDEPENDENT CLASSIFICATION
# ============================================

def classify_raw_data(raw):
    """Independently classify deduplicated raw transactions."""

    deduplicated_raw = raw.drop_duplicates().copy()

    invoice_number = (
        deduplicated_raw["InvoiceNo"]
        .astype("string")
        .fillna("")
    )

    is_cancelled = invoice_number.str.startswith("C")

    is_return = (
        ~is_cancelled
        & (deduplicated_raw["Quantity"] < 0)
    )

    is_clean_sale = (
        ~is_cancelled
        & (deduplicated_raw["Quantity"] > 0)
        & (deduplicated_raw["UnitPrice"] > 0)
        & deduplicated_raw["InvoiceNo"].notna()
        & deduplicated_raw["StockCode"].notna()
        & deduplicated_raw["Quantity"].notna()
        & deduplicated_raw["InvoiceDate"].notna()
        & deduplicated_raw["UnitPrice"].notna()
    )

    is_rejected = ~(
        is_cancelled
        | is_return
        | is_clean_sale
    )

    expected_clean = deduplicated_raw.loc[
        is_clean_sale
    ].copy()

    expected_returns = deduplicated_raw.loc[
        is_return
    ].copy()

    expected_cancelled = deduplicated_raw.loc[
        is_cancelled
    ].copy()

    expected_rejected = deduplicated_raw.loc[
        is_rejected
    ].copy()

    # Match the cleaning script's description handling.
    expected_clean["Description"] = (
        expected_clean["Description"]
        .fillna("Unknown Product")
    )

    return (
        deduplicated_raw,
        expected_clean,
        expected_returns,
        expected_cancelled,
        expected_rejected
    )


# ============================================
# 4. DATA NORMALIZATION
# ============================================

def normalize_for_comparison(df, source_columns):
    """Normalize data types and values for reliable comparison."""

    result = df[source_columns].copy()

    for column in source_columns:

        if column == "InvoiceDate":
            result[column] = pd.to_datetime(
                result[column],
                errors="coerce"
            ).dt.strftime("%Y-%m-%d %H:%M:%S")

        elif column in ["Quantity", "UnitPrice"]:
            values = pd.to_numeric(
                result[column],
                errors="coerce"
            )

            result[column] = values.map(
                lambda x: "<MISSING>"
                if pd.isna(x)
                else format(x, ".15g")
            )

        else:
            result[column] = (
                result[column]
                .astype("string")
                .str.strip()
                .fillna("<MISSING>")
            )

    # Sort records so row order does not matter.
    result = result.sort_values(
        by=source_columns,
        kind="stable",
        na_position="first"
    ).reset_index(drop=True)

    return result


def compare_datasets(expected, actual, source_columns):
    """Compare expected and actual transaction records."""

    expected_normalized = normalize_for_comparison(
        expected,
        source_columns
    )

    actual_normalized = normalize_for_comparison(
        actual,
        source_columns
    )

    return expected_normalized.equals(actual_normalized)


# ============================================
# 5. BUILD VALIDATION REPORT
# ============================================

def save_validation_report(report_rows):
    """Save validation results to CSV."""

    validation_report = pd.DataFrame(
        report_rows,
        columns=["Metric", "Value"]
    )

    validation_report.to_csv(
        REPORT_PATH,
        index=False
    )

    print("\nValidation report saved to:", REPORT_PATH)


# ============================================
# 6. MAIN VALIDATION PROCESS
# ============================================

def main():

    print("\n========================================")
    print("       RETAILPULSE ETL VALIDATION")
    print("========================================")

    try:

        # Load all datasets.
        (
            raw,
            clean,
            returns,
            cancelled,
            rejected
        ) = load_datasets()

        # Independently classify raw data.
        (
            deduplicated_raw,
            expected_clean,
            expected_returns,
            expected_cancelled,
            expected_rejected
        ) = classify_raw_data(raw)

        print("\n========== RAW DATA SUMMARY ==========")

        print("Original raw records:", len(raw))

        print(
            "Duplicate records removed:",
            len(raw) - len(deduplicated_raw)
        )

        print(
            "Deduplicated raw records:",
            len(deduplicated_raw)
        )

        # Expected dataset counts.
        print("\n========== PRIMARY CLASSIFICATION ==========")

        print("Expected clean sales:", len(expected_clean))
        print("Expected returns:", len(expected_returns))
        print("Expected cancelled:", len(expected_cancelled))
        print("Expected rejected:", len(expected_rejected))

        # Compare source columns only.
        # Revenue is a derived field and is excluded.
        source_columns = list(deduplicated_raw.columns)

        checks = {
            "Clean Sales Match": compare_datasets(
                expected_clean,
                clean,
                source_columns
            ),

            "Returns Match": compare_datasets(
                expected_returns,
                returns,
                source_columns
            ),

            "Cancelled Match": compare_datasets(
                expected_cancelled,
                cancelled,
                source_columns
            ),

            "Rejected Match": compare_datasets(
                expected_rejected,
                rejected,
                source_columns
            )
        }

        # ====================================
        # 7. CLEAN SALES QUALITY CHECKS
        # ====================================

        negative_quantities = (
            clean["Quantity"] < 0
        ).sum()

        invalid_prices = (
            clean["UnitPrice"].isna()
            | (clean["UnitPrice"] <= 0)
        ).sum()

        cancelled_in_clean = (
            clean["InvoiceNo"]
            .astype("string")
            .fillna("")
            .str.startswith("C")
        ).sum()

        missing_invoice_numbers = (
            clean["InvoiceNo"].isna().sum()
        )

        print("\n========== CLEAN SALES QUALITY ==========")

        print("Negative quantities:", negative_quantities)
        print("Invalid prices:", invalid_prices)
        print("Cancelled invoices:", cancelled_in_clean)
        print("Missing invoice numbers:", missing_invoice_numbers)

        # ====================================
        # 8. RETURN QUALITY CHECKS
        # ====================================

        invalid_return_prices = (
            returns["UnitPrice"].isna()
            | (returns["UnitPrice"] <= 0)
        ).sum()

        print(
            "\nReturns with invalid prices:",
            invalid_return_prices
        )

        # ====================================
        # 9. CLASSIFICATION RECONCILIATION
        # ====================================

        classified_rows = (
            len(expected_clean)
            + len(expected_returns)
            + len(expected_cancelled)
            + len(expected_rejected)
        )

        reconciliation_difference = (
            len(deduplicated_raw) - classified_rows
        )

        print("\n========== RECONCILIATION ==========")

        print("Deduplicated raw records:", len(deduplicated_raw))
        print("Classified records:", classified_rows)
        print("Reconciliation difference:", reconciliation_difference)

        # ====================================
        # 10. FINAL VALIDATION CONDITIONS
        # ====================================

        all_output_checks_passed = all(checks.values())

        clean_quality_passed = (
            negative_quantities == 0
            and invalid_prices == 0
            and cancelled_in_clean == 0
            and missing_invoice_numbers == 0
        )

        classification_passed = (
            reconciliation_difference == 0
        )

        # ====================================
        # 11. DISPLAY OUTPUT CHECKS
        # ====================================

        print("\n========== OUTPUT FILE VALIDATION ==========")

        for check_name, passed in checks.items():
            print(
                f"{check_name}:",
                "PASS" if passed else "FAIL"
            )

        # ====================================
        # 12. GENERATE VALIDATION REPORT
        # ====================================

        report_rows = [
            ("Original Raw Records", len(raw)),
            (
                "Duplicate Records Removed",
                len(raw) - len(deduplicated_raw)
            ),
            (
                "Deduplicated Raw Records",
                len(deduplicated_raw)
            ),
            ("Expected Clean Sales", len(expected_clean)),
            ("Actual Clean Sales", len(clean)),
            ("Expected Returns", len(expected_returns)),
            ("Actual Returns", len(returns)),
            ("Expected Cancelled", len(expected_cancelled)),
            ("Actual Cancelled", len(cancelled)),
            ("Expected Rejected", len(expected_rejected)),
            ("Actual Rejected", len(rejected)),
            ("Classified Records", classified_rows),
            (
                "Reconciliation Difference",
                reconciliation_difference
            ),
            (
                "Negative Quantities in Clean Sales",
                negative_quantities
            ),
            (
                "Invalid Prices in Clean Sales",
                invalid_prices
            ),
            (
                "Cancelled Invoices in Clean Sales",
                cancelled_in_clean
            ),
            (
                "Missing Invoice Numbers in Clean Sales",
                missing_invoice_numbers
            ),
            (
                "Returns with Invalid Prices",
                invalid_return_prices
            )
        ]

        for check_name, passed in checks.items():
            report_rows.append(
                (check_name, "PASS" if passed else "FAIL")
            )

        report_rows.extend([
            (
                "Clean Sales Quality",
                "PASS" if clean_quality_passed else "FAIL"
            ),
            (
                "Classification Reconciliation",
                "PASS" if classification_passed else "FAIL"
            )
        ])

        save_validation_report(report_rows)

        # ====================================
        # 13. FINAL VALIDATION STATUS
        # ====================================

        print("\n========== FINAL ETL VALIDATION ==========")

        if (
            all_output_checks_passed
            and clean_quality_passed
            and classification_passed
        ):

            print("SUCCESS: All ETL validation checks passed!")

            return True

        else:

            print("FAILURE: Some ETL validation checks failed.")

            print(
                "Review the output above and "
                "the reconciliation report."
            )

            raise RuntimeError(
                "ETL validation failed. "
                "Database loading must not continue."
            )

    except Exception as error:

        print("\nETL VALIDATION ERROR:", error)

        raise


# ============================================
# 14. SCRIPT ENTRY POINT
# ============================================

if __name__ == "__main__":
        main()
