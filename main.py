from src.config import *
from src.preprocessing import clean_data, encode_data
from src.recommend import train_recommender, recommend
from src.user_input import get_user_input
from src.regression_model import build_regression_pipeline
from src.nn_model import train_nn
from src.classifier import train_classifier
import pandas as pd
import torch
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import classification_report, confusion_matrix

# 1. Clean and encode
df = clean_data(DATA_PATH)

# from src.web_scraper import scrape_autovit
# scraped_path = scrape_autovit(num_pages=2)  # sau câte pagini vrei
# df = clean_data(scraped_path)
df, encoders = encode_data(df, CATEGORICAL_VARS)

print(df)


# 2. Recommender
features = df[NUMERIC_VARS + CATEGORICAL_VARS]
scaler = StandardScaler()
features_scaled = scaler.fit_transform(features)
model = train_recommender(features_scaled)

# 3. Get recommendations
user_data = get_user_input()
for col in CATEGORICAL_VARS:
    user_data[col] = encoders[col].transform([user_data[col]])[0]
user_vector = [user_data[col] for col in NUMERIC_VARS + CATEGORICAL_VARS]
recs = recommend(model, user_vector, df, scaler)
print("\nRecomandări auto:")
print(recs)

# 4. Regression
X = df[FEATURE_VARS]
X_scaled = scaler.fit_transform(X)

y = df['price']
y_classification = df[CLASSIFICATION_TARGET]
pipe = build_regression_pipeline()
pipe.fit(X, y)
print(f"\nRegresie Liniară R²: {pipe.score(X, y):.2f}")

# 5. NN training
# X_nn = torch.tensor(scaler.transform(df[NUMERIC_VARS]), dtype=torch.float32)
X_nn = torch.tensor(X_scaled, dtype=torch.float32)
y_nn = torch.tensor(y.values, dtype=torch.float32).view(-1, 1)
X_train, X_test, y_train, y_test = train_test_split(X_nn, y_nn, test_size=0.2)
train_nn(X_train, y_train, X_test, y_test)
print("\nNN Loss plot salvat în visuals/nn_loss_plot.png")

# 6. Classification
from sklearn.model_selection import train_test_split
X_train_cls, X_test_cls, y_train_cls, y_test_cls = train_test_split(X_scaled, y_classification, test_size=0.2, random_state=42)

clf = train_classifier(X_train_cls, y_train_cls, FEATURE_VARS)

# 7. Evaluation
print("\n--- Classification Report ---")
y_pred_cls = clf.predict(X_test_cls)
print(classification_report(y_test_cls, y_pred_cls))
print("\n--- Confusion Matrix ---")
print(confusion_matrix(y_test_cls, y_pred_cls))


