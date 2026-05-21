from __future__ import annotations

import re
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
            "make --no-print-directory package-check",
            "make --no-print-directory package-install-check",
            "make --no-print-directory security-checks",
        ):
            self.assertIn(command, script)

        self.assertNotIn("npm run lint:docs", script)
        self.assertNotIn("./scripts/check_end_docs.py", script)

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
            "make package-install-check",
            "make security-checks",
            "make end-docs-check",
        ):
            self.assertIn(command, docs)


if __name__ == "__main__":
    unittest.main()
