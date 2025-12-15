# Testing Guide for LLM Applications

## Quick Reference Guide for Testing Common LLM Patterns

This guide shows practical examples of testing patterns specific to LLM applications, with real code you can copy and adapt.

---

## Pattern 1: Testing Prompt Construction

### Why Test Prompts?
- Prompts are the interface to LLMs
- Small changes can drastically affect output
- Need to ensure required context is included
- Helps catch missing variables or formatting errors

### Example Test

```python
import unittest

def build_summary_prompt(title, content, max_words=100):
    """Build a prompt for summarizing website content."""
    return f"""You are a helpful assistant that summarizes websites.
    
Website Title: {title}

Summarize the following content in {max_words} words or less:

{content}
"""

class TestPromptConstruction(unittest.TestCase):
    
    def test_prompt_includes_title(self):
        """Verify website title appears in prompt."""
        prompt = build_summary_prompt("Example Site", "Some content")
        self.assertIn("Example Site", prompt)
    
    def test_prompt_includes_content(self):
        """Verify content appears in prompt."""
        prompt = build_summary_prompt("Title", "Important content")
        self.assertIn("Important content", prompt)
    
    def test_prompt_respects_max_words(self):
        """Verify max_words parameter is included."""
        prompt = build_summary_prompt("Title", "Content", max_words=50)
        self.assertIn("50 words", prompt)
    
    def test_prompt_has_system_instruction(self):
        """Verify system instruction is present."""
        prompt = build_summary_prompt("Title", "Content")
        self.assertIn("summarizes websites", prompt.lower())
```

**Key Points:**
- ✅ Check that all variables are included
- ✅ Verify instructions are clear
- ✅ Test different parameter values
- ✅ Ensure formatting is consistent

---

## Pattern 2: Testing LLM API Calls (with Mocking)

### Why Mock LLM APIs?
- Real API calls cost money 💰
- Real API calls are slow ⏱️
- Real API calls can fail intermittently 
- Tests need to be deterministic (same input → same output)

### Example Test

```python
import unittest
from unittest.mock import Mock, patch

# The function we want to test
def call_llm_for_summary(text, api_client):
    """Call LLM API to generate a summary."""
    try:
        response = api_client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": "You are a helpful assistant."},
                {"role": "user", "content": f"Summarize: {text}"}
            ]
        )
        return response.choices[0].message.content
    except Exception as e:
        return f"Error: {e}"


class TestLLMAPICalls(unittest.TestCase):
    
    def test_successful_api_call(self):
        """
        Test successful LLM API call returns summary.
        
        Explanation:
        - Create mock API client
        - Configure mock to return fake response
        - Verify our function processes response correctly
        - NO real API call is made!
        """
        # Create mock API client
        mock_client = Mock()
        
        # Create mock response structure
        mock_response = Mock()
        mock_response.choices = [Mock()]
        mock_response.choices[0].message.content = "This is a test summary."
        
        # Configure mock to return our response
        mock_client.chat.completions.create.return_value = mock_response
        
        # Call the function with mock
        result = call_llm_for_summary("Long text here...", mock_client)
        
        # Verify result
        self.assertEqual(result, "This is a test summary.")
        
        # Verify API was called with correct parameters
        mock_client.chat.completions.create.assert_called_once()
        call_args = mock_client.chat.completions.create.call_args
        
        # Check the model parameter
        self.assertEqual(call_args[1]["model"], "gpt-4o-mini")
        
        # Check messages structure
        messages = call_args[1]["messages"]
        self.assertEqual(len(messages), 2)
        self.assertEqual(messages[0]["role"], "system")
        self.assertEqual(messages[1]["role"], "user")
    
    def test_api_call_handles_errors(self):
        """
        Test that API errors are handled gracefully.
        
        Explanation:
        - Configure mock to raise an exception
        - Verify our function catches it and returns error message
        - Ensures application doesn't crash on API failures
        """
        mock_client = Mock()
        mock_client.chat.completions.create.side_effect = Exception("API rate limit exceeded")
        
        result = call_llm_for_summary("Text", mock_client)
        
        self.assertIn("Error", result)
        self.assertIn("rate limit", result)
```

**Key Points:**
- ✅ Mock the API client completely
- ✅ Test both success and failure paths
- ✅ Verify correct parameters are sent
- ✅ Check error handling works

---

## Pattern 3: Testing Streaming Responses

### Why Test Streaming?
- Streaming provides progressive output (better UX)
- Different code path than non-streaming
- Need to handle partial chunks correctly
- Error handling is more complex

### Example Test

```python
import unittest
from unittest.mock import Mock

def stream_llm_response(prompt, api_client):
    """
    Stream LLM response, yielding chunks as they arrive.
    
    Yields:
        Chunks of text from the LLM
    """
    try:
        stream = api_client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[{"role": "user", "content": prompt}],
            stream=True
        )
        
        for chunk in stream:
            content = chunk.choices[0].delta.content or ""
            if content:
                yield content
                
    except Exception as e:
        yield f"Error: {e}"


class TestStreamingResponses(unittest.TestCase):
    
    def test_streaming_yields_chunks(self):
        """
        Test that streaming yields individual chunks.
        
        Explanation:
        - Create mock chunks (simulating API stream)
        - Configure mock to return iterator of chunks
        - Collect all yielded values
        - Verify they match expected chunks
        """
        mock_client = Mock()
        
        # Create mock chunks
        chunk1 = Mock()
        chunk1.choices = [Mock()]
        chunk1.choices[0].delta.content = "Hello "
        
        chunk2 = Mock()
        chunk2.choices = [Mock()]
        chunk2.choices[0].delta.content = "world!"
        
        # Mock stream returns list of chunks
        mock_client.chat.completions.create.return_value = [chunk1, chunk2]
        
        # Collect all chunks
        chunks = list(stream_llm_response("Test prompt", mock_client))
        
        # Verify chunks
        self.assertEqual(len(chunks), 2)
        self.assertEqual(chunks[0], "Hello ")
        self.assertEqual(chunks[1], "world!")
    
    def test_streaming_handles_empty_chunks(self):
        """
        Test that empty chunks are filtered out.
        
        Explanation:
        - Sometimes API returns chunks with no content
        - Our function should skip these (the 'or ""' and 'if content')
        - This test verifies that behavior
        """
        mock_client = Mock()
        
        chunk1 = Mock()
        chunk1.choices = [Mock()]
        chunk1.choices[0].delta.content = "Text"
        
        # Empty chunk
        chunk2 = Mock()
        chunk2.choices = [Mock()]
        chunk2.choices[0].delta.content = None
        
        chunk3 = Mock()
        chunk3.choices = [Mock()]
        chunk3.choices[0].delta.content = "More"
        
        mock_client.chat.completions.create.return_value = [chunk1, chunk2, chunk3]
        
        chunks = list(stream_llm_response("Prompt", mock_client))
        
        # Should only have 2 chunks (empty filtered out)
        self.assertEqual(len(chunks), 2)
        self.assertEqual(chunks, ["Text", "More"])
```

**Key Points:**
- ✅ Mock returns an iterable (list of chunks)
- ✅ Test empty/None content handling
- ✅ Collect all yielded values for verification
- ✅ Test error handling in streams

---

## Pattern 4: Testing Web Scraping Functions

### Why Test Web Scraping?
- Websites can be malformed
- Need to handle network errors
- Unicode and special characters
- Different HTML structures

### Example Test

```python
import unittest
from unittest.mock import Mock, patch
import requests

def scrape_website_title(url):
    """
    Scrape the title from a website.
    
    Returns:
        Website title as string
    """
    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        
        from bs4 import BeautifulSoup
        soup = BeautifulSoup(response.content, 'html.parser')
        
        if soup.title and soup.title.string:
            return soup.title.string.strip()
        else:
            return "No title found"
            
    except requests.RequestException as e:
        return f"Error fetching {url}: {e}"


class TestWebScraping(unittest.TestCase):
    
    @patch('requests.get')
    def test_scrape_title_success(self, mock_get):
        """
        Test successful title scraping.
        
        Explanation:
        - Use @patch to replace requests.get
        - Provide fake HTML with a title
        - Verify title is extracted correctly
        - NO real HTTP request is made!
        """
        # Create mock response
        mock_response = Mock()
        mock_response.content = b"<html><head><title>Test Page</title></head></html>"
        mock_response.raise_for_status = Mock()  # No exception
        
        # Configure requests.get to return our mock
        mock_get.return_value = mock_response
        
        # Call function
        result = scrape_website_title("https://example.com")
        
        # Verify result
        self.assertEqual(result, "Test Page")
        
        # Verify requests.get was called correctly
        mock_get.assert_called_once_with("https://example.com", timeout=10)
    
    @patch('requests.get')
    def test_scrape_handles_missing_title(self, mock_get):
        """Test handles HTML without title tag."""
        mock_response = Mock()
        mock_response.content = b"<html><body>No title here</body></html>"
        mock_response.raise_for_status = Mock()
        mock_get.return_value = mock_response
        
        result = scrape_website_title("https://example.com")
        
        self.assertEqual(result, "No title found")
    
    @patch('requests.get')
    def test_scrape_handles_network_error(self, mock_get):
        """Test handles network errors gracefully."""
        mock_get.side_effect = requests.Timeout("Connection timed out")
        
        result = scrape_website_title("https://example.com")
        
        self.assertIn("Error fetching", result)
        self.assertIn("timed out", result)
    
    @patch('requests.get')
    def test_scrape_handles_unicode(self, mock_get):
        """Test handles Unicode characters in title."""
        mock_response = Mock()
        mock_response.content = "<html><head><title>Café ☕ 中文</title></head></html>".encode('utf-8')
        mock_response.raise_for_status = Mock()
        mock_get.return_value = mock_response
        
        result = scrape_website_title("https://example.com")
        
        self.assertEqual(result, "Café ☕ 中文")
```

**Key Points:**
- ✅ Mock requests.get to avoid real network calls
- ✅ Test normal case and edge cases
- ✅ Test error handling
- ✅ Test Unicode support

---

## Pattern 5: Testing Gradio/Chat Interfaces

### Why Test UI Functions?
- UI logic can be complex
- Chat history management is error-prone
- Need to ensure proper state handling
- Streaming to UI needs special care

### Example Test

```python
import unittest
from unittest.mock import Mock

def chat_response(user_message, chat_history, llm_client):
    """
    Generate chat response and update history.
    
    Args:
        user_message: User's input
        chat_history: List of previous messages
        llm_client: Mock or real LLM client
        
    Returns:
        Updated chat history
    """
    # Build messages for API
    messages = [{"role": "system", "content": "You are helpful."}]
    
    for msg in chat_history:
        messages.append(msg)
    
    messages.append({"role": "user", "content": user_message})
    
    # Get response
    response = llm_client.chat.completions.create(
        model="gpt-4o-mini",
        messages=messages
    )
    
    assistant_message = response.choices[0].message.content
    
    # Update history
    updated_history = chat_history + [
        {"role": "user", "content": user_message},
        {"role": "assistant", "content": assistant_message}
    ]
    
    return updated_history


class TestChatInterface(unittest.TestCase):
    
    def test_chat_adds_user_and_assistant_messages(self):
        """
        Test that both user and assistant messages are added to history.
        
        Explanation:
        - Start with empty history
        - Mock LLM response
        - Verify both messages added
        - Verify order is correct
        """
        # Mock LLM client
        mock_client = Mock()
        mock_response = Mock()
        mock_response.choices = [Mock()]
        mock_response.choices[0].message.content = "I'm here to help!"
        mock_client.chat.completions.create.return_value = mock_response
        
        # Call function
        history = chat_response("Hello", [], mock_client)
        
        # Verify history
        self.assertEqual(len(history), 2)
        self.assertEqual(history[0]["role"], "user")
        self.assertEqual(history[0]["content"], "Hello")
        self.assertEqual(history[1]["role"], "assistant")
        self.assertEqual(history[1]["content"], "I'm here to help!")
    
    def test_chat_preserves_previous_history(self):
        """Test that previous messages are preserved."""
        mock_client = Mock()
        mock_response = Mock()
        mock_response.choices = [Mock()]
        mock_response.choices[0].message.content = "Response 2"
        mock_client.chat.completions.create.return_value = mock_response
        
        # Start with existing history
        initial_history = [
            {"role": "user", "content": "First message"},
            {"role": "assistant", "content": "First response"}
        ]
        
        # Add new message
        history = chat_response("Second message", initial_history, mock_client)
        
        # Verify all messages present
        self.assertEqual(len(history), 4)
        self.assertEqual(history[0]["content"], "First message")
        self.assertEqual(history[1]["content"], "First response")
        self.assertEqual(history[2]["content"], "Second message")
        self.assertEqual(history[3]["content"], "Response 2")
    
    def test_chat_includes_history_in_api_call(self):
        """Test that previous context is sent to LLM."""
        mock_client = Mock()
        mock_response = Mock()
        mock_response.choices = [Mock()]
        mock_response.choices[0].message.content = "Response"
        mock_client.chat.completions.create.return_value = mock_response
        
        previous_history = [
            {"role": "user", "content": "Previous"},
            {"role": "assistant", "content": "Prev response"}
        ]
        
        chat_response("New message", previous_history, mock_client)
        
        # Check API was called with full context
        call_args = mock_client.chat.completions.create.call_args
        messages = call_args[1]["messages"]
        
        # Should have: system + 2 history + 1 new = 4 messages
        self.assertEqual(len(messages), 4)
        self.assertEqual(messages[0]["role"], "system")
        self.assertEqual(messages[1]["content"], "Previous")
        self.assertEqual(messages[3]["content"], "New message")
```

**Key Points:**
- ✅ Test history management carefully
- ✅ Verify message order
- ✅ Test that context is passed to LLM
- ✅ Test empty history and existing history cases

---

## Pattern 6: Testing Evaluation Functions

### Why Test Evaluation?
- Evaluation logic determines feedback quality
- Need to ensure all components are included in prompt
- Error cases need handling
- Critical for educational applications

### Example Test

```python
import unittest

def evaluate_answer(question, student_answer, expected_keywords=None):
    """
    Evaluate if student answer is reasonable.
    
    This is a simplified version - real version would call LLM.
    
    Returns:
        Dictionary with evaluation results
    """
    if not question or not student_answer:
        return {"error": "Question and answer are required"}
    
    # Simple keyword check (real version uses LLM)
    score = 0
    if expected_keywords:
        for keyword in expected_keywords:
            if keyword.lower() in student_answer.lower():
                score += 1
    
    return {
        "score": score,
        "max_score": len(expected_keywords) if expected_keywords else 0,
        "question": question,
        "answer": student_answer
    }


class TestEvaluation(unittest.TestCase):
    
    def test_evaluation_includes_question_and_answer(self):
        """Verify evaluation returns both question and answer."""
        result = evaluate_answer(
            "What is Python?",
            "Python is a programming language.",
            ["python", "programming"]
        )
        
        self.assertEqual(result["question"], "What is Python?")
        self.assertEqual(result["answer"], "Python is a programming language.")
    
    def test_evaluation_scores_keywords(self):
        """Test keyword scoring works."""
        result = evaluate_answer(
            "What is Python?",
            "Python is a high-level programming language.",
            ["python", "programming", "language"]
        )
        
        # All 3 keywords present
        self.assertEqual(result["score"], 3)
        self.assertEqual(result["max_score"], 3)
    
    def test_evaluation_handles_missing_answer(self):
        """Test error handling for missing answer."""
        result = evaluate_answer("Question?", "", ["keyword"])
        
        self.assertIn("error", result)
        self.assertIn("required", result["error"])
    
    def test_evaluation_is_case_insensitive(self):
        """Test that keyword matching ignores case."""
        result = evaluate_answer(
            "Test?",
            "PYTHON is great",
            ["python"]
        )
        
        self.assertEqual(result["score"], 1)
```

---

## Running Your Tests

### Basic Run
```bash
# Run all tests
python -m pytest tests/ -v

# Run specific file
python tests/test_examples_explained.py

# Run specific test
python -m pytest tests/test_examples_explained.py::TestCalculateDiscount::test_normal_discount -v
```

### With Coverage
```bash
python -m pytest tests/ --cov=src --cov-report=html
```

### Debug Mode
```bash
python -m pytest tests/ -v -s  # -s shows print statements
```

---

## Quick Testing Checklist

When writing tests for LLM applications:

- [ ] **Mock all external APIs** (OpenAI, Anthropic, etc.)
- [ ] **Test prompt construction** - verify all variables included
- [ ] **Test both success and error paths**
- [ ] **Test edge cases** - empty strings, None, very long inputs
- [ ] **Test Unicode/special characters** if handling text
- [ ] **Verify error messages are helpful**
- [ ] **Check that context/history is preserved** in chat
- [ ] **Test streaming separately** from normal responses
- [ ] **Verify API parameters** are correct (model, temperature, etc.)
- [ ] **Test with and without optional parameters**

---

## Common Mistakes to Avoid

❌ **Making real API calls in tests**
```python
# DON'T DO THIS - costs money and is slow!
def test_bad():
    client = OpenAI()  # Real client!
    response = client.chat.completions.create(...)  # Real API call!
```

✅ **Always mock API calls**
```python
# DO THIS - fast and free!
@patch('module.client')
def test_good(mock_client):
    mock_response = Mock()
    # ... configure mock ...
    mock_client.chat.completions.create.return_value = mock_response
```

❌ **Not testing error cases**
```python
# DON'T - only tests happy path
def test_incomplete():
    result = my_function("valid input")
    assert result == "expected"
```

✅ **Test both success and failure**
```python
# DO THIS - tests error handling too
def test_complete():
    # Test success
    result = my_function("valid")
    assert result == "expected"
    
    # Test error
    with pytest.raises(ValueError):
        my_function("invalid")
```

---

## Summary

Key takeaways for testing LLM applications:

1. **Always mock external dependencies** (APIs, network, time)
2. **Test prompts thoroughly** - they're your LLM interface
3. **Test error handling** - APIs fail, networks fail
4. **Test edge cases** - empty, None, Unicode, very long
5. **Keep tests fast** - no real API calls, no sleeps
6. **Document your tests** - explain what and why
7. **Run tests frequently** - catch bugs early

Remember: **Good tests = confident code changes!**
