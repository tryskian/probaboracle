from pathlib import Path
from tempfile import TemporaryDirectory
from unittest import TestCase

from probaboracle.eval_db import counts, init_db, judge_output, list_outputs, record_output


class EvalDbTests(TestCase):
    def test_round_trip_output_and_judgment(self) -> None:
        with TemporaryDirectory() as tmpdir:
            db_path = Path(tmpdir) / "evals.sqlite"
            init_db(db_path)

            output_id = record_output(
                db_path=db_path,
                prompt_type="what",
                output_text="Apparently the answer remains indistinct.",
                model="gpt-4.1",
            )
            judge_output(db_path, output_id, "pass", "deadpan and vague")

            rows = list_outputs(db_path, prompt_type="what", limit=5)
            self.assertEqual(len(rows), 1)
            self.assertEqual(rows[0]["current_verdict"], "pass")
            self.assertEqual(rows[0]["current_note"], "deadpan and vague")

            summary = counts(db_path)
            self.assertEqual(summary["total"], 1)
            self.assertEqual(summary["pass"], 1)
            self.assertEqual(summary["fail"], 0)
            self.assertEqual(summary["pending"], 0)
