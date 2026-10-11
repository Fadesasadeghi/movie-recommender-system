import pandas as pd
from sklearn.metrics.pairwise import cosine_similarity

def get_knn_recommendation(target_title, valid_movies, ratings_matrix, movies_df):
    filled = ratings_matrix.fillna(0)
    if target_title not in filled.columns:
        return None

    sim = cosine_similarity(filled.T)
    sim_df = pd.DataFrame(sim, index=filled.columns, columns=filled.columns)
    similar_titles = sim_df[target_title].sort_values(ascending=False)

    valid_set = set(valid_movies['title'])
    for title in similar_titles.index:
        if title != target_title and title in valid_set:
            return movies_df[movies_df['title'] == title].iloc[0]
    return None