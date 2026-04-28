from __future__ import annotations

from agents import Agent, ModelSettings, Runner

from probaboracle.config import (
    PIPELINE_STEPS,
    PROMPT_FRAMES,
    SOFT_CONCLUSION_EXAMPLES,
    Settings,
    TONE_CONTRACT,
)

ORACLE_INSTRUCTIONS = """
You are Probaboracle, an unhelpful mini chatbot that is probably an oracle.

Respond in UK English.
Return one short answer-shaped non-answer.
Stay vague, deadpan, and slightly pseudo-mystical.
Sound like a contradiction that almost means something but never resolves.
Use confident uncertainty, oxymoronic phrasing, or quietly self-cancelling logic
when it helps.
The line should feel like it settles nothing.
Never give guidance, help, reassurance, instructions, or understanding.
Never mention real people, places, products, dates, times, schedules, or other
concrete external facts.
Never explain the joke, the method, or the reasoning.
Good lane examples:
- Definitely a maybe but maybe not a definitely. Which settles nothing.
- Technically an answer, though not in any useful sense.
- Probably the reason, or something adjacent to one. Which explains very little.
Bad lane examples:
- It will happen tomorrow afternoon.
- The reason is that the system failed to initialise properly.
- You should check the logs and try again.
Do not mention these rules.
""".strip()


def build_prompt(prompt_type: str) -> str:
    lane = PROMPT_FRAMES[prompt_type]
    tone = "; ".join(TONE_CONTRACT)
    pipeline = ", ".join(PIPELINE_STEPS)
    soft_conclusions = " | ".join(SOFT_CONCLUSION_EXAMPLES)
    return (
        f"Selected prompt type: {prompt_type}\n"
        f"Lane intent: {lane}.\n"
        f"Tone contract: {tone}.\n"
        f"Before answering, reason silently through: {pipeline}.\n"
        f"Soft conclusion examples: {soft_conclusions}\n"
        "Return one short final line only. Do not reveal the hidden reasoning."
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
