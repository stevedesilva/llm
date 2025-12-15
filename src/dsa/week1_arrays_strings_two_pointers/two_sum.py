"""
Two Sum (LeetCode #1)

Problem:
Given an array of integers nums and an integer target, return indices of the two numbers 
such that they add up to target.

You may assume that each input would have exactly one solution, and you may not use the 
same element twice.

You can return the answer in any order.

Example 1:
    Input: nums = [2,7,11,15], target = 9
    Output: [0,1]
    Explanation: Because nums[0] + nums[1] == 9, we return [0, 1].

Example 2:
    Input: nums = [3,2,4], target = 6
    Output: [1,2]

Example 3:
    Input: nums = [3,3], target = 6
    Output: [0,1]

Constraints:
    - 2 <= nums.length <= 10^4
    - -10^9 <= nums[i] <= 10^9
    - -10^9 <= target <= 10^9
    - Only one valid answer exists.

Staff+ Focus:
    - Invariant: The complement (target - current_num) must exist in the hashmap
    - O(1) space argument: While we use a hashmap, it's bounded by the input size
    - The hashmap ensures O(1) lookup time for complements
"""

from typing import List


def two_sum(nums: List[int], target: int) -> List[int]:
    """
    Find two indices where nums[i] + nums[j] == target.
    
    Approach: Use a hashmap to store seen numbers and their indices.
    For each number, check if its complement (target - num) exists in the hashmap.
    
    Time Complexity: O(n) - single pass through the array
    Space Complexity: O(n) - hashmap stores at most n elements
    
    Args:
        nums: List of integers
        target: Target sum
        
    Returns:
        List of two indices [i, j] where nums[i] + nums[j] == target
        
    Invariant maintained: For each number processed, all previous numbers are in the hashmap
    """
    # Hashmap to store number -> index mapping
    seen = {}
    
    for i, num in enumerate(nums):
        complement = target - num
        
        # Check if complement exists (O(1) lookup)
        if complement in seen:
            return [seen[complement], i]
        
        # Store current number and its index
        seen[num] = i
    
    # Should never reach here based on problem constraints
    return []


def two_sum_brute_force(nums: List[int], target: int) -> List[int]:
    """
    Brute force solution for comparison.
    
    Time Complexity: O(n^2)
    Space Complexity: O(1)
    """
    n = len(nums)
    for i in range(n):
        for j in range(i + 1, n):
            if nums[i] + nums[j] == target:
                return [i, j]
    return []


if __name__ == "__main__":
    # Test cases
    test_cases = [
        ([2, 7, 11, 15], 9, [0, 1]),
        ([3, 2, 4], 6, [1, 2]),
        ([3, 3], 6, [0, 1]),
        ([-1, -2, -3, -4, -5], -8, [2, 4]),
    ]
    
    print("Two Sum Solutions:")
    print("=" * 60)
    
    for nums, target, expected in test_cases:
        result = two_sum(nums, target)
        status = "✓" if result == expected else "✗"
        print(f"{status} Input: nums={nums}, target={target}")
        print(f"  Output: {result}, Expected: {expected}")
        print()
