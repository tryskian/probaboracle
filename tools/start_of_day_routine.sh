#!/usr/bin/env bash
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$ROOT_DIR"

echo "[start] starting morning routine in: $ROOT_DIR"
echo "[start] 1/4 workspace context"
printf 'repo root: %s\n' "$ROOT_DIR"
printf 'branch: %s\n' "$(git branch --show-current)"
git status --short --branch

echo "[start] 2/4 doctor-env"
make --no-print-directory doctor-env

echo "[start] 3/4 session-status"
make --no-print-directory session-status

echo "[start] 4/4 STOP"
echo "[start] read these docs:"
echo "  - README.md"
echo "  - docs/governance/CHARTER.md"
echo "  - docs/governance/DECISIONS.md"
echo "  - docs/runtime/ARCHITECTURE.md"
echo "  - docs/runtime/RUNBOOK.md"
echo "  - docs/governance/SESSION_HANDOFF.md"
echo "[start] before any repo action:"
echo "  1. give the startup read"
echo "  2. name exactly one active kernel"
echo "  3. do not branch, search, or edit until that is stated"
