# indicators-signal-or-illusion

**Do trading indicators show real market patterns, or do they just make noise look like patterns?**

## What This Is

Indicators are built from price data. So when price "bounces" off an indicator line, it might just be price bouncing off its own smoothed average. That would happen on random data too. This project tests three indicators I use together (SSL Channels, AlphaTrend, EMA 200) to find out if the patterns they show are real.

## What I Test

**H1: Do SSL channels act as real support and resistance?**
Compare rejection rates on real data vs 1000 GARCH-generated synthetic price series. If fake data shows the same rate, the pattern is not real.

**H2: Does price move toward EMA 200 after a crossover?**
Compare EMA reach rate after crossovers against two baselines: random entry points and similar sized moves without a crossover.

**H3: Does AlphaTrend help filter bad crossovers?**
Split crossovers into confirmed and unconfirmed by AlphaTrend, then run a permutation test with 10,000 shuffles to check if the difference is real.

All p-values go through Benjamini-Hochberg correction to account for running ~60 tests.

## Data

| Asset | Instrument | Source | Period |
|-------|-----------|---------|--------|
| BTC/USDT |CME Globex        | Databento | Jan 2023 to Feb 2025 |
| ETH/USDT | CME Globex       | Databento | Jan 2023 to Feb 2025 |
| EUR/USD | CME 6E Futures    | Databento | Jan 2023 to Feb 2025 |

All futures. All real exchange volume. Single data provider. Timeframes: 15m, 30m, 1h, 2h, 4h

## Methodology

Based on Lopez de Prado, Advances in Financial Machine Learning (2018). Synthetic nulls (Ch 13), multiple testing correction (Ch 14). No train/test split. Each test builds its own null internally.

## Results

TODO
