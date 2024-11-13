class ExpenseManagerError(Exception):
    """Base exception for ExpenseTracker app"""


class ExchangeAPIError(ExpenseManagerError):
    """Currency exchange rate API error"""


class ExchangeAPIValueError(ExchangeAPIError):
    """ValueError for ExchangeAPI"""


class ExpenseChartsError(ExpenseManagerError):
    """Expense Charts error"""


class ExpenseReportError(ExpenseManagerError):
    """Expense Reports error"""
