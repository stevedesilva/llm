"""
Comprehensive test suite for Week 1 DSA problems.

Tests all implemented solutions with various test cases including:
- Normal cases
- Edge cases
- Boundary conditions
- Special cases (zeros, negatives, duplicates)
"""

import sys
from typing import List, Callable

# Import all solutions
from two_sum import two_sum, two_sum_brute_force
from container_with_most_water import max_area, max_area_brute_force
from trapping_rain_water import trap, trap_dp
from product_of_array_except_self import product_except_self, product_except_self_with_arrays
from move_zeroes import move_zeroes, move_zeroes_swap, move_zeroes_optimal


class TestRunner:
    """Simple test runner for algorithm problems."""
    
    def __init__(self):
        self.total_tests = 0
        self.passed_tests = 0
        self.failed_tests = 0
    
    def test(self, name: str, func: Callable, input_args: tuple, expected: any) -> bool:
        """Run a single test case."""
        self.total_tests += 1
        try:
            result = func(*input_args)
            if result == expected:
                self.passed_tests += 1
                print(f"  ✓ {name}")
                return True
            else:
                self.failed_tests += 1
                print(f"  ✗ {name}")
                print(f"    Input: {input_args}")
                print(f"    Expected: {expected}")
                print(f"    Got: {result}")
                return False
        except Exception as e:
            self.failed_tests += 1
            print(f"  ✗ {name} - Exception: {e}")
            return False
    
    def summary(self):
        """Print test summary."""
        print("\n" + "=" * 60)
        print(f"Test Summary: {self.passed_tests}/{self.total_tests} passed")
        if self.failed_tests > 0:
            print(f"Failed: {self.failed_tests}")
            return False
        else:
            print("All tests passed! ✓")
            return True


def test_two_sum():
    """Test Two Sum problem."""
    print("\n1. Testing Two Sum")
    print("-" * 60)
    runner = TestRunner()
    
    runner.test("Basic case 1", two_sum, ([2, 7, 11, 15], 9), [0, 1])
    runner.test("Basic case 2", two_sum, ([3, 2, 4], 6), [1, 2])
    runner.test("Duplicate numbers", two_sum, ([3, 3], 6), [0, 1])
    runner.test("Negative numbers", two_sum, ([-1, -2, -3, -4, -5], -8), [2, 4])
    runner.test("Large numbers", two_sum, ([1000000, 2000000, 3000000], 5000000), [1, 2])
    
    return runner.summary()


def test_container_with_most_water():
    """Test Container With Most Water problem."""
    print("\n2. Testing Container With Most Water")
    print("-" * 60)
    runner = TestRunner()
    
    runner.test("Example 1", max_area, ([1, 8, 6, 2, 5, 4, 8, 3, 7],), 49)
    runner.test("Example 2", max_area, ([1, 1],), 1)
    runner.test("Increasing heights", max_area, ([1, 2, 3, 4, 5],), 6)
    runner.test("Decreasing heights", max_area, ([5, 4, 3, 2, 1],), 6)
    runner.test("Equal heights", max_area, ([4, 4, 4, 4],), 12)
    runner.test("Two tall ends", max_area, ([4, 3, 2, 1, 4],), 16)
    
    return runner.summary()


def test_trapping_rain_water():
    """Test Trapping Rain Water problem."""
    print("\n3. Testing Trapping Rain Water")
    print("-" * 60)
    runner = TestRunner()
    
    runner.test("Example 1", trap, ([0, 1, 0, 2, 1, 0, 1, 3, 2, 1, 2, 1],), 6)
    runner.test("Example 2", trap, ([4, 2, 0, 3, 2, 5],), 9)
    runner.test("Simple valley", trap, ([3, 0, 2, 0, 4],), 7)
    runner.test("Multiple valleys", trap, ([0, 1, 0, 2, 1, 0, 3, 1, 0, 1, 2],), 8)
    runner.test("Descending slope", trap, ([5, 4, 1, 2],), 1)
    runner.test("Small valley", trap, ([2, 1, 2],), 1)
    runner.test("All zeros", trap, ([0, 0, 0],), 0)
    
    # Test both implementations match
    test_case = [4, 2, 0, 3, 2, 5]
    runner.test("Two-pointer matches DP", lambda x: trap(x) == trap_dp(x), (test_case,), True)
    
    return runner.summary()


def test_product_except_self():
    """Test Product of Array Except Self problem."""
    print("\n4. Testing Product of Array Except Self")
    print("-" * 60)
    runner = TestRunner()
    
    runner.test("Example 1", product_except_self, ([1, 2, 3, 4],), [24, 12, 8, 6])
    runner.test("With zero", product_except_self, ([-1, 1, 0, -3, 3],), [0, 0, 9, 0, 0])
    runner.test("All same", product_except_self, ([1, 1, 1, 1],), [1, 1, 1, 1])
    runner.test("Two elements", product_except_self, ([5, 2],), [2, 5])
    runner.test("With negative", product_except_self, ([-1, 2, -3, 4],), [-24, 12, -8, 6])
    
    # Test both implementations match
    test_case = [2, 3, 4, 5]
    result_o1 = product_except_self(test_case)
    result_on = product_except_self_with_arrays(test_case)
    runner.test("O(1) matches O(n)", lambda: result_o1 == result_on, (), True)
    
    return runner.summary()


def test_move_zeroes():
    """Test Move Zeroes problem."""
    print("\n5. Testing Move Zeroes")
    print("-" * 60)
    runner = TestRunner()
    
    def test_move_zeroes_case(nums: List[int], expected: List[int]) -> bool:
        """Helper to test move_zeroes which modifies in-place."""
        test_nums = nums.copy()
        move_zeroes(test_nums)
        return test_nums == expected
    
    runner.test("Example 1", test_move_zeroes_case, ([0, 1, 0, 3, 12], [1, 3, 12, 0, 0]), True)
    runner.test("Single zero", test_move_zeroes_case, ([0], [0]), True)
    runner.test("No zeros", test_move_zeroes_case, ([1, 2, 3], [1, 2, 3]), True)
    runner.test("Leading zeros", test_move_zeroes_case, ([0, 0, 1], [1, 0, 0]), True)
    runner.test("Multiple zeros", test_move_zeroes_case, ([1, 0, 0, 2, 0, 3], [1, 2, 3, 0, 0, 0]), True)
    runner.test("No zeros at all", test_move_zeroes_case, ([2, 1], [2, 1]), True)
    
    # Test all three implementations match
    test_case = [0, 1, 0, 3, 12]
    nums1, nums2, nums3 = test_case.copy(), test_case.copy(), test_case.copy()
    move_zeroes(nums1)
    move_zeroes_swap(nums2)
    move_zeroes_optimal(nums3)
    runner.test("All implementations match", lambda: nums1 == nums2 == nums3, (), True)
    
    return runner.summary()


def main():
    """Run all tests."""
    print("=" * 60)
    print("Week 1: Arrays, Strings, Two Pointers - Test Suite")
    print("=" * 60)
    
    all_passed = True
    
    all_passed &= test_two_sum()
    all_passed &= test_container_with_most_water()
    all_passed &= test_trapping_rain_water()
    all_passed &= test_product_except_self()
    all_passed &= test_move_zeroes()
    
    print("\n" + "=" * 60)
    if all_passed:
        print("🎉 ALL TESTS PASSED! 🎉")
        print("=" * 60)
        return 0
    else:
        print("❌ SOME TESTS FAILED")
        print("=" * 60)
        return 1


if __name__ == "__main__":
    sys.exit(main())
