from enum import Enum
from typing import Dict, List, TypedDict, Union


class _ExpenseDefinition(TypedDict):
    name: str
    percent: float


class Expenses(str, Enum):
    TAX = "tax"
    RENT = "rent"
    LOAN = "loan"
    GIFT = "gift"
    DINING = "dining"
    OTHER = "other"
    GROCERY = "grocery"
    UTILITY = "utility"
    TRANSPORT = "transport"
    INVESTMENT = "investment"
    HEALTHCARE = "healthcare"
    ENTERTAINMENT = "entertainment"


EXPENSES = {
    Expenses.RENT: _ExpenseDefinition(name="rent", percent=7),
    Expenses.LOAN: _ExpenseDefinition(name="loan", percent=20),
    Expenses.TAX: _ExpenseDefinition(name="tax", percent=26),
    Expenses.GIFT: _ExpenseDefinition(name="gift", percent=3),
    Expenses.DINING: _ExpenseDefinition(name="dining", percent=2),
    Expenses.OTHER: _ExpenseDefinition(name="other", percent=4),
    Expenses.UTILITY: _ExpenseDefinition(name="utility", percent=2),
    Expenses.TRANSPORT: _ExpenseDefinition(name="transport", percent=6),
    Expenses.GROCERY: _ExpenseDefinition(name="grocery", percent=4),
    Expenses.INVESTMENT: _ExpenseDefinition(name="investment", percent=20),
    Expenses.HEALTHCARE: _ExpenseDefinition(name="healthcare", percent=2),
    Expenses.ENTERTAINMENT: _ExpenseDefinition(name="entertainment", percent=2),
}

FILES = {
    "transaction_file": "transaction_data_{date_mmyyyy}.csv",
    "pdf_file": "monthly_expense_report_{date_mmyyyy}.pdf",
}

URLS = {
    "base_url": "https://api.frankfurter.app",
    "currencies": "/currencies",
    "latest_base": "/latest?base={base}",
    "latest_symbol": "/latest?base={base}&to={target}",
    "history_base": "/{YYYYMMDD}?base={base}",
    "history_symbol": "/{YYYYMMDD}?base={base}&to={target}",
}

charts_config = [
    {
        "title": "Monthly Summary",
        "type": "pie",
        "labels": ["Income", "Expenses"],
        "sizes": None,
        "colors": ["#32CD32", "#FF0000"],
    },
    {
        "title": "Expense by Category",
        "type": "pie",
        "labels": None,
        "sizes": None,
        "colors": None,
    },
    {
        "title": "Monthly Summary by category",
        "type": "bar",
        "labels": None,
        "sizes": None,
        "xlabel": "Category",
        "ylabel": "Amount (₹)",
        "colors": "#6495ED",
    },
]

reports_config = {
    "total_income": None,
    "total_expenses": None,
    "expense_ratio": None,
    "currency": "USD",
    "expenses": None,
    "insights": None,
    "charts": [
        "expense_by_category.png",
        "monthly_summary.png",
        "monthly_summary_by_category.png",
    ],
}


def get_url(*urls: str) -> str:
    """
    This function joins the number of url strings
    if defined in URL config
    Args:
        *urls: Number of url strings

    Returns:
        url string
    """
    url_names = [*urls]
    return "".join([URLS[url] for url in url_names])


def get_expense_percent(expense_category: str) -> Union[int, float]:
    """
    This function gets expense goal defined for given
    expense category
    Args:
        expense_category: expense category

    Returns:
        defined expense goal
    """
    return EXPENSES[expense_category]["percent"]


def get_expenses_definition(expense_record: Dict) -> Dict:
    """
    This function filters expense definition from expense records
    Args:
        expense_record:

    Returns: filtered expense definition
    """
    return {_value["name"]: _value["percent"] for _, _value in expense_record.items()}


def init_charts_config(
    monthly_summary: Dict,
    monthly_income: float,
    monthly_expenses: float,
    expense_summary: Dict,
    charts_: List[Dict],
) -> List[Dict]:
    """
    This function updates charts config
    Args:
        monthly_summary: Monthly summary records
        monthly_income: total income
        monthly_expenses: total expense
        expense_summary: expense summary
        charts_: charts config

    Returns:updated charts config
    """
    for chart_ in charts_:
        if chart_["title"] == "Monthly Summary":
            chart_.update(sizes=[monthly_income, monthly_expenses])
        elif chart_["title"] == "Expense by Category":
            chart_.update(sizes=[item["amount"] for item in expense_summary])
            chart_.update(labels=[item["expense_category"] for item in expense_summary])
        elif chart_["title"] == "Monthly Summary by category":
            chart_.update(sizes=[item["amount"] for item in monthly_summary])
            chart_.update(labels=[item["expense_category"] for item in monthly_summary])

    return charts_


def init_reports_config(reports_: Dict, data: List) -> Dict:
    """
    This function updates reports config
    Args:
        reports_: reports config
        data: Application data

    Returns: updated reports config
    """
    reports_.update(dict(zip(reports_.keys(), data)))
    return reports_
