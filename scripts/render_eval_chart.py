from __future__ import annotations

import argparse
import json
import subprocess
from pathlib import Path
from tempfile import TemporaryDirectory

from probaboracle.config import load_settings
from probaboracle.eval_chart import build_eval_chart_payload

REPO_ROOT = Path(__file__).resolve().parents[1]
NODE_RENDERER = REPO_ROOT / "scripts" / "render_eval_chart.mjs"
DEFAULT_OUTPUT = REPO_ROOT / "docs" / "diagrams" / "probaboracle-pass-fail.svg"


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Render the static Probaboracle pass/fail/pending chart."
    )
    parser.add_argument(
        "--db",
        type=Path,
        default=None,
        help="Override the eval sqlite path. Defaults to the configured local db.",
    )
    parser.add_argument(
        "--output",
        type=Path,
        default=DEFAULT_OUTPUT,
        help="Output SVG path.",
    )
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    settings = load_settings()
    db_path = args.db or settings.eval_db_path
    output_path = args.output.resolve()

    if not db_path.exists():
        raise FileNotFoundError(
            f"Eval database not found at {db_path}. Run make eval-init first."
        )
    if not NODE_RENDERER.exists():
        raise FileNotFoundError(f"D3 renderer not found: {NODE_RENDERER}")

    payload = build_eval_chart_payload(db_path)

    output_path.parent.mkdir(parents=True, exist_ok=True)
    with TemporaryDirectory() as tmpdir:
        payload_path = Path(tmpdir) / "eval_chart_payload.json"
        payload_path.write_text(json.dumps(payload, indent=2), encoding="utf-8")
        subprocess.run(
            ["node", str(NODE_RENDERER), str(payload_path), str(output_path)],
            check=True,
            cwd=REPO_ROOT,
        )

    print(f"Rendered Probaboracle eval chart to {output_path}")


if __name__ == "__main__":
    main()
