import os
import sqlite3
import json
from datetime import datetime, timedelta, timezone

def init_progress_db(db_path: str) -> None:
    db_dir = os.path.dirname(db_path)
    if db_dir:
        os.makedirs(db_dir, exist_ok=True)
    with sqlite3.connect(db_path) as conn:
        # The `mistake_tags` column has been added to store error patterns.
        conn.execute(
            """
            CREATE TABLE IF NOT EXISTS attempts (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                created_at TEXT NOT NULL,
                topic TEXT NOT NULL,
                solved INTEGER NOT NULL,
                interactions INTEGER NOT NULL,
                mistake_tags TEXT
            )
            """
        )
        # Column Check (for updating legacy databases). 
        cursor = conn.execute("PRAGMA table_info(attempts)")
        columns = [column[1] for column in cursor.fetchall()]
        if "mistake_tags" not in columns:
            conn.execute("ALTER TABLE attempts ADD COLUMN mistake_tags TEXT")
        
        conn.commit()

def record_attempt(db_path: str, topic: str, solved: bool, interactions: int, mistake_tags: list = None) -> None:
    """Hata desenleri dahil olmak üzere problem denemesini kaydeder."""
    # I converted the list to JSON format to save it to the database.
    tags_json = json.dumps(mistake_tags if mistake_tags else [])
    
    with sqlite3.connect(db_path) as conn:
        conn.execute(
            "INSERT INTO attempts (created_at, topic, solved, interactions, mistake_tags) VALUES (?, ?, ?, ?, ?)",
            (
                datetime.now(timezone.utc).isoformat(), 
                topic, 
                int(solved), 
                max(interactions, 1),
                tags_json
            ),
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

        # Calculate Common Mistakes
        rows_tags = conn.execute("SELECT mistake_tags FROM attempts WHERE mistake_tags IS NOT NULL").fetchall()
        mistake_counts = {}
        for row in rows_tags:
            try:
                tags = json.loads(row[0])
                for tag in tags:
                    mistake_counts[tag] = mistake_counts.get(tag, 0) + 1
            except:
                continue
        
        common_mistakes = sorted(mistake_counts.items(), key=lambda x: x[1], reverse=True)

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
        "common_mistakes": common_mistakes
    }
