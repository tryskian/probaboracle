import os
from pathlib import Path
from tempfile import TemporaryDirectory
from unittest import TestCase
from unittest.mock import patch

import probaboracle.config as config
from probaboracle.config import (
    PROMPT_TYPES,
    VERDICTS,
    load_settings,
    normalise_prompt_type,
    normalise_verdict,
)


class ConfigContractTests(TestCase):
    def test_prompt_types_match_repo_contract(self) -> None:
        self.assertEqual(PROMPT_TYPES, ("what", "when", "why", "where"))

    def test_verdicts_are_binary_only(self) -> None:
        self.assertEqual(VERDICTS, ("pass", "fail"))

    def test_config_stays_structural_without_prompt_phrase_banks(self) -> None:
        removed_prompt_bank_names = (
            "PROMPT_FRAMES",
            "LANE_GUARDS",
            "TONE_CONTRACT",
            "PIPELINE_STEPS",
            "STYLE_SIGNALS",
            "OUTPUT_GUARDS",
        )

        for name in removed_prompt_bank_names:
            with self.subTest(name=name):
                self.assertFalse(hasattr(config, name))

    def test_prompt_type_normalisation_rejects_unknown_value(self) -> None:
        with self.assertRaises(ValueError):
            normalise_prompt_type("how")

    def test_verdict_normalisation_rejects_unknown_value(self) -> None:
        with self.assertRaises(ValueError):
            normalise_verdict("mixed")

    def test_load_settings_bootstraps_repo_dotenv(self) -> None:
        with TemporaryDirectory() as tmpdir:
            root = Path(tmpdir)
            (root / ".env").write_text(
                "PROBABORACLE_MODEL=test-model\nOPENAI_API_KEY=test-key\n",
                encoding="utf-8",
            )
            with patch.dict(os.environ, {}, clear=True):
                with patch("probaboracle.config.ROOT", root):
                    settings = load_settings()
                    self.assertEqual(settings.model, "test-model")
                    self.assertEqual(os.environ.get("OPENAI_API_KEY"), "test-key")
