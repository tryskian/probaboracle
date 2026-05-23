from unittest import TestCase

from probaboracle.agent import (
    ORACLE_INSTRUCTIONS,
    build_prompt,
    normalise_response_text,
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
        self.assertNotIn("Vary the opener across signals like", ORACLE_INSTRUCTIONS)
        self.assertNotIn("Good lane examples:", ORACLE_INSTRUCTIONS)
        self.assertNotIn("Bad lane examples:", ORACLE_INSTRUCTIONS)
        self.assertNotIn("Sound like a contradiction", ORACLE_INSTRUCTIONS)
        self.assertNotIn("Prefer clean contradiction", ORACLE_INSTRUCTIONS)
        self.assertNotIn("reasoning lane", ORACLE_INSTRUCTIONS)
        self.assertNotIn("flavour pool", ORACLE_INSTRUCTIONS)

    def test_build_prompt_uses_shape_contract_without_lane_examples(self) -> None:
        prompt = build_prompt("why")

        self.assertIn("Shared style signals:", prompt)
        self.assertIn("compact", prompt)
        self.assertIn("slot c", prompt)
        self.assertIn("choose one plain sentence claim", prompt)
        self.assertIn("make grammar carry the answer shape", prompt)
        self.assertIn("prefer one clear subject and finite verb", prompt)
        self.assertIn("keep imagery secondary to the sentence claim", prompt)
        self.assertIn("vary sentence openings across samples", prompt)
        self.assertNotIn("Lane example:", prompt)
        self.assertNotIn("Selected prompt type:", prompt)
        self.assertNotIn("why", prompt.lower())
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
