"""
file crud.py
manage CRUD and adapt model data from db to schema data to api rest
"""

from typing import Optional, List
from sqlalchemy.orm import Session
from sqlalchemy import extract, desc, between
from sqlalchemy import func
from datetime import date
from fastapi.logger import logger

import models, schemas

def get_movie(db: Session, movie_id: int):
    # read from the database (get method read from cache)
    db_movie = db.query(models.Movie).filter(models.Movie.id == movie_id).first()
    logger.error('Movie retrieved from database : {} ; director : {}'.format(db_movie.title, db_movie.director.name if db_movie.director.name is not None else "no director"))
    return db_movie

def get_movies(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Movie).offset(skip).limit(limit).all()

def _get_movies_by_predicate(*predicate, db: Session):
    """ partial request to apply one or more predicate(s) to model Movie"""
    return db.query(models.Movie)   \
            .filter(*predicate)

def get_movies_by_title(db: Session, title: str):
    return db.query(models.Movie).filter(models.Movie.title == title).all()

def get_movies_by_parttitle(db: Session, title: str):
    return db.query(models.Movie).filter(models.Movie.title.like(f'%{title}%')).all()

def get_movies_by_range_year(db: Session, year_min: Optional[int] = None, year_max: Optional[int] = None):
    if year_min is None and year_max is None:
        return None
    elif year_min is None:
        return db.query(models.Movie).filter(models.Movie.year <= year_max).all()
    elif year_max is None:
        return db.query(models.Movie).filter(models.Movie.year >= year_min).all()
    else:
        return db.query(models.Movie) \
                .filter(
                    models.Movie.year >= year_min,
                    models.Movie.year <= year_max) \
                .order_by(models.Movie.year) \
                .all()

def create_movie(db: Session, movie: schemas.MovieCreate):
    # convert schema object from rest api to db model object
    db_movie = models.Movie(title=movie.title, year=movie.year, duration=movie.duration)
    # add in db cache and force insert
    db.add(db_movie)
    db.commit()
    # retreive object from db (to read at least generated id)
    db.refresh(db_movie)
    return db_movie

def update_movie(db: Session, movie: schemas.Movie):
    db_movie = db.query(models.Movie).filter(models.Movie.id == movie.id).first()
    if db_movie is not None:
        # update data from db
        db_movie.title = movie.title
        db_movie.year = movie.year
        db_movie.duration = movie.duration
        # validate update in db
        db.commit()
    # return updated object or None if not found
    return db_movie

def update_movie_director(db: Session, movie_id: int, director: int):
    db_movie = db.query(models.Movie).filter(models.Movie.id == movie_id).first()
    db_star = get_star(db=db, star_id = director)
    if (db_star is None):
        db_movie = None
    if db_movie is not None and db_star is not None:
        # update data from db
        db_movie.director = db_star
        # validate update in db
        db.commit()
    # return updated object or None if not found
    return db_movie


def add_movie_actor(db: Session, mid: int, sid: int):
    db_movie = db.query(models.Movie).filter(models.Movie.id == mid).first()
    db_star = get_star(db=db, star_id = sid)
    if (db_star is None):
        db_movie = None
    if db_movie is not None and db_star is not None:
        if (db_star not in db_movie.actors):
            db_movie.actors.append(db_star)
            db.commit()
    return db_movie

def update_movie_actors(db: Session, mid: int, sids: List[int]):
    db_movie = db.query(models.Movie).filter(models.Movie.id == mid).first()
    db_stars = db.query(models.Star).filter(models.Star.id.in_(sids)).all()
    if db_movie is not None and db_stars is not None:
        db_movie.actors = db_stars
        db.commit()
    return db_movie


def delete_movie(db: Session, movie_id: int):
     db_movie = db.query(models.Movie).filter(models.Movie.id == movie_id).first()
     if db_movie is not None:
         # delete object from ORM
         db.delete(db_movie)
         # validate delete in db
         db.commit()
     # return deleted object or None if not found
     return db_movie

def get_movies_by_director_endname(db: Session, endname: str):
    return db.query(models.Movie).join(models.Movie.director).filter(models.Star.name.like(f"%{endname}")).order_by(desc(models.Movie.year)).all()

def get_movies_by_actor_endname(db: Session, endname: str):
    return db.query(models.Movie).join(models.Movie.actors).filter(models.Star.name.like(f"%{endname}")).order_by(desc(models.Movie.year)).all()

def get_movies_actors(db: Session, title: str):
    return db.query(models.Movie).join(models.Movie.actors).filter(models.Movie.title.like(f'%{title}%')).order_by(desc(models.Star.name)).all()

def get_movies_count(db: Session):
    return db.query(models.Movie).count()

def get_movies_count_year(db: Session, year: int):
    return _get_movies_by_predicate(models.Movie.year == year).count()

def get_movies_count_by_year(db: Session):
    return db.query(models.Movie.year, func.count()).group_by(models.Movie.year).order_by(models.Movie.year).all()

def get_movies_duration_info_by_year(db: Session):
    return db.query(models.Movie.year, func.min(models.Movie.duration), func.avg(models.Movie.duration), func.max(models.Movie.duration)).group_by(models.Movie.year).order_by(models.Movie.year).all()

# CRUD for Star objects
def _get_stars_by_predicate(*predicate, db: Session):
    """ partial request to apply one or more predicate(s) to model Star"""
    return db.query(models.Star)   \
            .filter(*predicate)    

def get_star(db: Session, star_id: int):
    # read from the database (get method read from cache)
    return db.query(models.Star).filter(models.Star.id == star_id).first()

def get_stars(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Star).offset(skip).limit(limit).all()

def get_stars_by_name(db: Session, name: str):
    return db.query(models.Star).filter(models.Star.name == name).all()

def get_stars_by_partname(db: Session, name: str):
    return db.query(models.Star).filter(models.Star.name.like(f'%{name}%')).all()


def get_stars_by_birthyear(db: Session, year: Optional[date] = None):
    if year is None:
        return None
    else:
        return db.query(models.Star) \
                .filter(
                    extract("year", models.Star.birthdate) == year) \
                .order_by(models.Star.name).all()

def create_star(db: Session, star: schemas.StarCreate):
    # convert schema object from rest api to db model object
    db_star = models.Star(name=star.name, birthdate=star.birthdate)
    # add in db cache and force insert
    db.add(db_star)
    db.commit()
    # retreive object from db (to read at least generated id)
    db.refresh(db_star)
    return db_star

def update_star(db: Session, star: schemas.Star):
    db_star = db.query(models.Star).filter(models.Star.id == star.id).first()
    if db_star is not None:
        # update data from db
        db_star.name = star.name
        db_star.birthdate = star.birthdate
        # validate update in db
        db.commit()
    # return updated object or None if not found
    return db_star

def delete_star(db: Session, star_id: int):
     db_star = db.query(models.Star).filter(models.Star.id == star_id).first()
     if db_star is not None:
         # delete object from ORM
         db.delete(db_star)
         # validate delete in db
         db.commit()
     # return deleted object or None if not found
     return db_star

def get_stars_director_by_title(db: Session, title: str):
    return db.query(models.Star).join(models.Star.title).filter(models.Movie.title.like(f"%{title}%")).all()

def get_stars_count(db: Session):
    return db.query(models.Star).count()

def get_stats_movies_by_director(db: Session, min_count: int=10):
    return db.query(models.Star, func.count(models.Movie.id).label("movie_count")).join(models.Movie.director).group_by(models.Star).having(func.count(models.Movie.id) >= min_count).order_by(desc("movie_count")).all()

def get_stats_movies_by_actor(db: Session, min_count: int=15):
    return db.query(models.Star, func.count(models.Movie.id).label("movie_count"), func.min(models.Movie.year).label("year_first_film"), func.max(models.Movie.year).label("year_last_film")).join(models.Movie.actors).group_by(models.Star).having(func.count(models.Movie.id) >= min_count).order_by(desc("movie_count")).all()
