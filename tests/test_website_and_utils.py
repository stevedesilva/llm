"""
Comprehensive Test Suite for LLM Engineering Repository

This test file demonstrates best practices for testing Python code in an LLM-based project.
It includes tests for:
1. The Website class - web scraping functionality
2. OpenAI utility functions - LLM integration
3. Chatbot helper functions - prompt building and evaluation

Each test includes detailed explanations of:
- What is being tested
- Why it's important
- How the test works
- Common edge cases to consider
"""

import unittest
from unittest.mock import Mock, patch, MagicMock
import sys
import os

# Add the source directories to the Python path so we can import the modules
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src', 'wk1', '1_summarize_open_ai'))
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src', 'wk2', '3_chatbot'))

# Set a dummy API key to prevent import errors
os.environ['OPENAI_API_KEY'] = 'sk-test-dummy-key-for-testing-only'


class TestWebsiteClass(unittest.TestCase):
    """
    Test Suite for the Website Class
    
    The Website class is responsible for:
    - Fetching HTML content from a URL
    - Parsing the HTML using BeautifulSoup
    - Extracting clean text content
    - Extracting the page title
    
    Testing web scraping code is important because:
    1. Network requests can fail in many ways (timeouts, DNS errors, HTTP errors)
    2. HTML structure can vary widely between sites
    3. We need to handle edge cases like missing titles or malformed HTML
    """
    
    @patch('requests.get')
    def test_website_successful_fetch(self, mock_get):
        """
        Test: Website successfully fetches and parses a valid HTML page
        
        Explanation:
        - We use @patch to mock the requests.get function
        - This prevents actual HTTP requests during testing (faster, more reliable)
        - We create a fake response with known HTML content
        - We verify that the Website class correctly extracts the title and text
        
        Why this matters:
        - Ensures the basic happy path works correctly
        - Validates that HTML parsing logic is sound
        """
        from website import Website
        
        # Create a mock response object that simulates a successful HTTP request
        mock_response = Mock()
        mock_response.content = b"""
            <html>
                <head><title>Test Website</title></head>
                <body>
                    <h1>Welcome</h1>
                    <p>This is test content.</p>
                    <script>alert('This should be removed');</script>
                </body>
            </html>
        """
        mock_response.raise_for_status = Mock()  # No exception means success
        mock_get.return_value = mock_response
        
        # Create a Website instance
        website = Website("https://example.com")
        
        # Verify the title was extracted correctly
        self.assertEqual(website.title, "Test Website")
        
        # Verify the text content was extracted (scripts should be removed)
        self.assertIn("Welcome", website.text)
        self.assertIn("This is test content", website.text)
        self.assertNotIn("alert", website.text)  # Scripts should be removed
        
    @patch('requests.get')
    def test_website_missing_title(self, mock_get):
        """
        Test: Website handles pages without a title tag
        
        Explanation:
        - Not all HTML pages have a <title> tag (though they should)
        - Our code should handle this gracefully with a default value
        - This prevents crashes when scraping non-standard HTML
        
        Edge case importance:
        - Real-world HTML is messy and often malformed
        - Defensive programming prevents runtime errors
        """
        from website import Website
        
        mock_response = Mock()
        mock_response.content = b"<html><body>Content without title</body></html>"
        mock_response.raise_for_status = Mock()
        mock_get.return_value = mock_response
        
        website = Website("https://example.com")
        
        # Should have a default title instead of crashing
        self.assertEqual(website.title, "No title")
        self.assertIn("Content without title", website.text)
    
    @patch('requests.get')
    def test_website_network_error(self, mock_get):
        """
        Test: Website raises appropriate error when network request fails
        
        Explanation:
        - Network requests can fail for many reasons (no internet, DNS failure, timeout)
        - We mock requests.get to raise a RequestException
        - We verify that our code converts this to a RuntimeError with a clear message
        
        Why this matters:
        - Error handling is crucial for production code
        - Users need clear error messages to diagnose problems
        - Tests ensure errors are propagated correctly up the call stack
        """
        from website import Website
        import requests
        
        # Simulate a network timeout
        mock_get.side_effect = requests.Timeout("Connection timed out")
        
        # Verify that a RuntimeError is raised with a helpful message
        with self.assertRaises(RuntimeError) as context:
            Website("https://example.com")
        
        self.assertIn("Failed to fetch", str(context.exception))
        self.assertIn("Connection timed out", str(context.exception))
    
    @patch('requests.get')
    def test_website_removes_unwanted_tags(self, mock_get):
        """
        Test: Website removes script, style, and other unwanted HTML elements
        
        Explanation:
        - When extracting text from HTML, we don't want JavaScript, CSS, or images
        - These elements clutter the text and aren't useful for LLM processing
        - This test verifies the cleanup logic works correctly
        
        Testing importance:
        - Clean text input leads to better LLM outputs
        - Ensures our preprocessing is consistent
        """
        from website import Website
        
        mock_response = Mock()
        mock_response.content = b"""
            <html>
                <head>
                    <title>Test</title>
                    <style>body { color: red; }</style>
                </head>
                <body>
                    <p>Visible content</p>
                    <script>console.log('hidden');</script>
                    <img src="test.jpg" alt="image">
                </body>
            </html>
        """
        mock_response.raise_for_status = Mock()
        mock_get.return_value = mock_response
        
        website = Website("https://example.com")
        
        # Verify visible content is present
        self.assertIn("Visible content", website.text)
        
        # Verify unwanted content is removed
        self.assertNotIn("color: red", website.text)
        self.assertNotIn("console.log", website.text)
        # Note: alt text might still be present, which is actually useful


class TestOpenAIUtils(unittest.TestCase):
    """
    Test Suite for OpenAI Utility Functions
    
    These functions handle:
    - Building prompts for the OpenAI API
    - Making API calls to generate summaries
    - Error handling for API failures
    
    Testing LLM integration code is critical because:
    1. API calls cost money - we don't want to make real calls in tests
    2. API responses can fail or timeout
    3. Prompt engineering affects output quality
    4. We need to ensure error handling works correctly
    """
    
    @patch('openai_utils.client')
    def test_build_prompt_structure(self, mock_client):
        """
        Test: build_prompt creates correctly structured messages for OpenAI API
        
        Explanation:
        - OpenAI's Chat API requires messages in a specific format
        - Each message needs a "role" (system/user/assistant) and "content"
        - The system message sets the assistant's behavior
        - The user message provides the specific task
        
        Why test this:
        - Incorrect message structure causes API errors
        - The prompt determines the quality of LLM responses
        - We want to ensure consistent prompt formatting
        """
        from openai_utils import build_prompt
        from website import Website
        
        # Create a mock Website object instead of making a real HTTP request
        mock_website = Mock(spec=Website)
        mock_website.title = "Example Site"
        mock_website.text = "Example content for testing."
        
        # Call the function we're testing
        messages = build_prompt(mock_website)
        
        # Verify the structure
        self.assertEqual(len(messages), 2)  # Should have system and user messages
        
        # Verify system message
        self.assertEqual(messages[0]["role"], "system")
        self.assertIn("summarizes websites", messages[0]["content"])
        
        # Verify user message includes website details
        self.assertEqual(messages[1]["role"], "user")
        self.assertIn("Example Site", messages[1]["content"])
        self.assertIn("Example content for testing", messages[1]["content"])
    
    @patch('openai_utils.Website')
    @patch('openai_utils.client')
    def test_summarize_url_success(self, mock_client, mock_website_class):
        """
        Test: summarize_url successfully calls OpenAI and returns a summary
        
        Explanation:
        - This tests the entire flow: fetch website -> build prompt -> call API -> return result
        - We mock both the Website class and the OpenAI client
        - We verify the function returns the expected summary text
        
        Mocking strategy:
        - Mock Website to avoid HTTP requests
        - Mock OpenAI client to avoid API calls (and costs!)
        - This makes tests fast, deterministic, and free
        """
        from openai_utils import summarize_url
        
        # Mock the Website class
        mock_site = Mock()
        mock_site.title = "Test"
        mock_site.text = "Content"
        mock_website_class.return_value = mock_site
        
        # Mock the OpenAI API response
        mock_response = Mock()
        mock_response.choices = [Mock()]
        mock_response.choices[0].message.content = "This is a test summary."
        mock_client.chat.completions.create.return_value = mock_response
        
        # Call the function
        result = summarize_url("https://example.com")
        
        # Verify the result
        self.assertEqual(result, "This is a test summary.")
        
        # Verify the OpenAI client was called correctly
        mock_client.chat.completions.create.assert_called_once()
        call_args = mock_client.chat.completions.create.call_args
        self.assertEqual(call_args[1]["model"], "gpt-4o")
        self.assertIsNotNone(call_args[1]["messages"])
    
    @patch('openai_utils.Website')
    @patch('openai_utils.client')
    def test_summarize_url_api_error(self, mock_client, mock_website_class):
        """
        Test: summarize_url handles API errors gracefully
        
        Explanation:
        - API calls can fail (rate limits, network issues, authentication errors)
        - Instead of crashing, we return an error message
        - This allows the application to continue running and inform the user
        
        Error handling importance:
        - Prevents complete application failure
        - Provides actionable feedback to users
        - Makes debugging easier
        """
        from openai_utils import summarize_url
        
        # Mock Website successfully
        mock_site = Mock()
        mock_site.title = "Test"
        mock_site.text = "Content"
        mock_website_class.return_value = mock_site
        
        # Mock the API to raise an error
        mock_client.chat.completions.create.side_effect = Exception("API rate limit exceeded")
        
        # Call the function
        result = summarize_url("https://example.com")
        
        # Verify we get an error message instead of an exception
        self.assertIn("❌ Error summarizing", result)
        self.assertIn("API rate limit exceeded", result)


class TestChatbotHelpers(unittest.TestCase):
    """
    Test Suite for Chatbot Helper Functions
    
    These functions handle:
    - Building prompts for chatbot questions
    - Building prompts for evaluating answers
    - Formatting messages for the chat interface
    
    Testing chatbot code ensures:
    1. Prompts are well-structured and clear
    2. Different difficulty levels work correctly
    3. Error messages are helpful
    4. The conversation flow is logical
    """
    
    def test_build_system_prompt_beginner(self):
        """
        Test: System prompt is correctly formatted for beginner level
        
        Explanation:
        - The system prompt sets the LLM's behavior and constraints
        - Different difficulty levels should be clearly indicated
        - The prompt should specify the programming language
        
        Why this matters:
        - Prompt quality directly affects LLM output quality
        - Clear difficulty specification ensures appropriate questions
        - Testing ensures consistency across different parameters
        """
        # Import the function (may be from code_syntax_checker or software_engineer_tester)
        try:
            from code_syntax_checker import build_system_prompt
        except ImportError:
            from software_engineer_tester import build_system_prompt
        
        result = build_system_prompt("Python", "Beginner")
        
        # Verify the prompt includes all necessary elements
        self.assertIn("Python", result)
        self.assertIn("beginner", result.lower())
        self.assertIn("question", result.lower())
        self.assertIn("programming", result.lower())
    
    def test_build_system_prompt_advanced(self):
        """
        Test: System prompt adapts correctly for advanced level
        
        Explanation:
        - Advanced level prompts should still include the language and level
        - The structure should be consistent across difficulty levels
        - This ensures predictable behavior
        """
        try:
            from code_syntax_checker import build_system_prompt
        except ImportError:
            from software_engineer_tester import build_system_prompt
        
        result = build_system_prompt("Java", "Advanced")
        
        self.assertIn("Java", result)
        self.assertIn("advanced", result.lower())
    
    def test_build_evaluation_prompt_includes_context(self):
        """
        Test: Evaluation prompt includes both the question and the answer
        
        Explanation:
        - To evaluate an answer, the LLM needs both the original question and the student's answer
        - The prompt should clearly separate these components
        - It should instruct the LLM to provide constructive feedback
        
        Why this matters:
        - Without the question, the LLM can't properly evaluate the answer
        - Clear structure leads to better evaluation quality
        - Constructive feedback helps students learn
        """
        try:
            from code_syntax_checker import build_evaluation_prompt
        except ImportError:
            from software_engineer_tester import build_evaluation_prompt
        
        question = "What is a Python list?"
        answer = "A list is a mutable sequence of elements."
        
        result = build_evaluation_prompt(question, answer)
        
        # Verify both question and answer are in the prompt
        self.assertIn(question, result)
        self.assertIn(answer, result)
        
        # Verify it asks for feedback
        self.assertIn("feedback", result.lower())
    
    def test_build_evaluation_prompt_asks_for_constructive_feedback(self):
        """
        Test: Evaluation prompt requests constructive and educational feedback
        
        Explanation:
        - Good educational software provides helpful, not just critical, feedback
        - The prompt should explicitly request this type of feedback
        - We test that the instruction is present in the prompt
        """
        try:
            from code_syntax_checker import build_evaluation_prompt
        except ImportError:
            from software_engineer_tester import build_evaluation_prompt
        
        result = build_evaluation_prompt("Test question", "Test answer")
        
        # Check for constructive/educational language
        self.assertTrue(
            "constructive" in result.lower() or 
            "feedback" in result.lower() or
            "explain" in result.lower(),
            "Evaluation prompt should request helpful feedback"
        )


class TestEdgeCasesAndIntegration(unittest.TestCase):
    """
    Advanced Test Cases for Edge Scenarios and Integration
    
    These tests cover:
    - Empty or malformed inputs
    - Special characters and encoding
    - Integration between components
    
    Edge case testing is essential because:
    1. Real-world data is messy
    2. Users provide unexpected inputs
    3. Systems need to be robust
    """
    
    @patch('requests.get')
    def test_website_with_unicode_content(self, mock_get):
        """
        Test: Website correctly handles Unicode characters
        
        Explanation:
        - Modern websites use Unicode (emojis, international characters)
        - Our code should preserve these characters, not crash or mangle them
        - This is especially important for international content
        
        Real-world importance:
        - Many websites use non-ASCII characters
        - LLMs can process Unicode text
        - Users expect international support
        """
        from website import Website
        
        mock_response = Mock()
        # Unicode content: Chinese, emojis, accents
        mock_response.content = """
            <html>
                <head><title>国际网站 🌍</title></head>
                <body>
                    <p>Café résumé naïve</p>
                    <p>日本語 中文 한국어</p>
                </body>
            </html>
        """.encode('utf-8')
        mock_response.raise_for_status = Mock()
        mock_get.return_value = mock_response
        
        website = Website("https://example.com")
        
        # Verify Unicode is preserved
        self.assertIn("国际网站", website.title)
        self.assertIn("日本語", website.text)
        self.assertIn("Café", website.text)
    
    @patch('requests.get')
    def test_website_with_empty_body(self, mock_get):
        """
        Test: Website handles pages with minimal or no content
        
        Explanation:
        - Some pages might have very little content
        - Our code should handle this without errors
        - Empty text should be handled gracefully
        """
        from website import Website
        
        mock_response = Mock()
        mock_response.content = b"<html><head><title>Empty</title></head><body></body></html>"
        mock_response.raise_for_status = Mock()
        mock_get.return_value = mock_response
        
        website = Website("https://example.com")
        
        self.assertEqual(website.title, "Empty")
        # Text might be empty or just whitespace
        self.assertIsInstance(website.text, str)


# Test runner with detailed output
if __name__ == '__main__':
    # Create a test suite
    loader = unittest.TestLoader()
    suite = unittest.TestSuite()
    
    # Add all test classes
    suite.addTests(loader.loadTestsFromTestCase(TestWebsiteClass))
    suite.addTests(loader.loadTestsFromTestCase(TestOpenAIUtils))
    suite.addTests(loader.loadTestsFromTestCase(TestChatbotHelpers))
    suite.addTests(loader.loadTestsFromTestCase(TestEdgeCasesAndIntegration))
    
    # Run tests with verbose output
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)
    
    # Print summary
    print("\n" + "="*70)
    print("TEST SUMMARY")
    print("="*70)
    print(f"Tests run: {result.testsRun}")
    print(f"Successes: {result.testsRun - len(result.failures) - len(result.errors)}")
    print(f"Failures: {len(result.failures)}")
    print(f"Errors: {len(result.errors)}")
    print("="*70)
