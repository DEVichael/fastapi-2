from fastapi import APIRouter, HTTPException
from db import fetch_all, fetch_one, execute
from models import Movie

router = APIRouter()

@router.get("/movies")
def get_movies():
    rows = fetch_all("SELECT id, title, year, director, description FROM movie")
    return [
        {"id": r[0], "title": r[1], "year": r[2], "director": r[3], "description": r[4]}
        for r in rows
    ]

@router.post("/movies")
def add_movie(movie: Movie):
    movie_id = execute(
        "INSERT INTO movie (title, year, director, description) VALUES (?, ?, ?, ?)",
        (movie.title, movie.year, movie.director, movie.description)
    )
    return {"message": "Movie added successfully", "id": movie_id}

@router.put("/movies/{movie_id}")
def update_movie(movie_id: int, movie: Movie):
    execute(
        "UPDATE movie SET title = ?, year = ?, director = ?, description = ? WHERE id = ?",
        (movie.title, movie.year, movie.director, movie.description, movie_id)
    )
    return {"message": "Movie updated successfully"}

@router.delete("/movies/{movie_id}")
def delete_movie(movie_id: int):
    execute("DELETE FROM movie WHERE id = ?", (movie_id,))
    return {"message": "Movie deleted successfully"}

@router.get("/movies/{movie_id}/actors")
def get_movie_actors(movie_id: int):
    rows = fetch_all("""
        SELECT actor.id, actor.name, actor.surname
        FROM actor
        JOIN movie_actor_through ON actor.id = movie_actor_through.actor_id
        WHERE movie_actor_through.movie_id = ?
    """, (movie_id,))
    return [{"id": r[0], "name": r[1], "surname": r[2]} for r in rows]
