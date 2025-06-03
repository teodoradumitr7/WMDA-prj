import pandas as pd
from sklearn.preprocessing import LabelEncoder

def clean_data(path):
    df = pd.read_csv(path)
    if df.empty:
        raise ValueError("Fișierul este gol sau calea este greșită.")
    df.dropna(inplace=True)
    df['mileage'] = df['mileage'].str.extract(r'([0-9.]+)').astype(float)
    df['engine'] = df['engine'].str.extract(r'([0-9.]+)').astype(float)
    df['max_power'] = df['max_power'].str.extract(r'([0-9.]+)').astype(float)
    df['torque'] = df['torque'].str.extract(r'([0-9.]+)').astype(float)
    df['price_category'] = pd.qcut(df['selling_price'], q=3, labels=["Buget", "Mediu", "Premium"])
    return df

def encode_data(df, cat_vars):
    encoders = {}
    for col in cat_vars:
        le = LabelEncoder()
        df[col] = le.fit_transform(df[col])
        encoders[col] = le
    return df, encoders
