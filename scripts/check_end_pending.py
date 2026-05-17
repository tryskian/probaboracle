from __future__ import annotations

import sys

from probaboracle.config import load_settings
from probaboracle.eval_db import counts


def main() -> int:
    settings = load_settings()
    if not settings.eval_db_path.exists():
        print(
            "end-pending-check: PASS "
            f"(no eval db at {settings.eval_db_path}; pending=0)"
        )
        return 0

    summary = counts(settings.eval_db_path)
    if summary["pending"] != 0:
        print("end-pending-check: FAIL", file=sys.stderr)
        print(
            f"- active product pending count is {summary['pending']}", file=sys.stderr
        )
        print(
            f"- totals: total={summary['total']} pass={summary['pass']} "
            f"fail={summary['fail']} pending={summary['pending']}",
            file=sys.stderr,
        )
        print(
            "Judge or archive stale product-pending rows before rerunning make end.",
            file=sys.stderr,
        )
        return 1

    print(
        "end-pending-check: PASS "
        f"(total={summary['total']} pass={summary['pass']} "
        f"fail={summary['fail']} pending={summary['pending']})"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
