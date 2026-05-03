from io import StringIO
from pathlib import Path
from unittest import TestCase
from unittest.mock import patch

from probaboracle.config import Settings
from probaboracle.main import (
    choose_banner_lines,
    main,
    prompt_for_question_selector,
    prompt_to_continue_selector,
    render_continue_break,
)


class FakeTTY(StringIO):
    def isatty(self) -> bool:
        return True


class MainAppLoopTests(TestCase):
    def test_choose_banner_lines_uses_box_when_wide(self) -> None:
        lines = choose_banner_lines(terminal_width=80, style_active=False)

        self.assertEqual(lines[0], "┌──────────────────────────────────────────────────────────────┐")
        self.assertIn("PROBABORACLE BETA 4.1", lines[1])

    def test_choose_banner_lines_uses_stacked_header_when_mid_width(self) -> None:
        lines = choose_banner_lines(terminal_width=56, style_active=False)

        self.assertEqual(
            lines,
            (
                "PROBABORACLE BETA 4.1",
                "probably a mini oracle. definitely a mini chatbot.",
                "github.com/tryskian/probaboracle",
            ),
        )

    def test_choose_banner_lines_uses_minimal_header_when_narrow(self) -> None:
        lines = choose_banner_lines(terminal_width=40, style_active=False)

        self.assertEqual(
            lines,
            (
                "probaboracle beta 4.1",
                "probably a mini oracle.",
                "definitely a mini chatbot.",
                "github.com/tryskian/probaboracle",
            ),
        )

    def test_choose_banner_lines_drops_repo_when_tiny(self) -> None:
        lines = choose_banner_lines(terminal_width=28, style_active=False)

        self.assertEqual(
            lines,
            (
                "probaboracle beta 4.1",
                "probably a mini oracle.",
                "definitely a mini chatbot.",
            ),
        )

    def test_selector_can_choose_with_motion_keys(self) -> None:
        stdout = StringIO()
        keys = iter(["down", "down", "enter"])

        selected_index, choice = prompt_for_question_selector(
            read_key_fn=lambda: next(keys),
            output_stream=stdout,
        )

        rendered = stdout.getvalue()
        self.assertEqual(selected_index, 2)
        self.assertEqual(choice, "why")
        self.assertIn("\x1b[?25l", rendered)
        self.assertIn("\x1b[?25h", rendered)
        self.assertIn("⊹˙⋆ ask probaboracle [arrow keys]:", rendered)
        self.assertIn("\x1b[1m> where? [enter] [esc to exit]\x1b[0m", rendered)
        self.assertIn("\x1b[38;5;245m  what\x1b[0m", rendered)
        self.assertIn("\x1b[1m> why? [enter] [esc to exit]\x1b[0m", rendered)
        self.assertIn("\x1b[38;5;245m  when\x1b[0m", rendered)
        self.assertIn(
            "⊹˙⋆ ask probaboracle [arrow keys]:\n\r\x1b[0m\x1b[2K\x1b[1m> where? [enter] [esc to exit]\x1b[0m",
            rendered,
        )

    def test_selector_can_exit_with_escape(self) -> None:
        stdout = StringIO()
        keys = iter(["escape"])

        selected_index, choice = prompt_for_question_selector(
            read_key_fn=lambda: next(keys),
            output_stream=stdout,
        )

        rendered = stdout.getvalue()
        self.assertIsNone(selected_index)
        self.assertIsNone(choice)
        self.assertIn("\x1b[?25l", rendered)
        self.assertIn("\x1b[?25h", rendered)

    def test_continue_selector_renders_divider_only_for_yes(self) -> None:
        stdout = StringIO()
        keys = iter(["y", "enter"])

        keep_running = prompt_to_continue_selector(
            read_key_fn=lambda: next(keys),
            output_stream=stdout,
        )

        rendered = stdout.getvalue()
        self.assertTrue(keep_running)
        self.assertIn("another question [y/n]? y\n────────────\n", rendered)

    def test_continue_selector_skips_divider_for_no(self) -> None:
        stdout = StringIO()
        keys = iter(["n", "enter"])

        keep_running = prompt_to_continue_selector(
            read_key_fn=lambda: next(keys),
            output_stream=stdout,
        )

        rendered = stdout.getvalue()
        self.assertFalse(keep_running)
        self.assertIn("another question [y/n]? n\n", rendered)
        self.assertNotIn("────────────", rendered)

    def test_continue_selector_escape_exits_without_divider(self) -> None:
        stdout = StringIO()
        keys = iter(["escape"])

        keep_running = prompt_to_continue_selector(
            read_key_fn=lambda: next(keys),
            output_stream=stdout,
        )

        rendered = stdout.getvalue()
        self.assertFalse(keep_running)
        self.assertIn("another question [y/n]? \n", rendered)
        self.assertNotIn("────────────", rendered)

    def test_render_continue_break_hides_cursor_without_printing_newline(self) -> None:
        stdout = StringIO()

        with patch("probaboracle.main.time.sleep"):
            render_continue_break(output_stream=stdout)

        self.assertEqual(stdout.getvalue(), "\x1b[?25l")

    def test_main_without_subcommand_opens_interactive_app_loop(self) -> None:
        stdout = StringIO()
        settings = Settings(
            app_name="Probaboracle",
            model="gpt-5-nano",
            eval_db_path=Path("/tmp/evals.sqlite"),
        )
        with patch("probaboracle.main.load_settings", return_value=settings):
            with patch("probaboracle.main.ensure_local_dirs"):
                with patch("probaboracle.main.require_openai_api_key"):
                    with patch(
                        "probaboracle.main.generate_response",
                        return_value="probably the unclaimed edge of it.",
                    ):
                        with patch("builtins.input", side_effect=["1", "n"]):
                            with patch("sys.stdout", stdout):
                                exit_code = main([])

        rendered = stdout.getvalue()
        self.assertEqual(exit_code, 0)
        self.assertIn("┌──────────────────────────────────────────────────────────────┐", rendered)
        self.assertIn("PROBABORACLE", rendered)
        self.assertIn(
            "probably a mini oracle. definitely a mini chatbot.",
            rendered,
        )
        self.assertIn("github.com/tryskian/probaboracle", rendered)
        self.assertIn("────────────", rendered)
        self.assertIn("⊹˙⋆ ask probaboracle:", rendered)
        self.assertIn("[1] where?  [2] what?  [3] why?  [4] when?", rendered)
        self.assertIn(
            "⊹˙⋆ probably the unclaimed edge of it. ⋆˙⊹",
            rendered,
        )
        self.assertIn("another question [y/n]?", rendered)

    def test_interactive_app_loop_reprompts_for_invalid_question(self) -> None:
        stdout = StringIO()
        settings = Settings(
            app_name="Probaboracle",
            model="gpt-5-nano",
            eval_db_path=Path("/tmp/evals.sqlite"),
        )
        with patch("probaboracle.main.load_settings", return_value=settings):
            with patch("probaboracle.main.ensure_local_dirs"):
                with patch("probaboracle.main.require_openai_api_key"):
                    with patch(
                        "probaboracle.main.generate_response",
                        return_value="probably a curve that hints at a shape.",
                    ):
                        with patch("builtins.input", side_effect=["9", "2", "n"]):
                            with patch("sys.stdout", stdout):
                                exit_code = main([])

        rendered = stdout.getvalue()
        self.assertEqual(exit_code, 0)
        self.assertIn("choose 1, 2, 3, or 4.", rendered)
        self.assertIn(
            "⊹˙⋆ probably a curve that hints at a shape. ⋆˙⊹",
            rendered,
        )

    def test_main_uses_selector_in_live_tty_mode(self) -> None:
        stdout = FakeTTY()
        stdin = FakeTTY()
        settings = Settings(
            app_name="Probaboracle",
            model="gpt-5-nano",
            eval_db_path=Path("/tmp/evals.sqlite"),
        )
        with patch("probaboracle.main.load_settings", return_value=settings):
            with patch("probaboracle.main.ensure_local_dirs"):
                with patch("probaboracle.main.require_openai_api_key"):
                    with patch(
                        "probaboracle.main.generate_response",
                        return_value="probably the unclaimed edge of it.",
                    ):
                        def fake_continue_selector(*, output_stream):
                            output_stream.write("another question [y/n]? y\n────────────\n")
                            return False

                        with patch(
                            "probaboracle.main.prompt_for_question_selector",
                            return_value=(0, "where"),
                        ) as prompt_selector:
                            with patch(
                                "probaboracle.main.prompt_to_continue_selector",
                                side_effect=fake_continue_selector,
                            ) as continue_selector:
                                with patch("probaboracle.main.time.sleep"):
                                    with patch("sys.stdin", stdin):
                                        with patch("sys.stdout", stdout):
                                            exit_code = main([])

        self.assertEqual(exit_code, 0)
        prompt_selector.assert_called_once_with()
        continue_selector.assert_called_once_with(output_stream=stdout)
        rendered = stdout.getvalue()
        self.assertIn("⊹˙⋆ ask probaboracle [arrow keys]:", rendered)
        self.assertIn(
            "⊹˙⋆ ask probaboracle [arrow keys]:\n\r\x1b[0m\x1b[2K\n\r\x1b[0m\x1b[2K\x1b[1m> where:\x1b[0m",
            rendered,
        )
        self.assertIn("\x1b[1m> where:\x1b[0m", rendered)
        self.assertIn("  probably the unclaimed edge of it.", rendered)
        self.assertNotIn("> where: probably the unclaimed edge of it.", rendered)
        self.assertNotIn("  what", rendered)
        self.assertNotIn("  why", rendered)
        self.assertNotIn("  when", rendered)
        self.assertIn("another question [y/n]? y\n────────────", rendered)

    def test_explicit_subcommand_path_still_works(self) -> None:
        stdout = StringIO()
        settings = Settings(
            app_name="Probaboracle",
            model="gpt-5-nano",
            eval_db_path=Path("/tmp/evals.sqlite"),
        )
        with patch("probaboracle.main.load_settings", return_value=settings):
            with patch("probaboracle.main.ensure_local_dirs"):
                with patch("probaboracle.main.require_openai_api_key"):
                    with patch(
                        "probaboracle.main.generate_response",
                        return_value="probably a reason, or perhaps not.",
                    ):
                        with patch("sys.stdout", stdout):
                            exit_code = main(["ask", "why"])

        rendered = stdout.getvalue()
        self.assertEqual(exit_code, 0)
        self.assertEqual(rendered.strip(), "probably a reason, or perhaps not.")
