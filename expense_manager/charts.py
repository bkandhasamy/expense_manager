import logging
import os
from typing import Dict, List
from matplotlib import pyplot
from expense_manager.exception import ExpenseChartsError


class ExpenseCharts:
    DPI = 300
    FIG_SIZE = (10, 6)

    def __init__(self, month, log: logging.Logger, file_path: str):
        """
        This class generates Charts for ExpenseManager app
        Args:
            month: Report month
            log: logger object
            file_path: Working directory
        """
        self.month = month
        self.logger = log
        self.file_path = file_path

    def sort_data(self, data: List[Dict]) -> List[Dict]:
        """This methos sorts data"""
        try:
            data.sort(key=lambda x: x["amount"], reverse=True)
        except KeyError as e:
            self.logger.error(f"Error sorting expenses: {e}")

        return data

    def _save_figure(self, title: str) -> None:
        """Save the figure to a file."""
        pyplot.savefig(
            os.path.join(self.file_path, f'{title.replace(" ", "_").lower()}.png'),
            dpi=self.DPI,
            bbox_inches="tight",
        )

    def _annotate_month(self):
        """This method plots report month"""
        pyplot.annotate(
            f"**{self.month}**",
            xy=(1, 1),
            xycoords="axes fraction",
            ha="right",
            fontsize=16,
            fontweight="bold",
        )

    def plot_bar_chart(
        self,
        title: str,
        labels: List,
        sizes: List,
        xlabel: str,
        ylabel: str,
        color: str,
    ) -> None:
        """Generate bar charts"""
        try:
            pyplot.figure(figsize=self.FIG_SIZE)
            pyplot.bar(labels, sizes, color=color)
            pyplot.xlabel(xlabel)
            pyplot.ylabel(ylabel)
            pyplot.title(title, fontsize=16, fontweight="bold")
            pyplot.xticks(rotation=45)
            pyplot.tight_layout()
            self._annotate_month()
            self._save_figure(title)
        except ExpenseChartsError as exc:
            self.logger.error(f"Error plotting bar chart: {exc}")

    def plot_pie_chart(
        self, title: str, labels: List, sizes: List, colors: List = None
    ) -> None:
        """Generates pie charts"""
        try:
            pyplot.figure(figsize=self.FIG_SIZE)
            pyplot.pie(
                sizes,
                labels=labels,
                colors=colors,
                autopct="%1.1f%%",
                startangle=90,
                radius=1.2,
                textprops={"fontsize": 12},
            )
            pyplot.title(title, fontsize=16, fontweight="bold")
            pyplot.axis("equal")
            pyplot.tight_layout()
            self._annotate_month()
            self._save_figure(title)
        except ExpenseChartsError as exc:
            self.logger.error(f"Error plotting pie chart: {exc}")

    def build(self, charts):
        """Build charts for given configuration"""
        for chart in charts:
            if chart["type"] == "pie":
                self.plot_pie_chart(
                    chart["title"], chart["labels"], chart["sizes"], chart["colors"]
                )
            elif chart["type"] == "bar":
                self.plot_bar_chart(
                    chart["title"],
                    chart["labels"],
                    chart["sizes"],
                    chart["xlabel"],
                    chart["ylabel"],
                    chart["colors"],
                )
            self.logger.info(
                f"Downloading chart {chart['title']:<27} .................. [Complete]"
            )
