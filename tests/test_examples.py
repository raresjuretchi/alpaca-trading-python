import datetime as dt
from types import SimpleNamespace

import pytest

from alpaca_examples import account, config, paper_order, quotes, sma_signal


def test_sma_matches_manual_calculation():
    assert sma_signal.sma([1, 2, 3, 4, 5], 3) == pytest.approx([2, 3, 4])
    assert sma_signal.sma([1, 2], 3) == []


def test_sma_rejects_bad_window():
    with pytest.raises(ValueError):
        sma_signal.sma([1, 2, 3], 0)


def test_crossover_detects_buy_and_sell():
    falling_then_jump = [10.0] * 10 + [9.0, 8.0, 7.0, 6.0] + [20.0]
    assert sma_signal.crossover_signal(falling_then_jump, fast=2, slow=5) == "buy"
    rising_then_drop = [1.0] * 10 + [2.0, 3.0, 4.0, 5.0] + [-10.0]
    assert sma_signal.crossover_signal(rising_then_drop, fast=2, slow=5) == "sell"


def test_crossover_holds_in_trend_and_needs_data():
    uptrend = [float(i) for i in range(1, 30)]
    assert sma_signal.crossover_signal(uptrend, fast=3, slow=10) == "hold (uptrend)"
    assert sma_signal.crossover_signal([1.0, 2.0], fast=3, slow=10) == "not enough data"
    with pytest.raises(ValueError):
        sma_signal.crossover_signal(uptrend, fast=10, slow=3)


def test_daily_closes_reads_bars_from_client():
    bars = [SimpleNamespace(close=100.5), SimpleNamespace(close=101.25)]
    client = SimpleNamespace(get_stock_bars=lambda req: SimpleNamespace(data={"AAPL": bars}))
    assert sma_signal.daily_closes(client, "AAPL", 10) == [100.5, 101.25]


def test_format_quote_computes_mid_and_spread():
    quote = SimpleNamespace(bid_price=99.0, ask_price=101.0,
                            timestamp=dt.datetime(2026, 1, 2, 15, 30, tzinfo=dt.timezone.utc))
    line = quotes.format_quote("AAPL", quote)
    assert "mid     100.00" in line and "spread 2.00" in line


def test_account_summary_lists_positions(monkeypatch):
    monkeypatch.setenv("ALPACA_PAPER", "true")
    acct = SimpleNamespace(status="ACTIVE", equity="100000", cash="50000", buying_power="200000")
    pos = SimpleNamespace(symbol="AAPL", qty="2", market_value="400", unrealized_pl="10", unrealized_plpc="0.025")
    text = account.summarize(acct, [pos])
    assert "PAPER" in text and "$100,000.00" in text and "AAPL" in text and "+2.50%" in text


@pytest.mark.parametrize("value,expected", [(None, True), ("true", True), ("false", False), ("0", False)])
def test_paper_is_the_default(monkeypatch, value, expected):
    if value is None:
        monkeypatch.delenv("ALPACA_PAPER", raising=False)
    else:
        monkeypatch.setenv("ALPACA_PAPER", value)
    assert config.is_paper() is expected


def test_build_order():
    order = paper_order.build_order("aapl", 0.5, "buy")
    assert order.symbol == "AAPL" and order.qty == 0.5 and order.side.value == "buy"
    with pytest.raises(ValueError):
        paper_order.build_order("AAPL", 0, "buy")


def test_order_script_refuses_live_accounts(monkeypatch):
    monkeypatch.setenv("ALPACA_PAPER", "false")
    assert paper_order.main(["AAPL", "1", "buy", "--submit"]) == 2


def test_order_script_previews_without_submit(monkeypatch, capsys):
    monkeypatch.setenv("ALPACA_PAPER", "true")
    monkeypatch.setattr(paper_order, "trading_client", lambda: pytest.fail("must not connect in preview"))
    assert paper_order.main(["MSFT", "3", "sell"]) == 0
    assert "Preview only" in capsys.readouterr().out
