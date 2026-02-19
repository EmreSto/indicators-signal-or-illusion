import numpy as np
import pandas as pd 
def hma(series, length):
    half_wma = series.rolling(length // 2).apply(lambda x: np.average(x, weights=range(1, len(x)+1)))
    full_wma = series.rolling(length).apply(lambda x: np.average(x, weights=range(1, len(x)+1)))
    sqrt_len = round(np.sqrt(length))
    diff = 2 * half_wma - full_wma
    return diff.rolling(sqrt_len).apply(lambda x: np.average(x, weights=range(1, len(x)+1)))   
def ssl_channels(df,length):
    high = df['High']
    low = df['Low']
    close = df['Close']
    hma_high = hma(high, length)
    hma_low = hma(low, length)
    hlv = np.zeros(len(df))
    for i in range(length, len(df)):
        if close[i] >hma_high[i]:
            hlv[i] = 1
        elif close[i] < hma_low[i]:
            hlv[i] = -1
        else:
            hlv[i] = hlv[i-1]    
    return hlv, hma_high, hma_low
def crossoverdetection(df):
    ssl60, hma_high60, hma_low60 = ssl_channels(df,60)
    ssl120, hma_high120, hma_low120 = ssl_channels(df,120)  
    crossover = np.zeros(len(df))
    for i in range(1, len(df)):
        if ssl60[i] == 1 and ssl120[i] == 1 and (ssl60[i-1] != 1 or ssl120[i-1] != 1):
            crossover[i] = 1
        elif ssl60[i] == -1 and ssl120[i] == -1 and (ssl60[i-1] != -1 or ssl120[i-1] != -1):
            crossover[i] = -1
    return crossover
def alpha_trend(df, length=14, alpha=1.0):
    high = df['High']
    low = df['Low']
    close = df['Close']
    
    tr = np.zeros(len(df))
    for i in range(1, len(df)):
        tr[i] = max(high[i] - low[i], abs(high[i] - close[i-1]), abs(low[i] - close[i-1]))
    atr = pd.Series(tr).rolling(length).mean()
    upT = low - alpha * atr
    downT = high + alpha * atr
    typical_price = (high + low + close) / 3
    raw_money_flow = typical_price * df['Volume']
    positive_flow = np.zeros(len(df))
    negative_flow = np.zeros(len(df))
    for i in range(length, len(df)):
        if typical_price[i] > typical_price[i-1]:
            positive_flow[i] = raw_money_flow[i]
        elif typical_price[i] < typical_price[i-1]:
            negative_flow[i] = raw_money_flow[i]
    positive_sum = pd.Series(positive_flow).rolling(length).sum()
    negative_sum = pd.Series(negative_flow).rolling(length).sum()
    negative_sum = negative_sum.replace(0, np.nan)
    money_flow_index = 100 - (100 / (1 + (positive_sum / negative_sum)))
    at = np.zeros(len(df))
    for i in range(length, len(df)):
        if money_flow_index[i] >= 50:
            at[i] = max(upT[i], at[i-1])
        else:
            at[i] = min(downT[i], at[i-1])
    return at
def EMA200(df):
    ema_close = df['Close'].ewm(span=200, adjust=False).mean()
    ema_high  = df['High'].ewm(span=200, adjust=False).mean()
    cloud_upper = ema_high
    cloud_lower = ema_close
    return ema_close, cloud_upper, cloud_lower
