"""Rumsbokning. Starta med: flask --app app run --debug

Databasen (SQLite) skapas första gången du startar appen. Ta bort filen bokning.db för att börja om.
"""
import sqlite3
from pathlib import Path

from flask import Flask, g, redirect, render_template, request, url_for

DB_PATH = Path(__file__).parent / "bokning.db"
app = Flask(__name__)

ROOMS = [("Kajutan", 4), ("Maskinrummet", 10), ("Utkiken", 2)]


def get_db() -> sqlite3.Connection:
    if "db" not in g:
        g.db = sqlite3.connect(DB_PATH)
        g.db.row_factory = sqlite3.Row
    return g.db


@app.teardown_appcontext
def close_db(_error):
    db = g.pop("db", None)
    if db is not None:
        db.close()


def init_db() -> None:
    db = sqlite3.connect(DB_PATH)
    db.executescript("""
        CREATE TABLE IF NOT EXISTS rooms (
            id INTEGER PRIMARY KEY, name TEXT NOT NULL, seats INTEGER NOT NULL);
        CREATE TABLE IF NOT EXISTS bookings (
            id INTEGER PRIMARY KEY, room_id INTEGER NOT NULL REFERENCES rooms(id),
            booked_by TEXT NOT NULL, day TEXT NOT NULL, start_hour INTEGER NOT NULL,
            end_hour INTEGER NOT NULL);
    """)
    if db.execute("SELECT COUNT(*) FROM rooms").fetchone()[0] == 0:
        db.executemany("INSERT INTO rooms (name, seats) VALUES (?, ?)", ROOMS)
    db.commit()
    db.close()


init_db()


@app.get("/")
def index():
    db = get_db()
    rooms = db.execute("SELECT * FROM rooms ORDER BY name").fetchall()
    bookings = db.execute("""
        SELECT b.*, r.name AS room_name FROM bookings b
        JOIN rooms r ON r.id = b.room_id ORDER BY b.day, b.start_hour""").fetchall()
    return render_template("index.html", rooms=rooms, bookings=bookings)


@app.route("/boka", methods=["GET", "POST"])
def book():
    db = get_db()
    rooms = db.execute("SELECT * FROM rooms ORDER BY name").fetchall()
    if request.method == "POST":
        db.execute(
            "INSERT INTO bookings (room_id, booked_by, day, start_hour, end_hour) VALUES (?, ?, ?, ?, ?)",
            (request.form["room_id"], request.form["booked_by"], request.form["day"],
             request.form["start_hour"], request.form["end_hour"]))
        db.commit()
        return redirect(url_for("index"))
    return render_template("boka.html", rooms=rooms)
