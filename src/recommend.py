from sklearn.neighbors import NearestNeighbors

def train_recommender(features_scaled):
    model = NearestNeighbors(n_neighbors=5)
    model.fit(features_scaled)
    return model

def recommend(model, user_vector, df_original, scaler):
    scaled = scaler.transform([user_vector])
    _, indices = model.kneighbors(scaled)
    return df_original.iloc[indices[0]][['name', 'year', 'price']]
