# Test Suite Overview

## 📚 Complete Test Documentation for LLM Repository

This test suite provides comprehensive examples of testing Python code for LLM applications, with detailed explanations of testing concepts, patterns, and best practices.

---

## 🗂️ Files in This Test Suite

### 1. `test_examples_explained.py` ⭐ **Start Here**
**What it is:** Self-contained examples demonstrating core testing concepts

**Contains:**
- ✅ 19 passing tests (verified)
- Simple function testing (calculate_discount)
- Mocking external APIs (fetch_user_data)
- Testing classes with state (ShoppingCart)
- Patching time-dependent code (get_greeting)

**Best for:** Learning testing fundamentals

**Run with:**
```bash
python tests/test_examples_explained.py
```

**Key Learning Points:**
- How to structure a test
- Using assertEqual, assertIn, assertRaises
- Mock objects and their return_value
- @patch decorator for replacing dependencies
- setUp method for test initialization

---

### 2. `test_repository_integration.py` ⭐ **Repository-Specific Tests**
**What it is:** Integration tests for the actual code in this repository

**Contains:**
- ✅ 7 passing tests (verified)
- Tests for the real `Website` class
- Tests for `build_system_prompt` functions
- Tests for `build_evaluation_prompt` functions
- Pattern demonstrations for common LLM tasks

**Best for:** Understanding how to test this codebase

**Run with:**
```bash
python tests/test_repository_integration.py
```

**Key Learning Points:**
- How to mock network requests with `@patch('requests.get')`
- Testing HTML parsing with BeautifulSoup
- Verifying Unicode handling
- Testing prompt construction
- Handling import issues gracefully

---

### 3. `test_website_and_utils.py` 📖 **Comprehensive Reference**
**What it is:** Detailed tests with extensive documentation

**Contains:**
- Tests for Website class (4 tests)
- Tests for OpenAI utils (3 tests)
- Tests for chatbot helpers (4 tests)
- Edge case tests (2 tests)

**Best for:** Deep dive into testing patterns

**Note:** Some tests may require additional dependencies

**Key Learning Points:**
- Mocking complex API responses
- Testing streaming responses
- Error handling patterns
- Edge case coverage

---

### 4. `TESTING_GUIDE.md` 📘 **Practical Guide**
**What it is:** Pattern-based guide for common LLM testing scenarios

**Contains:**
- Pattern 1: Testing Prompt Construction
- Pattern 2: Testing LLM API Calls (with Mocking)
- Pattern 3: Testing Streaming Responses
- Pattern 4: Testing Web Scraping Functions
- Pattern 5: Testing Gradio/Chat Interfaces
- Pattern 6: Testing Evaluation Functions

**Best for:** Copy-paste examples for your own tests

**Features:**
- Real code examples you can adapt
- Explanation of why each pattern matters
- Common mistakes to avoid
- Quick testing checklist

---

### 5. `README.md` 📄 **Setup & Instructions**
**What it is:** Complete guide to running and understanding the tests

**Contains:**
- Overview of the test suite
- How to run tests (multiple methods)
- Detailed explanation of each test file
- Testing concepts explained
- Best practices
- Troubleshooting guide

**Best for:** Getting started and reference

---

### 6. `requirements-test.txt` 📦
**What it is:** Python dependencies needed for testing

**Install with:**
```bash
pip install -r tests/requirements-test.txt
```

**Includes:**
- pytest and pytest plugins
- Mock and coverage tools
- Required dependencies (beautifulsoup4, requests, etc.)

---

### 7. Configuration Files

#### `pytest.ini` (in root directory)
- Configures pytest test discovery
- Sets verbose output by default
- Defines test markers

#### `__init__.py`
- Makes `tests/` a Python package
- Enables proper test discovery

---

## 🎯 Learning Path

### For Complete Beginners
1. **Read** `README.md` - Understand what testing is and why it matters
2. **Run** `test_examples_explained.py` - See tests in action
3. **Study** the code in `test_examples_explained.py` - Each test is thoroughly documented
4. **Experiment** - Modify tests and see what breaks

### For Those Familiar with Testing
1. **Start with** `TESTING_GUIDE.md` - See LLM-specific patterns
2. **Review** `test_repository_integration.py` - See real-world examples
3. **Reference** `test_website_and_utils.py` - Deep dive when needed

### For Writing Your Own Tests
1. **Copy patterns** from `TESTING_GUIDE.md`
2. **Adapt examples** from `test_examples_explained.py`
3. **Use** the checklist in `TESTING_GUIDE.md`

---

## 🚀 Quick Start

### Run All Standalone Tests (No Dependencies)
```bash
cd /home/runner/work/llm/llm
python tests/test_examples_explained.py
```
**Expected output:** All 19 tests pass ✅

### Run Integration Tests (Requires Dependencies)
```bash
python tests/test_repository_integration.py
```
**Expected output:** All 7 tests pass ✅

### Run with Pytest (More Features)
```bash
pip install pytest
pytest tests/ -v
```

### Generate Coverage Report
```bash
pip install pytest-cov
pytest tests/ --cov=src --cov-report=html
# Open htmlcov/index.html in browser
```

---

## 📊 Test Statistics

| File | Tests | Status | Dependencies |
|------|-------|--------|--------------|
| `test_examples_explained.py` | 19 | ✅ All Pass | None (stdlib only) |
| `test_repository_integration.py` | 7 | ✅ All Pass | beautifulsoup4, requests |
| `test_website_and_utils.py` | 13 | ⚠️ Some Skip | Full environment |

---

## 💡 Key Concepts Covered

### Testing Fundamentals
- ✅ Test structure and organization
- ✅ Assertions (assertEqual, assertIn, etc.)
- ✅ setUp and tearDown methods
- ✅ Test independence
- ✅ Descriptive test names

### Mocking & Patching
- ✅ Mock objects and return_value
- ✅ side_effect for exceptions
- ✅ @patch decorator
- ✅ Mocking API clients
- ✅ Verifying mock calls

### LLM-Specific Testing
- ✅ Testing prompt construction
- ✅ Mocking OpenAI/Anthropic APIs
- ✅ Testing streaming responses
- ✅ Testing chat history management
- ✅ Testing evaluation functions

### Web Scraping Testing
- ✅ Mocking requests.get
- ✅ Testing HTML parsing
- ✅ Unicode handling
- ✅ Error scenarios

### Best Practices
- ✅ Fast tests (no real API calls)
- ✅ Deterministic tests (same input → same output)
- ✅ Clear documentation
- ✅ Edge case coverage
- ✅ Error handling verification

---

## 🎓 What You'll Learn

After studying this test suite, you'll understand:

1. **How to write effective unit tests** for Python functions and classes
2. **How to use mocks** to test code with external dependencies
3. **How to test LLM applications** without making expensive API calls
4. **How to test web scraping** code without making network requests
5. **How to structure test files** for maintainability
6. **Best practices** for testing in general

---

## 🔍 Finding Examples

Looking for a specific testing pattern?

| I want to test... | See file | See function |
|------------------|----------|--------------|
| A simple function | `test_examples_explained.py` | `TestCalculateDiscount` |
| Error handling | `test_examples_explained.py` | `test_invalid_discount_too_high` |
| API calls | `test_examples_explained.py` | `TestFetchUserData` |
| Classes with state | `test_examples_explained.py` | `TestShoppingCart` |
| Time-dependent code | `test_examples_explained.py` | `TestGetGreeting` |
| Web scraping | `test_repository_integration.py` | `TestWebsiteClassIntegration` |
| LLM prompts | `test_repository_integration.py` | `TestPromptBuildingFunctions` |
| Streaming | `TESTING_GUIDE.md` | Pattern 3 |
| Chat interfaces | `TESTING_GUIDE.md` | Pattern 5 |

---

## 📝 Common Questions

### Q: Do I need API keys to run the tests?
**A:** No! The tests use mocks to simulate API calls. No real API keys needed.

### Q: Will running tests cost money?
**A:** No! Tests never make real API calls. They're completely free to run.

### Q: How long do tests take to run?
**A:** Very fast! `test_examples_explained.py` runs in ~0.003 seconds.

### Q: Can I modify the tests?
**A:** Yes! Please do. The best way to learn is by experimenting.

### Q: What if a test fails?
**A:** Read the error message carefully. It will tell you what was expected vs. what actually happened.

### Q: How do I add my own tests?
**A:** Copy a pattern from `test_examples_explained.py` or `TESTING_GUIDE.md` and adapt it.

---

## 🎯 Success Criteria

You've mastered this test suite when you can:

- [ ] Run all test files successfully
- [ ] Explain what each test is checking
- [ ] Identify which assertion is being used and why
- [ ] Understand how mocks replace real objects
- [ ] Write a new test for a simple function
- [ ] Mock an API call in a test
- [ ] Test error handling
- [ ] Use @patch to replace a dependency

---

## 🤝 Contributing

Want to add more tests? Great!

1. Follow the existing style (detailed docstrings)
2. Include explanations of what and why
3. Make sure tests are independent
4. Use mocks for external dependencies
5. Run the test to verify it works

---

## 📚 Additional Resources

- [Python unittest docs](https://docs.python.org/3/library/unittest.html)
- [unittest.mock guide](https://docs.python.org/3/library/unittest.mock.html)
- [Pytest documentation](https://docs.pytest.org/)
- [Testing Best Practices](https://docs.python-guide.org/writing/tests/)

---

## 🎉 Summary

This test suite is designed to be:
- **Educational** - Detailed explanations of concepts
- **Practical** - Real examples you can use
- **Comprehensive** - Covers many testing scenarios
- **Accessible** - No dependencies for basic examples
- **Maintainable** - Well-organized and documented

**Start with `test_examples_explained.py` and work your way through!**

Happy Testing! 🧪✨
