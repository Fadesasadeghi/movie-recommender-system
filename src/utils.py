def extract_all_genres(movies_df):
    return sorted({g for sublist in movies_df["genre_list"] for g in sublist})

def get_content_types():
    return ["Movie", "TV Show"]