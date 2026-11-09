
import pandas as pd

# Load original dataset
df = pd.read_excel("data/raw/Online Retail.xlsx")

# Identify unusual records
cancelled = df["InvoiceNo"].astype(str).str.startswith("C")
negative_qty = df["Quantity"] < 0
invalid_price = df["UnitPrice"] <= 0
missing_customer = df["CustomerID"].isna()
duplicates = df.duplicated(keep=False)

print("\n========== OVERLAPPING DATA ISSUES ==========")

print("Cancelled AND Negative Quantity:",
      (cancelled & negative_qty).sum())

print("Cancelled AND Invalid Price:",
      (cancelled & invalid_price).sum())

print("Negative Quantity AND Invalid Price:",
      (negative_qty & invalid_price).sum())

print("Missing Customer AND Cancelled:",
      (missing_customer & cancelled).sum())

print("Duplicate Rows Associated With Cancellations:",
      (duplicates & cancelled).sum())


print("\n========== CANCELLATION INVESTIGATION ==========")

print("Invoice number examples:")
print(df.loc[cancelled, "InvoiceNo"].head(10).tolist())

print("\nSample cancelled transactions:")
print(df.loc[cancelled].head(10).to_string(index=False))


print("\n========== NEGATIVE QUANTITY INVESTIGATION ==========")

print(df.loc[negative_qty, [
    "InvoiceNo",
    "StockCode",
    "Description",
    "Quantity",
    "UnitPrice",
    "CustomerID"
]].head(10).to_string(index=False))


print("\n========== INVALID PRICE INVESTIGATION ==========")

print(df.loc[invalid_price, [
    "InvoiceNo",
    "StockCode",
    "Description",
    "Quantity",
    "UnitPrice",
    "CustomerID"
]].head(10).to_string(index=False))


print("\n========== DUPLICATE INVESTIGATION ==========")

duplicate_examples = df[df.duplicated(keep=False)]

print(duplicate_examples.head(20).to_string(index=False))


print("\n========== INVESTIGATION COMPLETED ==========")


# Save investigation results

from pathlib import Path

Path("reports").mkdir(parents=True, exist_ok=True)

investigation_results = {
    "Cancelled AND Negative Quantity":
        (cancelled & negative_qty).sum(),

    "Cancelled AND Invalid Price":
        (cancelled & invalid_price).sum(),

    "Negative Quantity AND Invalid Price":
        (negative_qty & invalid_price).sum(),

    "Missing Customer AND Cancelled":
        (missing_customer & cancelled).sum(),

    "Duplicate Rows Associated With Cancellations":
        (duplicates & cancelled).sum()
}

investigation_report = pd.DataFrame(
    list(investigation_results.items()),
    columns=["Investigation", "Affected_Rows"]
)

investigation_report.to_csv(
    "reports/anomaly_investigation.csv",
    index=False
)

print("\nInvestigation report saved successfully!")
