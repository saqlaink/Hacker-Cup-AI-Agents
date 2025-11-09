import sys

def solve():
    N, A, B = map(int, input().split())
    print(f"DEBUG: solve() called with N={N}, A={A}, B={B}", file=sys.stderr)

    # Find the largest possible coolness C_N after N days,
    # such that C_N <= A and C_N divides B.
    # Since a solution is guaranteed, such a C_N always exists (at least 1).
    target_C_N = 1
    print(f"DEBUG: Initial target_C_N = {target_C_N}", file=sys.stderr)
    for x in range(A, 0, -1):
        print(f"DEBUG: Checking x={x} for B % x == 0 (B={B})", file=sys.stderr)
        if B % x == 0:
            target_C_N = x
            print(f"DEBUG: Found target_C_N = {target_C_N} when x={x}. Breaking loop.", file=sys.stderr)
            break
    print(f"DEBUG: Final target_C_N after loop = {target_C_N}", file=sys.stderr)
    
    # Initialize all multipliers to 1
    multipliers = [1] * (2 * N)
    print(f"DEBUG: Initial multipliers (length {2*N}) = {multipliers}", file=sys.stderr)
    
    # Set the N-th multiplier (at index N-1) to achieve target_C_N
    # This corresponds to M_N in 1-indexed problem statement
    multiplier_N_idx = N - 1
    multipliers[multiplier_N_idx] = target_C_N
    print(f"DEBUG: Setting multipliers[{multiplier_N_idx}] (M_{N}) = {target_C_N}", file=sys.stderr)
    
    # Set the 2N-th multiplier (at index 2N-1)
    # This corresponds to M_{2N} in 1-indexed problem statement
    multiplier_2N_idx = 2 * N - 1
    multipliers[multiplier_2N_idx] = B // target_C_N
    print(f"DEBUG: Setting multipliers[{multiplier_2N_idx}] (M_{2*N}) = {B // target_C_N} (B // target_C_N)", file=sys.stderr)
    
    print(f"DEBUG: Final multipliers list before joining = {multipliers}", file=sys.stderr)
    return " ".join(map(str, multipliers))

T = int(input())
print(f"DEBUG: Total test cases T = {T}", file=sys.stderr)
for i in range(1, T + 1):
    print(f"DEBUG: --- Starting Case #{i} ---", file=sys.stderr)
    print(f"Case #{i}: {solve()}")
    print(f"DEBUG: --- Finished Case #{i} ---", file=sys.stderr)