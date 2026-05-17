from __future__ import annotations

import os
from dataclasses import dataclass
from pathlib import Path

from dotenv import load_dotenv

ROOT = Path(__file__).resolve().parents[2]

PROMPT_TYPES: tuple[str, ...] = ("what", "when", "why", "where")
VERDICTS: tuple[str, ...] = ("pass", "fail")

PROMPT_FRAMES: dict[str, str] = {
    "what": "hint at the shape of a thing without actually defining it",
    "when": "gesture at timing without giving any usable date or schedule",
    "why": "suggest a reason without becoming a real explanation",
    "where": "gesture at position without becoming navigable",
}

LANE_GUARDS: dict[str, str] = {
    "what": (
        "Keep the line shape-first; hint at form without turning the answer into "
        "a definition or a location claim."
    ),
    "when": (
        "Keep one timing relation only; resolve as one sentence, avoid stacked "
        "timing pivots, and deny schedule usefulness without piling on."
    ),
    "why": (
        "Stay deadpan and causal-adjacent; prefer one plain contradiction over "
        "decorative metaphor or fallback loops."
    ),
    "where": (
        "Resolve as a full answer-shaped sentence about relation or placement "
        "without becoming navigable or collapsing into repeated simple contrast."
    ),
}

TONE_CONTRACT: tuple[str, ...] = (
    "answer-shaped non-answer",
    "deadpan but slightly pseudo-mystical",
    "confident and indecisive at the same time",
    "resolved in grammar but unresolved in meaning",
    "non-concrete and unhelpful",
    "clean contradiction over florid vagueness",
)

PIPELINE_STEPS: tuple[str, ...] = (
    "certainty signal",
    "indecision signal",
    "connective or hinge",
    "soft conclusion",
)

STYLE_SIGNALS: tuple[str, ...] = (
    "certainty without commitment",
    "indecision without collapse",
    "one light hinge",
    "soft non-resolving close",
)

OUTPUT_GUARDS: tuple[str, ...] = (
    "keep the final line fully lowercase",
    "keep repeated structures rare",
    "let wording vary instead of falling back to stock phrases",
    "use occasional first-person framing only when it sharpens the line",
    "prefer one clean contradiction over stacked clauses",
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
