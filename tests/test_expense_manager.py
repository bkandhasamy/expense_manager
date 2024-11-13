import pytest
import logging
from pandas import DataFrame, Timestamp
from expense_manager import (
    ExpenseManager,
)  # Assuming the class is in `expense_manager.py`


# Mock dependencies
@pytest.fixture
def logger():
    return logging.getLogger("test_logger")


@pytest.fixture
def sample_expense_file(tmp_path):
    """Creates a temporary CSV file with sample expense data for testing"""
    file_path = tmp_path / "sample_expenses.csv"
    data = """date,expense_category,amount
2024-01-01,salary,5000
2024-01-05,groceries,-300
2024-01-10,rent,-1000
2024-01-15,utilities,-150
2024-01-20,entertainment,-200"""
    file_path.write_text(data)
    return str(file_path)


@pytest.fixture
def expense_manager(sample_expense_file, logger):
    return ExpenseManager(
        expense_file=sample_expense_file,
        sort_column="date",
        log=logger,
        savings_goal=2000,
        expenses_goal={"groceries": 10, "rent": 30, "utilities": 5, "entertainment": 5},
    )


# Test cases
def test_load_data(expense_manager):
    """Test that data is loaded correctly"""
    df = expense_manager.df_expense
    assert not df.empty
    assert len(df) == 5
    assert set(df.columns) == {"date", "expense_category", "amount"}


def test_sort_data(expense_manager):
    """Test that data is sorted correctly by date"""
    expense_manager.sort_data()
    dates = expense_manager.df_expense["date"].tolist()
    assert dates == sorted(dates)


def test_calculate_monthly_summary(expense_manager):
    """Test calculation of monthly summary"""
    month, summary, income, expenses, savings = (
        expense_manager.calculate_monthly_summary()
    )

    assert month == "Jan-2024"
    assert income == 5000
    assert expenses == 1650
    assert savings == 3350
    assert len(summary) == 5


def test_calculate_ratio(expense_manager):
    """Test calculation of expense-to-income ratio"""
    expense_manager.calculate_monthly_summary()
    ratio = expense_manager.calculate_ratio()
    assert ratio == pytest.approx(0.33, rel=1e-2)


def test_get_total_expense_percent(expense_manager):
    """Test calculation of total expense percentage"""
    expense_manager.calculate_monthly_summary()
    percent = expense_manager.get_total_expense_percent()
    assert percent == 33.0


def test_calculate_percent_savings(expense_manager):
    """Test calculation of savings percentage"""
    expense_manager.calculate_monthly_summary()
    percent = expense_manager.calculate_percent()
    assert percent == "67.00%"


def test_check_savings_goal_achieved(expense_manager):
    """Test savings goal achievement check"""
    expense_manager.calculate_monthly_summary()
    result = expense_manager.check_savings_goal()
    assert "Monthly Savings goal is achieved" in result


def test_check_savings_goal_not_achieved(expense_manager):
    """Test when savings goal is not achieved"""
    expense_manager._savings_goal = 4000  # Set a higher savings goal
    expense_manager.calculate_monthly_summary()
    result = expense_manager.check_savings_goal()
    assert "Monthly expense exceeds saving goal" in result


def test_insights(expense_manager):
    """Test insights based on expense goals"""
    expense_manager.calculate_monthly_summary()
    summary, insights = expense_manager.insights()

    assert isinstance(insights, list)
    assert len(insights) > 0
    for insight in insights:
        assert "It is recommended to reduce" in insight


def test_load_data_missing_columns(tmp_path, logger):
    """Test loading data with missing required columns"""
    file_path = tmp_path / "missing_columns.csv"
    file_path.write_text("date,category,amount\n2024-01-01,salary,5000")

    with pytest.raises(ValueError, match="must contains columns"):
        ExpenseManager(str(file_path), "date", logger)


def test_calculate_percent_with_zero_income(expense_manager):
    """Test calculation when income is zero"""
    # Mock data with zero income
    expense_manager.df_expense = DataFrame(
        {
            "date": [Timestamp("2024-01-05"), Timestamp("2024-01-10")],
            "expense_category": ["groceries", "rent"],
            "amount": [-300, -1000],
        }
    )
    expense_manager.calculate_monthly_summary()
    percent = expense_manager.calculate_percent()
    assert percent == "100.00%"


def test_expenses_goal_update(expense_manager):
    """Test updating expense goals"""
    expense_manager.expenses_goal = {"new_category": 15}
    assert expense_manager._expenses_goal["new_category"] == 15
