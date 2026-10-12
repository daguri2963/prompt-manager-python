"""프롬프트 관리 프로그램의 주요 사용자 동작 확인."""

import io
import unittest
from contextlib import redirect_stdout
from unittest.mock import patch

import main


class PromptManagerTests(unittest.TestCase):
    def setUp(self):
        self.prompts = main.initial_prompts()

    def test_initial_prompts_have_required_fields(self):
        self.assertGreaterEqual(len(self.prompts), 3)
        for prompt in self.prompts:
            self.assertEqual(
                set(prompt), {"title", "content", "category", "favorite"}
            )
            self.assertTrue(prompt["title"])
            self.assertTrue(prompt["content"])

    def test_add_prompt_accepts_custom_category_and_defaults_favorite(self):
        answers = ["새 프롬프트", "새 내용", "7", "새 카테고리"]
        with patch("builtins.input", side_effect=answers), redirect_stdout(io.StringIO()):
            main.add_prompt(self.prompts)
        self.assertEqual(self.prompts[-1]["title"], "새 프롬프트")
        self.assertEqual(self.prompts[-1]["category"], "새 카테고리")
        self.assertFalse(self.prompts[-1]["favorite"])

    def test_search_matches_content_without_case_sensitivity(self):
        self.prompts.append(
            {
                "title": "검색 대상",
                "content": "Write a HELLO message",
                "category": "텍스트 생성",
                "favorite": False,
            }
        )
        output = io.StringIO()
        with patch("builtins.input", return_value="hello"), redirect_stdout(output):
            main.search_prompt(self.prompts)
        self.assertIn("4. [텍스트 생성] 검색 대상", output.getvalue())
        self.assertIn("총 1개", output.getvalue())

    def test_invalid_number_does_not_change_favorites(self):
        output = io.StringIO()
        with patch("builtins.input", return_value="99"), redirect_stdout(output):
            main.toggle_favorite(self.prompts)
        self.assertIn("올바른 프롬프트 번호", output.getvalue())
        self.assertFalse(any(prompt["favorite"] for prompt in self.prompts))

    def test_favorite_can_be_added_and_removed(self):
        with patch("builtins.input", return_value="1"), redirect_stdout(io.StringIO()):
            main.toggle_favorite(self.prompts)
        self.assertTrue(self.prompts[0]["favorite"])
        with patch("builtins.input", return_value="1"), redirect_stdout(io.StringIO()):
            main.toggle_favorite(self.prompts)
        self.assertFalse(self.prompts[0]["favorite"])

    def test_invalid_menu_choice_returns_to_menu(self):
        output = io.StringIO()
        with patch("builtins.input", side_effect=["잘못된 값", "0"]), redirect_stdout(output):
            main.main()
        self.assertIn("메뉴에 있는 번호", output.getvalue())
        self.assertGreaterEqual(output.getvalue().count("=== 나만의 프롬프트 관리 ==="), 2)


if __name__ == "__main__":
    unittest.main()
