import pandas as pd
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.preprocessing import StandardScaler

def preprocess_items(items_data):
    items_data['genres'] = items_data['genres'].apply(lambda genre_list: ','.join([genre.name for genre in genre_list]) if genre_list else '')
    genres = items_data["genres"].str.get_dummies(sep=",")
    items_data = pd.concat([items_data, genres], axis=1)
    directors = pd.get_dummies(items_data["director"], prefix="director")
    items_data = pd.concat([items_data, directors], axis=1)
    items_data = items_data.drop(columns=["genres", "director"], errors="ignore")
    return items_data

def recommend_items(user_id, preferences, items_data):
    items_data = preprocess_items(items_data)
    user_prefs = preferences[preferences["user_id"] == user_id]

    liked_movies = user_prefs[user_prefs["interaction"] == 1]["item_id"].tolist()
    disliked_movies = user_prefs[user_prefs["interaction"] == -1]["item_id"].tolist()

    if not liked_movies and not disliked_movies:
        return []

    user_profile = items_data[items_data["id"].isin(liked_movies)]

    # Добавляем отсутствующие столбцы в user_profile и заполняем нулями
    missing_cols = set(items_data.columns) - set(user_profile.columns)
    for c in missing_cols:
        user_profile[c] = 0

    numeric_columns = user_profile.select_dtypes(include=["number"]).drop(columns=["id", "interaction"], errors="ignore")

    if not numeric_columns.empty:
        user_vector = numeric_columns.mean(axis=0)
    else:
        return []

    numeric_items_data = items_data.select_dtypes(include=["number"]).drop(columns=["id"], errors="ignore")
    scaler = StandardScaler()
    numeric_items_data_scaled = scaler.fit_transform(numeric_items_data)
    user_vector_scaled = scaler.transform([user_vector])

    similarity_scores = cosine_similarity(user_vector_scaled, numeric_items_data_scaled)
    items_data["similarity"] = similarity_scores[0]

    unseen_items = items_data[~items_data["id"].isin(user_prefs["item_id"])]
    unseen_items = unseen_items[~unseen_items["id"].isin(disliked_movies)]

    recommendations = unseen_items.sort_values("similarity", ascending=False)
    return recommendations[["id", "title", "similarity"]].head(10)
