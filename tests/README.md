# Test Suite Documentation

This directory contains comprehensive tests for the LLM Engineering repository, demonstrating best practices for testing Python code that integrates with LLMs and web services.

## Overview

The test suite covers:
- **Website Class**: Web scraping and HTML parsing functionality
- **OpenAI Utils**: LLM API integration and prompt building
- **Chatbot Helpers**: Question generation and answer evaluation
- **Edge Cases**: Unicode handling, empty content, error scenarios

## Why These Tests Matter

### 1. Mocking External Dependencies
- **Network Requests**: Tests use `unittest.mock` to avoid real HTTP calls
- **API Calls**: OpenAI API calls are mocked to prevent costs and ensure deterministic results
- **Benefits**: Fast execution, no external dependencies, consistent results

### 2. Comprehensive Coverage
- **Happy Path**: Normal operation with valid inputs
- **Edge Cases**: Empty content, Unicode, missing elements
- **Error Handling**: Network failures, API errors, malformed data

### 3. Educational Value
Each test includes detailed explanations:
- **What** is being tested
- **Why** it's important
- **How** the test works
- **Common pitfalls** to avoid

## Running the Tests

### Prerequisites

Install required testing packages:
```bash
pip install pytest pytest-cov
```

Or use the existing environment:
```bash
conda env create -f environment_v2.yml
conda activate llms
```

### Run All Tests

Using unittest (built-in):
```bash
cd /home/runner/work/llm/llm
python -m pytest tests/test_website_and_utils.py -v
```

Or directly with Python:
```bash
python tests/test_website_and_utils.py
```

### Run Specific Test Classes

```bash
# Test only the Website class
python -m pytest tests/test_website_and_utils.py::TestWebsiteClass -v

# Test only OpenAI utilities
python -m pytest tests/test_website_and_utils.py::TestOpenAIUtils -v

# Test only chatbot helpers
python -m pytest tests/test_website_and_utils.py::TestChatbotHelpers -v
```

### Run with Coverage Report

```bash
python -m pytest tests/ --cov=src --cov-report=html
```

## Test Structure Explained

### TestWebsiteClass

Tests the `Website` class from `src/wk1/1_summarize_open_ai/website.py`:

1. **test_website_successful_fetch**: Verifies basic HTML parsing
   - Mocks HTTP request with sample HTML
   - Validates title extraction
   - Confirms text cleanup (removes scripts/styles)

2. **test_website_missing_title**: Handles malformed HTML
   - Tests default value when `<title>` tag is missing
   - Ensures no crashes on non-standard HTML

3. **test_website_network_error**: Error handling
   - Simulates network timeout
   - Verifies proper error message propagation

4. **test_website_removes_unwanted_tags**: Content cleanup
   - Confirms removal of `<script>`, `<style>`, `<img>` tags
   - Ensures clean text for LLM processing

### TestOpenAIUtils

Tests functions from `src/wk1/1_summarize_open_ai/openai_utils.py`:

1. **test_build_prompt_structure**: Prompt formatting
   - Validates message structure for OpenAI API
   - Ensures system and user messages are correctly formatted
   - Checks that website content is included

2. **test_summarize_url_success**: End-to-end flow
   - Mocks both Website and OpenAI client
   - Tests complete summarization pipeline
   - Verifies correct API call parameters

3. **test_summarize_url_api_error**: API error handling
   - Simulates API failures (rate limits, etc.)
   - Confirms graceful degradation
   - Checks error message clarity

### TestChatbotHelpers

Tests functions from `src/wk2/3_chatbot/software_engineer_tester.py`:

1. **test_build_system_prompt_***: Prompt generation
   - Tests different difficulty levels (Beginner, Advanced)
   - Validates language and difficulty are included
   - Ensures consistent structure

2. **test_build_evaluation_prompt_***: Answer evaluation
   - Confirms both question and answer are included
   - Checks for constructive feedback instructions
   - Validates educational focus

### TestEdgeCasesAndIntegration

Advanced scenarios:

1. **test_website_with_unicode_content**: International support
   - Tests Chinese, Japanese, Korean characters
   - Validates emoji handling
   - Ensures UTF-8 encoding works correctly

2. **test_website_with_empty_body**: Minimal content
   - Handles pages with no content
   - Prevents crashes on edge cases

## Key Testing Concepts Demonstrated

### 1. Mocking (`unittest.mock`)

```python
@patch('requests.get')
def test_example(self, mock_get):
    # mock_get replaces the real requests.get function
    mock_response = Mock()
    mock_response.content = b"<html>...</html>"
    mock_get.return_value = mock_response
    # Now any call to requests.get returns our mock response
```

**Why**: Prevents actual network requests, making tests fast and reliable.

### 2. Assertions

```python
self.assertEqual(actual, expected)        # Values must be equal
self.assertIn(substring, text)           # Substring must be present
self.assertNotIn(substring, text)        # Substring must NOT be present
self.assertIsInstance(obj, type)         # Type checking
```

**Why**: Clearly expresses what we're testing and provides helpful error messages.

### 3. Test Organization

- One test class per component/module
- Descriptive test names (`test_what_when_expected`)
- Detailed docstrings explaining the test
- Logical grouping of related tests

### 4. Error Testing

```python
with self.assertRaises(RuntimeError) as context:
    problematic_function()
self.assertIn("expected message", str(context.exception))
```

**Why**: Ensures errors are handled gracefully and provide useful feedback.

## Best Practices Demonstrated

1. ✅ **Never make real API calls in tests** - Always mock external services
2. ✅ **Test both success and failure paths** - Don't just test the happy path
3. ✅ **Use descriptive test names** - Name should explain what's being tested
4. ✅ **Document each test** - Explain WHY the test exists, not just what it does
5. ✅ **Test edge cases** - Empty strings, Unicode, missing data, etc.
6. ✅ **Keep tests independent** - Each test should run in isolation
7. ✅ **Use setup/teardown when needed** - Though simple mocks often suffice

## Common Testing Patterns for LLM Applications

### Pattern 1: Mock the LLM API

```python
@patch('module.openai_client')
def test_llm_function(self, mock_client):
    # Create a fake response
    mock_response = Mock()
    mock_response.choices[0].message.content = "Expected output"
    mock_client.chat.completions.create.return_value = mock_response
    
    # Test your function
    result = your_function()
    assert result == "Expected output"
```

### Pattern 2: Test Prompt Construction

```python
def test_prompt_includes_context():
    prompt = build_prompt(context_data)
    assert "important_keyword" in prompt
    assert len(prompt) < MAX_TOKEN_LIMIT
```

### Pattern 3: Test Error Handling

```python
def test_handles_api_timeout():
    with patch('api_call', side_effect=Timeout()):
        result = your_function()
        assert "error" in result.lower()
```

## Extending the Test Suite

To add new tests:

1. **Identify the component** you want to test
2. **Create a test class** that inherits from `unittest.TestCase`
3. **Write test methods** starting with `test_`
4. **Use mocks** for external dependencies
5. **Add documentation** explaining the test's purpose

Example:
```python
class TestNewFeature(unittest.TestCase):
    """Test suite for the new feature."""
    
    def test_new_feature_works(self):
        """Test that new feature produces expected output."""
        result = new_feature("input")
        self.assertEqual(result, "expected_output")
```

## Troubleshooting

### Import Errors

If you get `ModuleNotFoundError`:
- Ensure you're running from the project root
- Check that `PYTHONPATH` includes the source directories
- Verify the imports in `test_website_and_utils.py`

### Mock Not Working

If mocks aren't being applied:
- Check the patch path (should match the import in the code under test)
- Use `@patch('module.function')` not `@patch('other_module.function')`
- Remember: patch where it's used, not where it's defined

### Tests Pass Locally But Fail in CI

- Check for environment-specific paths
- Ensure all dependencies are in `environment_v2.yml`
- Verify Python version compatibility

## Further Reading

- [Python unittest documentation](https://docs.python.org/3/library/unittest.html)
- [unittest.mock guide](https://docs.python.org/3/library/unittest.mock.html)
- [Pytest documentation](https://docs.pytest.org/)
- [Testing Best Practices](https://docs.python-guide.org/writing/tests/)

## Summary

This test suite demonstrates:
- ✅ Comprehensive coverage of core functionality
- ✅ Proper mocking of external dependencies
- ✅ Clear documentation and explanations
- ✅ Best practices for testing LLM applications
- ✅ Edge case handling
- ✅ Error scenario testing

Use these tests as a reference when writing tests for new features!
