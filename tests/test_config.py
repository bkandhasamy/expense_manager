import pytest
from expense_manager.config import (
    get_url,
    get_expense_percent,
    get_expenses_definition,
    init_charts_config,
    init_reports_config,
    URLS,
    EXPENSES,
    charts_config,
    reports_config,
)


# Test cases for get_url function
def test_get_url_single():
    """Test get_url with a single URL key."""
    result = get_url("base_url")
    assert result == "https://api.frankfurter.app"


def test_get_url_multiple():
    """Test get_url with multiple URL keys."""
    result = get_url("base_url", "latest_base")
    assert result == "https://api.frankfurter.app/latest?base={base}"


def test_get_url_invalid_key():
    """Test get_url with an invalid URL key."""
    with pytest.raises(KeyError):
        get_url("invalid_key")


# Test cases for get_expense_percent function
def test_get_expense_percent_valid():
    """Test get_expense_percent with a valid expense category."""
    result = get_expense_percent("rent")
    assert result == 7


def test_get_expense_percent_invalid():
    """Test get_expense_percent with an invalid expense category."""
    with pytest.raises(KeyError):
        get_expense_percent("unknown")


# Test cases for get_expenses_definition function
def test_get_expenses_definition_valid():
    """Test get_expenses_definition with a valid expense record."""
    expense_record = {
        "rent": {"name": "rent", "percent": 7},
        "tax": {"name": "tax", "percent": 26},
    }
    result = get_expenses_definition(expense_record)
    assert result == {"rent": 7, "tax": 26}


def test_get_expenses_definition_empty():
    """Test get_expenses_definition with an empty expense record."""
    result = get_expenses_definition({})
    assert result == {}


# Test cases for init_charts_config function
def test_init_charts_config_monthly_summary():
    """Test init_charts_config with Monthly Summary chart."""
    updated_charts = init_charts_config(
        monthly_summary=[{"expense_category": "rent", "amount": 500}],
        monthly_income=3000,
        monthly_expenses=2000,
        expense_summary=[{"expense_category": "rent", "amount": 500}],
        charts_=charts_config,
    )
    assert updated_charts[0]["sizes"] == [3000, 2000]


def test_init_charts_config_expense_by_category():
    """Test init_charts_config with Expense by Category chart."""
    updated_charts = init_charts_config(
        monthly_summary=[{"expense_category": "grocery", "amount": 150}],
        monthly_income=5000,
        monthly_expenses=3000,
        expense_summary=[{"expense_category": "grocery", "amount": 150}],
        charts_=charts_config,
    )
    assert updated_charts[1]["labels"] == ["grocery"]
    assert updated_charts[1]["sizes"] == [150]


def test_init_charts_config_monthly_summary_by_category():
    """Test init_charts_config with Monthly Summary by Category chart."""
    updated_charts = init_charts_config(
        monthly_summary=[{"expense_category": "transport", "amount": 100}],
        monthly_income=4000,
        monthly_expenses=2500,
        expense_summary=[{"expense_category": "transport", "amount": 100}],
        charts_=charts_config,
    )
    assert updated_charts[2]["labels"] == ["transport"]
    assert updated_charts[2]["sizes"] == [100]
