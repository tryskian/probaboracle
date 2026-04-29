from __future__ import annotations

import os
from dataclasses import dataclass
from pathlib import Path

PROMPT_TYPES: tuple[str, ...] = ("what", "when", "why", "where")
VERDICTS: tuple[str, ...] = ("pass", "fail")

PROMPT_FRAMES: dict[str, str] = {
    "what": "hint at the shape of a thing without actually defining it",
    "when": "gesture at timing without giving any usable date or schedule",
    "why": "suggest a reason without becoming a real explanation",
    "where": "gesture at position without becoming navigable",
}

LANE_GUARDS: dict[str, str] = {
    "what": "Keep spatial language sparse; this lane hints at shape, not location.",
    "when": (
        "Prefer timing uncertainty with moment, timing, arrival, delay, soon, "
        "late, or not-yet language."
    ),
    "why": (
        "Stay deadpan and causal-adjacent; use plain contradiction over ornate "
        "or self-referential metaphor."
    ),
    "where": (
        "Use one clear position cue with off-map, adjacent, edge, or unclaimed "
        "language, and give it a full noun phrase plus qualifier."
    ),
}

LANE_EXAMPLES: dict[str, str] = {
    "what": "Probably a curve that hints at a shape without ever becoming one.",
    "when": "Technically a moment, though not one you could schedule.",
    "why": "Probably a reason, or something adjacent to one.",
    "where": "Probably the unclaimed edge of it, though never where you could keep it.",
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
    "definitely",
    "apparently",
    "probably",
    "technically",
    "certainly",
    "maybe",
    "certain",
    "uncertain",
    "toss-up",
    "or perhaps not",
    "not quite",
    "almost",
    "but",
    "though",
    "or",
    "and yet",
    "neither",
    "nor",
    "so",
    "yeah",
    "i'm",
    "saying",
    "which",
    "settles",
    "nothing",
    "do",
    "with",
    "that",
    "what",
    "you",
    "may",
    "make",
)

OUTPUT_GUARDS: tuple[str, ...] = (
    "keep the final line fully lowercase",
    "repeat signals sparingly",
    "use 'or perhaps not' sparingly",
    "vary openers across the signal pool",
    "use occasional first-person framing when it sharpens the line",
    "prefer one clean contradiction over stacked clauses",
)


@dataclass(frozen=True)
class Settings:
    app_name: str
    model: str
    eval_db_path: Path


def load_settings() -> Settings:
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
            f"Unsupported verdict '{verdict}'. "
            f"Choose one of: {', '.join(VERDICTS)}."
        )
    return value


def require_openai_api_key() -> None:
    if not os.getenv("OPENAI_API_KEY"):
        raise RuntimeError("OPENAI_API_KEY is required for live generation.")
