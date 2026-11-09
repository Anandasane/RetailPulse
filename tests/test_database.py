
import pandas as pd
import pytest

from pathlib import Path

from src.database.load_data import (
    prepare_chunk,
    validate_csv
)


# ============================================
# TEST 1: COLUMN MAPPING
# ============================================

def test_prepare_chunk_column_mapping():

    df = pd.DataFrame({
        "InvoiceNo": ["1001"],
        "StockCode": ["A"],
        "Description": ["Product A"],
        "Quantity": [2],
        "InvoiceDate": ["2010-12-01 09:00:00"],
        "UnitPrice": [10.5],
        "CustomerID": ["100"],
        "Country": ["UK"],
        "Revenue": [21.0]
    })

    result = prepare_chunk(df)

    expected_columns = {
        "invoice_no",
        "stock_code",
        "description",
        "quantity",
        "invoice_date",
        "unit_price",
        "customer_id",
        "country",
        "revenue"
    }

    assert set(result.columns) == expected_columns


# ============================================
# TEST 2: NUMERIC DATA CONVERSION
# ============================================

def test_prepare_chunk_numeric_conversion():

    df = pd.DataFrame({
        "InvoiceNo": ["1001"],
        "StockCode": ["A"],
        "Description": ["Product A"],
        "Quantity": ["2"],
        "InvoiceDate": ["2010-12-01 09:00:00"],
        "UnitPrice": ["10.5"],
        "CustomerID": ["100"],
        "Country": ["UK"],
        "Revenue": ["21.0"]
    })

    result = prepare_chunk(df)

    assert pd.api.types.is_numeric_dtype(result["quantity"])
    assert pd.api.types.is_numeric_dtype(result["unit_price"])
    assert pd.api.types.is_numeric_dtype(result["revenue"])

    assert result.iloc[0]["quantity"] == 2
    assert result.iloc[0]["unit_price"] == 10.5
    assert result.iloc[0]["revenue"] == 21.0


# ============================================
# TEST 3: DATE CONVERSION
# ============================================

def test_prepare_chunk_date_conversion():

    df = pd.DataFrame({
        "InvoiceNo": ["1001"],
        "StockCode": ["A"],
        "Description": ["Product A"],
        "Quantity": [2],
        "InvoiceDate": ["2010-12-01 09:00:00"],
        "UnitPrice": [10.5],
        "CustomerID": ["100"],
        "Country": ["UK"],
        "Revenue": [21.0]
    })

    result = prepare_chunk(df)

    assert pd.api.types.is_datetime64_any_dtype(
        result["invoice_date"]
    )


# ============================================
# TEST 4: MISSING VALUES
# ============================================

def test_prepare_chunk_missing_values():

    df = pd.DataFrame({
        "InvoiceNo": ["1001"],
        "StockCode": ["A"],
        "Description": [None],
        "Quantity": [2],
        "InvoiceDate": ["2010-12-01 09:00:00"],
        "UnitPrice": [10.5],
        "CustomerID": [None],
        "Country": ["UK"],
        "Revenue": [21.0]
    })

    result = prepare_chunk(df)

    assert result.iloc[0]["description"] is None
    assert result.iloc[0]["customer_id"] is None


# ============================================
# TEST 5: VALID CSV FILE
# ============================================

def test_validate_csv_valid_file(tmp_path):

    df = pd.DataFrame({
        "InvoiceNo": ["1001"],
        "StockCode": ["A"],
        "Description": ["Product A"],
        "Quantity": [2],
        "InvoiceDate": ["2010-12-01 09:00:00"],
        "UnitPrice": [10.5],
        "CustomerID": ["100"],
        "Country": ["UK"],
        "Revenue": [21.0]
    })

    csv_file = tmp_path / "valid_data.csv"
    df.to_csv(csv_file, index=False)

    # Should not raise an exception.
    validate_csv(csv_file)


# ============================================
# TEST 6: MISSING CSV FILE
# ============================================

def test_validate_csv_missing_file(tmp_path):

    missing_file = tmp_path / "missing.csv"

    with pytest.raises(FileNotFoundError):
        validate_csv(missing_file)


# ============================================
# TEST 7: INVALID CSV SCHEMA
# ============================================

def test_validate_csv_invalid_schema(tmp_path):

    df = pd.DataFrame({
        "InvoiceNo": ["1001"],
        "Quantity": [2]
    })

    csv_file = tmp_path / "invalid_data.csv"
    df.to_csv(csv_file, index=False)

    with pytest.raises(ValueError):
        validate_csv(csv_file)
