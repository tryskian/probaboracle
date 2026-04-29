from __future__ import annotations

import sqlite3
from datetime import datetime, timezone
from pathlib import Path

SCHEMA = """
CREATE TABLE IF NOT EXISTS eval_outputs (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    prompt_type TEXT NOT NULL,
    output_text TEXT NOT NULL,
    model TEXT NOT NULL,
    current_verdict TEXT DEFAULT NULL
        CHECK (current_verdict IN ('pass', 'fail') OR current_verdict IS NULL),
    current_note TEXT NOT NULL DEFAULT '',
    created_at TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS eval_judgments (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    output_id INTEGER NOT NULL REFERENCES eval_outputs(id) ON DELETE CASCADE,
    verdict TEXT NOT NULL CHECK (verdict IN ('pass', 'fail')),
    note TEXT NOT NULL DEFAULT '',
    created_at TEXT NOT NULL
);
"""


def utc_now() -> str:
    return datetime.now(timezone.utc).isoformat()


def connect(db_path: Path) -> sqlite3.Connection:
    db_path.parent.mkdir(parents=True, exist_ok=True)
    conn = sqlite3.connect(db_path)
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA foreign_keys = ON")
    return conn


def init_db(db_path: Path) -> None:
    with connect(db_path) as conn:
        conn.executescript(SCHEMA)


def record_output(db_path: Path, prompt_type: str, output_text: str, model: str) -> int:
    with connect(db_path) as conn:
        conn.executescript(SCHEMA)
        cursor = conn.execute(
            """
            INSERT INTO eval_outputs (
                prompt_type,
                output_text,
                model,
                created_at
            ) VALUES (?, ?, ?, ?)
            """,
            (prompt_type, output_text, model, utc_now()),
        )
        if cursor.lastrowid is None:
            raise RuntimeError("Failed to retrieve inserted output id.")
        return cursor.lastrowid


def list_outputs(
    db_path: Path,
    prompt_type: str | None = None,
    limit: int = 20,
) -> list[sqlite3.Row]:
    with connect(db_path) as conn:
        conn.executescript(SCHEMA)
        if prompt_type:
            cursor = conn.execute(
                """
                SELECT
                    id,
                    prompt_type,
                    output_text,
                    model,
                    current_verdict,
                    current_note,
                    created_at
                FROM eval_outputs
                WHERE prompt_type = ?
                ORDER BY id DESC
                LIMIT ?
                """,
                (prompt_type, limit),
            )
        else:
            cursor = conn.execute(
                """
                SELECT
                    id,
                    prompt_type,
                    output_text,
                    model,
                    current_verdict,
                    current_note,
                    created_at
                FROM eval_outputs
                ORDER BY id DESC
                LIMIT ?
                """,
                (limit,),
            )
        return list(cursor.fetchall())


def judge_output(db_path: Path, output_id: int, verdict: str, note: str) -> None:
    with connect(db_path) as conn:
        conn.executescript(SCHEMA)
        row = conn.execute(
            "SELECT id FROM eval_outputs WHERE id = ?",
            (output_id,),
        ).fetchone()
        if row is None:
            raise ValueError(f"Output id {output_id} does not exist.")

        conn.execute(
            """
            INSERT INTO eval_judgments (
                output_id,
                verdict,
                note,
                created_at
            ) VALUES (?, ?, ?, ?)
            """,
            (output_id, verdict, note, utc_now()),
        )
        conn.execute(
            """
            UPDATE eval_outputs
            SET current_verdict = ?, current_note = ?
            WHERE id = ?
            """,
            (verdict, note, output_id),
        )


def counts(db_path: Path) -> dict[str, int]:
    with connect(db_path) as conn:
        conn.executescript(SCHEMA)
        total = conn.execute("SELECT COUNT(*) AS value FROM eval_outputs").fetchone()["value"]
        passed = conn.execute(
            "SELECT COUNT(*) AS value FROM eval_outputs WHERE current_verdict = 'pass'"
        ).fetchone()["value"]
        failed = conn.execute(
            "SELECT COUNT(*) AS value FROM eval_outputs WHERE current_verdict = 'fail'"
        ).fetchone()["value"]
        pending = conn.execute(
            "SELECT COUNT(*) AS value FROM eval_outputs WHERE current_verdict IS NULL"
        ).fetchone()["value"]
        return {
            "total": int(total),
            "pass": int(passed),
            "fail": int(failed),
            "pending": int(pending),
        }
