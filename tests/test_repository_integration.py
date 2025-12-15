"""
Integration Test Examples for This Repository

This file contains tests specifically designed for the code in this LLM repository.
It demonstrates how to test the actual Website class, summarization functions, and
chatbot helper functions that exist in the codebase.

These tests are designed to work even when some dependencies (like API keys) are missing.
"""

import unittest
from unittest.mock import Mock, patch, MagicMock, patch
import sys
import os

# Set up paths and environment BEFORE importing any modules
os.environ['OPENAI_API_KEY'] = 'sk-test-key-for-testing-only-not-real'
os.environ['ANTHROPIC_API_KEY'] = 'sk-ant-test-key'
os.environ['GOOGLE_API_KEY'] = 'test-google-key'

# Add source directories to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src', 'wk1', '1_summarize_open_ai'))


class TestWebsiteClassIntegration(unittest.TestCase):
    """
    Integration tests for the Website class from src/wk1/1_summarize_open_ai/website.py
    
    These tests verify the actual implementation works correctly with mocked network calls.
    """
    
    @patch('requests.get')
    def test_website_parses_html_correctly(self, mock_get):
        """
        INTEGRATION TEST: Website class successfully extracts title and content
        
        What this tests:
        - Real Website class implementation
        - BeautifulSoup HTML parsing
        - Content cleaning (removing scripts, styles)
        
        Why it matters:
        - Validates core web scraping functionality
        - Ensures BeautifulSoup integration works
        - Tests real code paths (not just mocks)
        
        How it works:
        1. Mock requests.get to return fake HTML
        2. Create real Website instance (not mocked)
        3. Verify it extracts title correctly
        4. Verify it cleans text content correctly
        """
        try:
            from website import Website
        except ImportError as e:
            self.skipTest(f"Could not import Website: {e}")
        
        # Create realistic HTML response
        html_content = """
        <!DOCTYPE html>
        <html>
            <head>
                <title>AI Research Lab</title>
                <style>
                    body { font-family: Arial; }
                </style>
            </head>
            <body>
                <h1>Welcome to Our Lab</h1>
                <p>We research artificial intelligence and machine learning.</p>
                <script>
                    console.log('This should not appear in text');
                </script>
                <p>Our team includes world-class researchers.</p>
            </body>
        </html>
        """
        
        # Set up mock response
        mock_response = Mock()
        mock_response.content = html_content.encode('utf-8')
        mock_response.raise_for_status = Mock()
        mock_get.return_value = mock_response
        
        # Create Website instance (uses real code)
        website = Website("https://example.com")
        
        # VERIFY: Title extracted correctly
        self.assertEqual(website.title, "AI Research Lab",
                        "Website should extract title from <title> tag")
        
        # VERIFY: Visible text is extracted
        self.assertIn("Welcome to Our Lab", website.text,
                     "Website should extract visible heading text")
        self.assertIn("artificial intelligence", website.text,
                     "Website should extract paragraph text")
        self.assertIn("world-class researchers", website.text,
                     "Website should extract all paragraphs")
        
        # VERIFY: Scripts and styles are removed
        self.assertNotIn("console.log", website.text,
                        "Scripts should be removed from text content")
        self.assertNotIn("font-family", website.text,
                        "Styles should be removed from text content")
        
        # VERIFY: URL was requested correctly
        mock_get.assert_called_once()
        call_args = mock_get.call_args
        self.assertEqual(call_args[0][0], "https://example.com")
        self.assertIn("timeout", call_args[1],
                     "Should include timeout parameter")
    
    @patch('requests.get')
    def test_website_handles_unicode_correctly(self, mock_get):
        """
        INTEGRATION TEST: Website preserves Unicode characters
        
        Real-world importance:
        - Many websites use international characters
        - Emojis are common in modern content
        - LLMs can process Unicode text
        
        This test uses real Website class to ensure proper encoding.
        """
        try:
            from website import Website
        except ImportError:
            self.skipTest("Website module not available")
        
        # HTML with various Unicode characters
        html_content = """
        <html>
            <head><title>Global Tech 🌍</title></head>
            <body>
                <p>Café résumé naïve</p>
                <p>日本語のテキスト</p>
                <p>Emoji test: 🚀 💻 ✨</p>
                <p>中文文本</p>
            </body>
        </html>
        """.encode('utf-8')
        
        mock_response = Mock()
        mock_response.content = html_content
        mock_response.raise_for_status = Mock()
        mock_get.return_value = mock_response
        
        website = Website("https://example.com")
        
        # Verify Unicode is preserved
        self.assertIn("🌍", website.title)
        self.assertIn("Café", website.text)
        self.assertIn("日本語", website.text)
        self.assertIn("🚀", website.text)
        self.assertIn("中文", website.text)
    
    @patch('requests.get')
    def test_website_error_handling(self, mock_get):
        """
        INTEGRATION TEST: Website raises RuntimeError on network failure
        
        Error handling is critical:
        - Network can fail in many ways
        - Users need clear error messages
        - Application shouldn't crash
        
        This tests the real error handling code.
        """
        try:
            from website import Website
        except ImportError:
            self.skipTest("Website module not available")
        
        import requests
        
        # Simulate network timeout
        mock_get.side_effect = requests.Timeout("Connection timed out after 10 seconds")
        
        # Verify RuntimeError is raised
        with self.assertRaises(RuntimeError) as context:
            Website("https://slow-site.com")
        
        # Verify error message is helpful
        error_message = str(context.exception)
        self.assertIn("Failed to fetch", error_message,
                     "Error should explain what failed")
        self.assertIn("timed out", error_message,
                     "Error should include specific cause")


class TestPromptBuildingFunctions(unittest.TestCase):
    """
    Tests for prompt building functions used in chatbots
    
    These functions are critical because:
    - Prompts directly affect LLM output quality
    - Small changes can have big impacts
    - Need to ensure all context is included
    """
    
    @patch.dict('sys.modules', {'gradio': MagicMock()})
    def test_build_system_prompt_for_code_questions(self):
        """
        TEST: System prompts include language and difficulty level
        
        Testing approach:
        - Import actual build_system_prompt function
        - Call with different parameters
        - Verify output includes all required elements
        
        This ensures prompts are well-formed for LLM consumption.
        """
        # Try to import from either location
        build_system_prompt = None
        try:
            sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src', 'wk2', '3_chatbot'))
            from software_engineer_tester import build_system_prompt
        except ImportError:
            try:
                from code_syntax_checker import build_system_prompt
            except ImportError:
                self.skipTest("Could not import build_system_prompt function")
        
        # Test with different languages
        prompt_python = build_system_prompt("Python", "Beginner")
        self.assertIn("Python", prompt_python,
                     "Prompt should mention the programming language")
        self.assertIn("beginner", prompt_python.lower(),
                     "Prompt should mention the difficulty level")
        
        prompt_java = build_system_prompt("Java", "Advanced")
        self.assertIn("Java", prompt_java,
                     "Prompt should adapt to different languages")
        self.assertIn("advanced", prompt_java.lower(),
                     "Prompt should adapt to different difficulty levels")
    
    @patch.dict('sys.modules', {'gradio': MagicMock()})
    def test_build_evaluation_prompt_structure(self):
        """
        TEST: Evaluation prompts include question, answer, and instructions
        
        For effective evaluation:
        - LLM needs to see the original question
        - LLM needs to see the student's answer
        - LLM needs instructions on how to evaluate
        
        This test ensures all components are present.
        """
        build_evaluation_prompt = None
        try:
            sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src', 'wk2', '3_chatbot'))
            from software_engineer_tester import build_evaluation_prompt
        except ImportError:
            try:
                from code_syntax_checker import build_evaluation_prompt
            except ImportError:
                self.skipTest("Could not import build_evaluation_prompt function")
        
        question = "What is a Python list?"
        answer = "A list is a mutable, ordered collection of items."
        
        prompt = build_evaluation_prompt(question, answer)
        
        # Verify question is included
        self.assertIn(question, prompt,
                     "Evaluation prompt must include original question")
        
        # Verify answer is included
        self.assertIn(answer, prompt,
                     "Evaluation prompt must include student answer")
        
        # Verify evaluation instructions
        self.assertTrue(
            "feedback" in prompt.lower() or "evaluate" in prompt.lower(),
            "Prompt should request evaluation/feedback"
        )


class TestHelperFunctionPatterns(unittest.TestCase):
    """
    Tests demonstrating common patterns for helper functions
    
    Even without the actual code, we can test patterns and demonstrate
    best practices for testing LLM-related utilities.
    """
    
    def test_pattern_truncate_text(self):
        """
        PATTERN TEST: Text truncation for token limits
        
        Many LLM functions need to truncate text to fit token limits.
        This demonstrates testing such a function.
        """
        def truncate_for_llm(text, max_length=1000):
            """Truncate text to max_length, adding ellipsis if truncated."""
            if len(text) <= max_length:
                return text
            return text[:max_length] + "..."
        
        # Test no truncation needed
        short_text = "Short text"
        result = truncate_for_llm(short_text, max_length=100)
        self.assertEqual(result, short_text)
        
        # Test truncation occurs
        long_text = "A" * 1000
        result = truncate_for_llm(long_text, max_length=10)
        self.assertEqual(len(result), 13)  # 10 + "..."
        self.assertTrue(result.endswith("..."))
    
    def test_pattern_message_formatting(self):
        """
        PATTERN TEST: Formatting messages for LLM APIs
        
        Chat APIs require specific message format.
        This demonstrates testing format conversion.
        """
        def format_chat_messages(system_prompt, user_messages):
            """Convert to OpenAI chat format."""
            messages = [{"role": "system", "content": system_prompt}]
            for msg in user_messages:
                messages.append({"role": "user", "content": msg})
            return messages
        
        result = format_chat_messages(
            "You are helpful.",
            ["Hello", "How are you?"]
        )
        
        self.assertEqual(len(result), 3)
        self.assertEqual(result[0]["role"], "system")
        self.assertEqual(result[1]["content"], "Hello")
        self.assertEqual(result[2]["content"], "How are you?")


# Test runner
if __name__ == '__main__':
    print("="*70)
    print("Running Integration Tests for LLM Repository")
    print("="*70)
    print()
    print("These tests verify the actual code in this repository,")
    print("using mocks for external dependencies (network, APIs).")
    print()
    print("="*70)
    print()
    
    # Run tests with verbose output
    unittest.main(verbosity=2)
