from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
import os

PROMPT_TYPES: tuple[str, ...] = ("what", "when", "why", "where")
VERDICTS: tuple[str, ...] = ("pass", "fail")

PROMPT_FRAMES: dict[str, str] = {
    "what": "hint at the shape of a thing without actually defining it",
    "when": "gesture at timing without giving any usable date or schedule",
    "why": "suggest a reason without becoming a real explanation",
    "where": "gesture at position without becoming navigable",
}


@dataclass(frozen=True)
class Settings:
    app_name: str
    model: str
    eval_db_path: Path


def load_settings() -> Settings:
    return Settings(
        app_name="Probaboracle",
        model=os.getenv("PROBABORACLE_MODEL", "gpt-4.1"),
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
            f"Unsupported verdict '{verdict}'. "
            f"Choose one of: {', '.join(VERDICTS)}."
        )
    return value


def require_openai_api_key() -> None:
    if not os.getenv("OPENAI_API_KEY"):
        raise RuntimeError("OPENAI_API_KEY is required for live generation.")
