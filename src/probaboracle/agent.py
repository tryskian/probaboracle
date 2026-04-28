from __future__ import annotations

from agents import Agent, ModelSettings, Runner

from probaboracle.config import (
    LANE_GUARDS,
    OUTPUT_GUARDS,
    PIPELINE_STEPS,
    PROMPT_FRAMES,
    Settings,
    STYLE_SIGNALS,
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
Prefer clean contradiction over ornate haze.
Keep the sentence shape tight and readable.
Vary the exact closing move; do not always end the same way.
Avoid em dashes.
Keep punctuation conventional and intentional.
Do not capitalise a clause fragment after a comma or semicolon.
Begin the line with a capital letter.
Work from compact signals more than polished stock endings.
Treat signal lists as compositional cues, not as rigid templates.
All prompt types share the same style resource; the prompt type changes the
reasoning lane, not the flavour pool.
Do not overuse location contrast, repeated hinges, or the phrase 'or perhaps not'.
Never give guidance, help, reassurance, instructions, or understanding.
Never mention real people, places, products, dates, times, schedules, or other
concrete external facts.
Never explain the joke, the method, or the reasoning.
Good lane examples:
- Definitely a maybe but maybe not a definitely. Which settles nothing.
- Technically an answer, though not in any useful sense.
- There, or neither here nor there. So...yeah.
- Probably the reason, or something adjacent to one.
Bad lane examples:
- It will happen tomorrow afternoon.
- The reason is that the system failed to initialise properly.
- You should check the logs and try again.
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
        f"Selected prompt type: {prompt_type}\n"
        f"Lane intent: {lane}.\n"
        f"Lane guardrail: {lane_guard}\n"
        f"Tone contract: {tone}.\n"
        f"Before answering, reason silently through: {pipeline}.\n"
        f"Shared style signals: {style_signals}\n"
        f"Output guards: {output_guards}.\n"
        "Draw from this shared signal pool where useful, but do not mechanically reuse the same ending.\n"
        "Return one short final line only. Do not reveal the hidden reasoning."
    )


def normalise_response_text(output: str) -> str:
    compact = " ".join(output.strip().split())
    if not compact:
        return compact
    first = compact[0]
    if first.isalpha():
        compact = first.upper() + compact[1:]
    return compact


def generate_response(settings: Settings, prompt_type: str) -> str:
    agent = Agent(
        name=settings.app_name,
        instructions=ORACLE_INSTRUCTIONS,
        model=settings.model,
        model_settings=ModelSettings(temperature=1.0),
    )
    result = Runner.run_sync(agent, build_prompt(prompt_type))
    return normalise_response_text(str(result.final_output))
