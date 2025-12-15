"""
Standalone Test Examples with Detailed Explanations

This file contains self-contained test examples that demonstrate testing concepts
without complex dependencies. Perfect for learning and reference.

Topics covered:
1. Basic unit testing structure
2. Testing functions with mocks
3. Testing classes and methods
4. Error handling tests
5. Edge case testing
"""

import unittest
from unittest.mock import Mock, patch, MagicMock


# ============================================================================
# EXAMPLE 1: Simple Function Testing
# ============================================================================

def calculate_discount(price, discount_percent):
    """
    Calculate discounted price.
    
    Args:
        price: Original price
        discount_percent: Discount as percentage (0-100)
        
    Returns:
        Discounted price
        
    Explanation:
    - This is a simple pure function (no side effects)
    - Easy to test because output only depends on inputs
    - No mocking needed for pure functions
    """
    if discount_percent < 0 or discount_percent > 100:
        raise ValueError("Discount must be between 0 and 100")
    return price * (1 - discount_percent / 100)


class TestCalculateDiscount(unittest.TestCase):
    """
    Test Suite for calculate_discount function
    
    Demonstrates:
    - Testing normal cases
    - Testing edge cases (0%, 100% discount)
    - Testing error cases (invalid input)
    """
    
    def test_normal_discount(self):
        """
        Test: Normal discount calculation (20% off $100)
        
        Explanation:
        - Test the most common use case first
        - Use exact values to avoid floating point issues
        - Clear assertion shows expected behavior
        
        Why this matters:
        - Validates core functionality works
        - Catches calculation errors
        - Documents expected behavior
        """
        result = calculate_discount(100, 20)
        self.assertEqual(result, 80.0)
    
    def test_zero_discount(self):
        """
        Test: Zero discount returns original price
        
        Explanation:
        - Edge case: what happens when discount is 0?
        - Should return original price unchanged
        - Tests boundary condition
        
        Edge cases are important because:
        - They often reveal bugs
        - They clarify intended behavior
        - They prevent division by zero, etc.
        """
        result = calculate_discount(100, 0)
        self.assertEqual(result, 100.0)
    
    def test_full_discount(self):
        """
        Test: 100% discount makes item free
        
        Explanation:
        - Another edge case: maximum possible discount
        - Should result in price of 0
        """
        result = calculate_discount(100, 100)
        self.assertEqual(result, 0.0)
    
    def test_invalid_discount_too_high(self):
        """
        Test: Discount over 100% raises ValueError
        
        Explanation:
        - Tests error handling
        - Uses assertRaises context manager
        - Validates error message is helpful
        
        Testing errors is critical:
        - Ensures invalid input is rejected
        - Provides clear feedback to users
        - Prevents unexpected behavior
        """
        with self.assertRaises(ValueError) as context:
            calculate_discount(100, 150)
        self.assertIn("between 0 and 100", str(context.exception))
    
    def test_invalid_discount_negative(self):
        """Test: Negative discount raises ValueError"""
        with self.assertRaises(ValueError):
            calculate_discount(100, -10)


# ============================================================================
# EXAMPLE 2: Testing with Mocks
# ============================================================================

def fetch_user_data(user_id, api_client):
    """
    Fetch user data from an API.
    
    Args:
        user_id: ID of user to fetch
        api_client: API client object with a get method
        
    Returns:
        User data dictionary
        
    Explanation:
    - This function depends on an external API
    - We can't make real API calls in tests
    - Solution: mock the api_client
    """
    try:
        response = api_client.get(f"/users/{user_id}")
        if response.status_code == 200:
            return response.json()
        else:
            return {"error": f"Failed with status {response.status_code}"}
    except Exception as e:
        return {"error": str(e)}


class TestFetchUserData(unittest.TestCase):
    """
    Test Suite for fetch_user_data function
    
    Demonstrates:
    - Using Mock objects
    - Testing success and failure paths
    - Avoiding real API calls
    """
    
    def test_successful_fetch(self):
        """
        Test: Successfully fetch user data
        
        Explanation:
        - Create a mock API client
        - Configure it to return a successful response
        - Verify our function processes it correctly
        
        Mocking benefits:
        - Tests run instantly (no network delay)
        - Tests are reliable (no network failures)
        - Tests are free (no API costs)
        - Tests work offline
        """
        # Create a mock API client
        mock_api = Mock()
        
        # Configure the mock response
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            "id": 123,
            "name": "John Doe",
            "email": "john@example.com"
        }
        
        # Make the mock client return our mock response
        mock_api.get.return_value = mock_response
        
        # Call the function with the mock
        result = fetch_user_data(123, mock_api)
        
        # Verify the results
        self.assertEqual(result["id"], 123)
        self.assertEqual(result["name"], "John Doe")
        
        # Verify the API was called correctly
        mock_api.get.assert_called_once_with("/users/123")
    
    def test_fetch_with_404_error(self):
        """
        Test: Handle 404 not found error
        
        Explanation:
        - Configure mock to return 404 status
        - Verify our function handles it gracefully
        - Returns error dictionary instead of crashing
        """
        mock_api = Mock()
        mock_response = Mock()
        mock_response.status_code = 404
        mock_api.get.return_value = mock_response
        
        result = fetch_user_data(999, mock_api)
        
        self.assertIn("error", result)
        self.assertIn("404", result["error"])
    
    def test_fetch_with_exception(self):
        """
        Test: Handle network exceptions
        
        Explanation:
        - Configure mock to raise an exception
        - Verify exception is caught and converted to error dict
        - Ensures application doesn't crash
        """
        mock_api = Mock()
        mock_api.get.side_effect = ConnectionError("Network unavailable")
        
        result = fetch_user_data(123, mock_api)
        
        self.assertIn("error", result)
        self.assertIn("Network unavailable", result["error"])


# ============================================================================
# EXAMPLE 3: Testing Classes
# ============================================================================

class ShoppingCart:
    """
    Simple shopping cart implementation.
    
    Demonstrates:
    - Class with state (items list)
    - Methods that modify state
    - Methods that query state
    """
    
    def __init__(self):
        """Initialize empty cart"""
        self.items = []
    
    def add_item(self, name, price, quantity=1):
        """Add item to cart"""
        if price < 0:
            raise ValueError("Price cannot be negative")
        if quantity < 1:
            raise ValueError("Quantity must be at least 1")
        
        self.items.append({
            "name": name,
            "price": price,
            "quantity": quantity
        })
    
    def get_total(self):
        """Calculate total price of all items"""
        return sum(item["price"] * item["quantity"] for item in self.items)
    
    def get_item_count(self):
        """Get total number of items (counting quantities)"""
        return sum(item["quantity"] for item in self.items)
    
    def clear(self):
        """Remove all items from cart"""
        self.items = []


class TestShoppingCart(unittest.TestCase):
    """
    Test Suite for ShoppingCart class
    
    Demonstrates:
    - setUp method to create fresh instance for each test
    - Testing state changes
    - Testing calculations
    """
    
    def setUp(self):
        """
        Set up method runs before each test
        
        Explanation:
        - Creates a fresh ShoppingCart instance
        - Ensures tests are independent
        - Prevents one test from affecting another
        
        Why use setUp:
        - Reduces code duplication
        - Ensures clean state for each test
        - Makes tests more maintainable
        """
        self.cart = ShoppingCart()
    
    def test_empty_cart_total_is_zero(self):
        """
        Test: New cart has zero total
        
        Explanation:
        - Tests initial state
        - Verifies no items = $0 total
        """
        self.assertEqual(self.cart.get_total(), 0)
        self.assertEqual(self.cart.get_item_count(), 0)
    
    def test_add_single_item(self):
        """
        Test: Add one item to cart
        
        Explanation:
        - Tests basic add_item functionality
        - Verifies item is stored
        - Checks total is calculated correctly
        """
        self.cart.add_item("Apple", 1.50)
        
        self.assertEqual(self.cart.get_item_count(), 1)
        self.assertEqual(self.cart.get_total(), 1.50)
        self.assertEqual(len(self.cart.items), 1)
        self.assertEqual(self.cart.items[0]["name"], "Apple")
    
    def test_add_multiple_quantities(self):
        """
        Test: Add item with quantity > 1
        
        Explanation:
        - Tests quantity parameter
        - Verifies total calculation includes quantity
        """
        self.cart.add_item("Orange", 2.00, quantity=3)
        
        self.assertEqual(self.cart.get_item_count(), 3)
        self.assertEqual(self.cart.get_total(), 6.00)
    
    def test_add_multiple_items(self):
        """
        Test: Add several different items
        
        Explanation:
        - Tests that cart can hold multiple items
        - Verifies total is sum of all items
        """
        self.cart.add_item("Banana", 0.50, quantity=6)
        self.cart.add_item("Milk", 3.00)
        
        self.assertEqual(self.cart.get_item_count(), 7)
        self.assertEqual(self.cart.get_total(), 6.00)  # 0.50*6 + 3.00*1
    
    def test_add_item_negative_price_raises_error(self):
        """
        Test: Cannot add item with negative price
        
        Explanation:
        - Tests input validation
        - Prevents invalid data from entering system
        """
        with self.assertRaises(ValueError) as context:
            self.cart.add_item("Invalid", -5.00)
        self.assertIn("negative", str(context.exception).lower())
    
    def test_add_item_zero_quantity_raises_error(self):
        """Test: Cannot add item with zero quantity"""
        with self.assertRaises(ValueError):
            self.cart.add_item("Invalid", 10.00, quantity=0)
    
    def test_clear_cart(self):
        """
        Test: Clear removes all items
        
        Explanation:
        - Add items, then clear
        - Verify cart is empty after clear
        - Tests state reset functionality
        """
        self.cart.add_item("Item1", 5.00)
        self.cart.add_item("Item2", 3.00)
        
        self.cart.clear()
        
        self.assertEqual(self.cart.get_total(), 0)
        self.assertEqual(self.cart.get_item_count(), 0)
        self.assertEqual(len(self.cart.items), 0)


# ============================================================================
# EXAMPLE 4: Testing with Patches
# ============================================================================

import datetime


def get_greeting():
    """
    Return greeting based on current time.
    
    Returns:
        "Good morning", "Good afternoon", or "Good evening"
        
    Explanation:
    - Depends on datetime.datetime.now() (system time)
    - Hard to test without mocking
    - Time-dependent logic needs controlled testing
    """
    current_hour = datetime.datetime.now().hour
    
    if current_hour < 12:
        return "Good morning"
    elif current_hour < 18:
        return "Good afternoon"
    else:
        return "Good evening"


class TestGetGreeting(unittest.TestCase):
    """
    Test Suite for get_greeting function
    
    Demonstrates:
    - Using @patch decorator
    - Testing time-dependent code
    - Controlling external dependencies
    """
    
    @patch('datetime.datetime')
    def test_morning_greeting(self, mock_datetime):
        """
        Test: Returns "Good morning" before noon
        
        Explanation:
        - Use @patch to replace datetime.datetime
        - Set mock to return 9 AM
        - Verify morning greeting is returned
        
        Why patch datetime:
        - Makes test deterministic (always same result)
        - Can test all time periods
        - Tests run at same speed regardless of time
        """
        # Create a mock datetime object for 9 AM
        mock_now = Mock()
        mock_now.hour = 9
        mock_datetime.now.return_value = mock_now
        
        result = get_greeting()
        self.assertEqual(result, "Good morning")
    
    @patch('datetime.datetime')
    def test_afternoon_greeting(self, mock_datetime):
        """Test: Returns "Good afternoon" between 12-6 PM"""
        mock_now = Mock()
        mock_now.hour = 15  # 3 PM
        mock_datetime.now.return_value = mock_now
        
        result = get_greeting()
        self.assertEqual(result, "Good afternoon")
    
    @patch('datetime.datetime')
    def test_evening_greeting(self, mock_datetime):
        """Test: Returns "Good evening" after 6 PM"""
        mock_now = Mock()
        mock_now.hour = 20  # 8 PM
        mock_datetime.now.return_value = mock_now
        
        result = get_greeting()
        self.assertEqual(result, "Good evening")
    
    @patch('datetime.datetime')
    def test_boundary_noon(self, mock_datetime):
        """
        Test: Boundary condition at exactly noon
        
        Explanation:
        - Tests edge case: exactly 12:00
        - Clarifies which greeting to show
        - Boundary conditions often have bugs
        """
        mock_now = Mock()
        mock_now.hour = 12
        mock_datetime.now.return_value = mock_now
        
        result = get_greeting()
        self.assertEqual(result, "Good afternoon")


# ============================================================================
# SUMMARY AND BEST PRACTICES
# ============================================================================

"""
KEY TESTING CONCEPTS DEMONSTRATED:

1. UNIT TEST STRUCTURE
   - Test class inherits from unittest.TestCase
   - Test methods start with test_
   - Use descriptive test names
   - Include docstrings explaining what and why

2. ASSERTIONS
   - assertEqual(a, b) - values must be equal
   - assertIn(a, b) - a must be in b
   - assertRaises(Exception) - code must raise exception
   - assertTrue/assertFalse - boolean checks

3. MOCKING
   - Mock() - create fake object
   - mock.return_value - set what mock returns
   - mock.side_effect - make mock raise exception
   - mock.assert_called_once() - verify mock was used

4. PATCHING
   - @patch('module.function') - replace real function
   - Useful for time, random, API calls, file I/O
   - Makes tests deterministic and fast

5. TEST ORGANIZATION
   - setUp() - runs before each test
   - tearDown() - runs after each test (not shown)
   - Group related tests in same class
   - One assertion per test when possible

6. BEST PRACTICES
   ✅ Test normal cases first
   ✅ Test edge cases (0, empty, max values)
   ✅ Test error conditions
   ✅ Use mocks for external dependencies
   ✅ Keep tests independent
   ✅ Make tests fast
   ✅ Write clear test names
   ✅ Document why test exists

7. COMMON PATTERNS

   Testing a pure function:
   def test_function():
       result = my_function(input)
       self.assertEqual(result, expected)
   
   Testing with mock:
   def test_with_mock():
       mock = Mock()
       mock.method.return_value = "value"
       result = function_using_mock(mock)
       self.assertEqual(result, expected)
   
   Testing exceptions:
   def test_error():
       with self.assertRaises(ValueError):
           function_that_should_error()
   
   Testing with patch:
   @patch('module.dependency')
   def test_patched(self, mock_dep):
       mock_dep.return_value = "value"
       result = function()
       self.assertEqual(result, expected)

REMEMBER:
- Tests document how code should work
- Tests catch bugs before production
- Tests enable refactoring with confidence
- Good tests are as important as good code
"""


# Run tests if this file is executed directly
if __name__ == '__main__':
    # Run with verbose output
    unittest.main(verbosity=2)
