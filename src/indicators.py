import numpy as np
import pandas as pd 

def hma(series, length):
    half_wma = series.rolling(length // 2).apply(lambda x: np.average(x, weights=range(1, len(x)+1)))
    full_wma = series.rolling(length).apply(lambda x: np.average(x, weights=range(1, len(x)+1)))
    sqrt_len = round(np.sqrt(length))
    diff = 2 * half_wma - full_wma
    return diff.rolling(sqrt_len).apply(lambda x: np.average(x, weights=range(1, len(x)+1))) 
  
def ssl_channels(df,length):
    high = df['high']
    low = df['low']
    close = df['close']
    hma_high = hma(high, length)
    hma_low = hma(low, length)
    hlv = np.zeros(len(df))
    for i in range(length, len(df)):
        if close.iloc[i] >hma_high.iloc[i]:
            hlv[i] = 1
        elif close.iloc[i] < hma_low.iloc[i]:
            hlv[i] = -1
        else:
            hlv[i] = hlv[i-1]    
    return hlv, hma_high, hma_low

def alpha_trend(df, length=14, alpha=1.0):
    high = df['high']
    low = df['low']
    close = df['close']

    tr = np.zeros(len(df))
    for i in range(1, len(df)):
        tr[i] = max(high.iloc[i] - low.iloc[i], abs(high.iloc[i] - close.iloc[i-1]), abs(low.iloc[i] - close.iloc[i-1]))
    atr = pd.Series(tr, index=df.index).rolling(length).mean()
    upT = low - alpha * atr
    downT = high + alpha * atr
    typical_price = (high + low + close) / 3
    raw_money_flow = typical_price * df['volume']
    positive_flow = np.zeros(len(df))
    negative_flow = np.zeros(len(df))
    for i in range(length, len(df)):
        if typical_price.iloc[i] > typical_price.iloc[i-1]:
            positive_flow[i] = raw_money_flow.iloc[i]
        elif typical_price.iloc[i] < typical_price.iloc[i-1]:
            negative_flow[i] = raw_money_flow.iloc[i]
    positive_sum = pd.Series(positive_flow, index=df.index).rolling(length).sum()
    negative_sum = pd.Series(negative_flow, index=df.index).rolling(length).sum()
    negative_sum = negative_sum.replace(0, np.nan)
    money_flow_index = 100 - (100 / (1 + (positive_sum / negative_sum)))
    at = np.zeros(len(df))
    for i in range(length, len(df)):
        if money_flow_index.iloc[i] >= 50:
            at[i] = max(upT.iloc[i], at[i-1])
        else:
            at[i] = min(downT.iloc[i], at[i-1])
    return at

def EMA200(df):
    ema_close = df['close'].ewm(span=200, adjust=False).mean()
    ema_high  = df['high'].ewm(span=200, adjust=False).mean()
    cloud_upper = ema_high
    cloud_lower = ema_close
    return ema_close, cloud_upper, cloud_lower
