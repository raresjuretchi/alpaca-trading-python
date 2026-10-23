"""Credentials and clients. Paper trading is the default and the safe choice."""
from __future__ import annotations

import os
import sys

from dotenv import load_dotenv

load_dotenv()


def _keys() -> tuple[str, str]:
    key, secret = os.getenv("ALPACA_API_KEY"), os.getenv("ALPACA_SECRET_KEY")
    if not key or not secret:
        sys.exit("ALPACA_API_KEY / ALPACA_SECRET_KEY are not set. Copy .env.example to .env and add your keys.")
    return key, secret


def is_paper() -> bool:
    """True unless ALPACA_PAPER is explicitly set to false."""
    return os.getenv("ALPACA_PAPER", "true").strip().lower() not in {"0", "false", "no", "off"}


def data_feed():
    """IEX works on free accounts; set ALPACA_DATA_FEED=sip if your plan includes it."""
    from alpaca.data.enums import DataFeed

    return DataFeed(os.getenv("ALPACA_DATA_FEED", "iex").lower())


def trading_client():
    from alpaca.trading.client import TradingClient

    key, secret = _keys()
    return TradingClient(key, secret, paper=is_paper())


def data_client():
    from alpaca.data.historical import StockHistoricalDataClient

    key, secret = _keys()
    return StockHistoricalDataClient(key, secret)


def symbols_from_args(default: list[str]) -> list[str]:
    return [s.upper() for s in sys.argv[1:]] or default
