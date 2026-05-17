import contextlib
import importlib.util
import io
import tempfile
import unittest
from pathlib import Path
from unittest import mock

MODULE_PATH = Path(__file__).resolve().parents[1] / "scripts" / "check_end_pending.py"
SPEC = importlib.util.spec_from_file_location("check_end_pending", MODULE_PATH)
assert SPEC is not None and SPEC.loader is not None
check_end_pending = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(check_end_pending)


class CheckEndPendingTests(unittest.TestCase):
    def test_main_passes_when_db_is_missing(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            settings = mock.Mock(eval_db_path=Path(tmpdir) / "evals.sqlite")
            with mock.patch.object(
                check_end_pending, "load_settings", return_value=settings
            ):
                stdout = io.StringIO()
                with contextlib.redirect_stdout(stdout):
                    status = check_end_pending.main()

        self.assertEqual(status, 0)
        self.assertIn("end-pending-check: PASS", stdout.getvalue())

    def test_main_fails_when_pending_rows_exist(self) -> None:
        settings = mock.Mock(eval_db_path=Path("/tmp/evals.sqlite"))
        with mock.patch.object(
            check_end_pending, "load_settings", return_value=settings
        ):
            with mock.patch.object(
                check_end_pending,
                "counts",
                return_value={"total": 12, "pass": 5, "fail": 4, "pending": 3},
            ):
                with mock.patch.object(Path, "exists", return_value=True):
                    stderr = io.StringIO()
                    with contextlib.redirect_stderr(stderr):
                        status = check_end_pending.main()

        self.assertEqual(status, 1)
        self.assertIn("end-pending-check: FAIL", stderr.getvalue())
        self.assertIn("pending=3", stderr.getvalue())


if __name__ == "__main__":
    unittest.main()
