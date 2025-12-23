"""
Move Zeroes (LeetCode #283)

Problem:
Given an integer array nums, move all 0's to the end of it while maintaining the relative 
order of the non-zero elements.

Note: You must do this in-place without making a copy of the array.

Example 1:
    Input: nums = [0,1,0,3,12]
    Output: [1,3,12,0,0]

Example 2:
    Input: nums = [0]
    Output: [0]

Constraints:
    - 1 <= nums.length <= 10^4
    - -2^31 <= nums[i] <= 2^31 - 1

Follow up: Could you minimize the total number of operations done?

Staff+ Focus:
    - Invariant: All elements before 'write_pos' are non-zero and in original order
    - In-place operation: No extra array needed
    - O(1) space: Only using two pointers (read and write positions)
    - Minimal operations: Single pass, only swap when necessary
"""

from typing import List


def move_zeroes(nums: List[int]) -> None:
    """
    Move all zeros to the end in-place while maintaining relative order of non-zeros.
    
    Approach: Two-pointer technique
    - write_pos: position where next non-zero should be written
    - read_pos: scanning through array
    - When we find a non-zero, write it at write_pos and increment write_pos
    
    Key Invariant: Elements at indices [0, write_pos) are all non-zero and in original order
    
    Time Complexity: O(n) - single pass through array
    Space Complexity: O(1) - only using two pointer variables
    
    Args:
        nums: List to modify in-place
        
    Returns:
        None - modifies nums in-place
    """
    # Pointer for next position to write non-zero element
    write_pos = 0
    
    # First pass: move all non-zeros to the front
    # This maintains relative order since we process left to right
    for read_pos in range(len(nums)):
        if nums[read_pos] != 0:
            nums[write_pos] = nums[read_pos]
            write_pos += 1
    
    # Second pass: fill remaining positions with zeros
    for i in range(write_pos, len(nums)):
        nums[i] = 0


def move_zeroes_swap(nums: List[int]) -> None:
    """
    Alternative solution using swap - minimizes write operations.
    
    Approach: Swap non-zero elements with the leftmost zero.
    - Only swaps when we find a non-zero and write_pos is behind
    
    Time Complexity: O(n)
    Space Complexity: O(1)
    """
    write_pos = 0
    
    for read_pos in range(len(nums)):
        if nums[read_pos] != 0:
            # Swap only if positions are different
            if read_pos != write_pos:
                nums[write_pos], nums[read_pos] = nums[read_pos], nums[write_pos]
            write_pos += 1


def move_zeroes_optimal(nums: List[int]) -> None:
    """
    Most optimal solution with minimal operations.
    
    Only performs operations when absolutely necessary.
    
    Time Complexity: O(n)
    Space Complexity: O(1)
    """
    # Track position for next non-zero
    write_pos = 0
    
    # Move non-zeros forward
    for num in nums:
        if num != 0:
            nums[write_pos] = num
            write_pos += 1
    
    # Fill rest with zeros (only if needed)
    while write_pos < len(nums):
        nums[write_pos] = 0
        write_pos += 1


if __name__ == "__main__":
    # Test cases
    test_cases = [
        ([0, 1, 0, 3, 12], [1, 3, 12, 0, 0]),
        ([0], [0]),
        ([1, 2, 3], [1, 2, 3]),
        ([0, 0, 1], [1, 0, 0]),
        ([1, 0, 0, 2, 0, 3], [1, 2, 3, 0, 0, 0]),
        ([2, 1], [2, 1]),
    ]
    
    print("Move Zeroes Solutions:")
    print("=" * 60)
    
    for nums_input, expected in test_cases:
        # Test standard solution
        nums1 = nums_input.copy()
        move_zeroes(nums1)
        status1 = "✓" if nums1 == expected else "✗"
        
        # Test swap solution
        nums2 = nums_input.copy()
        move_zeroes_swap(nums2)
        status2 = "✓" if nums2 == expected else "✗"
        
        # Test optimal solution
        nums3 = nums_input.copy()
        move_zeroes_optimal(nums3)
        status3 = "✓" if nums3 == expected else "✗"
        
        print(f"{status1} Standard: Input={nums_input}")
        print(f"  Output: {nums1}, Expected: {expected}")
        print(f"{status2} Swap: {nums2}")
        print(f"{status3} Optimal: {nums3}")
        print()
