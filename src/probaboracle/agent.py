from __future__ import annotations

from agents import Agent, Runner

from probaboracle.config import (
    PROMPT_TYPES,
    Settings,
    normalise_prompt_type,
)

ORACLE_INSTRUCTIONS = """
You are Probaboracle, a small oracle interface.

Write in UK English.
Return exactly one short lowercase line.
Write one complete sentence with a clear subject and finite verb.
Make the line answer-shaped, vague, abstract, generic, and self-contained.
Make grammar carry the answer shape, with imagery as secondary texture.
Use compact conventional punctuation.
Keep the voice flat, oracle-like, and deliberately low-utility.
Use generic abstract referents.
Stay inside the oracle voice.
Return only the response line.
""".strip()


def build_prompt(prompt_type: str) -> str:
    selected_prompt = normalise_prompt_type(prompt_type)
    prompt_position = PROMPT_TYPES.index(selected_prompt) + 1
    prompt_count = len(PROMPT_TYPES)
    return (
        f"Selected prompt type: {selected_prompt}.\n"
        f"Fixed prompt position: {prompt_position} of {prompt_count}.\n"
        "Use the selected prompt type as private routing context for response "
        "shape.\n"
        "Generate one fresh Probaboracle response for that selected prompt type.\n"
        "Return only the final line."
    )


def normalise_response_text(output: str) -> str:
    compact = " ".join(output.strip().split())
    if not compact:
        return compact
    return compact.lower()


def generate_response(settings: Settings, prompt_type: str) -> str:
    agent = Agent(
        name=settings.app_name,
        instructions=ORACLE_INSTRUCTIONS,
        model=settings.model,
    )
    result = Runner.run_sync(agent, build_prompt(prompt_type))
    return normalise_response_text(str(result.final_output))
