import logging
import os
from datetime import datetime
from expense_manager import ExpenseManager
from expense_manager.charts import ExpenseCharts
from expense_manager.config import (
    EXPENSES,
    FILES,
    charts_config,
    get_expenses_definition,
    init_charts_config,
    init_reports_config,
    reports_config,
)
from expense_manager.exchange import CurrencyRatesAPI
from expense_manager.reports import ExpenseReport
from expense_manager.utils import parse_arguments, setup_logging

# parse arguments
args = parse_arguments()

now_ts = datetime.now().strftime("%Y%m%d.%H%M")
# setup logging
logger = setup_logging(
    log_name="ExpenseManager",
    log_level=logging.DEBUG if args.DEBUG else logging.INFO,
    is_file_handler=True,
    log_file=os.path.join(args.DATA_PATH, "logs", f"run_expense_manager_{now_ts}.log"),
)

logger.info("Start of expense manager scripts.")


def main(args):
    """Driving code to test ExpenseManager App"""

    # Get variables from arguments
    data_path = args.DATA_PATH
    date_mmyyyy = args.DATE_MMYYYY
    transaction_file = os.path.join(data_path, FILES["transaction_file"]).format(
        date_mmyyyy=date_mmyyyy
    )
    pdf_file = os.path.join(data_path, FILES["pdf_file"]).format(
        date_mmyyyy=date_mmyyyy
    )

    logger.info(f"DATA PATH: {data_path}")
    logger.info(f"PDF FILE: {pdf_file}")
    logger.info(f"TRANSACTION FILE: {transaction_file}")

    # Test ExchangeAPI
    rates = CurrencyRatesAPI(
        is_historical=False,
        url="latest_symbol",
        base_currency="USD",
        target_currency="INR",
        logger=logger,
    )
    logger.info(f"Available Currency: {CurrencyRatesAPI.get_currency_list()}")
    rates.get_exchange_rates()

    # get expenses goal
    expenses_goal = get_expenses_definition(EXPENSES)
    logger.info(f"Expenses Definition: {expenses_goal}")

    # Load and sort data
    expense = ExpenseManager(
        expense_file=transaction_file,
        sort_column=args.SORT_COLUMN,
        log=logger,
        expenses_goal=expenses_goal,
    )
    expense.sort_data()

    # Enter Savings Goal
    expense.savings_goal = 150000
    logger.info(f"Monthly savings Goal: {expense.savings_goal}")

    # Calculate Monthly Summary
    report_month, monthly_summary, monthly_income, monthly_expenses, monthly_savings = (
        expense.calculate_monthly_summary()
    )

    # Calculate Expense-to-income ratio
    expense_to_income_ratio = expense.calculate_ratio()
    total_expense_percent = expense.get_total_expense_percent()

    # Check Savings Goal
    goal = expense.check_savings_goal()

    # Get Insights
    expense_summary, insights = expense.insights()
    insights.insert(0, goal)

    logger.info(f"Report Month: {report_month}")
    logger.info(f"Monthly Savings Goal: {goal}")
    logger.info(f"Monthly income: {monthly_income}")
    logger.info(f"Monthly expenses: {monthly_expenses}")
    logger.info(f"Monthly Savings: {monthly_savings}")

    logger.info(
        f"Monthly expense-to-income ratio: {expense_to_income_ratio} [{total_expense_percent:.2f}%]"
    )
    logger.debug(
        f"""Monthly Summary:
    {monthly_summary}"""
    )

    logger.debug(
        f"""Expense Summary:
    {expense_summary}"""
    )
    logger.info("Insights & Recommendations:")
    for insight in insights:
        logger.info(insight)

    # Generate Charts
    logger.info("Generating Charts.....")
    chart_report = ExpenseCharts(month=report_month, log=logger, file_path=data_path)
    summary_records = monthly_summary.to_dict(orient="records")
    expense_records = expense_summary.to_dict(orient="records")

    _charts_config = init_charts_config(
        monthly_income=monthly_income,
        monthly_expenses=monthly_expenses,
        monthly_summary=chart_report.sort_data(summary_records),
        expense_summary=chart_report.sort_data(expense_records),
        charts_=charts_config,
    )

    chart_report.build(_charts_config)

    # Generate PDF Report
    logger.info("Generating PDF reports.....")
    pdf_report = ExpenseReport(
        customer_name="John Walther",
        report_month=report_month,
        rpt_file=pdf_file,
        log=logger,
        data=init_reports_config(
            reports_config,
            [
                monthly_income,
                monthly_expenses,
                total_expense_percent,
                "USD",
                {item["expense_category"]: item["amount"] for item in expense_records},
                insights,
            ],
        ),
    )
    pdf_report.build()
    logger.info("PDF report download ............[complete]")


if __name__ == "__main__":
    try:
        main(args)
    except Exception as exc:
        logger.exception(exc)
        raise
