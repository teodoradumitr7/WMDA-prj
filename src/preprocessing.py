import pandas as pd
from sklearn.preprocessing import LabelEncoder

def clean_data(path):
    df = pd.read_csv(path)
    if df.empty:
        raise ValueError("Fișierul este gol sau calea este greșită.")
    df.dropna(inplace=True)
    df['km_driven'] = df['km_driven'].str.extract(r'([0-9.]+)').astype(float)
    df['price'] = df['price'].str.replace(r'[^\d]', '', regex=True).astype(float)
    df['price_category'] = pd.qcut(df['price'], q=3, labels=["Buget", "Mediu", "Premium"])
    return df

def encode_data(df, cat_vars):
    encoders = {}
    for col in cat_vars:
        le = LabelEncoder()
        df[col] = le.fit_transform(df[col])
        encoders[col] = le
    return df, encoders
