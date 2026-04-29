from __future__ import annotations

from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from probaboracle.config import PROMPT_TYPES
from probaboracle.eval_db import SCHEMA, connect

VERDICT_ORDER: tuple[str, ...] = ("pending", "fail", "pass")


def _utc_now() -> str:
    return datetime.now(timezone.utc).isoformat()


def build_eval_chart_payload(db_path: Path) -> dict[str, Any]:
    lane_counts = {
        prompt_type: {"fail": 0, "pass": 0, "pending": 0}
        for prompt_type in PROMPT_TYPES
    }
    latest_created_at: str | None = None

    with connect(db_path) as conn:
        conn.executescript(SCHEMA)
        rows = conn.execute(
            """
            SELECT
                prompt_type,
                COALESCE(current_verdict, 'pending') AS verdict,
                COUNT(*) AS value
            FROM eval_outputs
            GROUP BY prompt_type, COALESCE(current_verdict, 'pending')
            """
        ).fetchall()
        latest_created_at = conn.execute(
            "SELECT MAX(created_at) AS value FROM eval_outputs"
        ).fetchone()["value"]

    for row in rows:
        prompt_type = row["prompt_type"]
        verdict = row["verdict"]
        value = int(row["value"])
        if prompt_type not in lane_counts:
            continue
        if verdict not in lane_counts[prompt_type]:
            continue
        lane_counts[prompt_type][verdict] = value

    lanes: list[dict[str, Any]] = []
    totals = {"fail": 0, "pass": 0, "pending": 0}
    max_lane_total = 0

    for prompt_type in PROMPT_TYPES:
        counts = lane_counts[prompt_type]
        lane_total = sum(counts.values())
        lanes.append(
            {
                "prompt_type": prompt_type,
                "counts": counts,
                "total": lane_total,
            }
        )
        max_lane_total = max(max_lane_total, lane_total)
        for verdict in VERDICT_ORDER:
            totals[verdict] += counts[verdict]

    return {
        "title": "probaboracle eval lanes",
        "subtitle": "strict pass/fail/pending counts by prompt lane from the live eval db",
        "generated_at": _utc_now(),
        "latest_created_at": latest_created_at,
        "series_order": list(VERDICT_ORDER),
        "summary": {
            "total": sum(totals.values()),
            "fail": totals["fail"],
            "pass": totals["pass"],
            "pending": totals["pending"],
            "max_lane_total": max_lane_total,
        },
        "lanes": lanes,
    }
