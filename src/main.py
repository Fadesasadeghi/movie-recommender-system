from data_loader import load_data
from utils import extract_all_genres, get_content_types
from gui import start_gui

def main():
    movies_df, ratings_matrix = load_data()
    all_genres = extract_all_genres(movies_df)
    content_types = get_content_types()
    start_gui(movies_df, ratings_matrix, all_genres, content_types)

if __name__ == "__main__":
    main()