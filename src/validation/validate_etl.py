
import pandas as pd
from pathlib import Path


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


# ============================================
# 2. LOAD DATA
# ============================================

print("\nLoading datasets...")

raw = pd.read_excel(RAW_FILE)

clean = pd.read_csv(CLEAN_FILE, dtype={"InvoiceNo": "string"})
returns = pd.read_csv(RETURNS_FILE, dtype={"InvoiceNo": "string"})
cancelled = pd.read_csv(CANCELLED_FILE, dtype={"InvoiceNo": "string"})
rejected = pd.read_csv(REJECTED_FILE, dtype={"InvoiceNo": "string"})


# ============================================
# 3. STANDARDIZE DATA TYPES
# ============================================

numeric_columns = ["Quantity", "UnitPrice", "Revenue"]

for dataset in [clean, returns, cancelled, rejected]:
    for column in numeric_columns:
        if column in dataset.columns:
            dataset[column] = pd.to_numeric(
                dataset[column],
                errors="coerce"
            )

print("All datasets loaded successfully.")


# ============================================
# 4. REMOVE EXACT DUPLICATES FROM RAW DATA
# ============================================

deduplicated_raw = raw.drop_duplicates().copy()

print("\n========== RAW DATA SUMMARY ==========")

print("Original raw records:", len(raw))
print("Duplicate records removed:", len(raw) - len(deduplicated_raw))
print("Deduplicated raw records:", len(deduplicated_raw))


# ============================================
# 5. DEFINE PRIMARY CLASSIFICATION RULES
# ============================================

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

# Any record not assigned to the above categories
# is classified as rejected / requiring investigation.

is_rejected = ~(
    is_cancelled
    | is_return
    | is_clean_sale
)


# ============================================
# 6. CREATE EXPECTED DATASETS
# ============================================

expected_clean = deduplicated_raw.loc[is_clean_sale].copy()
expected_returns = deduplicated_raw.loc[is_return].copy()
expected_cancelled = deduplicated_raw.loc[is_cancelled].copy()
expected_rejected = deduplicated_raw.loc[is_rejected].copy()


# ============================================
# 7. ROW COUNT RECONCILIATION
# ============================================

classification_summary = pd.DataFrame({
    "Dataset": [
        "Raw",
        "Deduplicated Raw",
        "Expected Clean Sales",
        "Actual Clean Sales",
        "Expected Returns",
        "Actual Returns",
        "Expected Cancelled",
        "Actual Cancelled",
        "Expected Rejected",
        "Actual Rejected"
    ],
    "Rows": [
        len(raw),
        len(deduplicated_raw),
        len(expected_clean),
        len(clean),
        len(expected_returns),
        len(returns),
        len(expected_cancelled),
        len(cancelled),
        len(expected_rejected),
        len(rejected)
    ]
})

print("\n========== ETL ROW COUNT RECONCILIATION ==========")
print(classification_summary.to_string(index=False))


# ============================================
# 8. CHECK CLEAN SALES QUALITY
# ============================================

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

missing_invoice_numbers = clean["InvoiceNo"].isna().sum()

print("\n========== CLEAN SALES QUALITY CHECKS ==========")

print("Negative quantities:", negative_quantities)
print("Invalid prices:", invalid_prices)
print("Cancelled invoices:", cancelled_in_clean)
print("Missing invoice numbers:", missing_invoice_numbers)


# ============================================
# 9. CHECK RETURNS WITH INVALID PRICES
# ============================================

invalid_return_prices = (
    returns["UnitPrice"].isna()
    | (returns["UnitPrice"] <= 0)
).sum()

print("\nReturns with invalid prices:", invalid_return_prices)



# ============================================
# 10. VERIFY ACTUAL OUTPUTS AGAINST EXPECTED
# ============================================

# Compare only original source columns.
# Revenue is a derived column, so it is excluded.

SOURCE_COLUMNS = list(deduplicated_raw.columns)


def normalize_for_comparison(df):
    """Normalize records to make Excel and CSV comparisons reliable."""

    result = df[SOURCE_COLUMNS].copy()

    for column in SOURCE_COLUMNS:

        # Normalize dates
        if column == "InvoiceDate":
            result[column] = pd.to_datetime(
                result[column],
                errors="coerce"
            ).dt.strftime("%Y-%m-%d %H:%M:%S")

        # Normalize numeric values
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

        # Normalize text values
        else:
            result[column] = (
                result[column]
                .astype("string")
                .str.strip()
                .fillna("<MISSING>")
            )

    # Sort records so row order does not matter
    result = result.sort_values(
        by=SOURCE_COLUMNS,
        kind="stable"
    ).reset_index(drop=True)

    return result


def compare_datasets(expected, actual):
    """Compare expected and actual transaction records."""

    expected_normalized = normalize_for_comparison(expected)
    actual_normalized = normalize_for_comparison(actual)

    return expected_normalized.equals(actual_normalized)


# The cleaning pipeline replaces missing descriptions
# in clean sales with "Unknown Product".
# Apply the same rule to expected clean sales.

expected_clean = expected_clean.copy()

expected_clean["Description"] = (
    expected_clean["Description"]
    .fillna("Unknown Product")
)


checks = {
    "Clean Sales Match": compare_datasets(
        expected_clean,
        clean
    ),

    "Returns Match": compare_datasets(
        expected_returns,
        returns
    ),

    "Cancelled Match": compare_datasets(
        expected_cancelled,
        cancelled
    ),

    "Rejected Match": compare_datasets(
        expected_rejected,
        rejected
    )
}


# ============================================
# 11. PRIMARY CLASSIFICATION RECONCILIATION
# ============================================

classified_rows = (
    len(expected_clean)
    + len(expected_returns)
    + len(expected_cancelled)
    + len(expected_rejected)
)

reconciliation_difference = (
    len(deduplicated_raw) - classified_rows
)

print("\n========== PRIMARY CLASSIFICATION ==========")

print("Expected clean sales:", len(expected_clean))
print("Expected returns:", len(expected_returns))
print("Expected cancelled:", len(expected_cancelled))
print("Expected rejected:", len(expected_rejected))

print("\n========== OUTPUT FILE VALIDATION ==========")

for check_name, passed in checks.items():
    print(
        f"{check_name}:",
        "PASS" if passed else "FAIL"
    )


# ============================================
# 12. BUILD VALIDATION REPORT
# ============================================

report_rows = [
    ("Original Raw Records", len(raw)),
    ("Duplicate Records Removed", len(raw) - len(deduplicated_raw)),
    ("Deduplicated Raw Records", len(deduplicated_raw)),
    ("Expected Clean Sales", len(expected_clean)),
    ("Actual Clean Sales", len(clean)),
    ("Expected Returns", len(expected_returns)),
    ("Actual Returns", len(returns)),
    ("Expected Cancelled", len(expected_cancelled)),
    ("Actual Cancelled", len(cancelled)),
    ("Expected Rejected", len(expected_rejected)),
    ("Actual Rejected", len(rejected)),
    ("Classified Records", classified_rows),
    ("Reconciliation Difference", reconciliation_difference),
    ("Negative Quantities in Clean Sales", negative_quantities),
    ("Invalid Prices in Clean Sales", invalid_prices),
    ("Cancelled Invoices in Clean Sales", cancelled_in_clean),
    ("Returns with Invalid Prices", invalid_return_prices)
]

for check_name, passed in checks.items():
    report_rows.append(
        (check_name, "PASS" if passed else "FAIL")
    )

validation_report = pd.DataFrame(
    report_rows,
    columns=["Metric", "Value"]
)

report_path = REPORT_DIR / "etl_reconciliation.csv"

validation_report.to_csv(
    report_path,
    index=False
)


# ============================================
# 13. FINAL VALIDATION STATUS
# ============================================

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

print("\n========== FINAL ETL VALIDATION ==========")

if (
    all_output_checks_passed
    and clean_quality_passed
    and classification_passed
):
    print("SUCCESS: All ETL validation checks passed!")
else:
    print("WARNING: Some ETL validation checks failed.")
    print("Review the output above and the reconciliation report.")

print("\nValidation report saved to:", report_path)
