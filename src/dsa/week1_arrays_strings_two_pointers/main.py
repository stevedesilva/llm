"""
Week 1: Arrays, Strings, Two Pointers - Main Entry Point

Run all problem solutions with example cases.
"""

from two_sum import two_sum
from container_with_most_water import max_area
from trapping_rain_water import trap
from product_of_array_except_self import product_except_self
from move_zeroes import move_zeroes


def print_header(title: str):
    """Print a formatted header."""
    print("\n" + "=" * 60)
    print(title)
    print("=" * 60)


def run_two_sum():
    """Demonstrate Two Sum solution."""
    print_header("1. Two Sum")
    
    examples = [
        ([2, 7, 11, 15], 9),
        ([3, 2, 4], 6),
        ([3, 3], 6),
    ]
    
    for nums, target in examples:
        result = two_sum(nums, target)
        print(f"nums = {nums}, target = {target}")
        print(f"Output: {result}")
        print(f"Verification: nums[{result[0]}] + nums[{result[1]}] = "
              f"{nums[result[0]]} + {nums[result[1]]} = {nums[result[0]] + nums[result[1]]}")
        print()


def run_container_with_most_water():
    """Demonstrate Container With Most Water solution."""
    print_header("2. Container With Most Water")
    
    examples = [
        [1, 8, 6, 2, 5, 4, 8, 3, 7],
        [1, 1],
        [4, 3, 2, 1, 4],
    ]
    
    for height in examples:
        result = max_area(height)
        print(f"height = {height}")
        print(f"Max area = {result}")
        print()


def run_trapping_rain_water():
    """Demonstrate Trapping Rain Water solution."""
    print_header("3. Trapping Rain Water")
    
    examples = [
        [0, 1, 0, 2, 1, 0, 1, 3, 2, 1, 2, 1],
        [4, 2, 0, 3, 2, 5],
        [3, 0, 2, 0, 4],
    ]
    
    for height in examples:
        result = trap(height)
        print(f"height = {height}")
        print(f"Water trapped = {result} units")
        print()


def run_product_except_self():
    """Demonstrate Product of Array Except Self solution."""
    print_header("4. Product of Array Except Self")
    
    examples = [
        [1, 2, 3, 4],
        [-1, 1, 0, -3, 3],
        [2, 3, 4, 5],
    ]
    
    for nums in examples:
        result = product_except_self(nums)
        print(f"nums = {nums}")
        print(f"Output = {result}")
        
        # Verify result
        verification = []
        for i in range(len(nums)):
            product = 1
            for j in range(len(nums)):
                if i != j:
                    product *= nums[j]
            verification.append(product)
        print(f"Verification: {verification}")
        print()


def run_move_zeroes():
    """Demonstrate Move Zeroes solution."""
    print_header("5. Move Zeroes")
    
    examples = [
        [0, 1, 0, 3, 12],
        [0],
        [1, 0, 0, 2, 0, 3],
    ]
    
    for nums in examples:
        original = nums.copy()
        move_zeroes(nums)
        print(f"Input:  {original}")
        print(f"Output: {nums}")
        print()


def main():
    """Run all problem demonstrations."""
    print("=" * 60)
    print("Week 1: Arrays, Strings, Two Pointers")
    print("Demonstration of All Solutions")
    print("=" * 60)
    
    run_two_sum()
    run_container_with_most_water()
    run_trapping_rain_water()
    run_product_except_self()
    run_move_zeroes()
    
    print("=" * 60)
    print("Staff+ Focus Areas:")
    print("=" * 60)
    print("✓ Invariants - Each solution maintains clear loop invariants")
    print("✓ In-place Operations - Move Zeroes, Product Except Self")
    print("✓ O(1) Space - Container, Trapping Rain Water, Move Zeroes")
    print("✓ Two-Pointer Techniques - Container, Trapping, Move Zeroes")
    print("✓ Optimal Time Complexity - All solutions are O(n)")
    print("=" * 60)
    print("\nTo run tests: python test_week1.py")
    print("=" * 60)


if __name__ == "__main__":
    main()
