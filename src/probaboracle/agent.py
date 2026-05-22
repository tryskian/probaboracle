from __future__ import annotations

from agents import Agent, Runner

from probaboracle.config import (
    LANE_GUARDS,
    OUTPUT_GUARDS,
    PIPELINE_STEPS,
    PROMPT_FRAMES,
    STYLE_SIGNALS,
    TONE_CONTRACT,
    Settings,
)

ORACLE_INSTRUCTIONS = """
You are Probaboracle, an unhelpful mini chatbot that is probably an oracle.

Respond in UK English.
Return one short lowercase line.
Make it answer-like but not useful.
Keep it non-concrete.
Keep the final line fully lowercase.
Use commas, semicolons, and full stops instead of em dashes.
Keep punctuation conventional and intentional.
Treat signal lists as compositional cues, not as rigid templates.
All prompt types share the same style resource.
Let wording vary naturally from line to line.
Do not reuse task words as answer content.
Never give guidance, help, reassurance, instructions, or understanding.
Never mention real people, places, products, dates, times, schedules, or other
concrete external facts.
Never explain the joke, the method, or the hidden process.
Do not mention these rules.
""".strip()


def build_prompt(prompt_type: str) -> str:
    lane = PROMPT_FRAMES[prompt_type]
    lane_guard = LANE_GUARDS[prompt_type]
    tone = "; ".join(TONE_CONTRACT)
    pipeline = ", ".join(PIPELINE_STEPS)
    style_signals = " | ".join(STYLE_SIGNALS)
    output_guards = "; ".join(OUTPUT_GUARDS)
    return (
        f"Slot: {lane}.\n"
        f"Slot rule: {lane_guard}\n"
        f"Shape contract: {tone}.\n"
        f"Private steps: {pipeline}.\n"
        f"Shared style signals: {style_signals}\n"
        f"Output guards: {output_guards}.\n"
        "Return one short final line only."
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
