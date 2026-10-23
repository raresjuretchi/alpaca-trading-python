# Alpaca Trading Python

[![CI](https://github.com/raresjuretchi/alpaca-trading-python/actions/workflows/ci.yml/badge.svg)](https://github.com/raresjuretchi/alpaca-trading-python/actions/workflows/ci.yml)
![Python](https://img.shields.io/badge/python-3.11%2B-blue)
![License](https://img.shields.io/badge/license-MIT-green)

Small, runnable scripts for the [Alpaca](https://alpaca.markets) trading and market-data APIs with the official `alpaca-py` SDK: account and positions, live quotes, daily bars with a moving-average crossover signal, and a guarded paper-trading order.

> **Educational code, not financial advice.** Everything defaults to a **paper** (simulated) account, and the order script refuses to run against a live one.

## Quick start

```bash
git clone https://github.com/raresjuretchi/alpaca-trading-python.git
cd alpaca-trading-python
python -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
cp .env.example .env   # then add your paper-trading keys
python -m alpaca_examples.account
```

Create paper keys in the Alpaca dashboard under your **Paper** account.

## The scripts

| Script | What it shows |
|---|---|
| `python -m alpaca_examples.account` | Equity, cash, buying power and open positions |
| `python -m alpaca_examples.quotes AAPL MSFT` | Latest bid/ask, mid price and spread |
| `python -m alpaca_examples.sma_signal AAPL --fast 20 --slow 50` | Daily bars → SMA crossover signal (buy / sell / hold) |
| `python -m alpaca_examples.paper_order AAPL 1 buy [--submit]` | Market order on the paper account; previews unless `--submit` |

## Configuration

| Variable | Default | Purpose |
|---|---|---|
| `ALPACA_API_KEY` / `ALPACA_SECRET_KEY` | — | API key pair (required) |
| `ALPACA_PAPER` | `true` | Use the paper endpoint; the order script refuses `false` |
| `ALPACA_DATA_FEED` | `iex` | Market-data feed; `sip` needs a paid data plan |

## Tests

```bash
pip install -r requirements-dev.txt
pytest
```

The signal logic is pure Python and the clients are faked, so the tests run offline without keys.

## Maintenance

A scheduled workflow checks the pinned dependencies once a week at a random time, bumps them when the tests still pass and records the result in [MAINTENANCE.md](MAINTENANCE.md).

<!-- maintenance:start -->
**Last maintenance:** not run yet
<!-- maintenance:end -->

## License

MIT — see [LICENSE](LICENSE).
