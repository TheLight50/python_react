from typing import List, Optional, Tuple, Dict
from datetime import date
import logging

from fastapi import Depends, FastAPI, HTTPException
from fastapi.logger import logger as fastapi_logger
from sqlalchemy.orm import Session

import crud, models, schemas
from database import SessionLocal, engine

models.Base.metadata.create_all(bind=engine)

app = FastAPI()
logger = logging.getLogger("uvicorn")
fastapi_logger.handlers = logger.handlers
fastapi_logger.setLevel(logger.level)
logger.error("API started")

# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.get("/movies/", response_model=List[schemas.Movie])
def read_movies(skip: Optional[int] = 0, limit: Optional[int] = 100, db: Session = Depends(get_db)):
    # read movies from database
    movies = crud.get_movies(db, skip=skip, limit=limit)
    # return them as json
    return movies

@app.get("/movies/by_id/{movie_id}", response_model=schemas.MovieDetail)
def read_movie(movie_id: int, db: Session = Depends(get_db)):
    db_movie = crud.get_movie(db, movie_id=movie_id)
    if db_movie is None:
        raise HTTPException(status_code=404, detail="Movie to read not found")
    return db_movie

@app.get("/movies/{year_min}/{year_max}", response_model=List[schemas.Movie])
def read_movies_by_range_year(db: Session = Depends(get_db), year_min: Optional[int] = None, year_max: Optional[int] = None):
    # read movies from database
    movies = crud.get_movies_by_range_year(db, year_min=year_min, year_max=year_max)
    # return them as json
    return movies

@app.get("/movies/by_title", response_model=List[schemas.Movie]) #, response_model=List[schemas.Movie])
def read_movies_by_title(n: Optional[str] = None, db: Session = Depends(get_db)):
    # read movies from database
    movies = crud.get_movies_by_title(db=db, title=n)
    # return them as json
    return movies

@app.get("/movies/by_parttitle", response_model=List[schemas.Movie])
def read_movies_by_parttitle(n: Optional[str] = None, db: Session = Depends(get_db)):
    # read movies from database
    movies = crud.get_movies_by_parttitle(db=db, title=n)
    # return them as json
    return movies

@app.get("/movies/by_director", response_model=List[schemas.Movie])
def read_movies_by_director(n: str, db: Session = Depends(get_db)):
    # read movies from database
    return crud.get_movies_by_director_endname(db=db, endname=n)  

@app.get("/movies/by_actor", response_model=List[schemas.Movie])
def read_movies_by_actor(n: str, db: Session = Depends(get_db)):
    # read movies from database
    return crud.get_movies_by_actor_endname(db=db, endname=n)  

@app.get("/movies/actorss", response_model=List[schemas.MovieDetail])
def read_movies_actors(n: str, db: Session = Depends(get_db)):
    return crud.get_movies_actors(db=db, title=n)  

@app.post("/movies/", response_model=schemas.Movie)
def create_movie(movie: schemas.MovieCreate, db: Session = Depends(get_db)):
    # receive json item without id and return json item from database with new id
    return crud.create_movie(db=db, movie=movie)

@app.put("/movies/", response_model=schemas.Movie)
def update_movie(movie: schemas.Movie, db: Session = Depends(get_db)):
    db_movie = crud.update_movie(db, movie=movie)
    if db_movie is None:
        raise HTTPException(status_code=404, detail="Movie to update not found")
    return db_movie

@app.put("/movies/director", response_model=schemas.MovieDetail)
def update_movie_director(mid, sid, db: Session = Depends(get_db)):
    db_movie = crud.update_movie_director(db, movie_id=mid, director=sid)
    if db_movie is None:
        raise HTTPException(status_code=404, detail="Movie or Star to update not found")
    return db_movie


@app.post("/movies/actor", response_model=schemas.MovieDetail)
def add_movie_actor(mid: int, sid: int, db: Session = Depends(get_db)):
    db_movie = crud.add_movie_actor(db, mid=mid, sid=sid)
    if db_movie is None:
        raise HTTPException(status_code=404, detail="Movie or Star to update not found")
    return db_movie

@app.put("/movies/actors", response_model=schemas.MovieDetail)
def update_movie_actors(mid: int, sids: List[int], db: Session = Depends(get_db)):
    db_movie = crud.update_movie_actors(db, mid=mid, sids=sids)
    if db_movie is None:
        raise HTTPException(status_code=404, detail="Movie or Star to update not found")
    return db_movie


@app.delete("/movies/{movie_id}", response_model=schemas.Movie)
def delete_movie(movie_id: int, db: Session = Depends(get_db)):
    db_movie = crud.delete_movie(db, movie_id=movie_id)
    if db_movie is None:
        raise HTTPException(status_code=404, detail="Movie to delete not found")
    return db_movie

@app.get("/movies/count_by_year")
def read_movies_count_by_year(db: Session = Depends(get_db)) -> List[Tuple[int, int]]:
    return crud.get_movies_count_by_year(db=db) 

@app.get("/movies/duration_info_by_year")
def read_movies_duration_info_by_year(db: Session = Depends(get_db)) -> List[Tuple[int,int,float,int]]:
    return crud.get_movies_duration_info_by_year(db=db)

###

@app.get("/stars/", response_model=List[schemas.Star])
def read_stars(skip: Optional[int] = 0, limit: Optional[int] = 100, db: Session = Depends(get_db)):
    stars = crud.get_stars(db, skip=skip, limit=limit)
    return stars

@app.get("/stars/by_star_id/{star_id}", response_model=schemas.Star)
def read_star(star_id: int, db: Session = Depends(get_db)):
    db_star = crud.get_star(db, star_id=star_id)
    if db_star is None:
        raise HTTPException(status_code=404, detail="Star to read not found")
    return db_star

@app.get("/stars/by_name", response_model=List[schemas.Star])
def read_stars_by_name(n: Optional[str] = None, db: Session = Depends(get_db)):
    stars = crud.get_stars_by_name(db=db, name=n)
    return stars

@app.get("/stars/by_partname", response_model=List[schemas.Star])
def read_stars_by_partname(n: Optional[str] = None, db: Session = Depends(get_db)):
    stars = crud.get_stars_by_partname(db=db, name=n)
    return stars

@app.get("/stars/by_birthyear", response_model=List[schemas.Star])
def read_stars_by_birthyear(year: Optional[str] = None, db: Session = Depends(get_db)):
    stars = crud.get_stars_by_birthyear(db = db, year=year)
    return stars

@app.get("/stars/by_title", response_model=List[schemas.Star])
def read_stars_by_title(n: str, db: Session = Depends(get_db)):
    return crud.get_stars_director_by_title(db=db, title=n) 

@app.post("/stars/", response_model=schemas.Star)
def create_star(star: schemas.StarCreate, db: Session = Depends(get_db)):
    return crud.create_star(db=db, star=star)

@app.put("/stars/", response_model=schemas.Star)
def update_star(star: schemas.Star, db: Session = Depends(get_db)):
    db_star = crud.update_star(db, star=star)
    if db_star is None:
        raise HTTPException(status_code=404, detail="Star to update not found")
    return db_star

@app.delete("/stars/{star_id}", response_model=schemas.Star)
def delete_star(star_id: int, db: Session = Depends(get_db)):
    db_star = crud.delete_star(db, star_id=star_id)
    if db_star is None:
        raise HTTPException(status_code=404, detail="Star to delete not found")
    return db_star

@app.get("/stars/stats_movie_by_director")
def read_stats_movie_by_director(minc: Optional[int]=10, db: Session = Depends(get_db)):
    return crud.get_stats_movies_by_director(db=db, min_count=minc)

@app.get("/stars/stats_movies_by_actor")
def read_stats_movies_by_actor(minc: Optional[int]=15, db: Session = Depends(get_db)):
    return crud.get_stats_movies_by_actor(db=db, min_count=minc)
