from pathlib import Path

import pandas as pd


DATA_DIR = Path(__file__).resolve().parent.parent / "data"


def load_data():
    movies_df = pd.read_csv(DATA_DIR / "movies_1000_en.csv")
    ratings_matrix = pd.read_csv(DATA_DIR / "user_ratings.csv", index_col=0)
    movie_map = pd.read_csv(DATA_DIR / "movie_columns_map.csv")

    id_to_title = dict(zip(movie_map["movie_col"], movie_map["title"]))
    ratings_matrix.rename(columns=id_to_title, inplace=True)

    movies_df["genre_list"] = movies_df["genres"].apply(
        lambda x: x.split("|") if pd.notna(x) else []
    )

    return movies_df, ratings_matrix
