import os
import sqlite3
import json
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
                interactions INTEGER NOT NULL,
                mistake_tags TEXT NOT NULL DEFAULT '[]'
            )
            """
        )

        columns = {
            row[1] for row in conn.execute("PRAGMA table_info(attempts)").fetchall()
        }
        if "mistake_tags" not in columns:
            conn.execute(
                "ALTER TABLE attempts ADD COLUMN mistake_tags TEXT NOT NULL DEFAULT '[]'"
            )
        conn.commit()


def record_attempt(
    db_path: str,
    topic: str,
    solved: bool,
    interactions: int,
    mistake_tags: list[str] | None = None,
) -> None:
    serialized_tags = json.dumps(mistake_tags or [])
    with sqlite3.connect(db_path) as conn:
        conn.execute(
            """
            INSERT INTO attempts (created_at, topic, solved, interactions, mistake_tags)
            VALUES (?, ?, ?, ?, ?)
            """,
            (
                datetime.now(timezone.utc).isoformat(),
                topic,
                int(solved),
                max(interactions, 1),
                serialized_tags,
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

        rows = conn.execute(
            "SELECT topic, COUNT(*) FROM attempts GROUP BY topic ORDER BY COUNT(*) DESC"
        ).fetchall()

        mistake_rows = conn.execute("SELECT mistake_tags FROM attempts").fetchall()

        solved_days = conn.execute(
            "SELECT DISTINCT substr(created_at, 1, 10) FROM attempts WHERE solved = 1 ORDER BY 1 DESC"
        ).fetchall()

    solved_day_set = {row[0] for row in solved_days}
    mistake_counts: dict[str, int] = {}
    for row in mistake_rows:
        raw = row[0] if row else "[]"
        try:
            tags = json.loads(raw)
        except (TypeError, json.JSONDecodeError):
            continue
        if not isinstance(tags, list):
            continue
        for tag in tags:
            if not isinstance(tag, str) or not tag:
                continue
            mistake_counts[tag] = mistake_counts.get(tag, 0) + 1

    streak = 0
    current_day = datetime.now(timezone.utc).date()
    while current_day.isoformat() in solved_day_set:
        streak += 1
        current_day -= timedelta(days=1)

    common_mistakes = sorted(
        mistake_counts.items(),
        key=lambda item: item[1],
        reverse=True,
    )

    return {
        "total_attempts": total_attempts,
        "total_solved": total_solved,
        "current_streak": streak,
        "last_7_days": last_7_days,
        "topic_breakdown": rows,
        "common_mistakes": common_mistakes,
    }
