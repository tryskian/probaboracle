from unittest import TestCase

from probaboracle.agent import (
    ORACLE_INSTRUCTIONS,
    build_prompt,
    normalise_response_text,
)

PROHIBITION_DIRECTIVES = (
    "never",
    "do not",
    "don't",
    "not ",
    "without",
    "avoid",
    "instead of",
    "no ",
)


class AgentOutputNormalisationTests(TestCase):
    def test_normalise_response_text_compacts_whitespace(self) -> None:
        self.assertEqual(
            normalise_response_text("  A   Quiet   Line\n Settles.  "),
            "a quiet line settles.",
        )

    def test_normalise_response_text_lowercases_the_line(self) -> None:
        self.assertEqual(
            normalise_response_text("A Quiet Line Settles."),
            "a quiet line settles.",
        )


class AgentPromptContractTests(TestCase):
    def test_oracle_instructions_do_not_embed_stock_phrase_lists_or_examples(
        self,
    ) -> None:
        self.assertNotIn("Shared style signals:", ORACLE_INSTRUCTIONS)
        self.assertNotIn("Treat signal lists", ORACLE_INSTRUCTIONS)
        self.assertNotIn("Vary the opener across signals like", ORACLE_INSTRUCTIONS)
        self.assertNotIn("Good lane examples:", ORACLE_INSTRUCTIONS)
        self.assertNotIn("Bad lane examples:", ORACLE_INSTRUCTIONS)
        self.assertNotIn("Sound like a contradiction", ORACLE_INSTRUCTIONS)
        self.assertNotIn("Prefer clean contradiction", ORACLE_INSTRUCTIONS)
        self.assertNotIn("reasoning lane", ORACLE_INSTRUCTIONS)
        self.assertNotIn("flavour pool", ORACLE_INSTRUCTIONS)
        self.assertNotIn("slot", ORACLE_INSTRUCTIONS.lower())

    def test_oracle_instructions_use_positive_shape_targets(self) -> None:
        self.assertIn("Write in UK English.", ORACLE_INSTRUCTIONS)
        self.assertIn("Return exactly one short lowercase line.", ORACLE_INSTRUCTIONS)
        self.assertIn("clear subject and finite verb", ORACLE_INSTRUCTIONS)
        self.assertIn("answer-shaped, vague, abstract", ORACLE_INSTRUCTIONS)
        self.assertIn("Use generic abstract referents.", ORACLE_INSTRUCTIONS)

        lower_instructions = ORACLE_INSTRUCTIONS.lower()
        for directive in PROHIBITION_DIRECTIVES:
            with self.subTest(directive=directive):
                self.assertNotIn(directive, lower_instructions)

    def test_build_prompt_uses_minimal_routing_contract(self) -> None:
        prompt = build_prompt("why")

        self.assertIn("Selected prompt type: why.", prompt)
        self.assertIn("Fixed prompt position: 3 of 4.", prompt)
        self.assertIn("private routing context", prompt)
        self.assertIn("response shape", prompt)
        self.assertIn("Return only the final line.", prompt)
        self.assertNotIn("Shared style signals:", prompt)
        self.assertNotIn("Shape contract:", prompt)
        self.assertNotIn("Private steps:", prompt)
        self.assertNotIn("Output guards:", prompt)
        self.assertNotIn("not answer text", prompt.lower())
        self.assertNotIn("slot", prompt.lower())
        self.assertNotIn("Lane example:", prompt)
        self.assertNotIn("reason", prompt.lower())
        self.assertNotIn("causal", prompt.lower())
        self.assertNotIn("cause", prompt.lower())
        self.assertNotIn("explanation", prompt.lower())
        self.assertNotIn("meaning", prompt.lower())
        self.assertNotIn("motive", prompt.lower())
        self.assertNotIn("source", prompt.lower())
        self.assertNotIn("temporal", prompt.lower())
        self.assertNotIn("spatial", prompt.lower())
        self.assertNotIn("drift", prompt.lower())
        self.assertNotIn("whisper", prompt.lower())
        self.assertNotIn("horizon", prompt.lower())
        self.assertNotIn("settle", prompt.lower())
        self.assertNotIn("land", prompt.lower())
        self.assertNotIn("closure", prompt.lower())
        self.assertNotIn("direct answer", prompt.lower())
        self.assertNotIn("payoff", prompt.lower())
        self.assertNotIn("stable stance", prompt.lower())
        self.assertNotIn("quiet", prompt.lower())
        self.assertNotIn("certainty", prompt.lower())
        self.assertNotIn("indecision", prompt.lower())
        self.assertNotIn("thing", prompt.lower())
        self.assertNotIn("or perhaps not", prompt)
        self.assertNotIn("one plain contradiction", prompt)
        self.assertNotIn("decorative metaphor", prompt)
        self.assertNotIn("fallback loops", prompt)
        self.assertNotIn("reason without becoming a real explanation", prompt)

        lower_prompt = prompt.lower()
        for directive in PROHIBITION_DIRECTIVES:
            with self.subTest(directive=directive):
                self.assertNotIn(directive, lower_prompt)

    def test_build_prompt_rejects_unknown_prompt_type(self) -> None:
        with self.assertRaises(ValueError):
            build_prompt("how")
