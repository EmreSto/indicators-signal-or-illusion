# indicators-signal-or-illusion

**Do multi-timeframe regime indicators capture market structure, or just reshape noise into patterns?**

I trade discretionarily using a combined indicator system: SSL Channels (periods 60 and 120) + AlphaTrend (14, 1.0) + EMA 200 cloud. Over three years of live trading on crypto and forex, I developed intuitions about when these indicators "work." This project tests whether those intuitions have statistical basis or whether I've been pattern-matching on mathematical artifacts.

## The Core Question

Technical indicators are computed FROM price. An SMA channel is just smoothed price — so price bouncing off it is partly price bouncing off its own average. AlphaTrend is a volatility-adjusted trailing stop — so its "confirmation" might just be restating what price already told us. The question is: **do these tools capture something real about market microstructure, or do they produce patterns that look meaningful to the human eye but have no predictive content?**

## Three Hypotheses

### H1: Do SSL channels produce real support/resistance?
I observe that price rejects off channel boundaries on some timeframes. But would the same thing happen on synthetic data with no market structure?
- **Method:** Compare real rejection rates against 1000 GARCH-simulated price series
- **Null:** No difference between real and synthetic

### H2: Does price gravitate toward EMA 200 after crossovers?
After an SSL crossover, price seems to move toward EMA 200. But price oscillates around its average naturally — is this just mean reversion?
- **Method:** Compare crossover-triggered EMA approach rate vs (A) random timestamps and (B) equivalent directional moves without crossovers
- **Null A:** Crossover rate = random rate. **Null B:** Crossover rate = directional move rate

### H3: Does AlphaTrend filter false crossovers?
When AlphaTrend confirms an SSL crossover (staircase steps in same direction), the trade seems to work more often. Is this real?
- **Method:** Permutation test — shuffle confirmed/unconfirmed labels 10,000 times
- **Null:** Return difference could arise from random label assignment

## Statistical Rigor

Inspired by Lopez de Prado's *Advances in Financial Machine Learning* (2018), this project applies:

- **Synthetic null distributions** (Ch 13): Test indicators against structureless data, not just historical splits
- **Proper control groups**: Don't just ask "does it work?" — ask "does it work better than the obvious alternative?"
- **Permutation tests**: Distribution-free hypothesis testing with no normality assumptions
- **Benjamini-Hochberg correction**: With ~60 individual tests, some will be "significant" by chance. BH controls the false discovery rate at 5%

We do NOT use a train/test split because hypothesis formation occurred across the entire data period. Instead, each test generates its own null distribution internally.

> "Backtesting is not a research tool. Researching and backtesting is like drinking and driving." — Lopez de Prado (2018)

## Data

| Asset | Instrument | Source | Period |
|-------|-----------|--------|--------|
| BTC/USDT | Binance Perpetual Futures | Databento | Jan 2023 - Feb 2025 |
| ETH/USDT | Binance Perpetual Futures | Databento | Jan 2023 - Feb 2025 |
| EUR/USD | CME 6E Futures | Databento | Jan 2023 - Feb 2025 |

All three are exchange-traded futures with real volume. Single data provider ensures consistent quality.

Timeframes: 15m, 30m, 1h, 2h, 4h

## Project Structure
```
├── docs/
│   ├── methodology.md              # Full research framework
│   ├── ssl_channel_math.md         # Indicator math derivation
│   └── alphatrend_math.md          # Indicator math derivation
├── pinescript/
│   ├── ssl_channel.pine            # Documented PineScript rebuild
│   ├── alpha_trend.pine            # Documented PineScript rebuild
│   └── mtf_regime_combined.pine    # Combined system (my live config)
├── src/
│   ├── indicators.py               # Python indicator implementations
│   ├── signals.py                  # Event detection and classification
│   ├── synthetic.py                # GARCH fitting + synthetic data generation
│   ├── tests.py                    # H1, H2, H3 statistical tests
│   ├── corrections.py              # Benjamini-Hochberg correction
│   └── fetch_data.py               # Databento loading + standardization
├── notebooks/
│   ├── 00_validation.ipynb         # Indicator implementation verification
│   ├── 01_h1_synthetic_null.ipynb  # H1 analysis
│   ├── 02_h2_ema_attraction.ipynb  # H2 analysis
│   ├── 03_h3_permutation.ipynb     # H3 analysis
│   └── 04_summary.ipynb            # BH correction + conclusions
├── output/figures/                  # Generated plots
├── output/tables/                   # Summary statistics
├── data/raw/                        # Raw Databento exports (gitignored)
└── data/                            # Processed CSVs (gitignored)
```

## Indicator Attribution

- **SSL Channel:** ErwinBeckers (TradingView). Reverse-engineered and documented.
- **AlphaTrend:** KivancOzbilgic. Open source (Mozilla Public License 2.0). Reverse-engineered and documented.
- **EMA Cloud:** Standard implementation.

Settings match my live trading configuration. No optimization was performed.

## Running
```bash
pip install -r requirements.txt

# Place Databento exports in data/raw/ directory
# Then process into standardized CSVs:
python -m src.fetch_data

# Run notebooks in order
jupyter notebook notebooks/
```

## Results

TODO: Summary table of all p-values (raw and BH-corrected) will go here after analysis.

## Author

Yusuf Emre Yilmaz — MSc Data Science applicant with 3 years of live algorithmic trading experience.
