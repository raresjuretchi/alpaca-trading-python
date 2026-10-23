"""Moving-average crossover signal from daily bars.

    python -m alpaca_examples.sma_signal AAPL MSFT --fast 20 --slow 50

A textbook example, not a trading recommendation: "buy" when the fast SMA
crosses above the slow SMA on the latest bar, "sell" when it crosses below,
otherwise "hold" with the current trend.
"""
from __future__ import annotations

import argparse
import datetime as dt

from alpaca_examples.config import data_client, data_feed


def sma(values: list[float], window: int) -> list[float]:
    """Simple moving average; the result is len(values) - window + 1 long."""
    if window <= 0:
        raise ValueError("window must be positive")
    if len(values) < window:
        return []
    total = sum(values[:window])
    out = [total / window]
    for i in range(window, len(values)):
        total += values[i] - values[i - window]
        out.append(total / window)
    return out


def crossover_signal(closes: list[float], fast: int = 20, slow: int = 50) -> str:
    if fast >= slow:
        raise ValueError("fast window must be shorter than slow window")
    if len(closes) < slow + 1:
        return "not enough data"
    fast_ma = sma(closes, fast)[-2:]
    slow_ma = sma(closes, slow)[-2:]
    was_above, is_above = fast_ma[0] > slow_ma[0], fast_ma[1] > slow_ma[1]
    if is_above and not was_above:
        return "buy"
    if was_above and not is_above:
        return "sell"
    return "hold (uptrend)" if is_above else "hold (downtrend)"


def daily_closes(client, symbol: str, days: int, feed=None) -> list[float]:
    from alpaca.data.requests import StockBarsRequest
    from alpaca.data.timeframe import TimeFrame

    start = dt.datetime.now(dt.timezone.utc) - dt.timedelta(days=int(days * 1.6) + 10)
    request = StockBarsRequest(symbol_or_symbols=symbol, timeframe=TimeFrame.Day, start=start,
                               feed=feed or data_feed())
    bars = client.get_stock_bars(request).data.get(symbol, [])
    return [float(bar.close) for bar in bars]


def main() -> None:
    parser = argparse.ArgumentParser(description="SMA crossover signal")
    parser.add_argument("symbols", nargs="*", default=["AAPL", "MSFT", "SPY"])
    parser.add_argument("--fast", type=int, default=20)
    parser.add_argument("--slow", type=int, default=50)
    args = parser.parse_args()

    client = data_client()
    for symbol in (s.upper() for s in args.symbols):
        closes = daily_closes(client, symbol, args.slow + 5)
        last = f"{closes[-1]:.2f}" if closes else "n/a"
        print(f"{symbol:<6} last close {last:>10}  SMA{args.fast}/{args.slow}: {crossover_signal(closes, args.fast, args.slow)}")


if __name__ == "__main__":
    main()
