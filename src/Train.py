import numpy as np
import pandas as pd
from sklearn.model_selection import TimeSeriesSplit
from sklearn.preprocessing import StandardScaler
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import classification_report, confusion_matrix
from xgboost import XGBClassifier
from lightgbm import LGBMClassifier
import joblib

def prepare_data(df_features, df_labels):
    #loading data

    if len(df_features) != len(df_labels):
        df_merged = pd.concat([df_features, df_labels], axis=1, join="inner" )
    else:
        df_merged = pd.concat([df_features, df_labels], axis=1)
    
    df_clean = df.merged.dropna()

    columns = ["dist_sma_7","dist_sma_20", "dist_sma_50", "dist_sma_200 ", "bb_pct_b", "rsi","volume_ratio", "close_open_pct" ,"high_low_pct", "macd_diff","label" ]
    df_processed = df_clean[columns]

    x = df_processed.drop("label", axis=1)
    y = df_processed["label"]

    print(f'successful',x.info(),y.info())

cont_data = prepare_data(
    "data/processed/features.csv",
    "data/processed/df_with_labels.csv"
)
