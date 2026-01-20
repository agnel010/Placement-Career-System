import sqlite3
from contextlib import contextmanager
from typing import List, Dict, Any

DB_NAME = "placement_system.db"

@contextmanager
def get_connection():
    conn = sqlite3.connect(DB_NAME)
    conn.row_factory = sqlite3.Row
    try:
        yield conn
    finally:
        conn.close()

def init_db() -> None:
    with get_connection() as conn:
        cursor = conn.cursor()

        cursor.execute("""
            CREATE TABLE IF NOT EXISTS users (
                id          INTEGER PRIMARY KEY AUTOINCREMENT,
                username    TEXT UNIQUE NOT NULL,
                password    BLOB NOT NULL,
                role        TEXT NOT NULL CHECK(role IN ('user', 'admin')),
                created_at  DATETIME DEFAULT CURRENT_TIMESTAMP
            )
        """)

        cursor.execute("""
            CREATE TABLE IF NOT EXISTS predictions (
                id                  INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id             INTEGER NOT NULL,
                cgpa                REAL NOT NULL,
                internships         INTEGER NOT NULL DEFAULT 0,
                projects            INTEGER NOT NULL DEFAULT 0,
                workshops           INTEGER NOT NULL DEFAULT 0,
                aptitude_score      INTEGER NOT NULL,
                soft_skills         REAL NOT NULL,
                extracurricular     INTEGER NOT NULL CHECK(extracurricular IN (0, 1)),
                placement_training  INTEGER NOT NULL CHECK(placement_training IN (0, 1)),
                ssc_marks           REAL,
                hsc_marks           REAL,
                placement_status    INTEGER NOT NULL CHECK(placement_status IN (0, 1)),
                predicted_at        DATETIME DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
            )
        """)

        cursor.execute("CREATE INDEX IF NOT EXISTS idx_predictions_user_id ON predictions(user_id)")

        conn.commit()

def insert_prediction(
    user_id: int,
    cgpa: float,
    internships: int,
    projects: int,
    workshops: int,
    aptitude: int,
    soft_skills: float,
    extracurricular: int,
    placement_training: int,
    ssc: float | None = None,
    hsc: float | None = None,
    status: int = 0
) -> bool:
    try:
        with get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("""
                INSERT INTO predictions (
                    user_id, cgpa, internships, projects, workshops, aptitude_score,
                    soft_skills, extracurricular, placement_training, ssc_marks, hsc_marks, placement_status
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, (
                user_id, cgpa, internships, projects, workshops, aptitude,
                soft_skills, extracurricular, placement_training, ssc, hsc, status
            ))
            conn.commit()
        return True
    except Exception as e:
        print(f"Insert error: {e}")
        return False

def get_user_predictions(user_id: int, limit: int = 50) -> List[Dict[str, Any]]:
    try:
        with get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("""
                SELECT 
                    cgpa, internships, projects, workshops, aptitude_score, soft_skills,
                    extracurricular, placement_training, ssc_marks, hsc_marks,
                    placement_status, predicted_at
                FROM predictions
                WHERE user_id = ?
                ORDER BY predicted_at DESC
                LIMIT ?
            """, (user_id, limit))
            return [dict(row) for row in cursor.fetchall()]
    except Exception as e:
        print(f"Fetch user predictions error: {e}")
        return []

def get_all_predictions(limit: int = 500) -> List[Dict[str, Any]]:
    try:
        with get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("""
                SELECT 
                    p.id, u.username, p.cgpa, p.internships, p.projects, p.workshops,
                    p.aptitude_score, p.soft_skills, p.extracurricular, p.placement_training,
                    p.ssc_marks, p.hsc_marks, p.placement_status, p.predicted_at
                FROM predictions p
                JOIN users u ON p.user_id = u.id
                ORDER BY p.predicted_at DESC
                LIMIT ?
            """, (limit,))
            return [dict(row) for row in cursor.fetchall()]
    except Exception as e:
        print(f"Fetch all predictions error: {e}")
        return []