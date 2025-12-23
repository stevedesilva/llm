"""
Trapping Rain Water (LeetCode #42)

Problem:
Given n non-negative integers representing an elevation map where the width of each bar is 1, 
compute how much water it can trap after raining.

Example 1:
    Input: height = [0,1,0,2,1,0,1,3,2,1,2,1]
    Output: 6
    Explanation: The elevation map traps 6 units of water.

Example 2:
    Input: height = [4,2,0,3,2,5]
    Output: 9

Constraints:
    - n == height.length
    - 1 <= n <= 2 * 10^4
    - 0 <= height[i] <= 10^5

Staff+ Focus:
    - Invariant: Water at position i = min(max_left, max_right) - height[i]
    - Two-pointer technique with O(1) space
    - Key insight: Process from both ends, tracking running max heights
"""

from typing import List


def trap(height: List[int]) -> int:
    """
    Calculate trapped rainwater using two-pointer technique with O(1) space.
    
    Approach: Use two pointers starting from both ends.
    - Track max heights seen from left (left_max) and right (right_max)
    - Water trapped at a position depends on min(left_max, right_max) - current_height
    - Move pointer with smaller max height inward
    
    Key Invariant: At each position, we only need to know the minimum of max_left and max_right
    to calculate trapped water. We don't need to know both maximums precisely.
    
    Time Complexity: O(n) - single pass through array
    Space Complexity: O(1) - only using pointers and running max variables
    
    Args:
        height: List of non-negative integers representing elevation map
        
    Returns:
        Total units of water trapped
    """
    if not height or len(height) < 3:
        return 0
    
    left = 0
    right = len(height) - 1
    left_max = 0
    right_max = 0
    water = 0
    
    while left < right:
        # Update running maximums
        left_max = max(left_max, height[left])
        right_max = max(right_max, height[right])
        
        # Process the side with smaller max height
        # This maintains the invariant that we have enough information
        # to calculate water at this position
        if left_max < right_max:
            # Water trapped at left position
            water += left_max - height[left]
            left += 1
        else:
            # Water trapped at right position
            water += right_max - height[right]
            right -= 1
    
    return water


def trap_dp(height: List[int]) -> int:
    """
    Dynamic Programming solution with O(n) space.
    Pre-compute max heights from left and right for each position.
    
    Time Complexity: O(n)
    Space Complexity: O(n) - two auxiliary arrays
    """
    if not height or len(height) < 3:
        return 0
    
    n = len(height)
    left_max = [0] * n
    right_max = [0] * n
    
    # Build left_max array
    left_max[0] = height[0]
    for i in range(1, n):
        left_max[i] = max(left_max[i - 1], height[i])
    
    # Build right_max array
    right_max[n - 1] = height[n - 1]
    for i in range(n - 2, -1, -1):
        right_max[i] = max(right_max[i + 1], height[i])
    
    # Calculate trapped water
    water = 0
    for i in range(n):
        water += min(left_max[i], right_max[i]) - height[i]
    
    return water


if __name__ == "__main__":
    # Test cases
    test_cases = [
        ([0, 1, 0, 2, 1, 0, 1, 3, 2, 1, 2, 1], 6),
        ([4, 2, 0, 3, 2, 5], 9),
        ([3, 0, 2, 0, 4], 7),
        ([0, 1, 0, 2, 1, 0, 3, 1, 0, 1, 2], 8),
        ([5, 4, 1, 2], 1),
        ([2, 1, 2], 1),
        ([3, 0, 0, 2, 0, 4], 10),
    ]
    
    print("Trapping Rain Water Solutions:")
    print("=" * 60)
    
    for height, expected in test_cases:
        result_two_pointer = trap(height)
        result_dp = trap_dp(height)
        
        status_tp = "✓" if result_two_pointer == expected else "✗"
        status_dp = "✓" if result_dp == expected else "✗"
        
        print(f"{status_tp} Two-Pointer: height={height}")
        print(f"  Output: {result_two_pointer}, Expected: {expected}")
        print(f"{status_dp} DP Solution: {result_dp}")
        print()
