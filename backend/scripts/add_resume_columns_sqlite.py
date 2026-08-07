"""SQLite migration script: add nullable resume fields if they are missing.

This script uses the application's DATABASE_URL to connect and will only run
against SQLite databases. It is safe to run multiple times: each ALTER TABLE is
executed only if the corresponding column does not already exist.

Usage:
    python backend/scripts/add_resume_columns_sqlite.py

Do NOT run against non-SQLite databases. The script will refuse to run if the
configured DATABASE_URL does not point to an SQLite file.
"""
from __future__ import annotations

import sys
from typing import Iterable

from sqlalchemy import create_engine, text

from app.config import DATABASE_URL


COLUMNS_TO_ADD = [
    ("qualification", "VARCHAR(100)"),
    ("skills", "TEXT"),
    ("district", "VARCHAR(100)"),
    ("state", "VARCHAR(100)"),
    ("profile_summary", "TEXT"),
]


def is_sqlite_url(url: str) -> bool:
    return url.startswith("sqlite:")


def get_existing_columns(conn) -> set[str]:
    """Return a set of column names already present on the resumes table."""
    res = conn.execute(text("PRAGMA table_info(resumes);"))
    # PRAGMA table_info returns rows: cid, name, type, notnull, dflt_value, pk
    return {row[1] for row in res.fetchall()}


def add_column_if_missing(conn, column_name: str, column_type: str) -> bool:
    """Add the column to resumes if it's missing. Returns True if added."""
    stmt = text(f"ALTER TABLE resumes ADD COLUMN {column_name} {column_type};")
    conn.execute(stmt)
    return True


def main() -> int:
    if not is_sqlite_url(DATABASE_URL):
        print("ERROR: DATABASE_URL is not an SQLite URL. This migration only supports SQLite.")
        print(f"DATABASE_URL={DATABASE_URL!r}")
        return 2

    engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})

    with engine.begin() as conn:
        # Ensure the resumes table exists
        existing = conn.execute(text("SELECT name FROM sqlite_master WHERE type='table' AND name='resumes';")).fetchone()
        if existing is None:
            print("ERROR: 'resumes' table does not exist in the configured database.")
            return 3

        present = get_existing_columns(conn)

        added: list[str] = []
        skipped: list[str] = []

        for col_name, col_type in COLUMNS_TO_ADD:
            if col_name in present:
                skipped.append(col_name)
            else:
                print(f"Adding column: {col_name} {col_type}")
                add_column_if_missing(conn, col_name, col_type)
                added.append(col_name)

    print("Migration complete.")
    if added:
        print("Added columns:", ", ".join(added))
    if skipped:
        print("Already present:", ", ".join(skipped))

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
