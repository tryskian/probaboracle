#!/usr/bin/env bash
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$ROOT_DIR"

echo "[start] starting morning routine in: $ROOT_DIR"
echo "[start] 1/6 workspace context"
printf 'repo root: %s\n' "$ROOT_DIR"
printf 'branch: %s\n' "$(git branch --show-current)"
git status --short --branch

echo "[start] 2/6 doctor-env"
make --no-print-directory doctor-env

echo "[start] 3/6 caffeinate"
make --no-print-directory caffeinate

echo "[start] 4/6 caffeinate-status"
make --no-print-directory caffeinate-status

echo "[start] 5/6 session-status"
make --no-print-directory session-status

echo "[start] 6/6 REHYDRATE PROMPT"
cat <<'EOF'
Read README.md, docs/governance/CHARTER.md, docs/governance/DECISIONS.md, docs/runtime/ARCHITECTURE.md, docs/runtime/RUNBOOK.md, and docs/governance/SESSION_HANDOFF.md.

In 5 bullets: current state, risks, and next kernel.

Before starting implementation, confirm environment/workspace context: canonical repo path is /abs/path/to/probaboracle, confirm host vs devcontainer mode, confirm active git branch, and say whether the thread is on clean main or a feature branch.

Apply no-guessing controls: prefer repo-scoped edits and do not modify user shell profile file or global VS Code settings unless explicitly approved in-chat.

Run in one active kernel at a time.

Then execute the Next Slice from SESSION_HANDOFF with minimal behavior drift and full validation.
EOF
