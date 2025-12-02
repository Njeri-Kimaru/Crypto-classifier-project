import pandas as pd
import ta

def generate_features(df):
    """
    Generating price action, volume, technical indicators and features
    """
    df = df.copy()

    # 1. PRICE BASED FEATURES eg computing returns
    # return day 1
    df['return_1d'] = df['close'].pct_change(1)

    # return day 7
    df['return_7d'] = df['close'].pct_change(7)

    # return 30-day
    df['return_30d'] = df['close'].pct_change(30)

    # rolling volatility
    df['volatility_7d'] = df['return_1d'].rolling(7).std()
    df['volatility_30d'] = df['return_1d'].rolling(30).std()

    # 2. MOVING AVERAGES
    df['sma_7'] = df['close'].rolling(7).mean()
    df['sma_20'] = df['close'].rolling(20).mean()
    df['sma_50'] = df['close'].rolling(50).mean()
    df['sma_200'] = df['close'].rolling(200).mean()

    # price relative to moving averages
    df['close_to_sma20'] = df['close']/df['sma_20']-1
    df['close_to_sma50'] = df['close']/df['sma_50']-1

    # 3. MOMENTUM INDICATORS
    # a) RSI indicator
    # best window to use on RSI is 14 day
    # above 70 is overbought hence reducing value(so its better to sell)
    # below 30 is oversold
    df['rsi'] = ta.momentum.RSIIndicator(df['close'], window=14).rsi()

    # b). Stochastic oscillator
    # percentage k current closing price 
    # percentage d  
    df['stoch'] = ta.momentum.StochasticOscillator(
    df['high'], df['low'], df['close']
    ).stoch()

    # 4. TREND INDICATORS
    # a). MACD (MOVING AAVERAGES CONVERGENCE AND DIVERGENCE)
    macd = ta.trend.MACD(df['close'])
    df['macd'] = macd.macd()
    df['macd_signal'] = macd.macd_signal()
    df['macd_diff'] = macd.macd_diff()

    # 5. VOLATILITY INDICATOR
    bollinger = ta.volatility.BollingerBands(df['close'])
    df['bb_high'] = bollinger.bollinger_hband()
    df['bb_low'] = bollinger.bollinger_lband()
    df['bb_width'] = (df['bb_high'] - df['bb_low']) / df['close']

    # 6. VOLUME FEATURES
    df['volume_ma_7'] = df['volume'].rolling(7).mean()
    df['volume_ratio'] = df['volume'] / df['volume_ma_7']

    # 7.PRICE PATTERNS
    df['high_low_ratio'] = df['high'] / df['low'] -1
    df['close_open_ratio'] =df['close'] / df['open'] -1

    return df

def add_stationary_features(df):
    # transforming smas to distance from sma
    df['dist_sma_7'] = (df['close'] / df['sma_7']) - 1
    df['dist_sma_20'] = (df['close'] / df['sma_20']) - 1
    df['dist_sma_50'] = (df['close'] / df['sma_50']) - 1
    df['dist_sma_200'] = (df['close'] / df['sma_200']) - 1

    # 2. Transforming bbs to %b
    df['bb_width_2'] = df['bb_high'] - df['bb_low']
    df['bb_pct_b'] = (df['close'] - df['bb_low'])/ df['bb_width_2']

    #3. Transforming OHLC
    df["close_open_pct"] = (df["close"] - df["open"])/ df["open"]
    df["high_low_pct"] = (df["high"] - df["low"])/ df["low"]

    return df