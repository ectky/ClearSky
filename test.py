# from flask import Flask, request, jsonify
import sqlite3
import re
import pandas as pd

conn = sqlite3.connect("users.db")

conn.execute(
    """CREATE TABLE IF NOT EXISTS users (
    id INTEGER PRIMARY KEY,
    name TEXT,
    is_superuser INTEGER DEFAULT 0
);"""
)

conn.close()

conn = sqlite3.connect("courses_service/courses.db")

conn.execute(
    """CREATE TABLE IF NOT EXISTS courses (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT,
    owner_id INTEGER,
    FOREIGN KEY (owner_id) REFERENCES users(id)
);"""
)

conn.close()

# Add users
users = [
    (3184623, "Alice", 0),
    (3184610, "Bob", 0),
    (3184620, "Carol", 0),
    (3184621, "David", 0),
    (3184625, "Eve", 0),
    (3170676, "SuperUser", 1),
]

# Add courses
courses = [
    ("Matematyka", 3184623),
    ("Fizyka", 3184620),
    ("Biologia", 3184625),
]

conn = sqlite3.connect("users.db")
cursor = conn.cursor()

cursor.executemany(
    "INSERT OR IGNORE INTO users (id, name, is_superuser) VALUES (?, ?, ?)", users
)

conn.commit()
conn.close()
conn = sqlite3.connect("/courses_service/courses.db")
cursor = conn.cursor()
cursor.executemany("INSERT INTO courses (name, owner_id) VALUES (?, ?)", courses)
conn.commit()
conn.close()
