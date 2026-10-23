"""Latest bid/ask quotes for one or more stocks.

    python -m alpaca_examples.quotes AAPL MSFT NVDA
"""
from alpaca_examples.config import data_client, data_feed, symbols_from_args


def latest_quotes(client, symbols: list[str], feed=None) -> dict:
    from alpaca.data.requests import StockLatestQuoteRequest

    request = StockLatestQuoteRequest(symbol_or_symbols=symbols, feed=feed or data_feed())
    return client.get_stock_latest_quote(request)


def format_quote(symbol: str, quote) -> str:
    bid, ask = float(quote.bid_price), float(quote.ask_price)
    mid = (bid + ask) / 2 if bid and ask else bid or ask
    spread = ask - bid if bid and ask else 0.0
    return f"{symbol:<6} bid {bid:>10.2f}  ask {ask:>10.2f}  mid {mid:>10.2f}  spread {spread:.2f}  ({quote.timestamp:%H:%M:%S %Z})"


def main() -> None:
    symbols = symbols_from_args(["AAPL", "MSFT", "SPY"])
    for symbol, quote in latest_quotes(data_client(), symbols).items():
        print(format_quote(symbol, quote))


if __name__ == "__main__":
    main()
