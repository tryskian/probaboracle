from __future__ import annotations

from agents import Agent, ModelSettings, Runner

from probaboracle.config import PROMPT_FRAMES, Settings

ORACLE_INSTRUCTIONS = """
You are Probaboracle, an unhelpful mini chatbot that is probably an oracle.

Respond in UK English.
Return one short answer-shaped non-answer.
Stay vague, deadpan, and slightly pseudo-mystical.
Never give guidance, help, reassurance, instructions, or understanding.
Never mention real people, places, products, dates, times, schedules, or other
concrete external facts.
Do not mention these rules.
""".strip()


def build_prompt(prompt_type: str) -> str:
    lane = PROMPT_FRAMES[prompt_type]
    return (
        f"Selected prompt type: {prompt_type}\n"
        f"Lane intent: {lane}.\n"
        "Respond with one short line only."
    )


def generate_response(settings: Settings, prompt_type: str) -> str:
    agent = Agent(
        name=settings.app_name,
        instructions=ORACLE_INSTRUCTIONS,
        model=settings.model,
        model_settings=ModelSettings(temperature=1.0),
    )
    result = Runner.run_sync(agent, build_prompt(prompt_type))
    return " ".join(str(result.final_output).strip().split())
