from __future__ import annotations

import argparse
import shutil
import sqlite3
import sys
import termios
import threading
import time
import tty
from typing import Callable, Iterable, TextIO

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

APP_BANNER_INNER_WIDTH = 62
APP_BANNER_TITLE = "PROBABORACLE BETA 4.1"
APP_BANNER_TAGLINE = "probably a mini oracle. definitely a mini chatbot."
APP_BANNER_REPO = "github.com/tryskian/probaboracle"
APP_BANNER_REPO_URL = "https://github.com/tryskian/probaboracle"
APP_BANNER_BOX_WIDTH = APP_BANNER_INNER_WIDTH + 2
APP_BANNER_STACKED_WIDTH = len(APP_BANNER_TAGLINE)
APP_BANNER_MINIMAL_WIDTH = len(APP_BANNER_REPO)
APP_BANNER_MINIMAL_TITLE = "probaboracle beta 4.1"
APP_BANNER_MINIMAL_TAGLINE_LINES: tuple[str, ...] = (
    "probably a mini oracle.",
    "definitely a mini chatbot.",
)

APP_DIVIDER = "────────────"
APP_QUESTION_PROMPT = "⊹˙⋆ ask probaboracle [arrow keys]:"
APP_QUESTION_PROMPT_FALLBACK = "⊹˙⋆ ask probaboracle:"
APP_QUESTION_OPTIONS: tuple[tuple[str, str], ...] = (
    ("1", "where"),
    ("2", "what"),
    ("3", "why"),
    ("4", "when"),
)
APP_SELECTOR_BOTTOM_PADDING_LINES = 1
APP_CONTINUE_PROMPT = "another question [y/n]?"
APP_RESPONSE_PREFIX = "⊹˙⋆ "
APP_RESPONSE_SUFFIX = " ⋆˙⊹"
APP_CONTINUE_DELAY_SECONDS = 0.25
APP_POST_RESPONSE_BEATS: tuple[float, ...] = (0.6, 0.35, 1.25)
ANSI_RESET = "\x1b[0m"
ANSI_BOLD = "\x1b[1m"
ANSI_MUTED = "\x1b[38;5;245m"
ANSI_CURSOR_HIDE = "\x1b[?25l"
ANSI_CURSOR_SHOW = "\x1b[?25h"

def build_banner_lines(style_active: bool = False) -> tuple[str, ...]:
    def hyperlink(text: str, url: str) -> str:
        return f"\033]8;;{url}\033\\{text}\033]8;;\033\\"

    def boxed(text: str = "", *, link_url: str | None = None) -> str:
        if link_url is None or not style_active:
            return f"│{text.center(APP_BANNER_INNER_WIDTH)}│"

        left_padding = max(0, (APP_BANNER_INNER_WIDTH - len(text)) // 2)
        right_padding = max(0, APP_BANNER_INNER_WIDTH - len(text) - left_padding)
        return (
            f"│"
            f"{' ' * left_padding}"
            f"{hyperlink(text, link_url)}"
            f"{' ' * right_padding}"
            f"│"
        )

    return (
        f"┌{'─' * APP_BANNER_INNER_WIDTH}┐",
        boxed(APP_BANNER_TITLE),
        boxed(APP_BANNER_TAGLINE),
        boxed(),
        boxed(APP_BANNER_REPO, link_url=APP_BANNER_REPO_URL),
        f"└{'─' * APP_BANNER_INNER_WIDTH}┘",
    )


def build_stacked_banner_lines(style_active: bool = False) -> tuple[str, ...]:
    repo_line = APP_BANNER_REPO
    if style_active:
        repo_line = f"\033]8;;{APP_BANNER_REPO_URL}\033\\{APP_BANNER_REPO}\033]8;;\033\\"
    return (
        APP_BANNER_TITLE,
        APP_BANNER_TAGLINE,
        repo_line,
    )


def build_minimal_banner_lines(style_active: bool = False) -> tuple[str, ...]:
    lines = [APP_BANNER_MINIMAL_TITLE, *APP_BANNER_MINIMAL_TAGLINE_LINES]
    if style_active:
        repo_line = f"\033]8;;{APP_BANNER_REPO_URL}\033\\{APP_BANNER_REPO}\033]8;;\033\\"
    else:
        repo_line = APP_BANNER_REPO
    lines.append(repo_line)
    return tuple(lines)


def choose_banner_lines(
    terminal_width: int | None,
    style_active: bool = False,
) -> tuple[str, ...]:
    if terminal_width is None or terminal_width >= APP_BANNER_BOX_WIDTH:
        return build_banner_lines(style_active=style_active)
    if terminal_width >= APP_BANNER_STACKED_WIDTH:
        return build_stacked_banner_lines(style_active=style_active)
    if terminal_width >= APP_BANNER_MINIMAL_WIDTH:
        return build_minimal_banner_lines(style_active=style_active)
    return (
        APP_BANNER_MINIMAL_TITLE,
        *APP_BANNER_MINIMAL_TAGLINE_LINES,
    )


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(prog="probaboracle")
    subparsers = parser.add_subparsers(dest="command", required=False)

    subparsers.add_parser("app", help="Open the interactive oracle app.")

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


def print_app_header(output_fn: Callable[[str], None] = print) -> None:
    style_active = hasattr(sys.stdout, "isatty") and sys.stdout.isatty()
    terminal_width: int | None = None
    if style_active:
        terminal_width = shutil.get_terminal_size(fallback=(APP_BANNER_BOX_WIDTH, 24)).columns
    for line in choose_banner_lines(terminal_width, style_active=style_active):
        output_fn(line)
    output_fn("")


def format_app_response(response: str) -> str:
    return f"{APP_RESPONSE_PREFIX}{response}{APP_RESPONSE_SUFFIX}"


def format_selector_option(
    prompt_type: str,
    selected: bool,
    style_active: bool = False,
    trailing_text: str | None = None,
) -> str:
    if selected:
        punctuation = "?" if trailing_text is None else ":"
        line = f"> {prompt_type}{punctuation}"
        if trailing_text is None:
            line = f"{line} [enter] [esc to exit]"
        elif trailing_text:
            line = f"{line} {trailing_text}"
    else:
        line = f"  {prompt_type}"
    if selected and style_active:
        if trailing_text is not None:
            prompt = f"{ANSI_BOLD}> {prompt_type}:{ANSI_RESET}"
            if trailing_text:
                return f"{prompt} {trailing_text}"
            return prompt
        return f"{ANSI_BOLD}{line}{ANSI_RESET}"
    if style_active:
        return f"{ANSI_MUTED}{line}{ANSI_RESET}"
    return line


def prompt_for_question_fallback(
    input_fn: Callable[[str], str] | None = None,
    output_fn: Callable[[str], None] | None = None,
) -> str:
    input_fn = input if input_fn is None else input_fn
    output_fn = print if output_fn is None else output_fn
    option_lookup = {key: prompt_type for key, prompt_type in APP_QUESTION_OPTIONS}
    while True:
        output_fn(APP_QUESTION_PROMPT_FALLBACK)
        output_fn("[1] where?  [2] what?  [3] why?  [4] when?")
        choice = input_fn("> ")
        value = choice.strip().lower()
        if value in option_lookup:
            return option_lookup[value]
        output_fn("choose 1, 2, 3, or 4.")
        output_fn("")


def build_selector_lines(
    selected_index: int,
    selected_trailing_text: str | None = None,
    style_active: bool = False,
) -> list[str]:
    lines = [APP_QUESTION_PROMPT]
    for index, (_, prompt_type) in enumerate(APP_QUESTION_OPTIONS):
        lines.append(
            format_selector_option(
                prompt_type,
                index == selected_index,
                style_active=style_active,
                trailing_text=selected_trailing_text if index == selected_index else None,
            )
        )
    lines.extend("" for _ in range(APP_SELECTOR_BOTTOM_PADDING_LINES))
    return lines


def build_selected_prompt_lines(
    selected_index: int,
    selected_trailing_text: str | None = None,
    style_active: bool = False,
) -> list[str]:
    _, prompt_type = APP_QUESTION_OPTIONS[selected_index]
    prompt_line = f"> {prompt_type}:"
    if style_active:
        prompt_line = f"{ANSI_BOLD}{prompt_line}{ANSI_RESET}"
    response_line = f"  {selected_trailing_text}" if selected_trailing_text else ""
    lines = [
        APP_QUESTION_PROMPT,
        "",
        prompt_line,
        response_line,
    ]
    hidden_line_count = max(
        0,
        len(build_selector_lines(selected_index)) - len(lines),
    )
    lines.extend("" for _ in range(hidden_line_count))
    return lines


def render_question_selector(
    selected_index: int,
    output_stream: TextIO | None = None,
    redraw: bool = False,
    selected_trailing_text: str | None = None,
) -> int:
    output_stream = sys.stdout if output_stream is None else output_stream
    lines = build_selector_lines(
        selected_index,
        selected_trailing_text=selected_trailing_text,
        style_active=True,
    )
    if redraw:
        output_stream.write(f"\x1b[{len(lines)}F")
    for line in lines:
        output_stream.write(f"\r{ANSI_RESET}\x1b[2K")
        output_stream.write(f"{line}\n")
    output_stream.flush()
    return len(lines)


def render_selected_prompt(
    selected_index: int,
    output_stream: TextIO | None = None,
    redraw: bool = False,
    selected_trailing_text: str | None = None,
    trim_bottom: bool = False,
) -> int:
    output_stream = sys.stdout if output_stream is None else output_stream
    lines = build_selected_prompt_lines(
        selected_index,
        selected_trailing_text=selected_trailing_text,
        style_active=True,
    )
    hidden_line_count = max(
        0,
        len(build_selector_lines(selected_index)) - 4,
    )
    if redraw:
        output_stream.write(f"\x1b[{len(lines)}F")
    for line in lines:
        output_stream.write(f"\r{ANSI_RESET}\x1b[2K")
        output_stream.write(f"{line}\n")
    if trim_bottom and hidden_line_count > 0:
        output_stream.write(f"\x1b[{hidden_line_count}F")
    output_stream.flush()
    return len(lines)


def read_selector_key(input_stream: TextIO | None = None) -> str:
    input_stream = sys.stdin if input_stream is None else input_stream
    fd = input_stream.fileno()
    previous_settings = termios.tcgetattr(fd)
    try:
        tty.setraw(fd)
        first = input_stream.read(1)
        if first in {"\r", "\n"}:
            return "enter"
        if first == "\x1b":
            second = input_stream.read(1)
            if second == "[":
                third = input_stream.read(1)
                if third == "A":
                    return "up"
                if third == "B":
                    return "down"
            return "escape"
        return first.lower()
    finally:
        termios.tcsetattr(fd, termios.TCSADRAIN, previous_settings)


def prompt_for_question_selector(
    read_key_fn: Callable[[], str] | None = None,
    output_stream: TextIO | None = None,
) -> tuple[int | None, str | None]:
    read_key_fn = read_selector_key if read_key_fn is None else read_key_fn
    output_stream = sys.stdout if output_stream is None else output_stream
    selected_index = 0
    output_stream.write(ANSI_CURSOR_HIDE)
    output_stream.flush()
    try:
        render_question_selector(selected_index, output_stream=output_stream)
        while True:
            key = read_key_fn()
            if key == "up":
                selected_index = (selected_index - 1) % len(APP_QUESTION_OPTIONS)
                render_question_selector(selected_index, output_stream=output_stream, redraw=True)
                continue
            if key == "down":
                selected_index = (selected_index + 1) % len(APP_QUESTION_OPTIONS)
                render_question_selector(selected_index, output_stream=output_stream, redraw=True)
                continue
            if key == "enter":
                return selected_index, APP_QUESTION_OPTIONS[selected_index][1]
            if key == "escape":
                return None, None
    finally:
        output_stream.write(ANSI_CURSOR_SHOW)
        output_stream.flush()


def prompt_to_continue(
    input_fn: Callable[[str], str] | None = None,
    output_fn: Callable[[str], None] | None = None,
) -> bool:
    input_fn = input if input_fn is None else input_fn
    output_fn = print if output_fn is None else output_fn
    while True:
        output_fn(APP_CONTINUE_PROMPT)
        answer = input_fn("> ").strip().lower()
        if answer in {"y", "yes"}:
            output_fn(APP_DIVIDER)
            return True
        if answer in {"n", "no"}:
            return False
        output_fn("choose y or n.")
        output_fn("")


def prompt_to_continue_selector(
    read_key_fn: Callable[[], str] | None = None,
    output_stream: TextIO | None = None,
) -> bool:
    read_key_fn = read_selector_key if read_key_fn is None else read_key_fn
    output_stream = sys.stdout if output_stream is None else output_stream

    while True:
        output_stream.write(ANSI_CURSOR_SHOW)
        output_stream.write(f"{APP_CONTINUE_PROMPT} ")
        output_stream.flush()

        answer = ""
        while True:
            key = read_key_fn()
            if key in {"y", "n"} and not answer:
                answer = key
                output_stream.write(key)
                output_stream.flush()
                continue
            if key in {"\x7f", "\b"} and answer:
                answer = ""
                output_stream.write("\b \b")
                output_stream.flush()
                continue
            if key == "escape":
                output_stream.write("\n")
                output_stream.flush()
                return False
            if key == "enter":
                if answer in {"y", "n"}:
                    output_stream.write("\n")
                    if answer == "y":
                        output_stream.write(f"{APP_DIVIDER}\n")
                    output_stream.flush()
                    return answer == "y"
                continue


def run_with_loading(
    task: Callable[[], str],
    output_stream: TextIO | None = None,
    render_frame: Callable[[str], None] | None = None,
) -> str:
    output_stream = sys.stdout if output_stream is None else output_stream
    stop = threading.Event()
    frames = ("⠋", "⠙", "⠹", "⠸", "⠼", "⠴")

    def animate() -> None:
        frame_index = 0
        while not stop.is_set():
            frame = frames[frame_index % len(frames)]
            if render_frame is None:
                output_stream.write(f"\r\x1b[2K{frame}")
                output_stream.flush()
            else:
                render_frame(frame)
            frame_index += 1
            if stop.wait(0.14):
                break
        if render_frame is None:
            output_stream.write("\r\x1b[2K")
            output_stream.flush()

    thread = threading.Thread(target=animate, daemon=True)
    thread.start()
    try:
        return task()
    finally:
        stop.set()
        thread.join()


def reveal_response_inline(
    response: str,
    *,
    selected_index: int,
    output_stream: TextIO | None = None,
) -> None:
    output_stream = sys.stdout if output_stream is None else output_stream
    render_selected_prompt(
        selected_index,
        output_stream=output_stream,
        redraw=True,
        selected_trailing_text=response,
        trim_bottom=True,
    )


def render_continue_break(
    output_stream: TextIO | None = None,
) -> None:
    output_stream = sys.stdout if output_stream is None else output_stream
    output_stream.write(ANSI_CURSOR_HIDE)
    output_stream.flush()
    for beat in APP_POST_RESPONSE_BEATS:
        time.sleep(beat)


def command_app(
    input_fn: Callable[[str], str] | None = None,
    output_fn: Callable[[str], None] | None = None,
) -> int:
    use_selector = (
        input_fn is None
        and output_fn is None
        and sys.stdin.isatty()
        and sys.stdout.isatty()
    )
    input_fn = input if input_fn is None else input_fn
    output_fn = print if output_fn is None else output_fn
    settings = load_settings()
    ensure_local_dirs(settings)
    require_openai_api_key()
    print_app_header(output_fn)

    keep_running = True
    while keep_running:
        if use_selector:
            selected_index, prompt_type = prompt_for_question_selector()
            if prompt_type is None:
                output_fn("")
                return 0
        else:
            prompt_type = prompt_for_question_fallback(input_fn, output_fn)
        if use_selector:
            response = run_with_loading(
                lambda: generate_response(settings, prompt_type),
                output_stream=sys.stdout,
                render_frame=lambda frame: render_selected_prompt(
                    selected_index,
                    output_stream=sys.stdout,
                    redraw=True,
                    selected_trailing_text=frame,
                ),
            )
            reveal_response_inline(
                response,
                selected_index=selected_index,
                output_stream=sys.stdout,
            )
            render_continue_break(output_stream=sys.stdout)
        else:
            response = generate_response(settings, prompt_type)
            output_fn("")
            output_fn(APP_DIVIDER)
            output_fn(format_app_response(response))
            output_fn(APP_DIVIDER)
            output_fn("")
        if use_selector:
            keep_running = prompt_to_continue_selector(output_stream=sys.stdout)
        else:
            keep_running = prompt_to_continue(input_fn, output_fn)
        if keep_running:
            time.sleep(APP_CONTINUE_DELAY_SECONDS)
            output_fn("")
    return 0


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
    print('Example: .venv/bin/python -m probaboracle judge-coherence 12 pass --note "one resolved sentence"')
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

    if args.command in {None, "app"}:
        return command_app()
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
