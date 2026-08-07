"""One-time SQLite migration using Python's built-in sqlite3 module.

Connects to backend/app.db and adds nullable columns to the resumes table only if
they don't already exist. Safe to run multiple times and preserves existing data.

Columns added:
- qualification VARCHAR(100)
- skills TEXT
- district VARCHAR(100)
- state VARCHAR(100)
- profile_summary TEXT

Usage:
    python backend/scripts/add_resume_columns_sqlite_stdlib.py

This script is intentionally minimal and does not require SQLAlchemy or Alembic.
"""
from __future__ import annotations

import os
import sqlite3
import sys
from typing import List, Tuple

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.abspath(os.path.join(SCRIPT_DIR, "..", "app.db"))

COLUMNS: List[Tuple[str, str]] = [
    ("qualification", "VARCHAR(100)"),
    ("skills", "TEXT"),
    ("district", "VARCHAR(100)"),
    ("state", "VARCHAR(100)"),
    ("profile_summary", "TEXT"),
]


def table_exists(conn: sqlite3.Connection, table_name: str) -> bool:
    cur = conn.execute(
        "SELECT name FROM sqlite_master WHERE type='table' AND name=?;",
        (table_name,),
    )
    return cur.fetchone() is not None


def get_existing_columns(conn: sqlite3.Connection, table_name: str) -> List[str]:
    cur = conn.execute(f"PRAGMA table_info({table_name});")
    rows = cur.fetchall()
    return [row[1] for row in rows]


def add_column(conn: sqlite3.Connection, table_name: str, column_name: str, column_type: str) -> None:
    sql = f"ALTER TABLE {table_name} ADD COLUMN {column_name} {column_type};"
    conn.execute(sql)


def main() -> int:
    if not os.path.exists(DB_PATH):
        print(f"ERROR: database file not found at {DB_PATH}")
        return 2

    conn = sqlite3.connect(DB_PATH)
    try:
        if not table_exists(conn, "resumes"):
            print("ERROR: 'resumes' table does not exist in the database.")
            return 3

        existing = set(get_existing_columns(conn, "resumes"))

        added: List[str] = []
        skipped: List[str] = []

        for name, col_type in COLUMNS:
            if name in existing:
                skipped.append(name)
            else:
                print(f"Adding column: {name} {col_type}")
                add_column(conn, "resumes", name, col_type)
                added.append(name)

        # Commit the ALTER TABLE operations
        conn.commit()

        print("Migration complete.")
        if added:
            print("Added columns:", ", ".join(added))
        if skipped:
            print("Already present:", ", ".join(skipped))

        return 0

    except sqlite3.DatabaseError as exc:
        # Rollback any partial changes on error
        conn.rollback()
        print("ERROR: database operation failed:", exc)
        return 4

    finally:
        conn.close()


if __name__ == "__main__":
    raise SystemExit(main())
