
import pandas as pd

# Load raw dataset
df = pd.read_excel("data/raw/Online Retail.xlsx")

# Identify cancelled invoices
cancelled = df["InvoiceNo"].astype(str).str.startswith("C")

# Calculate data-quality metrics
quality_report = pd.DataFrame({
    "Issue": [
        "Missing Description",
        "Missing CustomerID",
        "Duplicate Rows",
        "Cancelled Invoice Rows",
        "Negative Quantity Rows",
        "Zero or Negative Prices"
    ],
    "Affected_Rows": [
        df["Description"].isna().sum(),
        df["CustomerID"].isna().sum(),
        df.duplicated().sum(),
        cancelled.sum(),
        (df["Quantity"] < 0).sum(),
        (df["UnitPrice"] <= 0).sum()
    ]
})

# Calculate percentage of total records
quality_report["Affected_Percentage"] = (
    quality_report["Affected_Rows"] / len(df) * 100
).round(2)

# Display report
print("\n========== DATA QUALITY REPORT ==========")
print(quality_report.to_string(index=False))

# Save report
quality_report.to_csv(
    "reports/data_quality_report.csv",
    index=False
)

print("\nData quality report saved successfully!")
