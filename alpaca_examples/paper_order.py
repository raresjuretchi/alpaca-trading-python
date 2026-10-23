"""Place a market order on a PAPER account.

    python -m alpaca_examples.paper_order AAPL 1 buy            # preview only
    python -m alpaca_examples.paper_order AAPL 1 buy --submit   # actually send it

Fractional quantities (e.g. 0.5) are allowed for fractionable stocks.
This script refuses to run against a live account.
"""
from __future__ import annotations

import argparse
import sys

from alpaca_examples.config import is_paper, trading_client


def build_order(symbol: str, qty: float, side: str):
    from alpaca.trading.enums import OrderSide, TimeInForce
    from alpaca.trading.requests import MarketOrderRequest

    if qty <= 0:
        raise ValueError("qty must be positive")
    return MarketOrderRequest(
        symbol=symbol.upper(),
        qty=qty,
        side=OrderSide.BUY if side.lower() == "buy" else OrderSide.SELL,
        time_in_force=TimeInForce.DAY,
    )


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Paper-trading market order")
    parser.add_argument("symbol")
    parser.add_argument("qty", type=float)
    parser.add_argument("side", choices=["buy", "sell"])
    parser.add_argument("--submit", action="store_true", help="send the order (default: preview only)")
    args = parser.parse_args(argv)

    if not is_paper():
        print("Refusing to trade: ALPACA_PAPER is false. This example only places paper orders.", file=sys.stderr)
        return 2

    order = build_order(args.symbol, args.qty, args.side)
    print(f"Order: {order.side.value.upper()} {order.qty} {order.symbol} at market, time in force DAY (paper)")
    if not args.submit:
        print("Preview only. Re-run with --submit to send it to your paper account.")
        return 0

    placed = trading_client().submit_order(order_data=order)
    print(f"Submitted: id {placed.id}, status {placed.status}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
