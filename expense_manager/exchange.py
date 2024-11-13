from typing import Set
import requests
from expense_manager.config import URLS, get_url
from expense_manager.exception import ExchangeAPIError, ExchangeAPIValueError


class CurrencyRatesAPI:
    """Currency exchange rates API"""

    def __init__(
        self,
        is_historical: bool = False,
        url: str = "latest_symbol",
        base_currency: str = None,
        target_currency: str = None,
        date_yyyymmdd: str = None,
        **kwargs,
    ):
        """

        Args:
            **kwargs:
        """
        self.logger = None
        self.url = url
        self.base_currency = base_currency
        self.target_currency = target_currency
        self.date_yyyymmdd = date_yyyymmdd
        self.is_historical = is_historical
        self.supported_currency = CurrencyRatesAPI.get_currency_list()
        for _key, _value in kwargs.items():
            setattr(self, _key, _value)

        if self.is_historical:
            if self.date_yyyymmdd is None:
                raise ExchangeAPIValueError(
                    "For Historical request date_yyyymmdd parameter is required."
                )

        if self.url not in URLS.keys():
            raise ExchangeAPIValueError(
                f"Invalid url {self.url}. Allowed values are {URLS.keys()}"
            )

        if self.base_currency:
            if self.base_currency not in self.supported_currency:
                raise ExchangeAPIValueError(
                    f"Invalid Currency {self.url}. Allowed values are {self.supported_currency}"
                )

        if self.target_currency:
            if self.target_currency not in self.supported_currency:
                raise ExchangeAPIValueError(
                    f"Invalid Currency {self.url}. Allowed values are {self.supported_currency}"
                )

    @staticmethod
    def get_currency_list() -> Set:
        url = get_url("base_url", "currencies")
        return set(requests.get(url).json().keys())

    def get_exchange_rates(self):
        _url = get_url("base_url", self.url)

        # latest request
        if not self.is_historical:
            if self.target_currency:
                url = _url.format(base=self.base_currency, target=self.target_currency)
            else:
                url = _url.format(base=self.base_currency)
        # Historical request
        else:
            if self.target_currency:
                url = _url.format(
                    base=self.base_currency,
                    target=self.target_currency,
                    YYYYMMDD=self.date_yyyymmdd,
                )
            else:
                url = _url.format(base=self.base_currency, YYYYMMDD=self.date_yyyymmdd)
        try:
            self.logger.info(f"URL: {url}")
            response = requests.get(url)
            self.logger.info(f"API Response: {response.json()}")
        except ExchangeAPIError as exc:
            self.logger.error(f"API error {exc}")
            raise
