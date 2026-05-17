from unittest import TestCase

from probaboracle.agent import (
    ORACLE_INSTRUCTIONS,
    build_prompt,
    normalise_response_text,
)


class AgentOutputNormalisationTests(TestCase):
    def test_normalise_response_text_compacts_whitespace(self) -> None:
        self.assertEqual(
            normalise_response_text("  Perhaps   a reason,\n or perhaps not.  "),
            "perhaps a reason, or perhaps not.",
        )

    def test_normalise_response_text_lowercases_the_line(self) -> None:
        self.assertEqual(
            normalise_response_text("Probably a reason, or Perhaps Not."),
            "probably a reason, or perhaps not.",
        )


class AgentPromptContractTests(TestCase):
    def test_oracle_instructions_do_not_embed_stock_phrase_lists_or_examples(
        self,
    ) -> None:
        self.assertNotIn("Vary the opener across signals like", ORACLE_INSTRUCTIONS)
        self.assertNotIn("Good lane examples:", ORACLE_INSTRUCTIONS)
        self.assertNotIn("Bad lane examples:", ORACLE_INSTRUCTIONS)

    def test_build_prompt_uses_shape_contract_without_lane_examples(self) -> None:
        prompt = build_prompt("why")

        self.assertIn("Shared style signals:", prompt)
        self.assertIn("certainty without commitment", prompt)
        self.assertNotIn("Lane example:", prompt)
        self.assertNotIn("or perhaps not", prompt)
