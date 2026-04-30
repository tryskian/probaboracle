#!/usr/bin/env bash
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$ROOT_DIR"
TOTAL_STEPS=6

if [ "${EOD_SKIP_GIT_CHECK:-}" = "1" ]; then
	TOTAL_STEPS=5
fi

echo "[eod] starting end-of-day routine in: $ROOT_DIR"
echo "[eod] 1/$TOTAL_STEPS eod-docs-check"
make --no-print-directory eod-docs-check

echo "[eod] 2/$TOTAL_STEPS doctor-env"
make --no-print-directory doctor-env

echo "[eod] 3/$TOTAL_STEPS check"
make --no-print-directory check

echo "[eod] 4/$TOTAL_STEPS package-check"
make --no-print-directory package-check

echo "[eod] 5/$TOTAL_STEPS stop background tasks"
make --no-print-directory eod-stop

if [ "${EOD_SKIP_GIT_CHECK:-}" = "1" ]; then
	echo "[eod] git closeout skipped (preflight only)"
else
	echo "[eod] 6/$TOTAL_STEPS git closeout"
	make --no-print-directory eod-git-check
fi

echo "[eod] done"
