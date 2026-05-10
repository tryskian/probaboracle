#!/usr/bin/env bash
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$ROOT_DIR"

echo "[end] starting closeout routine in: $ROOT_DIR"

echo "[end] 1/5 doctor-env"
make --no-print-directory doctor-env

echo "[end] 2/5 lint:docs"
npm run lint:docs

echo "[end] 3/5 check"
make --no-print-directory check

echo "[end] 4/5 git diff --check"
git diff --check

echo "[end] 5/5 stop background tasks"
make --no-print-directory end-stop

echo "[end] done"
