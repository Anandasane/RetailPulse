
# =====================================================
# PROJECT: RetailPulse
# TASK: Initial Retail Dataset Inspection
# =====================================================

import pandas as pd

# 1. Load the raw Excel dataset
file_path = "data/raw/Online Retail.xlsx"

df = pd.read_excel(file_path)

# 2. Dataset dimensions
print("\n========== DATASET DIMENSIONS ==========")
print("Total Rows:", df.shape[0])
print("Total Columns:", df.shape[1])

# 3. Display first five records
print("\n========== FIRST FIVE RECORDS ==========")
print(df.head())

# 4. Display column names
print("\n========== COLUMN NAMES ==========")
print(df.columns.tolist())

# 5. Check data types and non-null records
print("\n========== DATASET INFORMATION ==========")
df.info()

# 6. Missing values
print("\n========== MISSING VALUES ==========")
print(df.isnull().sum())

# 7. Duplicate records
print("\n========== DUPLICATE RECORDS ==========")
print("Duplicate Rows:", df.duplicated().sum())

# 8. Statistical summary
print("\n========== STATISTICAL SUMMARY ==========")
print(df.describe(include="all").T)

# 9. Date range
df["InvoiceDate"] = pd.to_datetime(df["InvoiceDate"])

print("\n========== TRANSACTION DATE RANGE ==========")
print("First Date:", df["InvoiceDate"].min())
print("Last Date:", df["InvoiceDate"].max())

# 10. Investigate cancelled invoices
cancelled = df["InvoiceNo"].astype(str).str.startswith("C")

print("\n========== CANCELLATION ANALYSIS ==========")
print("Cancelled Transaction Rows:", cancelled.sum())

# 11. Investigate negative quantities
print("\n========== NEGATIVE QUANTITY ANALYSIS ==========")
print("Negative Quantity Rows:", (df["Quantity"] < 0).sum())

# 12. Investigate invalid prices
print("\n========== PRICE VALIDATION ==========")
print("Zero or Negative Prices:", (df["UnitPrice"] <= 0).sum())

print("\n========== INSPECTION COMPLETED ==========")
