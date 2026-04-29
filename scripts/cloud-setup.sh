#!/usr/bin/env bash
set -euo pipefail

current_branch="$(git branch --show-current || true)"

if [ -z "${current_branch}" ] || [ "${current_branch}" = "main" ]; then
  branch_name="codex/bigbrain/cloud-setup-$(date +%Y%m%d-%H%M%S)"
  git checkout -b "${branch_name}"
fi

make install
.venv/bin/python -m probaboracle eval-init
