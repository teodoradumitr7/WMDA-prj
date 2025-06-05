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


'''
                         name  year    price
42  FORD TRANSIT CUSTOM 2.0 D  2022  16500.0
49            VOLVO S90 2.0 D  2019  20900.0
19            VOLVO V60 2.0 L  2020  17990.0
34          BMW SERIA 5 2.0 D  2020  26400.0
63               BMW X3 2.0 D  2018  24900.0

intrari:
Introduceți detaliile mașinii:
Anul (ex: 2018): 2017
Km rulați: 25000
Tip combustibil (Diesel/Benzina): Benzina

Se remarca cele mai apropiate 5 mașini conform preferintelor introduse si conform algoritmului de recomandare K-Nearest Neighbors, cu k=5.
Modelul a comparat această intrare cu toate din baza de date, folosind caracteristicile (year, km_driven, fuel) și a găsit cele mai asemănătoare anunțuri.

Regresie Liniară R²: 0.37
R² = coeficientul de determinare ce măsoară cât de bine se pot explica valorile prețurilor reale folosind modelul
    doar 37% din variația prețurilor este explicată de model.
    modelul de regresie liniară nu este foarte bun, valoare mai aproape de 0 decat de 1
    poate fi îmbunătățit cu mai multe variabile (ex: marca, tip caroserie etc.).

    

--- Classification Report ---
              precision    recall  f1-score   support

       Buget       0.40      1.00      0.57         2
       Mediu       0.75      0.50      0.60         6
     Premium       0.80      0.67      0.73         6

    accuracy                           0.64        14
   macro avg       0.65      0.72      0.63        14
weighted avg       0.72      0.64      0.65        14

Precision: cât de precise sunt predicțiile (ex: din toate mașinile prezise ca "Premium", câte chiar erau "Premium"?).
Recall: din toate mașinile "Premium" reale, câte au fost recunoscute corect?
f1-score: media armonică dintre precision și recall (echilibru).
support: câte exemple au fost în fiecare clasă.
Acuratete 64%.

Clasa "Buget" are doar 2 exemple, dar a fost prezisă 100% corect (recall = 1.00), dar modelul e nesigur (precision = 0.40).
Clasa "Mediu" și "Premium" sunt mai echilibrate, dar încă au erori.

--- Confusion Matrix ---
[[2 0 0]    - Buget
 [2 3 1]    - Mediu
 [1 1 4]]   - Premium


 2+3+1=6 exemple reale "Mediu":
    2 prezise greșit ca "Buget"
    3 corect ca "Mediu"
    1 greșit ca "Premium"

'''