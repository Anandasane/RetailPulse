
import pandas as pd

from src.cleaning.clean_data import (
    remove_duplicates,
    clean_basic_data,
    classify_transactions
)


# ============================================
# TEST 1: DUPLICATE REMOVAL
# ============================================

def test_remove_duplicates():

    df = pd.DataFrame({
        "InvoiceNo": ["1001", "1001", "1002"],
        "StockCode": ["A", "A", "B"],
        "Quantity": [2, 2, 3]
    })

    cleaned_df, duplicates_removed = remove_duplicates(df)

    assert len(cleaned_df) == 2
    assert duplicates_removed == 1
    assert cleaned_df.duplicated().sum() == 0


# ============================================
# TEST 2: BASIC DATA CLEANING
# ============================================

def test_clean_basic_data():

    df = pd.DataFrame({
        "InvoiceNo": [" 1001 ", "1002"],
        "StockCode": [" A ", " B "],
        "Description": [" Product A ", "Product B"],
        "Country": [" UK ", "UK"],
        "Quantity": ["2", "3"],
        "UnitPrice": ["10.5", "20"],
        "InvoiceDate": [
            "2010-12-01 09:00:00",
            "2010-12-01 10:00:00"
        ]
    })

    result = clean_basic_data(df)

    assert result.loc[0, "InvoiceNo"] == "1001"
    assert result.loc[0, "StockCode"] == "A"
    assert result.loc[0, "Country"] == "UK"

    assert pd.api.types.is_numeric_dtype(result["Quantity"])
    assert pd.api.types.is_numeric_dtype(result["UnitPrice"])
    assert pd.api.types.is_datetime64_any_dtype(result["InvoiceDate"])


# ============================================
# TEST 3: TRANSACTION CLASSIFICATION
# ============================================

def test_classify_transactions():

    df = pd.DataFrame({
        "InvoiceNo": [
            "1001",
            "1002",
            "C1003",
            "1004"
        ],
        "StockCode": [
            "A",
            "B",
            "C",
            "D"
        ],
        "Description": [
            "Product A",
            "Product B",
            "Product C",
            "Product D"
        ],
        "Quantity": [
            2,
            -1,
            -2,
            3
        ],
        "InvoiceDate": pd.to_datetime([
            "2010-12-01",
            "2010-12-02",
            "2010-12-03",
            None
        ]),
        "UnitPrice": [
            10,
            5,
            4,
            8
        ],
        "CustomerID": [
            100,
            101,
            102,
            103
        ],
        "Country": [
            "UK",
            "UK",
            "UK",
            "UK"
        ]
    })

    clean, returns, cancelled, rejected = classify_transactions(df)

    assert len(clean) == 1
    assert len(returns) == 1
    assert len(cancelled) == 1
    assert len(rejected) == 1

    assert clean.iloc[0]["InvoiceNo"] == "1001"
    assert returns.iloc[0]["InvoiceNo"] == "1002"
    assert cancelled.iloc[0]["InvoiceNo"] == "C1003"
    assert rejected.iloc[0]["InvoiceNo"] == "1004"


# ============================================
# TEST 4: CLASSIFICATION RECONCILIATION
# ============================================

def test_classification_reconciliation():

    df = pd.DataFrame({
        "InvoiceNo": ["1001", "1002", "C1003"],
        "StockCode": ["A", "B", "C"],
        "Description": ["A", "B", "C"],
        "Quantity": [2, -1, -2],
        "InvoiceDate": pd.to_datetime([
            "2010-12-01",
            "2010-12-02",
            "2010-12-03"
        ]),
        "UnitPrice": [10, 5, 4],
        "CustomerID": [100, 101, 102],
        "Country": ["UK", "UK", "UK"]
    })

    clean, returns, cancelled, rejected = classify_transactions(df)

    total_classified = (
        len(clean)
        + len(returns)
        + len(cancelled)
        + len(rejected)
    )

    assert total_classified == len(df)


# ============================================
# TEST 5: EMPTY DATAFRAME DUPLICATE REMOVAL
# ============================================

def test_remove_duplicates_empty_dataframe():

    df = pd.DataFrame(columns=[
        "InvoiceNo",
        "StockCode",
        "Quantity"
    ])

    cleaned_df, duplicates_removed = remove_duplicates(df)

    assert len(cleaned_df) == 0
    assert duplicates_removed == 0
