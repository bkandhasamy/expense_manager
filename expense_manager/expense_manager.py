import logging
from typing import Dict, List, Tuple
import pandas
from pandas import DataFrame, read_csv

# pandas settings
pandas.options.mode.copy_on_write = True


class ExpenseManager:
    def __init__(
        self,
        expense_file: str,
        sort_column: str,
        log: logging.Logger,
        savings_goal: int = None,
        expenses_goal: dict = None,
    ):
        """
        This is base class of ExpenseManager App
        Args:
            expense_file: Monthly transaction file
            sort_column: Column to sort
            log: logger object
            savings_goal: Monthly savings goal
            expenses_goal: Monthly expense goal by category
        """
        self.logger = log
        self.month = None
        self.monthly_summary = None
        self.monthly_income = None
        self.monthly_savings = None
        self.monthly_expenses = None
        self.sort_column = sort_column
        self.expense_file = expense_file
        self._savings_goal = savings_goal
        self._expenses_goal = expenses_goal
        self.df_expense = self.load_data()

    @property
    def savings_goal(self) -> int:
        return self._savings_goal

    @savings_goal.setter
    def savings_goal(self, new_savings_goal: int):
        self._savings_goal = new_savings_goal

    @property
    def expenses_goal(self) -> Dict[str, float]:
        return self._expenses_goal

    @expenses_goal.setter
    def expenses_goal(self, new_expenses_goal):
        self._expenses_goal.update(**new_expenses_goal)

    def load_data(self) -> DataFrame:
        """
        This method load the monthly expense file during initialization.
        Returns:
            None
        """
        try:
            df_exp = read_csv(self.expense_file, parse_dates=["date"])
            required_columns = {"date", "expense_category", "amount"}
            if required_columns.issubset(df_exp.columns):
                self.logger.info("Expense file load complete.")
                return df_exp
            else:
                raise ValueError(
                    f"Expense file must contains columns {required_columns}"
                )
        except Exception as exc:
            self.logger.error("Expense file load failed: %s", exc)
            raise

    def sort_data(self) -> None:
        """This method sorts dataframe for given column"""
        if self.df_expense is not None:
            self.df_expense.sort_values(by=self.sort_column, inplace=True)
            self.logger.info(f"Expense file sorted by column {self.sort_column}")
        else:
            self.logger.warning("Expense file is empty, Skipping sort.")

    def calculate_monthly_summary(self) -> Tuple[str, DataFrame, float, float, float]:
        """This method calculates monthly summary"""

        # Convert date (yyyy-mm-dd) to Period of Month (yyyy-mm)
        self.df_expense["month"] = self.df_expense["date"].dt.to_period("M")

        # Aggregate amount by expense_category and month
        self.monthly_summary = (
            self.df_expense.groupby(["month", "expense_category"])["amount"]
            .sum()
            .reset_index()
        )

        # Calculate total income
        self.monthly_income = (
            self.monthly_summary["amount"]
            .apply(lambda amt: amt if amt > 0 else 0)
            .sum()
        )

        # Calculate total expenses
        self.monthly_expenses = abs(
            self.monthly_summary["amount"]
            .apply(lambda amt: amt if amt < 0 else 0)
            .sum()
        )

        # Calculate monthly savings
        self.monthly_savings = self.monthly_income - self.monthly_expenses

        # Alter formats of Monthly Summary DataFrame
        # Toggle lower case for expense category
        self.monthly_summary["expense_category"] = self.monthly_summary[
            "expense_category"
        ].apply(str.lower)

        # Remove negative signs in monthly summary
        self.monthly_summary["amount"] = self.monthly_summary["amount"].apply(abs)

        # Get expense month in format MON-YYYY
        self.month = self.monthly_summary.month[0].strftime("%b-%Y")

        # Drop column Month
        self.monthly_summary.drop("month", axis=1, inplace=True)

        return (
            self.month,
            self.monthly_summary,
            self.monthly_income,
            self.monthly_expenses,
            self.monthly_savings,
        )

    def calculate_ratio(self) -> float:
        """This method calculates and returns expense-to-income ratio in four decimals"""
        if self.monthly_income == 0:
            return 0
        return round(self.monthly_expenses / self.monthly_income, 4)

    def get_total_expense_percent(self) -> float:
        """This method calculates total expense percentage from income in two decimals"""
        return round(self.calculate_ratio() * 100, 2)

    def calculate_percent(self) -> str:
        """This method calculates and returns Monthly savings or loss in percentage"""
        if self.monthly_income >= self.monthly_expenses:
            return f"{(self.monthly_savings / self.monthly_income) * 100:.2f}%"
        else:
            monthly_loss = self.monthly_expenses - self.monthly_income
            return f"{(monthly_loss / self.monthly_expenses) * 100:.2f}%"

    def check_savings_goal(self) -> str:
        """This method checks progress of savings goal"""
        return (
            f"Monthly Savings goal is achieved by {self.calculate_percent()}"
            if self.monthly_savings >= self.savings_goal
            else f"Monthly expense exceeds saving goal by {self.calculate_percent()}"
        )

    def insights(self) -> Tuple[Dict, List]:
        """This method gets insights by comparing expense goals and actual expense"""
        # Localise Variable
        expenses_goal = self._expenses_goal
        insights = []
        insight_msg = "It is recommended to reduce {category} [{goal}%] expenses by {percent}% to meet savings goal."

        # remove row with salary
        _expenses_summary = self.monthly_summary.query('expense_category != "salary"')

        # Calculate expense percentage
        _expenses_summary["expense_percent"] = _expenses_summary["amount"].apply(
            lambda amt: round((amt / self.monthly_expenses) * 100)
        )

        # Convert expense_summary to records
        expense_records = _expenses_summary.to_dict(orient="records")

        # Get insights
        for expense_record in expense_records:
            expense_category = expense_record["expense_category"]
            expense_percent = expense_record["expense_percent"]
            expense_goal: str = expenses_goal.get(expense_category)

            # TODO: Implement model for insights
            if expense_percent > expense_goal:
                percent_diff = expense_percent - expense_goal
                insights.append(
                    insight_msg.format(
                        goal=expense_goal,
                        percent=percent_diff,
                        category=expense_category,
                    )
                )

        return _expenses_summary, insights
