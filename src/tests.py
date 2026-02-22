from indicators import ssl_channels
def compute_touch_returns(df,length, forward_bars):
    hlv, hma_high, hma_low = ssl_channels(df,length)
    returns = []
    for i in range(len(df)):
        if i + forward_bars >= len(df):
            continue
        if df['low'].iloc[i] <= hma_high[i] and hlv[i] == 1:
            ret = (df['close'].iloc[i + forward_bars] - df['close'].iloc[i]) / df['close'].iloc[i]
            returns.append(ret)
        elif df['high'].iloc[i] >= hma_low[i] and hlv[i] == -1:
            ret = (df['close'].iloc[i] - df['close'].iloc[i + forward_bars]) / df['close'].iloc[i]
            returns.append(ret)
    return returns

