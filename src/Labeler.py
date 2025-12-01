import pandas as pd
def generate_labels(df, threshold = 0.02, horizon = 1):
    df = df.copy()

    #calculate future returns
    df['future_return'] = df['close'].pct_change().shift(-horizon)

    def classify(ret):
        if pd.isna(ret):
            return None
        elif ret > threshold:
            return 2 #buy
        elif ret < -threshold:
            return 0 #sell
        else:
            return 1 #hold
            
    df['label'] = df['future_return'].apply(classify)

    #drop rows with nan values
    df = df.dropna(subset = ['label'])
    df['label'] = df['label'].astype(int)

    return df
            