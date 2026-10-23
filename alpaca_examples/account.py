"""Print account balances and open positions.

    python -m alpaca_examples.account
"""
from alpaca_examples.config import is_paper, trading_client


def money(value) -> str:
    return f"${float(value):,.2f}"


def summarize(account, positions) -> str:
    lines = [
        f"Mode:          {'PAPER' if is_paper() else 'LIVE'}",
        f"Status:        {account.status}",
        f"Equity:        {money(account.equity)}",
        f"Cash:          {money(account.cash)}",
        f"Buying power:  {money(account.buying_power)}",
        "",
        f"Open positions: {len(positions)}",
    ]
    for p in positions:
        lines.append(
            f"  {p.symbol:<6} qty {float(p.qty):>10,.4f}  value {money(p.market_value):>14}  "
            f"P/L {money(p.unrealized_pl):>12} ({float(p.unrealized_plpc) * 100:+.2f}%)"
        )
    return "\n".join(lines)


def main() -> None:
    client = trading_client()
    print(summarize(client.get_account(), client.get_all_positions()))


if __name__ == "__main__":
    main()
