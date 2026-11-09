
import pandas as pd
from pathlib import Path


# ==================================================
# 1. PROJECT CONFIGURATION
# ==================================================

RAW_FILE = Path("data/raw/Online Retail.xlsx")

PROCESSED_DIR = Path("data/processed")
REJECTED_DIR = Path("data/rejected")
REPORT_DIR = Path("reports")

PROCESSED_DIR.mkdir(parents=True, exist_ok=True)
REJECTED_DIR.mkdir(parents=True, exist_ok=True)
REPORT_DIR.mkdir(parents=True, exist_ok=True)


# ==================================================
# 2. LOAD RAW DATA
# ==================================================

def load_data():
    """Load the original retail dataset."""

    print("\nLoading raw dataset...")

    if not RAW_FILE.exists():
        raise FileNotFoundError(
            f"Raw dataset not found: {RAW_FILE}"
        )

    df = pd.read_excel(RAW_FILE)

    print("Raw records loaded:", len(df))
    print("Columns:", list(df.columns))

    return df


# ==================================================
# 3. REMOVE DUPLICATES
# ==================================================

def remove_duplicates(df):
    """Remove exact duplicate records."""

    original_count = len(df)

    df = df.drop_duplicates().copy()

    duplicates_removed = original_count - len(df)

    print("\n========== DUPLICATE REMOVAL ==========")
    print("Original records:", original_count)
    print("Duplicates removed:", duplicates_removed)
    print("Remaining records:", len(df))

    return df, duplicates_removed


# ==================================================
# 4. BASIC DATA CLEANING
# ==================================================

def clean_basic_data(df):
    """Standardize text fields and data types."""

    print("\nCleaning data...")

    # Remove unnecessary spaces from text columns
    text_columns = ["InvoiceNo", "StockCode", "Description", "Country"]

    for column in text_columns:
        if column in df.columns:
            df[column] = df[column].astype("string").str.strip()

            # Restore missing values after string conversion
            df[column] = df[column].replace("", pd.NA)

    # Standardize numeric columns
    df["Quantity"] = pd.to_numeric(
        df["Quantity"],
        errors="coerce"
    )

    df["UnitPrice"] = pd.to_numeric(
        df["UnitPrice"],
        errors="coerce"
    )

    # Convert invoice date
    df["InvoiceDate"] = pd.to_datetime(
        df["InvoiceDate"],
        errors="coerce"
    )

    print("Basic cleaning completed.")

    return df


# ==================================================
# 5. CLASSIFY TRANSACTIONS
# ==================================================

def classify_transactions(df):
    """
    Divide records into four mutually exclusive categories:

    1. Clean Sales
    2. Returns
    3. Cancelled Transactions
    4. Rejected Records
    """

    print("\nClassifying transactions...")

    invoice_number = (
        df["InvoiceNo"]
        .astype("string")
        .fillna("")
    )

    # Cancelled invoices begin with C
    is_cancelled = invoice_number.str.startswith("C")

    # Returns are negative quantities in non-cancelled invoices
    is_return = (
        ~is_cancelled
        & (df["Quantity"] < 0)
    )

    # Essential field validation
    has_required_fields = (
        df["InvoiceNo"].notna()
        & df["StockCode"].notna()
        & df["Quantity"].notna()
        & df["InvoiceDate"].notna()
        & df["UnitPrice"].notna()
    )

    # Valid analytical sales
    is_clean_sale = (
        ~is_cancelled
        & (df["Quantity"] > 0)
        & (df["UnitPrice"] > 0)
        & has_required_fields
    )

    # All records not assigned to the first three categories
    is_rejected = ~(
        is_cancelled
        | is_return
        | is_clean_sale
    )

    # Create separate datasets
    cancelled_df = df.loc[is_cancelled].copy()
    returns_df = df.loc[is_return].copy()
    clean_df = df.loc[is_clean_sale].copy()
    rejected_df = df.loc[is_rejected].copy()

    print("\n========== CLASSIFICATION SUMMARY ==========")
    print("Clean sales:", len(clean_df))
    print("Returns:", len(returns_df))
    print("Cancelled transactions:", len(cancelled_df))
    print("Rejected records:", len(rejected_df))

    return (
        clean_df,
        returns_df,
        cancelled_df,
        rejected_df
    )


# ==================================================
# 6. HANDLE MISSING PRODUCT DESCRIPTIONS
# ==================================================

def handle_missing_descriptions(df):
    """Replace missing product descriptions."""

    missing_before = df["Description"].isna().sum()

    df["Description"] = (
        df["Description"]
        .fillna("Unknown Product")
    )

    print("\nMissing descriptions filled:", missing_before)

    return df


# ==================================================
# 7. CALCULATE REVENUE
# ==================================================

def calculate_revenue(df):
    """Calculate transaction revenue."""

    df["Revenue"] = (
        df["Quantity"] * df["UnitPrice"]
    )

    return df


# ==================================================
# 8. SAVE OUTPUT FILES
# ==================================================

def save_outputs(
    clean_df,
    returns_df,
    cancelled_df,
    rejected_df
):
    """Save all classified datasets."""

    clean_path = PROCESSED_DIR / "cleaned_transactions.csv"
    returns_path = PROCESSED_DIR / "returns.csv"
    cancelled_path = PROCESSED_DIR / "cancelled_transactions.csv"
    rejected_path = PROCESSED_DIR / "rejected_records.csv"

    clean_df.to_csv(clean_path, index=False)
    returns_df.to_csv(returns_path, index=False)
    cancelled_df.to_csv(cancelled_path, index=False)
    rejected_df.to_csv(rejected_path, index=False)

    print("\n========== OUTPUT FILES ==========")

    print("Clean sales:", clean_path)
    print("Returns:", returns_path)
    print("Cancelled:", cancelled_path)
    print("Rejected:", rejected_path)


# ==================================================
# 9. GENERATE CLEANING SUMMARY REPORT
# ==================================================

def generate_summary(
    raw_count,
    duplicate_count,
    clean_df,
    returns_df,
    cancelled_df,
    rejected_df
):
    """Generate a CSV summary of the cleaning process."""

    classified_count = (
        len(clean_df)
        + len(returns_df)
        + len(cancelled_df)
        + len(rejected_df)
    )

    summary = pd.DataFrame({
        "Metric": [
            "Original Raw Records",
            "Duplicate Records Removed",
            "Deduplicated Records",
            "Clean Sales",
            "Returns",
            "Cancelled Transactions",
            "Rejected Records",
            "Total Classified Records",
            "Reconciliation Difference",
            "Total Sales Revenue"
        ],
        "Value": [
            raw_count,
            duplicate_count,
            raw_count - duplicate_count,
            len(clean_df),
            len(returns_df),
            len(cancelled_df),
            len(rejected_df),
            classified_count,
            (raw_count - duplicate_count) - classified_count,
            round(clean_df["Revenue"].sum(), 2)
        ]
    })

    summary_path = REPORT_DIR / "cleaning_summary.csv"

    summary.to_csv(summary_path, index=False)

    print("\n========== CLEANING SUMMARY ==========")
    print(summary.to_string(index=False))

    print("\nSummary saved to:", summary_path)

    if classified_count != raw_count - duplicate_count:
        raise ValueError(
            "Classification reconciliation failed!"
        )


# ==================================================
# 10. MAIN ETL EXECUTION
# ==================================================

def main():

    print("\n")
    print("=" * 55)
    print("       RETAILPULSE - DATA CLEANING PIPELINE")
    print("=" * 55)

    # Step 1: Load
    raw_df = load_data()

    original_count = len(raw_df)

    # Step 2: Remove duplicates
    df, duplicate_count = remove_duplicates(raw_df)

    # Step 3: Basic cleaning
    df = clean_basic_data(df)

    # Step 4: Classify transactions
    (
        clean_df,
        returns_df,
        cancelled_df,
        rejected_df
    ) = classify_transactions(df)

    # Step 5: Fill missing descriptions in analytical sales
    clean_df = handle_missing_descriptions(clean_df)

    # Step 6: Calculate revenue for clean sales
    clean_df = calculate_revenue(clean_df)

    # Step 7: Calculate revenue for other categories where useful
    returns_df = calculate_revenue(returns_df)
    cancelled_df = calculate_revenue(cancelled_df)
    rejected_df = calculate_revenue(rejected_df)

    # Step 8: Save outputs
    save_outputs(
        clean_df,
        returns_df,
        cancelled_df,
        rejected_df
    )

    # Step 9: Generate summary
    generate_summary(
        original_count,
        duplicate_count,
        clean_df,
        returns_df,
        cancelled_df,
        rejected_df
    )

    print("\n")
    print("=" * 55)
    print("RETAILPULSE DATA CLEANING COMPLETED SUCCESSFULLY")
    print("=" * 55)


# ==================================================
# 11. SCRIPT ENTRY POINT
# ==================================================

if __name__ == "__main__":
    main()
