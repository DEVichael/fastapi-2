from typing import Any
import os
import sqlite3
from fastapi import FastAPI, HTTPException
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles

app = FastAPI()

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(BASE_DIR, "movies-extended.db")

app.mount("/static", StaticFiles(directory=os.path.join(BASE_DIR, "static")), name="static")


def get_db():
    return sqlite3.connect(DB_PATH)


# ============================
# FRONTEND ROUTES
# ============================

@app.get("/", response_class=FileResponse)
def serve_index():
    return os.path.join(BASE_DIR, "frontend", "index.html")


@app.get("/index.html", response_class=FileResponse)
def serve_index_html():
    return os.path.join(BASE_DIR, "frontend", "index.html")


@app.get("/add.html", response_class=FileResponse)
def serve_add_html():
    return os.path.join(BASE_DIR, "frontend", "add.html")


@app.get("/actors.html", response_class=FileResponse)
def serve_actors_html():
    return os.path.join(BASE_DIR, "frontend", "actors.html")


@app.get("/add_actor.html", response_class=FileResponse)
def serve_add_actor_html():
    return os.path.join(BASE_DIR, "frontend", "add_actor.html")


@app.get("/movie_actors.html", response_class=FileResponse)
def serve_movie_actors():
    return os.path.join(BASE_DIR, "frontend", "movie_actors.html")


# ============================
# API: MOVIES
# ============================

@app.get("/movies")
def get_movies():
    db = get_db()
    cursor = db.cursor()

    rows = cursor.execute(
        "SELECT id, title, year, director, description FROM movie"
    ).fetchall()

    db.close()

    return [
        {
            "id": row[0],
            "title": row[1],
            "year": row[2],
            "director": row[3],
            "description": row[4]
        }
        for row in rows
    ]


@app.post("/movies")
def add_movie(params: dict[str, Any]):
    title = params.get("title")
    year = params.get("year")
    director = params.get("director")
    description = params.get("description")

    if not title or not year or not director or not description:
        raise HTTPException(status_code=400, detail="Missing required fields")

    db = get_db()
    cursor = db.cursor()

    cursor.execute(
        "INSERT INTO movie (title, year, director, description) VALUES (?, ?, ?, ?)",
        (title, year, director, description)
    )

    db.commit()
    new_id = cursor.lastrowid
    db.close()

    return {"message": "Movie added successfully", "id": new_id}


@app.put("/movies/{movie_id}")
def update_movie(movie_id: int, params: dict[str, Any]):
    title = params.get("title")
    year = params.get("year")
    director = params.get("director")
    description = params.get("description")

    if not title or not year or not director or not description:
        raise HTTPException(status_code=400, detail="Missing required fields")

    db = get_db()
    cursor = db.cursor()

    cursor.execute(
        "UPDATE movie SET title = ?, year = ?, director = ?, description = ? WHERE id = ?",
        (title, year, director, description, movie_id)
    )

    db.commit()
    db.close()

    return {"message": "Movie updated successfully", "id": movie_id}


@app.delete("/movies/{movie_id}")
def delete_movie(movie_id: int):
    db = get_db()
    cursor = db.cursor()

    cursor.execute("DELETE FROM movie WHERE id = ?", (movie_id,))
    db.commit()
    db.close()

    return {"message": "Movie deleted successfully"}


@app.delete("/movies")
def delete_all_movies():
    db = get_db()
    cursor = db.cursor()

    cursor.execute("DELETE FROM movie")
    db.commit()
    db.close()

    return {"message": "All movies deleted successfully"}


# ============================
# API: MOVIE → ACTORS
# ============================

@app.get("/movies/{movie_id}/actors")
def get_movie_actors(movie_id: int):
    db = get_db()
    cursor = db.cursor()

    rows = cursor.execute(
        """
        SELECT actor.id, actor.name, actor.surname
        FROM actor
        JOIN movie_actor_through ON actor.id = movie_actor_through.actor_id
        WHERE movie_actor_through.movie_id = ?
        """,
        (movie_id,)
    ).fetchall()

    db.close()

    return [
        {"id": row[0], "name": row[1], "surname": row[2]}
        for row in rows
    ]


# ============================
# API: ACTORS
# ============================

@app.get("/actors")
def get_actors():
    db = get_db()
    cursor = db.cursor()

    rows = cursor.execute(
        "SELECT id, name, surname FROM actor"
    ).fetchall()

    db.close()

    return [
        {"id": row[0], "name": row[1], "surname": row[2]}
        for row in rows
    ]


@app.get("/actors/{actor_id}")
def get_actor(actor_id: int):
    db = get_db()
    cursor = db.cursor()

    row = cursor.execute(
        "SELECT id, name, surname FROM actor WHERE id = ?",
        (actor_id,)
    ).fetchone()

    db.close()

    if not row:
        raise HTTPException(status_code=404, detail="Actor not found")

    return {"id": row[0], "name": row[1], "surname": row[2]}


@app.post("/actors")
def add_actor(params: dict[str, Any]):
    name = params.get("name")
    surname = params.get("surname")

    if not name or not surname:
        raise HTTPException(status_code=400, detail="Missing required fields")

    db = get_db()
    cursor = db.cursor()

    cursor.execute(
        "INSERT INTO actor (name, surname) VALUES (?, ?)",
        (name, surname)
    )

    db.commit()
    new_id = cursor.lastrowid
    db.close()

    return {"message": "Actor added successfully", "id": new_id}


@app.put("/actors/{actor_id}")
def update_actor(actor_id: int, params: dict[str, Any]):
    name = params.get("name")
    surname = params.get("surname")

    if not name or not surname:
        raise HTTPException(status_code=400, detail="Missing required fields")

    db = get_db()
    cursor = db.cursor()

    cursor.execute(
        "UPDATE actor SET name = ?, surname = ? WHERE id = ?",
        (name, surname, actor_id)
    )

    db.commit()
    db.close()

    return {"message": "Actor updated successfully", "id": actor_id}


@app.delete("/actors/{actor_id}")
def delete_actor(actor_id: int):
    db = get_db()
    cursor = db.cursor()

    cursor.execute("DELETE FROM actor WHERE id = ?", (actor_id,))
    db.commit()
    db.close()

    return {"message": "Actor deleted successfully"}


# ============================
# RUN SERVER
# ============================

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)
