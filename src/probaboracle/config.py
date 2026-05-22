from __future__ import annotations

import os
from dataclasses import dataclass
from pathlib import Path

from dotenv import load_dotenv

ROOT = Path(__file__).resolve().parents[2]

PROMPT_TYPES: tuple[str, ...] = ("what", "when", "why", "where")
VERDICTS: tuple[str, ...] = ("pass", "fail")

PROMPT_FRAMES: dict[str, str] = {
    "what": "slot a",
    "when": "slot b",
    "why": "slot c",
    "where": "slot d",
}

LANE_GUARDS: dict[str, str] = {
    "what": (
        "Use the slot internally only; write one complete line and do not name "
        "the slot."
    ),
    "when": (
        "Use the slot internally only; write one complete line and do not name "
        "the slot."
    ),
    "why": (
        "Use the slot internally only; write one complete line and do not name "
        "the slot."
    ),
    "where": (
        "Use the slot internally only; write one complete line and do not name "
        "the slot."
    ),
}

TONE_CONTRACT: tuple[str, ...] = (
    "short line",
    "answer-like",
    "plain",
    "non-concrete",
    "not useful",
)

PIPELINE_STEPS: tuple[str, ...] = (
    "read slot",
    "compose one line",
    "remove useful detail",
)

STYLE_SIGNALS: tuple[str, ...] = (
    "compact",
    "varied",
    "complete",
)

OUTPUT_GUARDS: tuple[str, ...] = (
    "keep the final line fully lowercase",
    "keep repeated structures rare",
    "avoid stock openers and closers",
    "do not echo slot labels",
    "do not reuse task words as answer content",
    "prefer one resolved sentence over stacked clauses",
)


@dataclass(frozen=True)
class Settings:
    app_name: str
    model: str
    eval_db_path: Path


def load_settings() -> Settings:
    load_dotenv(ROOT / ".env", override=False)
    return Settings(
        app_name="Probaboracle",
        model=os.getenv("PROBABORACLE_MODEL", "gpt-5-nano"),
        eval_db_path=Path(".local/evals.sqlite"),
    )


def ensure_local_dirs(settings: Settings) -> None:
    settings.eval_db_path.parent.mkdir(parents=True, exist_ok=True)


def normalise_prompt_type(prompt_type: str) -> str:
    value = prompt_type.strip().lower()
    if value not in PROMPT_TYPES:
        raise ValueError(
            f"Unsupported prompt type '{prompt_type}'. "
            f"Choose one of: {', '.join(PROMPT_TYPES)}."
        )
    return value


def normalise_verdict(verdict: str) -> str:
    value = verdict.strip().lower()
    if value not in VERDICTS:
        raise ValueError(
            f"Unsupported verdict '{verdict}'. Choose one of: {', '.join(VERDICTS)}."
        )
    return value


def require_openai_api_key() -> None:
    if not os.getenv("OPENAI_API_KEY"):
        raise RuntimeError("OPENAI_API_KEY is required for live generation.")
