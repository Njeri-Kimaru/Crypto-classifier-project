import pandas as pd
import os
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
            
df_generate_labels = pd.read_csv(r'data/processed/btcusdt_1dprocessed.csv')
print(df_generate_labels.head())

df_with_labels = generate_labels(df_generate_labels)
print(df_with_labels.tail())
print(df_with_labels.head())

print(df_with_labels['label'].value_counts())

dir = "data/processed/df_with_labels.csv"

if os.path.exists(dir):
    pass
else:
    df_with_labels.to_csv(dir, index=False)