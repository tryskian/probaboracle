from __future__ import annotations

import importlib.util
import os
import shutil
import subprocess
import sys
from pathlib import Path

from dotenv import load_dotenv

from probaboracle.config import load_settings

ROOT = Path(__file__).resolve().parents[2]
EXPECTED_VENV = ROOT / ".venv"
EXPECTED_PYTHON = EXPECTED_VENV / "bin" / "python"


def _ok(message: str) -> None:
    print(f"[ok]   {message}")


def _warn(message: str) -> None:
    print(f"[warn] {message}")


def _is_runnable_python(path: Path) -> bool:
    if not path.exists():
        return False
    try:
        proc = subprocess.run(
            [str(path), "-V"],
            capture_output=True,
            text=True,
            check=False,
        )
    except OSError:
        return False
    return proc.returncode == 0


def _check_interpreter() -> int:
    issues = 0
    current_raw = Path(sys.executable)
    current = current_raw.resolve()

    if _is_runnable_python(EXPECTED_PYTHON):
        expected = EXPECTED_PYTHON.resolve()
        if current == expected:
            _ok(f"Interpreter: {current_raw} (resolved: {current})")
        else:
            issues += 1
            _warn(f"Interpreter mismatch: {current_raw} (resolved: {current})")
            _warn(f"Expected: {EXPECTED_PYTHON} (resolved: {expected})")
            _warn("Use: source .venv/bin/activate")
    else:
        issues += 1
        _warn(f"Missing runnable project interpreter: {EXPECTED_PYTHON}")
        _warn("Run: make install")

    active_venv = os.environ.get("VIRTUAL_ENV")
    if active_venv:
        _ok(f"VIRTUAL_ENV={active_venv}")
    else:
        _warn("VIRTUAL_ENV is not set (ok when running via make with explicit interpreter)")

    python_on_path = shutil.which("python")
    if python_on_path:
        _ok(f"python on PATH: {python_on_path}")
    else:
        _warn("`python` is not on PATH")

    return issues


def _check_imports() -> int:
    issues = 0
    required_modules = [
        "agents",
        "openai",
        "dotenv",
        "pandas",
        "mypy",
    ]
    for name in required_modules:
        if importlib.util.find_spec(name) is None:
            issues += 1
            _warn(f"Missing module: {name}")
        else:
            _ok(f"Import available: {name}")
    return issues


def _check_runtime_settings() -> int:
    issues = 0
    load_dotenv(ROOT / ".env", override=False)
    settings = load_settings()
    _ok(f"Model: {settings.model}")
    _ok(f"Eval DB path: {settings.eval_db_path}")

    if os.getenv("OPENAI_API_KEY"):
        _ok("OPENAI_API_KEY is set")
    else:
        issues += 1
        _warn("OPENAI_API_KEY is not set")

    env_file = ROOT / ".env"
    if env_file.exists():
        _ok(f".env present: {env_file}")
    else:
        _warn(f".env not found at {env_file}")

    return issues


def main() -> int:
    print("Probaboracle environment doctor")
    print(f"Repo root: {ROOT}")

    issues = 0
    issues += _check_interpreter()
    issues += _check_imports()
    issues += _check_runtime_settings()

    if issues:
        print(f"\nFound {issues} issue(s).")
        return 1

    print("\nEnvironment looks healthy.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
