import sys

def solve():
    n = int(sys.stdin.readline())
    arr = list(map(int, sys.stdin.readline().split()))

    # Kadane's algorithm
    # max_so_far stores the maximum sum found ending at any point
    # current_max stores the maximum sum of a subarray ending at the current position
    
    max_so_far = arr[0]
    current_max = arr[0]

    for i in range(1, n):
        # For the current element arr[i], we have two choices:
        # 1. Start a new subarray with arr[i]
        # 2. Extend the previous subarray by adding arr[i] to current_max
        # We choose the option that yields a larger sum ending at arr[i]
        current_max = max(arr[i], current_max + arr[i])
        
        # Update the overall maximum sum found so far
        max_so_far = max(max_so_far, current_max)

    print(max_so_far)

solve()