from fastapi import FastAPI
from app.database import Base, engine
from app.routes import books, movies, users

Base.metadata.create_all(bind=engine)

app = FastAPI()

app.include_router(books.router, prefix="/books", tags=["Books"])
app.include_router(movies.router, prefix="/movies", tags=["Movies"])
app.include_router(users.router, prefix="/users", tags=["Users"])
