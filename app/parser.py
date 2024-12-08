from imdb import IMDb
from app.models import Genre
from app.routes.movies import _add_genre_helper, _add_movie_helper
from app.schemas import MovieCreate, GenreCreate
from app.database import SessionLocal

def fetch_movie_data(movie_title):
    ia = IMDb()
    movies = ia.search_movie(movie_title)
    if not movies:
        return None

    movies = ia.get_movie(movies[0].movieID)
    title = movies.get("title")
    director = ", ".join([person["name"] for person in movies.get("directors", [])])
    rating = movies.get("rating", 0.0)
    genres = movies.get("genres", [])

    return {
        "title": title,
        "director": director,
        "rating": rating,
        "genres": genres
    }

def add_movie_from_imdb(movie_title, db: SessionLocal):
    movie_data = fetch_movie_data(movie_title)
    if not movie_data:
        return {"detail": "Movie not found on IMDb"}

    existing_genres = {genre.name for genre in db.query(Genre).all()}
    new_genres = [GenreCreate(name=genre) for genre in movie_data["genres"] if genre not in existing_genres]

    for genre in new_genres:
        _add_genre_helper(genre, db)

    genres_in_db = db.query(Genre).filter(Genre.name.in_(movie_data["genres"])).all()
    genres_ids = [genre.id for genre in genres_in_db]

    movie_schema = MovieCreate(
        title=movie_data["title"],
        director=movie_data["director"],
        rating=movie_data["rating"],
        genres=genres_ids
    )
    return _add_movie_helper(movie_schema, db)
