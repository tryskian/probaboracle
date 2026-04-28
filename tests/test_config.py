from unittest import TestCase

from probaboracle.config import (
    PROMPT_TYPES,
    VERDICTS,
    normalise_prompt_type,
    normalise_verdict,
)


class ConfigContractTests(TestCase):
    def test_prompt_types_match_repo_contract(self) -> None:
        self.assertEqual(PROMPT_TYPES, ("what", "when", "why", "where"))

    def test_verdicts_are_binary_only(self) -> None:
        self.assertEqual(VERDICTS, ("pass", "fail"))

    def test_prompt_type_normalisation_rejects_unknown_value(self) -> None:
        with self.assertRaises(ValueError):
            normalise_prompt_type("how")

    def test_verdict_normalisation_rejects_unknown_value(self) -> None:
        with self.assertRaises(ValueError):
            normalise_verdict("mixed")
