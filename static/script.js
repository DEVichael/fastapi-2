console.log("script.js loaded, pathname =", window.location.pathname);

const API = "http://127.0.0.1:8000/movies";
const ACTORS_API = "http://127.0.0.1:8000/actors";

window.addEventListener("DOMContentLoaded", () => {

    // =========================
    // INDEX PAGE LOGIC
    // =========================
    const moviesList = document.getElementById("moviesList");
    if (moviesList) {
        console.log("index.html logic attached");

        fetch(API)
            .then(res => res.json())
            .then(movies => {
                movies.forEach(movie => {
                    const li = document.createElement("li");
                    li.innerHTML = `
                        <input type="checkbox" value="${movie.id}">
                        ${movie.title}, ${movie.year}, ${movie.director}${movie.description ? " — " + movie.description : ""}
                    `;
                    moviesList.appendChild(li);
                });
            });

        const deleteBtn = document.getElementById("deleteBtn");
        const deleteAllBtn = document.getElementById("deleteAllBtn");
        const editBtn = document.getElementById("editBtn");
        const showActorsBtn = document.getElementById("showActorsBtn");

        deleteBtn?.addEventListener("click", async () => {
            const checked = [...document.querySelectorAll("input[type=checkbox]:checked")];

            for (const checkbox of checked) {
                await fetch(`${API}/${checkbox.value}`, { method: "DELETE" });
            }

            location.reload();
        });

        deleteAllBtn?.addEventListener("click", async () => {
            if (!confirm("Are you sure you want to delete ALL movies?")) return;

            await fetch(API, { method: "DELETE" });
            location.reload();
        });

        editBtn?.addEventListener("click", () => {
            const checked = [...document.querySelectorAll("input[type=checkbox]:checked")];

            if (checked.length !== 1) {
                alert("Select exactly ONE movie to edit.");
                return;
            }

            const id = checked[0].value;
            window.location.href = `add.html?id=${id}`;
        });

        showActorsBtn?.addEventListener("click", () => {
            const checked = [...document.querySelectorAll("input[type=checkbox]:checked")];

            if (checked.length !== 1) {
                alert("Select exactly ONE movie to view its actors.");
                return;
            }

            const id = checked[0].value;
            window.location.href = `movie_actors.html?movie_id=${id}`;
        });
    }


    // =========================
    // ADD / EDIT MOVIE PAGE
    // =========================
    const addForm = document.getElementById("addForm");
    if (addForm) {
        console.log("add.html logic attached");

        const urlParams = new URLSearchParams(window.location.search);
        const editId = urlParams.get("id");

        if (editId) {
            fetch(API)
                .then(res => res.json())
                .then(movies => {
                    const movie = movies.find(m => m.id == editId);
                    if (!movie) return;

                    document.getElementById("title").value = movie.title;
                    document.getElementById("year").value = movie.year;
                    document.getElementById("director").value = movie.director;
                    document.getElementById("description").value = movie.description;
                });
        }

        addForm.addEventListener("submit", async (e) => {
            e.preventDefault();

            const movie = {
                title: document.getElementById("title").value,
                year: document.getElementById("year").value,
                director: document.getElementById("director").value,
                description: document.getElementById("description").value
            };

            if (editId) {
                await fetch(`${API}/${editId}`, {
                    method: "PUT",
                    headers: {"Content-Type": "application/json"},
                    body: JSON.stringify(movie)
                });
            } else {
                await fetch(API, {
                    method: "POST",
                    headers: {"Content-Type": "application/json"},
                    body: JSON.stringify(movie)
                });
            }

            window.location.href = "index.html";
        });
    }


    // =========================
    // ACTORS PAGE LOGIC
    // =========================
    const actorsList = document.getElementById("actorsList");
    if (actorsList) {
        console.log("actors.html logic attached");

        fetch(ACTORS_API)
            .then(res => res.json())
            .then(actors => {
                actors.forEach(actor => {
                    const li = document.createElement("li");
                    li.innerHTML = `
                        <input type="checkbox" value="${actor.id}">
                        ${actor.name} ${actor.surname}
                    `;
                    actorsList.appendChild(li);
                });
            });

        const deleteActorBtn = document.getElementById("deleteActorBtn");
        const deleteAllActorsBtn = document.getElementById("deleteAllActorsBtn");
        const editActorBtn = document.getElementById("editActorBtn");

        deleteActorBtn?.addEventListener("click", async () => {
            const checked = [...document.querySelectorAll("input[type=checkbox]:checked")];

            for (const checkbox of checked) {
                await fetch(`${ACTORS_API}/${checkbox.value}`, { method: "DELETE" });
            }

            location.reload();
        });

        deleteAllActorsBtn?.addEventListener("click", async () => {
            if (!confirm("Are you sure you want to delete ALL actors?")) return;

            // brak endpointu DELETE /actors – na razie tylko info
            alert("Bulk delete for actors not implemented.");
        });

        editActorBtn?.addEventListener("click", () => {
            const checked = [...document.querySelectorAll("input[type=checkbox]:checked")];

            if (checked.length !== 1) {
                alert("Select exactly ONE actor to edit.");
                return;
            }

            const id = checked[0].value;
            window.location.href = `add_actor.html?id=${id}`;
        });
    }


    // =========================
    // ADD / EDIT ACTOR PAGE
    // =========================
    const actorForm = document.getElementById("actorForm");
    if (actorForm) {
        console.log("add_actor.html logic attached");

        const urlParams = new URLSearchParams(window.location.search);
        const editId = urlParams.get("id");

        if (editId) {
            fetch(`${ACTORS_API}/${editId}`)
                .then(res => res.json())
                .then(actor => {
                    document.getElementById("name").value = actor.name;
                    document.getElementById("surname").value = actor.surname;
                });
        }

        actorForm.addEventListener("submit", async (e) => {
            e.preventDefault();

            const actor = {
                name: document.getElementById("name").value,
                surname: document.getElementById("surname").value
            };

            if (editId) {
                await fetch(`${ACTORS_API}/${editId}`, {
                    method: "PUT",
                    headers: {"Content-Type": "application/json"},
                    body: JSON.stringify(actor)
                });
            } else {
                await fetch(ACTORS_API, {
                    method: "POST",
                    headers: {"Content-Type": "application/json"},
                    body: JSON.stringify(actor)
                });
            }

            window.location.href = "actors.html";
        });
    }


    // =========================
    // MOVIE ACTORS PAGE LOGIC
    // =========================
    const movieActorsList = document.getElementById("movieActorsList");
    if (movieActorsList) {
        console.log("movie_actors.html logic attached (element found)");

        const params = new URLSearchParams(window.location.search);
        const movieId = params.get("movie_id");
        console.log("movieId =", movieId);

        if (!movieId) {
            movieActorsList.innerHTML = "<li>No movie_id provided in URL.</li>";
            return;
        }

        fetch(`http://127.0.0.1:8000/movies/${movieId}/actors`)
            .then(res => {
                if (!res.ok) {
                    throw new Error("Failed to fetch actors");
                }
                return res.json();
            })
            .then(actors => {
                console.log("actors from API:", actors);

                if (!actors || actors.length === 0) {
                    movieActorsList.innerHTML = "<li>No actors assigned to this movie.</li>";
                    return;
                }

                actors.forEach(actor => {
                    const li = document.createElement("li");
                    li.textContent = `${actor.name} ${actor.surname}`;
                    movieActorsList.appendChild(li);
                });
            })
            .catch(err => {
                console.error("Error fetching actors:", err);
                movieActorsList.innerHTML = "<li>Error loading actors.</li>";
            });
    }

});
