"""
schema.py : model to be converted in json by fastapi
"""
from typing import Optional, List
from datetime import date

from pydantic import BaseModel

# common Base Class for Movies (abstract class)
class MovieBase(BaseModel):
    title: str
    year: int
    duration: Optional[int] = None

# movie witout id, only for creation purpose
class MovieCreate(MovieBase):
    pass

# movie from database with id
class Movie(MovieBase):
    id: int

    class Config:
        orm_mode = True

class StarBase(BaseModel):
    name: str
    birthdate: Optional[date] = None

class StarCreate(StarBase):
    pass

class Star(StarBase):
    id: int

    class Config:
        orm_mode = True

class MovieDetail(Movie):
    director : Optional[Star] = None
    actors : List[Star] = []