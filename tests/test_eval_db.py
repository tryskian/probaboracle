from pathlib import Path
from tempfile import TemporaryDirectory
from unittest import TestCase

from probaboracle.eval_db import (
    absurdity_counts,
    coherence_counts,
    counts,
    handwaving_counts,
    init_db,
    judge_absurdity_output,
    judge_output,
    judge_handwaving_output,
    judge_relevance_output,
    judge_structure_output,
    list_outputs,
    relevance_counts,
    record_output,
    structure_counts,
)


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
            self.assertEqual(rows[0]["structure_current_verdict"], None)
            self.assertEqual(rows[0]["structure_current_note"], "")
            self.assertEqual(rows[0]["relevance_current_verdict"], None)
            self.assertEqual(rows[0]["relevance_current_note"], "")
            self.assertEqual(rows[0]["absurdity_current_verdict"], None)
            self.assertEqual(rows[0]["absurdity_current_note"], "")
            self.assertEqual(rows[0]["handwaving_current_verdict"], None)
            self.assertEqual(rows[0]["handwaving_current_note"], "")

            summary = counts(db_path)
            self.assertEqual(summary["total"], 1)
            self.assertEqual(summary["pass"], 1)
            self.assertEqual(summary["fail"], 0)
            self.assertEqual(summary["pending"], 0)

            structure_summary = structure_counts(db_path)
            self.assertEqual(structure_summary["total"], 1)
            self.assertEqual(structure_summary["pass"], 0)
            self.assertEqual(structure_summary["fail"], 0)
            self.assertEqual(structure_summary["pending"], 1)

            relevance_summary = relevance_counts(db_path)
            self.assertEqual(relevance_summary["total"], 1)
            self.assertEqual(relevance_summary["pass"], 0)
            self.assertEqual(relevance_summary["fail"], 0)
            self.assertEqual(relevance_summary["pending"], 1)

            absurdity_summary = absurdity_counts(db_path)
            self.assertEqual(absurdity_summary["total"], 1)
            self.assertEqual(absurdity_summary["pass"], 0)
            self.assertEqual(absurdity_summary["fail"], 0)
            self.assertEqual(absurdity_summary["pending"], 1)

            handwaving_summary = handwaving_counts(db_path)
            self.assertEqual(handwaving_summary["total"], 1)
            self.assertEqual(handwaving_summary["pass"], 0)
            self.assertEqual(handwaving_summary["fail"], 0)
            self.assertEqual(handwaving_summary["pending"], 1)

    def test_structure_judgment_round_trip_is_separate_from_product_verdict(self) -> None:
        with TemporaryDirectory() as tmpdir:
            db_path = Path(tmpdir) / "evals.sqlite"
            init_db(db_path)

            output_id = record_output(
                db_path=db_path,
                prompt_type="why",
                output_text="probably a reason, or something adjacent to one.",
                model="gpt-5-nano",
            )
            judge_structure_output(db_path, output_id, "pass", "coherent sentence")

            rows = list_outputs(db_path, prompt_type="why", limit=5)
            self.assertEqual(len(rows), 1)
            self.assertEqual(rows[0]["current_verdict"], None)
            self.assertEqual(rows[0]["current_note"], "")
            self.assertEqual(rows[0]["structure_current_verdict"], "pass")
            self.assertEqual(rows[0]["structure_current_note"], "coherent sentence")
            self.assertEqual(rows[0]["relevance_current_verdict"], None)
            self.assertEqual(rows[0]["relevance_current_note"], "")
            self.assertEqual(rows[0]["absurdity_current_verdict"], None)
            self.assertEqual(rows[0]["handwaving_current_verdict"], None)

            product_summary = counts(db_path)
            self.assertEqual(product_summary["pending"], 1)

            coherence_summary = coherence_counts(db_path)
            self.assertEqual(coherence_summary["pass"], 1)
            self.assertEqual(coherence_summary["fail"], 0)
            self.assertEqual(coherence_summary["pending"], 0)

            relevance_summary = relevance_counts(db_path)
            self.assertEqual(relevance_summary["pass"], 0)
            self.assertEqual(relevance_summary["fail"], 0)
            self.assertEqual(relevance_summary["pending"], 1)

            absurdity_summary = absurdity_counts(db_path)
            self.assertEqual(absurdity_summary["pending"], 1)

            handwaving_summary = handwaving_counts(db_path)
            self.assertEqual(handwaving_summary["pending"], 1)

    def test_relevance_judgment_round_trip_is_separate_from_other_verdicts(self) -> None:
        with TemporaryDirectory() as tmpdir:
            db_path = Path(tmpdir) / "evals.sqlite"
            init_db(db_path)

            output_id = record_output(
                db_path=db_path,
                prompt_type="when",
                output_text="technically a moment, though not one you could schedule.",
                model="gpt-5-nano",
            )
            judge_relevance_output(db_path, output_id, "pass", "coherent and in-lane")

            rows = list_outputs(db_path, prompt_type="when", limit=5)
            self.assertEqual(len(rows), 1)
            self.assertEqual(rows[0]["current_verdict"], None)
            self.assertEqual(rows[0]["structure_current_verdict"], None)
            self.assertEqual(rows[0]["relevance_current_verdict"], "pass")
            self.assertEqual(rows[0]["relevance_current_note"], "coherent and in-lane")
            self.assertEqual(rows[0]["absurdity_current_verdict"], None)
            self.assertEqual(rows[0]["handwaving_current_verdict"], None)

            product_summary = counts(db_path)
            self.assertEqual(product_summary["pending"], 1)

            coherence_summary = coherence_counts(db_path)
            self.assertEqual(coherence_summary["pending"], 1)

            relevance_summary = relevance_counts(db_path)
            self.assertEqual(relevance_summary["pass"], 1)
            self.assertEqual(relevance_summary["fail"], 0)
            self.assertEqual(relevance_summary["pending"], 0)

            absurdity_summary = absurdity_counts(db_path)
            self.assertEqual(absurdity_summary["pending"], 1)

            handwaving_summary = handwaving_counts(db_path)
            self.assertEqual(handwaving_summary["pending"], 1)

    def test_absurdity_and_handwaving_round_trip_stay_separate(self) -> None:
        with TemporaryDirectory() as tmpdir:
            db_path = Path(tmpdir) / "evals.sqlite"
            init_db(db_path)

            output_id = record_output(
                db_path=db_path,
                prompt_type="where",
                output_text="definitely a moment elsewhere, or perhaps not, that settles nothing.",
                model="gpt-5-nano",
            )
            judge_absurdity_output(db_path, output_id, "pass", "coherent absurdity")
            judge_handwaving_output(
                db_path,
                output_id,
                "pass",
                "answer-shaped handwaving",
            )

            rows = list_outputs(db_path, prompt_type="where", limit=5)
            self.assertEqual(len(rows), 1)
            self.assertEqual(rows[0]["current_verdict"], None)
            self.assertEqual(rows[0]["structure_current_verdict"], None)
            self.assertEqual(rows[0]["relevance_current_verdict"], None)
            self.assertEqual(rows[0]["absurdity_current_verdict"], "pass")
            self.assertEqual(rows[0]["absurdity_current_note"], "coherent absurdity")
            self.assertEqual(rows[0]["handwaving_current_verdict"], "pass")
            self.assertEqual(
                rows[0]["handwaving_current_note"],
                "answer-shaped handwaving",
            )

            absurdity_summary = absurdity_counts(db_path)
            self.assertEqual(absurdity_summary["pass"], 1)
            self.assertEqual(absurdity_summary["fail"], 0)
            self.assertEqual(absurdity_summary["pending"], 0)

            handwaving_summary = handwaving_counts(db_path)
            self.assertEqual(handwaving_summary["pass"], 1)
            self.assertEqual(handwaving_summary["fail"], 0)
            self.assertEqual(handwaving_summary["pending"], 0)
