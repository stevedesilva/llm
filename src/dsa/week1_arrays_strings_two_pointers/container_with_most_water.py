"""
Container With Most Water (LeetCode #11)

Problem:
You are given an integer array height of length n. There are n vertical lines drawn such that 
the two endpoints of the ith line are (i, 0) and (i, height[i]).

Find two lines that together with the x-axis form a container, such that the container 
contains the most water.

Return the maximum amount of water a container can store.

Notice that you may not slant the container.

Example 1:
    Input: height = [1,8,6,2,5,4,8,3,7]
    Output: 49
    Explanation: The vertical lines are at indices 1 and 8, with heights 8 and 7.
    Area = min(8, 7) * (8 - 1) = 7 * 7 = 49

Example 2:
    Input: height = [1,1]
    Output: 1

Constraints:
    - n == height.length
    - 2 <= n <= 10^5
    - 0 <= height[i] <= 10^4

Staff+ Focus:
    - Invariant: The greedy choice - always move the pointer with smaller height inward
    - Two-pointer technique with O(1) space
    - Proof of correctness: Moving the taller line can only decrease area
"""

from typing import List


def max_area(height: List[int]) -> int:
    """
    Find maximum water container area using two pointers.
    
    Approach: Start with widest container (left=0, right=n-1).
    At each step, move the pointer with smaller height inward.
    This greedy choice is optimal because:
    - Moving the taller line can only decrease area (same or smaller height, less width)
    - Moving the shorter line might find a taller line, potentially increasing area
    
    Time Complexity: O(n) - single pass with two pointers
    Space Complexity: O(1) - only using two pointers and max_area variable
    
    Args:
        height: List of heights of vertical lines
        
    Returns:
        Maximum area that can be contained
        
    Invariant: At each step, we've checked all containers with current width or greater
    """
    if not height or len(height) < 2:
        return 0
    
    left = 0
    right = len(height) - 1
    max_area_value = 0
    
    while left < right:
        # Calculate current area
        # Width is distance between pointers
        # Height is minimum of the two heights (water level limited by shorter line)
        width = right - left
        current_height = min(height[left], height[right])
        current_area = width * current_height
        
        # Update maximum area
        max_area_value = max(max_area_value, current_area)
        
        # Move the pointer with smaller height (greedy choice)
        # This maintains the invariant that we explore all promising candidates
        if height[left] < height[right]:
            left += 1
        else:
            right -= 1
    
    return max_area_value


def max_area_brute_force(height: List[int]) -> int:
    """
    Brute force solution for comparison - check all pairs.
    
    Time Complexity: O(n^2)
    Space Complexity: O(1)
    """
    n = len(height)
    max_area_value = 0
    
    for i in range(n):
        for j in range(i + 1, n):
            width = j - i
            current_height = min(height[i], height[j])
            current_area = width * current_height
            max_area_value = max(max_area_value, current_area)
    
    return max_area_value


if __name__ == "__main__":
    # Test cases
    test_cases = [
        ([1, 8, 6, 2, 5, 4, 8, 3, 7], 49),
        ([1, 1], 1),
        ([4, 3, 2, 1, 4], 16),
        ([1, 2, 1], 2),
        ([2, 3, 4, 5, 18, 17, 6], 17),
    ]
    
    print("Container With Most Water Solutions:")
    print("=" * 60)
    
    for height, expected in test_cases:
        result = max_area(height)
        status = "✓" if result == expected else "✗"
        print(f"{status} Input: height={height}")
        print(f"  Output: {result}, Expected: {expected}")
        print()
