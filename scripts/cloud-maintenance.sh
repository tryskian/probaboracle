#!/usr/bin/env bash
set -euo pipefail

make doctor-env
make session-status
make check

