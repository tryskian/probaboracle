from __future__ import annotations

import sys

from probaboracle.config import load_settings
from probaboracle.eval_db import counts, pending_debt_counts


def main() -> int:
    settings = load_settings()
    if not settings.eval_db_path.exists():
        print(
            "end-pending-check: PASS "
            f"(no eval db at {settings.eval_db_path}; pending=0)"
        )
        return 0

    summary = counts(settings.eval_db_path)
    debt = pending_debt_counts(settings.eval_db_path)
    if debt["unlabeled_product_pending"] != 0:
        print("end-pending-check: FAIL", file=sys.stderr)
        print(
            f"- unlabeled product-pending count is {debt['unlabeled_product_pending']}",
            file=sys.stderr,
        )
        print(
            "- pulse-labeled pending rows are allowed here: "
            f"{debt['pulse_labeled_pending']}",
            file=sys.stderr,
        )
        print(
            f"- totals: total={summary['total']} pass={summary['pass']} "
            f"fail={summary['fail']} pending={summary['pending']}",
            file=sys.stderr,
        )
        print(
            "Judge, pulse-label, or archive stale product-pending rows before "
            "rerunning make end.",
            file=sys.stderr,
        )
        return 1

    print(
        "end-pending-check: PASS "
        f"(total={summary['total']} pass={summary['pass']} "
        f"fail={summary['fail']} pending={summary['pending']} "
        f"pulse_labeled_pending={debt['pulse_labeled_pending']})"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
