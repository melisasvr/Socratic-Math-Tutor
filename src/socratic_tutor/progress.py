import os
import sqlite3
from datetime import datetime, timedelta, timezone


def init_progress_db(db_path: str) -> None:
    db_dir = os.path.dirname(db_path)
    if db_dir:
        os.makedirs(db_dir, exist_ok=True)
    with sqlite3.connect(db_path) as conn:
        conn.execute(
            """
            CREATE TABLE IF NOT EXISTS attempts (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                created_at TEXT NOT NULL,
                topic TEXT NOT NULL,
                solved INTEGER NOT NULL,
                interactions INTEGER NOT NULL
            )
            """
        )
        conn.commit()


def record_attempt(db_path: str, topic: str, solved: bool, interactions: int) -> None:
    with sqlite3.connect(db_path) as conn:
        conn.execute(
            "INSERT INTO attempts (created_at, topic, solved, interactions) VALUES (?, ?, ?, ?)",
            (datetime.now(timezone.utc).isoformat(), topic, int(solved), max(interactions, 1)),
        )
        conn.commit()


def get_progress_stats(db_path: str) -> dict:
    with sqlite3.connect(db_path) as conn:
        total_attempts = conn.execute("SELECT COUNT(*) FROM attempts").fetchone()[0]
        total_solved = conn.execute("SELECT COUNT(*) FROM attempts WHERE solved = 1").fetchone()[0]

        cutoff = (datetime.now(timezone.utc) - timedelta(days=7)).isoformat()
        last_7_days = conn.execute(
            "SELECT COUNT(*) FROM attempts WHERE created_at >= ?",
            (cutoff,),
        ).fetchone()[0]

        rows = conn.execute(
            "SELECT topic, COUNT(*) FROM attempts GROUP BY topic ORDER BY COUNT(*) DESC"
        ).fetchall()

        solved_days = conn.execute(
            "SELECT DISTINCT substr(created_at, 1, 10) FROM attempts WHERE solved = 1 ORDER BY 1 DESC"
        ).fetchall()

    solved_day_set = {row[0] for row in solved_days}
    streak = 0
    current_day = datetime.now(timezone.utc).date()
    while current_day.isoformat() in solved_day_set:
        streak += 1
        current_day -= timedelta(days=1)

    return {
        "total_attempts": total_attempts,
        "total_solved": total_solved,
        "current_streak": streak,
        "last_7_days": last_7_days,
        "topic_breakdown": rows,
    }
