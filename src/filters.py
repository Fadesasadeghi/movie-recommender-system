def apply_filters(movies_df, year_min, year_max, min_rating, min_votes, selected_type, selected_genres, search_title):
    filtered = movies_df[
        (movies_df["year"] >= year_min) & (movies_df["year"] <= year_max)
    ]
    filtered = filtered[filtered["imdb_rating"] >= min_rating]
    filtered = filtered[filtered["num_ratings"] >= min_votes]
    filtered = filtered[filtered["type"] == selected_type]

    if selected_genres:
        filtered = filtered[filtered["genre_list"].apply(
            lambda lst: any(g in lst for g in selected_genres)
        )]

    if search_title:
        filtered = filtered[filtered["title"].str.lower().str.contains(search_title)]

    return filtered