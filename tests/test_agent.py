from unittest import TestCase

from probaboracle.agent import normalise_response_text


class AgentOutputNormalisationTests(TestCase):
    def test_normalise_response_text_compacts_whitespace(self) -> None:
        self.assertEqual(
            normalise_response_text("  Perhaps   a reason,\n or perhaps not.  "),
            "Perhaps a reason, or perhaps not.",
        )

    def test_normalise_response_text_capitalises_first_letter(self) -> None:
        self.assertEqual(
            normalise_response_text("probably a reason, or perhaps not."),
            "Probably a reason, or perhaps not.",
        )
