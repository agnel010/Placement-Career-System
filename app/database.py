import sqlite3
from datetime import datetime

DB_NAME = "placement_system.db"


def get_connection():
    return sqlite3.connect(DB_NAME)


def create_tables():
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE,
            password TEXT,
            role TEXT
        )
    """)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS predictions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT,
            gender INTEGER,
            ssc_p REAL,
            hsc_p REAL,
            degree_p REAL,
            etest_p REAL,
            mba_p REAL,
            prediction TEXT,
            created_at TEXT
        )
    """)

    conn.commit()
    conn.close()


def insert_prediction(username, gender, ssc_p, hsc_p, degree_p, etest_p, mba_p, prediction):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        INSERT INTO predictions (
            username, gender, ssc_p, hsc_p, degree_p, etest_p, mba_p, prediction, created_at
        )
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, (
        username, gender, ssc_p, hsc_p, degree_p, etest_p, mba_p, prediction,
        datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    ))

    conn.commit()
    conn.close()


def get_all_predictions():
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM predictions")
    data = cursor.fetchall()

    conn.close()
    return data
