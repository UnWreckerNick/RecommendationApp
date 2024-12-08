from pydantic import BaseModel
from typing import Optional, List

class RegisterUser(BaseModel):
    username: str
    password: str

class MovieCreate(BaseModel):
    title: str
    director: str
    rating: float
    genres: List[int]

class GenreCreate(BaseModel):
    name: str

class PreferenceCreate(BaseModel):
    item_id: int
    item_type: str
    interaction: int

class GenreResponse(BaseModel):
    id: int
    name: str

class MovieResponse(BaseModel):
    id: int
    title: str
    director: str
    rating: float
    genres: List[GenreResponse]

    class Config:
        from_attributes = True