import logging
import os
from datetime import datetime
from typing import Dict
from reportlab.lib import colors
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.units import inch
from reportlab.platypus import Image, Paragraph, SimpleDocTemplate, Spacer, Table
from expense_manager.exception import ExpenseReportError


class ExpenseReport:
    """Class generates PDF report for ExpenseManager app"""

    def __init__(
        self,
        customer_name: str,
        report_month: str,
        data: Dict,
        rpt_file: str,
        log: logging.Logger,
    ):
        self.customer_name = customer_name
        self.report_month = report_month
        self.generated_on = datetime.now().strftime("%d/%m/%Y %H:%M")
        self.data = data
        self.rpt_file = rpt_file
        self.logger = log
        self.rpt_path = os.path.dirname(rpt_file)
        self.charts = [os.path.join(self.rpt_path, chart) for chart in data["charts"]]

    def _create_header_table(self) -> Table:
        """PDF header definition"""
        # Create header table with styles
        header_data = [
            ["Expense Manager", "", f"Generated on: {self.generated_on}"],
            [f"Customer name: {self.customer_name}", "", ""],
            [f"Report Month: {self.report_month}", "", ""],
            ["", "Monthly Expense Summary", ""],
        ]
        header_style = [
            ("BACKGROUND", (0, 0), (-1, 3), colors.blue),
            ("TEXTCOLOR", (0, 0), (-1, 3), colors.white),
            ("ALIGN", (0, 0), (0, 0), "LEFT"),
            ("ALIGN", (2, 0), (2, 0), "RIGHT"),
            ("ALIGN", (1, 3), (1, 3), "CENTER"),
            ("FONTNAME", (0, 0), (-1, 3), "Helvetica-Bold"),
            ("TOPPADDING", (0, 0), (-1, 3), 0),
            ("BOTTOMPADDING", (0, 0), (-1, 3), 0),
            ("LEFTPADDING", (0, 0), (-1, 3), 0),
            ("RIGHTPADDING", (0, 0), (-1, 3), 0),
        ]
        return Table(header_data, style=header_style, hAlign="LEFT")

    def _create_summary_table(self) -> Table:
        """Summary definition"""
        # Create summary table with styles
        summary_data = [
            ["Total Income", f"{self.data['currency']} {self.data['total_income']}"],
            [
                "Total Expenses",
                f"{self.data['currency']} {self.data['total_expenses']}",
            ],
            ["Expense to Income Ratio", f"{self.data['expense_ratio']}%"],
        ]
        summary_style = [
            ("FONTNAME", (0, 0), (-1, -1), "Helvetica"),
            ("FONTSIZE", (0, 0), (-1, -1), 10),
            ("ALIGN", (1, 0), (1, -1), "RIGHT"),
        ]
        return Table(summary_data, style=summary_style, hAlign="LEFT")

    def _create_expense_table(self) -> Table:
        """Expense summary definition"""
        # Create expense table with styles
        expense_data = []
        expense_data.append(["Expense Category", "Amount"])
        for category, amount in self.data["expenses"].items():
            expense_data.append([category, f"{self.data['currency']} {amount}"])
        expense_style = [
            ("FONTNAME", (0, 0), (-1, -1), "Helvetica"),
            ("FONTSIZE", (0, 0), (-1, -1), 10),
            ("ALIGN", (1, 0), (1, -1), "RIGHT"),
            ("GRID", (0, 0), (-1, -1), 0.5, colors.grey),
        ]
        return Table(expense_data, style=expense_style, hAlign="LEFT")

    def _add_charts(self, elements) -> None:
        """Chart element definition"""
        # Add charts to the report
        chart_files = self.charts
        for chart_file in chart_files:
            if os.path.exists(chart_file):
                elements.append(
                    Image(chart_file, width=4 * inch, height=2.5 * inch, hAlign="LEFT")
                )
                elements.append(Spacer(1, 12))

    def build(self) -> None:
        """Build PDF report"""
        # Create document template
        doc = SimpleDocTemplate(
            self.rpt_file,
            pagesize=A4,
            leftMargin=0.5 * inch,
            rightMargin=0.5 * inch,
            topMargin=0.5 * inch,
            bottomMargin=0.5 * inch,
        )

        elements = []
        # Create report elements
        elements.append(self._create_header_table())
        elements.append(Spacer(1, 12))

        # Add summary section
        elements.append(
            Paragraph(
                "Monthly Summary:",
                style=ParagraphStyle(
                    name="Heading4", fontName="Helvetica-Bold", underlineProportion=0.5
                ),
            )
        )
        elements.append(Spacer(1, 12))
        elements.append(self._create_summary_table())
        elements.append(Spacer(1, 12))

        # Add expense table
        elements.append(
            Paragraph(
                "Expense Summary:",
                style=ParagraphStyle(
                    name="Heading4", fontName="Helvetica-Bold", underlineProportion=0.5
                ),
            )
        )
        elements.append(Spacer(1, 12))
        elements.append(self._create_expense_table())
        elements.append(Spacer(1, 12))

        # Add insights and recommendations
        elements.append(
            Paragraph(
                "Insights and Recommendations:",
                style=ParagraphStyle(
                    name="Heading4", fontName="Helvetica-Bold", underlineProportion=0.5
                ),
            )
        )
        elements.append(Spacer(1, 12))

        # Add bullets to insights
        for insight in self.data["insights"]:
            elements.append(
                Paragraph(f"* {insight}", style=ParagraphStyle(name="BodyText"))
            )
            elements.append(Spacer(1, 6))
        elements.append(Spacer(1, 12))

        # Add charts
        self._add_charts(elements)

        try:
            # Build document
            doc.build(elements)
        except ExpenseReportError as exc:
            self.logger.error(f"Error building PDF reports: {exc}")
