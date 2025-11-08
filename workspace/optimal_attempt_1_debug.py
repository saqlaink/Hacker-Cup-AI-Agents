import sys

def solve():
    N, A, B = map(int, input().split())
    print(f"DEBUG: Input N={N}, A={A}, B={B}", file=sys.stderr)

    # Initialize all multipliers to 1.
    # This ensures coolness after N days is 1, satisfying C_N <= A (since A >= 1).
    multipliers = [1] * (2 * N)
    print(f"DEBUG: Initial multipliers (length {len(multipliers)}): {multipliers}", file=sys.stderr)

    # To achieve a final coolness of B, set the (N+1)-th multiplier to B.
    # In 0-indexed list, this is at index N.
    print(f"DEBUG: Setting multipliers[{N}] = {B}", file=sys.stderr)
    multipliers[N] = B
    print(f"DEBUG: Multipliers after setting index {N}: {multipliers}", file=sys.stderr)

    # The product of all multipliers will be B, satisfying C_{2*N} = B.
    print(f"DEBUG: Final multipliers before joining: {multipliers}", file=sys.stderr)
    return ' '.join(map(str, multipliers))

T = int(input())
print(f"DEBUG: Total test cases T={T}", file=sys.stderr)
for i in range(1, T + 1):
    print(f"DEBUG: Starting Case #{i}", file=sys.stderr)
    print(f"Case #{i}: {solve()}")
    print(f"DEBUG: Finished Case #{i}\n", file=sys.stderr)