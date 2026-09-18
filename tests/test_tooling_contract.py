from __future__ import annotations

import re
import subprocess
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def read(path: str) -> str:
    return (ROOT / path).read_text()


class ToolingContractTests(unittest.TestCase):
    def assert_make_target(self, makefile: str, target: str) -> None:
        self.assertRegex(makefile, rf"(?m)^{re.escape(target)}:", msg=target)

    def test_makefile_exposes_local_ci_and_closeout_targets(self) -> None:
        makefile = read("Makefile")

        for target in (
            "lint-docs",
            "scripts-check",
            "end-docs-check",
            "package-install-check",
            "python-security-check",
            "node-security-check",
            "security-checks",
        ):
            self.assert_make_target(makefile, target)

    def test_active_end_routine_uses_make_targets(self) -> None:
        script = read("tools/end_of_day_routine.sh")

        for command in (
            "make --no-print-directory end-docs-check",
            "make --no-print-directory lint-docs",
            "make --no-print-directory scripts-check",
            "make --no-print-directory package-check",
            "make --no-print-directory package-install-check",
            "make --no-print-directory security-checks",
        ):
            self.assertIn(command, script)

        self.assertNotIn("npm run lint:docs", script)
        self.assertNotIn("./scripts/check_end_docs.py", script)

    def test_repo_lifecycle_leaves_external_power_control_unchanged(self) -> None:
        makefile = read("Makefile")
        start_script = read("tools/start_of_day_routine.sh")
        end_script = read("tools/end_of_day_routine.sh")

        for target in (
            "caffeinate",
            "caffeinate-status",
            "decaffeinate",
            "decaffeinate-status",
        ):
            self.assertNotRegex(makefile, rf"(?m)^{re.escape(target)}:")

        for forbidden in (
            "CAFFEINATE_PID_FILE",
            "CAFFEINATE_LOG",
            "CAFFEINATE_CMD",
            "make --no-print-directory caffeinate",
            "make --no-print-directory decaffeinate",
        ):
            self.assertNotIn(forbidden, "\n".join((makefile, start_script, end_script)))

        self.assertIn("[start] 1/4 workspace context", start_script)
        self.assertIn("[start] 4/4 REHYDRATE PROMPT", start_script)
        self.assertIn("TOTAL_STEPS=14", end_script)
        self.assertIn("TOTAL_STEPS=13", end_script)
        self.assertIn("[end] 13/$TOTAL_STEPS session snapshot", end_script)
        self.assertIn("[end] 14/$TOTAL_STEPS git closeout", end_script)

        active_docs = "\n".join(
            read(path)
            for path in (
                "README.md",
                "docs/governance/SESSION_HANDOFF.md",
                "docs/runtime/ARCHITECTURE.md",
                "docs/runtime/RUNBOOK.md",
                "docs/runtime/START_END_REFERENCE.md",
            )
        )
        self.assertNotRegex(active_docs, r"(?i)caffeinate|decaffeinate|wake-lock")

    def test_legacy_end_routine_delegates_to_active_tool(self) -> None:
        script = read("scripts/end_of_day_routine.sh")

        self.assertIn('exec "$ROOT_DIR/tools/end_of_day_routine.sh" "$@"', script)
        self.assertNotIn("TOTAL_STEPS", script)

    def test_runtime_docs_name_the_make_targets(self) -> None:
        docs = "\n".join(
            read(path)
            for path in (
                "docs/runtime/RUNBOOK.md",
                "docs/runtime/START_END_REFERENCE.md",
                "docs/governance/DECISIONS.md",
            )
        )

        for command in (
            "make lint-docs",
            "make scripts-check",
            "make package-install-check",
            "make security-checks",
            "make end-docs-check",
        ):
            self.assertIn(command, docs)

    def test_import_sorting_is_owned_by_ruff_not_isort_extension(self) -> None:
        pyproject = read("pyproject.toml")
        doctor = read("src/probaboracle/doctor_env.py")

        self.assertIn('select = ["E", "F", "I", "UP", "B"]', pyproject)
        self.assertIn("ruff check scripts src tests", read("Makefile"))
        self.assertIn("ruff format --check scripts src tests", read("Makefile"))

        self.assertNotIn('"isort', pyproject)
        self.assertNotIn("[tool.isort]", pyproject)
        self.assertNotIn('"isort"', doctor)

    def test_shell_script_contract_checker_accepts_tracked_scripts(self) -> None:
        self.assertTrue((ROOT / "scripts/check_shell_scripts.py").exists())

        result = subprocess.run(
            [sys.executable, "scripts/check_shell_scripts.py"],
            cwd=ROOT,
            check=True,
            capture_output=True,
            text=True,
        )

        self.assertIn("shell-script-contracts: PASS", result.stdout)
        self.assertIn("scripts checked", result.stdout)


if __name__ == "__main__":
    unittest.main()
