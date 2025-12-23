# Week 1: Arrays, Strings, Two Pointers

This directory contains implementations of classic algorithm problems focusing on arrays, strings, and two-pointer techniques.

## Problems Implemented

### Core Problems

1. **Two Sum** (`two_sum.py`)
   - LeetCode #1
   - Find two indices that sum to target
   - Time: O(n), Space: O(n)
   - Uses hashmap for O(1) lookups

2. **Container With Most Water** (`container_with_most_water.py`)
   - LeetCode #11
   - Find max area between two vertical lines
   - Time: O(n), Space: O(1)
   - Two-pointer greedy approach

3. **Trapping Rain Water** (`trapping_rain_water.py`)
   - LeetCode #42
   - Calculate trapped rainwater in elevation map
   - Time: O(n), Space: O(1)
   - Two-pointer technique with running max values

### Depth Problems

4. **Product of Array Except Self** (`product_of_array_except_self.py`)
   - LeetCode #238
   - Calculate product of all elements except current
   - Time: O(n), Space: O(1) excluding output
   - Two-pass algorithm with prefix/suffix products

5. **Move Zeroes** (`move_zeroes.py`)
   - LeetCode #283
   - Move all zeros to end while maintaining order
   - Time: O(n), Space: O(1)
   - In-place two-pointer modification

## Staff+ Engineering Focus

### Key Concepts

#### 1. **Invariants**
Understanding and maintaining loop invariants is crucial for correctness:

- **Two Sum**: For each element processed, all previous elements are in the hashmap
- **Container With Most Water**: At each step, all containers with current width or greater have been checked
- **Trapping Rain Water**: Water level at position i = min(max_left, max_right) - height[i]
- **Product Except Self**: result[i] = prefix_product[i] * suffix_product[i]
- **Move Zeroes**: All elements before write_pos are non-zero and in original order

#### 2. **In-Place Operations**
Modifying data structures without extra copies:

- **Move Zeroes**: Two-pointer technique to rearrange array without extra space
- **Product Except Self**: Building result using the output array itself for intermediate results
- All solutions avoid unnecessary memory allocations

#### 3. **O(1) Space Arguments**
Achieving optimal space complexity:

- **Container With Most Water**: Only two pointers needed
- **Trapping Rain Water**: Two pointers + two running max variables (vs O(n) DP approach)
- **Product Except Self**: Using output array for intermediate computations
- **Move Zeroes**: Only pointer variables, no auxiliary arrays

### Design Patterns

1. **Two-Pointer Technique**
   - Used in: Container With Most Water, Trapping Rain Water, Move Zeroes
   - Pattern: Start from both ends, move based on greedy choice
   - Benefit: Reduces O(n²) to O(n)

2. **Hashmap for O(1) Lookup**
   - Used in: Two Sum
   - Pattern: Store seen elements for constant-time access
   - Trade-off: O(n) space for O(n) time

3. **Prefix/Suffix Processing**
   - Used in: Product of Array Except Self, Trapping Rain Water
   - Pattern: Process array in both directions to accumulate information
   - Benefit: Avoids nested loops

## Running the Code

Each file can be run independently to see test cases:

```bash
# Run individual solutions
python two_sum.py
python container_with_most_water.py
python trapping_rain_water.py
python product_of_array_except_self.py
python move_zeroes.py

# Run all tests
python test_week1.py
```

## Time and Space Complexity Summary

| Problem | Time | Space | Technique |
|---------|------|-------|-----------|
| Two Sum | O(n) | O(n) | Hashmap |
| Container With Most Water | O(n) | O(1) | Two Pointers |
| Trapping Rain Water | O(n) | O(1) | Two Pointers |
| Product Except Self | O(n) | O(1)* | Prefix/Suffix |
| Move Zeroes | O(n) | O(1) | Two Pointers |

*Excluding output array

## Learning Outcomes

By working through these problems, you will:

1. Master two-pointer techniques for array problems
2. Understand greedy algorithms and their correctness proofs
3. Learn to optimize space complexity from O(n) to O(1)
4. Practice maintaining and proving loop invariants
5. Recognize when in-place modifications are possible and beneficial
6. Develop intuition for trading time vs space complexity
