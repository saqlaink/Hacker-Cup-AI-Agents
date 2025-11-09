import sys

def solve():
    N, A, B = map(int, sys.stdin.readline().split())
    print(f"DEBUG: solve() called with N={N}, A={A}, B={B}", file=sys.stderr)

    # Construct a sequence of 2*N multipliers.
    # Set the first 2*N - 1 multipliers to 1.
    # Set the last multiplier to B.
    # This ensures:
    # 1. Coolness after N days is 1 (product of N ones), which is <= A (since A >= 1).
    
    multipliers = [1] * (2 * N - 1)
    multipliers.append(B)
    
    print(f"DEBUG: Constructed multipliers list (length {len(multipliers)}): {multipliers}", file=sys.stderr)
    
    return " ".join(map(str, multipliers))

T = int(sys.stdin.readline())
print(f"DEBUG: Total test cases T = {T}", file=sys.stderr)
for i in range(1, T + 1):
    print(f"DEBUG: Starting Case #{i}", file=sys.stderr)
    print(f"Case #{i}: {solve()}")
    print(f"DEBUG: Finished Case #{i}", file=sys.stderr)