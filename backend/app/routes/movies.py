from fastapi import APIRouter, Depends, HTTPException, Body
from backend.app.auth import get_current_user
from backend.app.database import get_db, SessionLocal
from backend.app.models import Movie, UserPreference, Genre
from backend.app.recommender import recommend_items
from backend.app.schemas import MovieCreate, MovieResponse, GenreCreate
from typing import List
import pandas as pd
from sqlalchemy.orm import joinedload

router = APIRouter()

@router.get("/", response_model=List[MovieResponse])
def get_movies(db: SessionLocal = Depends(get_db)):
    return db.query(Movie).all()

@router.get("/recommendations/")
def get_recommendations(db: SessionLocal = Depends(get_db), current_user=Depends(get_current_user)):
    preferences = pd.read_sql(db.query(UserPreference).statement, db.bind)
    movies_data = db.query(Movie).options(joinedload(Movie.genres)).all()

    # Convert SQLAlchemy objects to a Pandas DataFrame with correct columns
    movies_data_df = pd.DataFrame([vars(movie) for movie in movies_data])

    recommendations = recommend_items(current_user.id, preferences, movies_data_df)
    return recommendations.to_dict(orient="records")

def _add_genre_helper(genre: GenreCreate, db: SessionLocal):
    if db.query(Genre).filter(Genre.name == genre.name).first():
        raise HTTPException(status_code=400, detail="Genre already exists")
    new_genre = Genre(name=genre.name)
    db.add(new_genre)
    db.commit()
    db.refresh(new_genre)
    return new_genre

def _add_movie_helper(movie: MovieCreate, db: SessionLocal):
    if db.query(Movie).filter(Movie.title == movie.title).first():
        raise HTTPException(status_code=400, detail="Movie already exists")

    genres = db.query(Genre).filter(Genre.id.in_(movie.genres)).all()
    if len(genres) != len(movie.genres):
        raise HTTPException(status_code=400, detail="Some genres do not exist")

    new_movie = Movie(title=movie.title, director=movie.director, rating=movie.rating, genres=genres)
    db.add(new_movie)
    db.commit()
    db.refresh(new_movie)
    return new_movie

@router.post("/")
def add_movie(movie: MovieCreate, db: SessionLocal = Depends(get_db)):
    return _add_movie_helper(movie, db)

@router.post("/genres/")
def add_genre(genre: GenreCreate, db: SessionLocal = Depends(get_db)):
    return _add_genre_helper(genre, db)

@router.post("/import/")
def import_movie_from_imdb(movie_title: str = Body(..., embed=True), db: SessionLocal = Depends(get_db)):
    from backend.app.parser import add_movie_from_imdb
    result = add_movie_from_imdb(movie_title, db)
    return result

@router.post("/import_bulk/")
def import_movie_from_imdb(movie_titles: List[str] = Body(..., embed=True), db: SessionLocal = Depends(get_db)):
    from backend.app.parser import add_movie_from_imdb
    result = []
    for movie_title in movie_titles:
        try:
            movie = add_movie_from_imdb(movie_title, db)
            result.append({"title": movie_title, "status": "success", "movie": movie})
        except Exception as e:
            result.append({"title": movie_title, "status": "error", "error": str(e)})

    return result