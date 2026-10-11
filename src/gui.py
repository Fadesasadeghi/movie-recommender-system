import tkinter as tk
from tkinter import ttk, messagebox
from filters import apply_filters
from recommender import get_knn_recommendation

def show_movie_window(movie, root):
    win = tk.Toplevel(root)
    win.title(f"{movie['title']} ({movie['year']})")
    win.geometry("600x400")

    ttk.Label(
        win, 
        text=f"{movie['title']} ({movie['year']})", 
        font=("Arial", 14, "bold")
    ).pack(pady=5)

    ttk.Label(
        win,
        text=(
            f"Genres: {movie['genres']}\n"
            f"Type: {movie['type']}\n"
            f"IMDb: {movie['imdb_rating']} | Votes: {movie['num_ratings']}"
        ),
        font=("Arial", 10)
    ).pack(pady=5)

    frame = ttk.Frame(win)
    frame.pack(fill="both", expand=True, pady=5)

    scrollbar = ttk.Scrollbar(frame, orient="vertical")
    text = tk.Text(
        frame, wrap="word", yscrollcommand=scrollbar.set, font=("Arial", 10)
    )

    summary = movie.get("summary", None)
    summary = summary if summary and summary == summary else "No summary available."
    text.insert("1.0", summary)

    text.config(state="disabled")
    text.pack(side="left", fill="both", expand=True)
    scrollbar.config(command=text.yview)
    scrollbar.pack(side="right", fill="y")


def start_gui(movies_df, ratings_matrix, all_genres, content_types):
    root = tk.Tk()
    root.title("Movie Recommender with ML")
    root.geometry("900x650")

    filters_frame = ttk.LabelFrame(root, text="Filters", padding=15)
    filters_frame.pack(side="left", fill="y", padx=200, pady=15)

    ttk.Label(filters_frame, text="Select Genres:").pack(anchor="w")

    genres_canvas = tk.Canvas(filters_frame, width=260, height=220, highlightthickness=0)
    scrollbar = ttk.Scrollbar(filters_frame, orient="vertical", command=genres_canvas.yview)

    scrollable_frame = ttk.Frame(genres_canvas)
    scrollable_frame.bind(
        "<Configure>", 
        lambda e: genres_canvas.configure(scrollregion=genres_canvas.bbox("all"))
    )

    genres_canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
    genres_canvas.configure(yscrollcommand=scrollbar.set)

    genres_canvas.pack(side="left")
    scrollbar.pack(side="right", fill="y")

    genre_vars = {}
    for i, g in enumerate(all_genres):
        var = tk.IntVar()
        chk = ttk.Checkbutton(scrollable_frame, text=g, variable=var)
        chk.grid(row=i//2, column=i%2, sticky="w", padx=5, pady=2)
        genre_vars[g] = var

    type_var = tk.StringVar(value="Movie")
    ttk.Label(filters_frame, text="Content Type:").pack(anchor="w", pady=(10, 0))
    ttk.Combobox(
        filters_frame, values=content_types, textvariable=type_var, state="readonly"
    ).pack(pady=2)

    year_min_var = tk.IntVar(value=2020)
    year_max_var = tk.IntVar(value=2023)
    ttk.Label(filters_frame, text="Year Range:").pack(anchor="w", pady=(10, 0))
    ttk.Spinbox(filters_frame, from_=1970, to=2024, textvariable=year_min_var, width=6).pack(pady=2)
    ttk.Spinbox(filters_frame, from_=1970, to=2024, textvariable=year_max_var, width=6).pack(pady=2)

    imdb_var = tk.DoubleVar(value=7.0)
    ttk.Label(filters_frame, text="Minimum IMDb Rating:").pack(anchor="w", pady=(10, 0))
    ttk.Scale(
        filters_frame, from_=0, to=10, variable=imdb_var, orient="horizontal", length=200
    ).pack(pady=2)
    ttk.Label(filters_frame, textvariable=imdb_var).pack()

    votes_var = tk.IntVar(value=1000)
    ttk.Label(filters_frame, text="Minimum Number of Votes:").pack(anchor="w", pady=(10, 0))
    ttk.Scale(
        filters_frame,
        from_=0,
        to=int(movies_df["num_ratings"].max()),
        variable=votes_var,
        orient="horizontal",
        length=200
    ).pack(pady=2)
    ttk.Label(filters_frame, textvariable=votes_var).pack()

    search_var = tk.StringVar()
    ttk.Label(filters_frame, text="Search Title:").pack(anchor="w", pady=(10, 0))
    ttk.Entry(filters_frame, textvariable=search_var, width=25).pack(pady=2)

    def recommend_movies():
        selected_genres = [g for g, var in genre_vars.items() if var.get()]
        year_min = int(year_min_var.get())
        year_max = int(year_max_var.get())
        min_rating = float(imdb_var.get())
        min_votes = int(votes_var.get())
        selected_type = type_var.get()
        search_title = search_var.get().strip().lower()

        filtered = apply_filters(
            movies_df, year_min, year_max, min_rating, min_votes, selected_type, selected_genres, search_title
        )

        if filtered.empty:
            messagebox.showinfo("No Result", "No movie matches your filters.")
            return
        
        top_movie = filtered.sort_values("imdb_rating", ascending=False).iloc[0]

        recommended = get_knn_recommendation(top_movie['title'], filtered, ratings_matrix, movies_df)

        if recommended is not None:
            show_movie_window(recommended, root)
        else:
            show_movie_window(top_movie, root)

    ttk.Button(
        filters_frame, text="Recommend Movie/TV Show", command=recommend_movies
    ).pack(pady=20)

    root.mainloop()