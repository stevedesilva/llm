"""
Product of Array Except Self (LeetCode #238)

Problem:
Given an integer array nums, return an array answer such that answer[i] is equal to the 
product of all the elements of nums except nums[i].

The product of any prefix or suffix of nums is guaranteed to fit in a 32-bit integer.

You must write an algorithm that runs in O(n) time and without using the division operation.

Example 1:
    Input: nums = [1,2,3,4]
    Output: [24,12,8,6]

Example 2:
    Input: nums = [-1,1,0,-3,3]
    Output: [0,0,9,0,0]

Constraints:
    - 2 <= nums.length <= 10^5
    - -30 <= nums[i] <= 30
    - The product of any prefix or suffix of nums is guaranteed to fit in a 32-bit integer.

Follow up: Can you solve the problem in O(1) extra space complexity? 
(The output array does not count as extra space for space complexity analysis.)

Staff+ Focus:
    - Invariant: answer[i] = product_of_prefix[i] * product_of_suffix[i]
    - O(1) space solution: Build result array in-place using two passes
    - No division operation allowed - must handle zeros elegantly
"""

from typing import List


def product_except_self(nums: List[int]) -> List[int]:
    """
    Calculate product of array except self using O(1) extra space.
    
    Approach: Two-pass algorithm
    1. First pass (left to right): Build prefix products in result array
    2. Second pass (right to left): Multiply by suffix products using running variable
    
    Key Insight: answer[i] = (product of all elements left of i) * (product of all elements right of i)
    
    Time Complexity: O(n) - two passes through array
    Space Complexity: O(1) - excluding output array, only using constant extra space
    
    Args:
        nums: Input array of integers
        
    Returns:
        Array where result[i] is product of all nums except nums[i]
        
    Invariant maintained:
    - After first pass: result[i] contains product of all elements to the left of i
    - After second pass: result[i] contains product of all elements except nums[i]
    """
    n = len(nums)
    result = [1] * n
    
    # First pass: calculate prefix products
    # result[i] will contain product of all elements to the left of nums[i]
    prefix = 1
    for i in range(n):
        result[i] = prefix
        prefix *= nums[i]
    
    # Second pass: multiply by suffix products
    # Multiply result[i] by product of all elements to the right of nums[i]
    suffix = 1
    for i in range(n - 1, -1, -1):
        result[i] *= suffix
        suffix *= nums[i]
    
    return result


def product_except_self_with_arrays(nums: List[int]) -> List[int]:
    """
    Solution using O(n) extra space for clarity.
    This shows the concept more explicitly but uses extra space.
    
    Time Complexity: O(n)
    Space Complexity: O(n) - two auxiliary arrays
    """
    n = len(nums)
    prefix = [1] * n
    suffix = [1] * n
    result = [1] * n
    
    # Build prefix products
    for i in range(1, n):
        prefix[i] = prefix[i - 1] * nums[i - 1]
    
    # Build suffix products
    for i in range(n - 2, -1, -1):
        suffix[i] = suffix[i + 1] * nums[i + 1]
    
    # Combine prefix and suffix
    for i in range(n):
        result[i] = prefix[i] * suffix[i]
    
    return result


if __name__ == "__main__":
    # Test cases
    test_cases = [
        ([1, 2, 3, 4], [24, 12, 8, 6]),
        ([-1, 1, 0, -3, 3], [0, 0, 9, 0, 0]),
        ([2, 3, 4, 5], [60, 40, 30, 24]),
        ([1, 1, 1, 1], [1, 1, 1, 1]),
        ([5, 2], [2, 5]),
    ]
    
    print("Product of Array Except Self Solutions:")
    print("=" * 60)
    
    for nums, expected in test_cases:
        result_o1 = product_except_self(nums)
        result_on = product_except_self_with_arrays(nums)
        
        status_o1 = "✓" if result_o1 == expected else "✗"
        status_on = "✓" if result_on == expected else "✗"
        
        print(f"{status_o1} O(1) space: nums={nums}")
        print(f"  Output: {result_o1}")
        print(f"  Expected: {expected}")
        print(f"{status_on} O(n) space: {result_on}")
        print()
