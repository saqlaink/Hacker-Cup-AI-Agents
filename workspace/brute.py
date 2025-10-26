import sys

def solve():
    N = int(sys.stdin.readline())
    A = list(map(int, sys.stdin.readline().split()))

    if N == 1:
        return 0

    max_required_ladder_height = 0
    for i in range(N - 1):
        # A ladder can connect platform i and platform i+1 if their x-intervals overlap.
        # Platform i is [i, i+1] at height A[i].
        # Platform i+1 is [i+1, i+2] at height A[i+1].
        # They overlap at x = i+1.
        # The vertical distance between them at x = i+1 is abs(A[i] - A[i+1]).
        # Solid Snake needs to visit all platforms, so he must be able to traverse
        # between all adjacent platforms. The shortest ladder height required
        # is the maximum of these absolute differences.
        current_diff = abs(A[i] - A[i+1])
        if current_diff > max_required_ladder_height:
            max_required_ladder_height = current_diff
            
    return max_required_ladder_height

T = int(sys.stdin.readline())
for i in range(1, T + 1):
    result = solve()
    sys.stdout.write(f"Case #{i}: {result}\n")