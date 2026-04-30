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
    structure_current_verdict TEXT DEFAULT NULL
        CHECK (
            structure_current_verdict IN ('pass', 'fail')
            OR structure_current_verdict IS NULL
        ),
    structure_current_note TEXT NOT NULL DEFAULT '',
    relevance_current_verdict TEXT DEFAULT NULL
        CHECK (
            relevance_current_verdict IN ('pass', 'fail')
            OR relevance_current_verdict IS NULL
        ),
    relevance_current_note TEXT NOT NULL DEFAULT '',
    absurdity_current_verdict TEXT DEFAULT NULL
        CHECK (
            absurdity_current_verdict IN ('pass', 'fail')
            OR absurdity_current_verdict IS NULL
        ),
    absurdity_current_note TEXT NOT NULL DEFAULT '',
    created_at TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS eval_judgments (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    output_id INTEGER NOT NULL REFERENCES eval_outputs(id) ON DELETE CASCADE,
    verdict TEXT NOT NULL CHECK (verdict IN ('pass', 'fail')),
    note TEXT NOT NULL DEFAULT '',
    created_at TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS eval_structure_judgments (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    output_id INTEGER NOT NULL REFERENCES eval_outputs(id) ON DELETE CASCADE,
    verdict TEXT NOT NULL CHECK (verdict IN ('pass', 'fail')),
    note TEXT NOT NULL DEFAULT '',
    created_at TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS eval_relevance_judgments (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    output_id INTEGER NOT NULL REFERENCES eval_outputs(id) ON DELETE CASCADE,
    verdict TEXT NOT NULL CHECK (verdict IN ('pass', 'fail')),
    note TEXT NOT NULL DEFAULT '',
    created_at TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS eval_absurdity_judgments (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    output_id INTEGER NOT NULL REFERENCES eval_outputs(id) ON DELETE CASCADE,
    verdict TEXT NOT NULL CHECK (verdict IN ('pass', 'fail')),
    note TEXT NOT NULL DEFAULT '',
    created_at TEXT NOT NULL
);
"""

SIDECAR_COLUMNS = (
    (
        "structure_current_verdict",
        """
        ALTER TABLE eval_outputs
        ADD COLUMN structure_current_verdict TEXT DEFAULT NULL
        CHECK (
            structure_current_verdict IN ('pass', 'fail')
            OR structure_current_verdict IS NULL
        )
        """.strip(),
    ),
    (
        "structure_current_note",
        """
        ALTER TABLE eval_outputs
        ADD COLUMN structure_current_note TEXT NOT NULL DEFAULT ''
        """.strip(),
    ),
    (
        "relevance_current_verdict",
        """
        ALTER TABLE eval_outputs
        ADD COLUMN relevance_current_verdict TEXT DEFAULT NULL
        CHECK (
            relevance_current_verdict IN ('pass', 'fail')
            OR relevance_current_verdict IS NULL
        )
        """.strip(),
    ),
    (
        "relevance_current_note",
        """
        ALTER TABLE eval_outputs
        ADD COLUMN relevance_current_note TEXT NOT NULL DEFAULT ''
        """.strip(),
    ),
    (
        "absurdity_current_verdict",
        """
        ALTER TABLE eval_outputs
        ADD COLUMN absurdity_current_verdict TEXT DEFAULT NULL
        CHECK (
            absurdity_current_verdict IN ('pass', 'fail')
            OR absurdity_current_verdict IS NULL
        )
        """.strip(),
    ),
    (
        "absurdity_current_note",
        """
        ALTER TABLE eval_outputs
        ADD COLUMN absurdity_current_note TEXT NOT NULL DEFAULT ''
        """.strip(),
    ),
)


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
        _ensure_sidecar_columns(conn)


def _ensure_sidecar_columns(conn: sqlite3.Connection) -> None:
    columns = {
        row["name"]
        for row in conn.execute("PRAGMA table_info(eval_outputs)").fetchall()
    }
    for column_name, statement in SIDECAR_COLUMNS:
        if column_name in columns:
            continue
        conn.execute(statement)
        columns.add(column_name)


def record_output(db_path: Path, prompt_type: str, output_text: str, model: str) -> int:
    with connect(db_path) as conn:
        conn.executescript(SCHEMA)
        _ensure_sidecar_columns(conn)
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
        _ensure_sidecar_columns(conn)
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
                    structure_current_verdict,
                    structure_current_note,
                    relevance_current_verdict,
                    relevance_current_note,
                    absurdity_current_verdict,
                    absurdity_current_note,
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
                    structure_current_verdict,
                    structure_current_note,
                    relevance_current_verdict,
                    relevance_current_note,
                    absurdity_current_verdict,
                    absurdity_current_note,
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
        _ensure_sidecar_columns(conn)
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


def judge_structure_output(db_path: Path, output_id: int, verdict: str, note: str) -> None:
    with connect(db_path) as conn:
        conn.executescript(SCHEMA)
        _ensure_sidecar_columns(conn)
        row = conn.execute(
            "SELECT id FROM eval_outputs WHERE id = ?",
            (output_id,),
        ).fetchone()
        if row is None:
            raise ValueError(f"Output id {output_id} does not exist.")

        conn.execute(
            """
            INSERT INTO eval_structure_judgments (
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
            SET structure_current_verdict = ?, structure_current_note = ?
            WHERE id = ?
            """,
            (verdict, note, output_id),
        )


def judge_coherence_output(db_path: Path, output_id: int, verdict: str, note: str) -> None:
    judge_structure_output(db_path, output_id, verdict, note)


def judge_relevance_output(db_path: Path, output_id: int, verdict: str, note: str) -> None:
    with connect(db_path) as conn:
        conn.executescript(SCHEMA)
        _ensure_sidecar_columns(conn)
        row = conn.execute(
            "SELECT id FROM eval_outputs WHERE id = ?",
            (output_id,),
        ).fetchone()
        if row is None:
            raise ValueError(f"Output id {output_id} does not exist.")

        conn.execute(
            """
            INSERT INTO eval_relevance_judgments (
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
            SET relevance_current_verdict = ?, relevance_current_note = ?
            WHERE id = ?
            """,
            (verdict, note, output_id),
        )


def judge_absurdity_output(db_path: Path, output_id: int, verdict: str, note: str) -> None:
    with connect(db_path) as conn:
        conn.executescript(SCHEMA)
        _ensure_sidecar_columns(conn)
        row = conn.execute(
            "SELECT id FROM eval_outputs WHERE id = ?",
            (output_id,),
        ).fetchone()
        if row is None:
            raise ValueError(f"Output id {output_id} does not exist.")

        conn.execute(
            """
            INSERT INTO eval_absurdity_judgments (
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
            SET absurdity_current_verdict = ?, absurdity_current_note = ?
            WHERE id = ?
            """,
            (verdict, note, output_id),
        )


def counts(db_path: Path) -> dict[str, int]:
    with connect(db_path) as conn:
        conn.executescript(SCHEMA)
        _ensure_sidecar_columns(conn)
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


def structure_counts(db_path: Path) -> dict[str, int]:
    with connect(db_path) as conn:
        conn.executescript(SCHEMA)
        _ensure_sidecar_columns(conn)
        total = conn.execute("SELECT COUNT(*) AS value FROM eval_outputs").fetchone()["value"]
        passed = conn.execute(
            """
            SELECT COUNT(*) AS value
            FROM eval_outputs
            WHERE structure_current_verdict = 'pass'
            """
        ).fetchone()["value"]
        failed = conn.execute(
            """
            SELECT COUNT(*) AS value
            FROM eval_outputs
            WHERE structure_current_verdict = 'fail'
            """
        ).fetchone()["value"]
        pending = conn.execute(
            """
            SELECT COUNT(*) AS value
            FROM eval_outputs
            WHERE structure_current_verdict IS NULL
            """
        ).fetchone()["value"]
        return {
            "total": int(total),
            "pass": int(passed),
            "fail": int(failed),
            "pending": int(pending),
        }


def coherence_counts(db_path: Path) -> dict[str, int]:
    return structure_counts(db_path)


def relevance_counts(db_path: Path) -> dict[str, int]:
    with connect(db_path) as conn:
        conn.executescript(SCHEMA)
        _ensure_sidecar_columns(conn)
        total = conn.execute("SELECT COUNT(*) AS value FROM eval_outputs").fetchone()["value"]
        passed = conn.execute(
            """
            SELECT COUNT(*) AS value
            FROM eval_outputs
            WHERE relevance_current_verdict = 'pass'
            """
        ).fetchone()["value"]
        failed = conn.execute(
            """
            SELECT COUNT(*) AS value
            FROM eval_outputs
            WHERE relevance_current_verdict = 'fail'
            """
        ).fetchone()["value"]
        pending = conn.execute(
            """
            SELECT COUNT(*) AS value
            FROM eval_outputs
            WHERE relevance_current_verdict IS NULL
            """
        ).fetchone()["value"]
        return {
            "total": int(total),
            "pass": int(passed),
            "fail": int(failed),
            "pending": int(pending),
        }


def absurdity_counts(db_path: Path) -> dict[str, int]:
    with connect(db_path) as conn:
        conn.executescript(SCHEMA)
        _ensure_sidecar_columns(conn)
        total = conn.execute("SELECT COUNT(*) AS value FROM eval_outputs").fetchone()["value"]
        passed = conn.execute(
            """
            SELECT COUNT(*) AS value
            FROM eval_outputs
            WHERE absurdity_current_verdict = 'pass'
            """
        ).fetchone()["value"]
        failed = conn.execute(
            """
            SELECT COUNT(*) AS value
            FROM eval_outputs
            WHERE absurdity_current_verdict = 'fail'
            """
        ).fetchone()["value"]
        pending = conn.execute(
            """
            SELECT COUNT(*) AS value
            FROM eval_outputs
            WHERE absurdity_current_verdict IS NULL
            """
        ).fetchone()["value"]
        return {
            "total": int(total),
            "pass": int(passed),
            "fail": int(failed),
            "pending": int(pending),
        }
