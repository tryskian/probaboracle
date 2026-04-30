from __future__ import annotations

import argparse
import sqlite3
from typing import Iterable

from probaboracle.agent import generate_response
from probaboracle.config import (
    ensure_local_dirs,
    load_settings,
    normalise_prompt_type,
    normalise_verdict,
    require_openai_api_key,
)
from probaboracle.eval_db import (
    absurdity_counts,
    coherence_counts,
    counts,
    init_db,
    judge_absurdity_output,
    judge_output,
    judge_relevance_output,
    judge_coherence_output,
    list_outputs,
    relevance_counts,
    record_output,
)


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(prog="probaboracle")
    subparsers = parser.add_subparsers(dest="command", required=True)

    ask_parser = subparsers.add_parser("ask", help="Generate one oracle response.")
    ask_parser.add_argument("prompt_type")

    sample_parser = subparsers.add_parser("sample", help="Generate stored eval samples.")
    sample_parser.add_argument("prompt_type")
    sample_parser.add_argument("--count", type=int, default=5)

    subparsers.add_parser("eval-init", help="Initialise the local eval database.")

    list_parser = subparsers.add_parser("eval-list", help="List recent eval outputs.")
    list_parser.add_argument("--prompt-type", default=None)
    list_parser.add_argument("--limit", type=int, default=20)

    judge_parser = subparsers.add_parser(
        "judge",
        aliases=["eval-judge"],
        help="Record a binary verdict.",
    )
    judge_parser.add_argument("output_id", type=int)
    judge_parser.add_argument("verdict")
    judge_parser.add_argument("--note", default="")

    coherence_judge_parser = subparsers.add_parser(
        "judge-coherence",
        aliases=["judge-structure"],
        help="Record a binary coherence verdict.",
    )
    coherence_judge_parser.add_argument("output_id", type=int)
    coherence_judge_parser.add_argument("verdict")
    coherence_judge_parser.add_argument("--note", default="")

    relevance_judge_parser = subparsers.add_parser(
        "judge-relevance",
        help="Record a binary prompt-relevance verdict.",
    )
    relevance_judge_parser.add_argument("output_id", type=int)
    relevance_judge_parser.add_argument("verdict")
    relevance_judge_parser.add_argument("--note", default="")

    absurdity_judge_parser = subparsers.add_parser(
        "judge-absurdity",
        help="Record a binary coherent-absurdity verdict.",
    )
    absurdity_judge_parser.add_argument("output_id", type=int)
    absurdity_judge_parser.add_argument("verdict")
    absurdity_judge_parser.add_argument("--note", default="")

    return parser


def print_rows(rows: Iterable[sqlite3.Row]) -> None:
    print("ID  PROMPT  PRODUCT   COHERENCE  RELEVANCE  ABSURDITY  OUTPUT")
    for row in rows:
        product_verdict = row["current_verdict"] or "pending"
        coherence_verdict = row["structure_current_verdict"] or "pending"
        relevance_verdict = row["relevance_current_verdict"] or "pending"
        absurdity_verdict = row["absurdity_current_verdict"] or "pending"
        print(
            f"{row['id']:>2}  "
            f"{row['prompt_type']:<6}  "
            f"{product_verdict:<8}  "
            f"{coherence_verdict:<10}  "
            f"{relevance_verdict:<9}  "
            f"{absurdity_verdict:<9}  "
            f"{row['output_text']}"
        )


def command_ask(prompt_type: str) -> int:
    settings = load_settings()
    ensure_local_dirs(settings)
    require_openai_api_key()
    response = generate_response(settings, normalise_prompt_type(prompt_type))
    print(response)
    return 0


def command_sample(prompt_type: str, count: int) -> int:
    settings = load_settings()
    ensure_local_dirs(settings)
    require_openai_api_key()
    prompt_type = normalise_prompt_type(prompt_type)
    init_db(settings.eval_db_path)
    for _ in range(count):
        response = generate_response(settings, prompt_type)
        output_id = record_output(settings.eval_db_path, prompt_type, response, settings.model)
        print(f"{output_id}\t{response}")
    return 0


def command_eval_init() -> int:
    settings = load_settings()
    ensure_local_dirs(settings)
    init_db(settings.eval_db_path)
    print(f"Initialised {settings.eval_db_path}")
    return 0


def command_eval_list(prompt_type: str | None, limit: int) -> int:
    settings = load_settings()
    ensure_local_dirs(settings)
    if prompt_type is not None:
        prompt_type = normalise_prompt_type(prompt_type)
    rows = list_outputs(settings.eval_db_path, prompt_type=prompt_type, limit=limit)
    print_rows(rows)
    product_summary = counts(settings.eval_db_path)
    coherence_summary = coherence_counts(settings.eval_db_path)
    relevance_summary = relevance_counts(settings.eval_db_path)
    absurdity_summary = absurdity_counts(settings.eval_db_path)
    print(
        "\n"
        f"product total={product_summary['total']} "
        f"pass={product_summary['pass']} "
        f"fail={product_summary['fail']} "
        f"pending={product_summary['pending']}"
    )
    print(
        f"coherence total={coherence_summary['total']} "
        f"pass={coherence_summary['pass']} "
        f"fail={coherence_summary['fail']} "
        f"pending={coherence_summary['pending']}"
    )
    print(
        f"relevance total={relevance_summary['total']} "
        f"pass={relevance_summary['pass']} "
        f"fail={relevance_summary['fail']} "
        f"pending={relevance_summary['pending']}"
    )
    print(
        f"absurdity total={absurdity_summary['total']} "
        f"pass={absurdity_summary['pass']} "
        f"fail={absurdity_summary['fail']} "
        f"pending={absurdity_summary['pending']}"
    )
    print("\nPRODUCT VERDICT: PASS | FAIL [note]")
    print('Example: make judge ID=12 VERDICT=pass NOTE="deadpan and vague"')
    print("\nCOHERENCE VERDICT: PASS | FAIL [note]")
    print('Example: .venv/bin/python -m probaboracle judge-coherence 12 pass --note "coherent sentence"')
    print("\nPROMPT RELEVANCE VERDICT: PASS | FAIL [note]")
    print('Example: .venv/bin/python -m probaboracle judge-relevance 12 pass --note "coherent and in-lane"')
    print("\nCOHERENT ABSURDITY VERDICT: PASS | FAIL [note]")
    print('Example: .venv/bin/python -m probaboracle judge-absurdity 12 pass --note "coherent absurdity"')
    return 0


def command_eval_judge(output_id: int, verdict: str, note: str) -> int:
    settings = load_settings()
    ensure_local_dirs(settings)
    init_db(settings.eval_db_path)
    verdict = normalise_verdict(verdict)
    judge_output(settings.eval_db_path, output_id, verdict, note)
    print(f"Judged output {output_id} as {verdict}.")
    return 0


def command_coherence_judge(output_id: int, verdict: str, note: str) -> int:
    settings = load_settings()
    ensure_local_dirs(settings)
    init_db(settings.eval_db_path)
    verdict = normalise_verdict(verdict)
    judge_coherence_output(settings.eval_db_path, output_id, verdict, note)
    print(f"Judged output {output_id} for coherence as {verdict}.")
    return 0


def command_relevance_judge(output_id: int, verdict: str, note: str) -> int:
    settings = load_settings()
    ensure_local_dirs(settings)
    init_db(settings.eval_db_path)
    verdict = normalise_verdict(verdict)
    judge_relevance_output(settings.eval_db_path, output_id, verdict, note)
    print(f"Judged output {output_id} for prompt relevance as {verdict}.")
    return 0


def command_absurdity_judge(output_id: int, verdict: str, note: str) -> int:
    settings = load_settings()
    ensure_local_dirs(settings)
    init_db(settings.eval_db_path)
    verdict = normalise_verdict(verdict)
    judge_absurdity_output(settings.eval_db_path, output_id, verdict, note)
    print(f"Judged output {output_id} for absurdity as {verdict}.")
    return 0


def main(argv: list[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)

    if args.command == "ask":
        return command_ask(args.prompt_type)
    if args.command == "sample":
        return command_sample(args.prompt_type, args.count)
    if args.command == "eval-init":
        return command_eval_init()
    if args.command == "eval-list":
        return command_eval_list(args.prompt_type, args.limit)
    if args.command in {"judge", "eval-judge"}:
        return command_eval_judge(args.output_id, args.verdict, args.note)
    if args.command in {"judge-coherence", "judge-structure"}:
        return command_coherence_judge(args.output_id, args.verdict, args.note)
    if args.command == "judge-relevance":
        return command_relevance_judge(args.output_id, args.verdict, args.note)
    if args.command == "judge-absurdity":
        return command_absurdity_judge(args.output_id, args.verdict, args.note)

    parser.error("Unknown command.")
    return 2
