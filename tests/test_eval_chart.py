from pathlib import Path
from tempfile import TemporaryDirectory
from unittest import TestCase

from probaboracle.eval_chart import build_eval_chart_payload
from probaboracle.eval_db import init_db, judge_output, record_output


class EvalChartTests(TestCase):
    def test_build_eval_chart_payload_groups_counts_by_lane_and_verdict(self) -> None:
        with TemporaryDirectory() as tmpdir:
            db_path = Path(tmpdir) / "evals.sqlite"
            init_db(db_path)

            what_id = record_output(
                db_path=db_path,
                prompt_type="what",
                output_text="apparently something of that sort",
                model="gpt-5-nano",
            )
            when_id = record_output(
                db_path=db_path,
                prompt_type="when",
                output_text="probably a moment, more or less",
                model="gpt-5-nano",
            )
            record_output(
                db_path=db_path,
                prompt_type="when",
                output_text="technically around then",
                model="gpt-5-nano",
            )

            judge_output(db_path, what_id, "pass", "keeper")
            judge_output(db_path, when_id, "fail", "too clear")

            payload = build_eval_chart_payload(db_path)

            self.assertEqual(payload["summary"]["total"], 3)
            self.assertEqual(payload["summary"]["pass"], 1)
            self.assertEqual(payload["summary"]["fail"], 1)
            self.assertEqual(payload["summary"]["pending"], 1)

            lanes = {lane["prompt_type"]: lane for lane in payload["lanes"]}
            self.assertEqual(lanes["what"]["counts"], {"fail": 0, "pass": 1, "pending": 0})
            self.assertEqual(lanes["when"]["counts"], {"fail": 1, "pass": 0, "pending": 1})
            self.assertEqual(lanes["why"]["counts"], {"fail": 0, "pass": 0, "pending": 0})
