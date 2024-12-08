from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware
from backend.app.database import Base, engine
from backend.app.routes import users, books, movies

Base.metadata.create_all(bind=engine)

app = FastAPI()

app.include_router(books.router, prefix="/books", tags=["Books"])
app.include_router(movies.router, prefix="/movies", tags=["Movies"])
app.include_router(users.router, prefix="/users", tags=["Users"])

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)