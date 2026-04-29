from unittest import TestCase

from probaboracle.agent import normalise_response_text


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
