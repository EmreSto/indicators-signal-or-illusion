# Methodology

## Research Question

Do the patterns observed when using SSL Channels, AlphaTrend, and EMA 200 reflect real market behavior, or are they side effects of the indicator math?

## Why This Matters

Indicators are built from price. When price "bounces" off an indicator line, part of that is price interacting with its own smoothed version. This would happen on random data too. Lopez de Prado (2018) argues that skipping this check leads to false discoveries. This project does not try to find alpha. It tests whether the patterns are real in the first place.

## The Indicators

### SSL Channel

Two simple moving averages form a band around price. A regime variable tracks which side of the band price is on.

**Moving averages:**

$$SMA_H(t) = \frac{1}{N}\sum_{i=0}^{N-1} H_{t-i} \qquad SMA_L(t) = \frac{1}{N}\sum_{i=0}^{N-1} L_{t-i}$$

**Regime variable:**

$$hlv(t) = \begin{cases} +1 & \text{if } C_t > SMA_H(t) \\ -1 & \text{if } C_t < SMA_L(t) \\ hlv(t-1) & \text{otherwise} \end{cases}$$

The regime is sticky. It only flips when price closes beyond a boundary. Inside the channel, the previous state holds.

**Line swap:**

$$\text{If } hlv(t) = +1: \quad \text{upper} = SMA_H(t), \quad \text{lower} = SMA_L(t)$$

$$\text{If } hlv(t) = -1: \quad \text{upper} = SMA_L(t), \quad \text{lower} = SMA_H(t)$$

When the regime flips, the lines swap. This creates the visible crossover on the chart.

**Two channels:** We run $N = 60$ (fast) and $N = 120$ (slow) at the same time.

**Crossover (both channels agree):**

$$\text{crossover}(t) = \begin{cases} +1 & \text{if } hlv_{60}(t) = +1 \text{ and } hlv_{120}(t) = +1 \text{ and they were not both } +1 \text{ at } t-1 \\ -1 & \text{if } hlv_{60}(t) = -1 \text{ and } hlv_{120}(t) = -1 \text{ and they were not both } -1 \text{ at } t-1 \\ 0 & \text{otherwise} \end{cases}$$


The crossover fires on the bar where both regimes first agree on a new direction. The bands may visually cross without triggering this if the hlv values did not actually change.

### AlphaTrend

An adaptive trailing stop combining volatility (ATR), momentum (MFI), and a ratchet mechanism.


**Volatility:**

$$TR_t = \max(H_t - L_t, \; |H_t - C_{t-1}|, \; |L_t - C_{t-1}|)$$

$$ATR(t) = \frac{1}{N}\sum_{i=0}^{N-1} TR_{t-i}$$

ATR uses SMA, not Wilder's smoothing. $N = 14$.

**Support and resistance levels:**

$$upT_t = L_t - \alpha \cdot ATR(t) \qquad downT_t = H_t + \alpha \cdot ATR(t)$$

$\alpha = 1.0$. $upT$ sits one ATR below the low. $downT$ sits one ATR above the high.

**Momentum gate:**

$$\text{bullish}(t) = \begin{cases} \text{true} & \text{if } MFI(t) \geq 50 \\ \text{false} & \text{otherwise} \end{cases}$$

MFI is computed over 14 bars using $HLC3$ and volume. All assets in this project have real exchange volume, so MFI is used uniformly.

**Ratchet:**

$$AT(t) = \begin{cases} \max(upT_t, \; AT(t-1)) & \text{if bullish}(t) \\ \min(downT_t, \; AT(t-1)) & \text{if not bullish}(t) \end{cases}$$

The ratchet only allows movement in the trend direction. This creates the staircase shape. Flat sections mean the new level was not enough to move the line.

**Signal:**

$$\text{signal}(t) = \begin{cases} +1 & \text{if } AT(t) > AT(t-2) \text{ and } AT(t-1) \leq AT(t-3) \\ -1 & \text{if } AT(t) < AT(t-2) \text{ and } AT(t-1) \geq AT(t-3) \\ 0 & \text{otherwise} \end{cases}$$

Buy when AlphaTrend crosses above its 2-bar lagged version. Sell when it crosses below.

### EMA 200

$$EMA(t) = \lambda \cdot C_t + (1 - \lambda) \cdot EMA(t-1) \qquad \lambda = \frac{2}{N+1}$$

With $N = 200$, $\lambda \approx 0.01$. Moves slowly. Acts as a long-term trend reference.

**Cloud:**

$$\text{cloud upper} = EMA(t) \cdot (1 + w) \qquad \text{cloud lower} = EMA(t) \cdot (1 - w)$$

$w = 0.002$. A thin band around the EMA.

## How The System Works Together

1. SSL(60) and SSL(120) run simultaneously.
2. A crossover fires when both regimes first agree on a new direction.
3. AlphaTrend confirms or denies the crossover: if the staircase steps in the same direction, confirmed. If it stays flat or goes the other way, unconfirmed.
4. EMA 200 acts as a target price tends to move toward after a crossover.

## Hypotheses

### H1: SSL Channel Rejection Rates

- **Claim:** SSL channels capture real support and resistance
- **Null:** Rejection rates on real data are no different from synthetic GARCH data
- **Method:** Empirical p-value from 1000 synthetic series. Tested on each channel (60 and 120) separately.

### H2: EMA 200 Attraction Post-Crossover

- **Claim:** Price moves toward EMA 200 after a crossover (both SSLs agree)
- **Null A:** EMA reach rate from crossovers = from random timestamps
- **Null B:** EMA reach rate from crossovers = from similar sized moves without a crossover
- **Method:** Two-proportion z-test, Mann-Whitney U

### H3: AlphaTrend Confirmation Filter

- **Claim:** Confirmed crossovers perform better than unconfirmed ones
- **Null:** No difference. The gap could come from random label assignment
- **Method:** Permutation test (10,000 shuffles)

Confirmed = both SSLs agree + AlphaTrend steps in the same direction. Unconfirmed = both SSLs agree but AlphaTrend flat or opposite.

## Data

| Asset    | Instrument             | Source    | Period              |
|----------|------------------------|-----------|---------------------|
| BTC/USDT | Binance Perp Futures  | Databento | Jan 2023 to Feb 2025 |
| ETH/USDT | Binance Perp Futures  | Databento | Jan 2023 to Feb 2025 |
| EUR/USD  | CME 6E Futures        | Databento | Jan 2023 to Feb 2025 |

All futures. All real exchange volume. Single data provider.

Timeframes: 15m, 30m, 1h, 2h, 4h. Total tests: ~60.

## Test Procedures

### H1: Synthetic Data Comparison

1. Fit GARCH(1,1) to real returns for each asset and timeframe.
2. Generate 1000 synthetic price series from the fitted model. Same statistics, no market structure.
3. Compute SSL rejection rate on each synthetic series and on real data.
4. p-value = proportion of synthetic series with rejection rate >= real.
5. Rejection = price touches channel boundary then closes back inside within a few bars. Breakout = price closes beyond the boundary. Rejection rate = rejections / (rejections + breakouts).

Runs separately for SSL(60) and SSL(120).

### H2: Two-Control Comparison

1. Find all crossovers (both SSLs agree on new direction).
2. Track whether price reaches EMA 200 within 50 bars. Record bars to reach.
3. Control A: same metric from random timestamps (10x sample size).
4. Control B: same metric from points with similar sized price moves but no crossover.
5. Two-proportion z-test and Mann-Whitney U against each control.

Reading results:
- Beats random but not directional moves: crossover just flags big moves.
- Beats both: indicator captures something beyond price movement.
- Beats neither: no EMA attraction effect.

### H3: Permutation Test

1. Find all crossovers. Label as confirmed or unconfirmed by AlphaTrend.
2. Measure directional return at 5, 10, 20 bars forward. Positive = crossover was right.
3. Compute delta = mean(confirmed) - mean(unconfirmed).
4. Shuffle labels 10,000 times. Compute delta each time.
5. p-value = proportion of shuffles where |delta| >= observed.

## Overfitting Defense

No train/test split. Hypotheses came from trading the whole period, so splitting would be dishonest. Instead:

1. **Synthetic nulls (H1):** Must beat structureless data.
2. **Control groups (H2):** Must beat random and directional-move baselines.
3. **Permutation tests (H3):** Must survive random label shuffling.
4. **Multiple comparison correction:** Must survive correction across all tests.

## Multiple Comparison Correction

Benjamini-Hochberg at FDR = 0.05.

1. Sort all p-values: $p_{(1)} \leq p_{(2)} \leq \cdots \leq p_{(m)}$
2. For rank $i$, threshold = $\frac{i}{m} \times 0.05$
3. Find largest $i$ where $p_{(i)} \leq$ threshold.
4. All ranks $\leq i$ are discoveries.

Both raw and corrected p-values reported. Only BH-corrected results claimed.

## References

- Lopez de Prado, M. (2018). *Advances in Financial Machine Learning*. Wiley. Ch 11, 13, 14.
- Benjamini, Y. & Hochberg, Y. (1995). Controlling the false discovery rate.
- Fisher, R.A. (1935). The Design of Experiments.
- KivancOzbilgic. AlphaTrend. MPL 2.0. https://www.tradingview.com/script/o50NYLAZ-AlphaTrend/



