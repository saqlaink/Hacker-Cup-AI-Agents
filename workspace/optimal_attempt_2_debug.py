import sys

def solve():
    N = int(input())
    S = input()
    print(f"DEBUG: N = {N}, S = '{S}'", file=sys.stderr)

    first_A = S.find('A')
    last_A = S.rfind('A')
    first_B = S.find('B')
    last_B = S.rfind('B')
    print(f"DEBUG: first_A = {first_A}, last_A = {last_A}", file=sys.stderr)
    print(f"DEBUG: first_B = {first_B}, last_B = {last_B}", file=sys.stderr)

    if first_A == -1:
        print(f"DEBUG: No 'A's found. Returning 'Bob'.", file=sys.stderr)
        return "Bob"
    if first_B == -1:
        print(f"DEBUG: No 'B's found. Returning 'Alice'.", file=sys.stderr)
        return "Alice"

    total_moves = 0
    if last_A < first_B:
        print(f"DEBUG: Case: All 'A's before all 'B's (last_A={last_A} < first_B={first_B}). No contested region.", file=sys.stderr)
        # All 'A's are to the left of all 'B's. No contested region.
        # Each player eats all their preferred dishes.
        total_moves = S.count('A') + S.count('B')
        print(f"DEBUG: total_moves (all A + all B) = {total_moves}", file=sys.stderr)
    else:
        print(f"DEBUG: Case: 'A's and 'B's are interleaved (last_A={last_A} >= first_B={first_B}).", file=sys.stderr)
        # 'A's and 'B's are interleaved.
        # 'A's before first_B are safe for Alice.
        safe_A_count = S[0:first_B].count('A')
        total_moves += safe_A_count
        print(f"DEBUG: Safe 'A's (S[0:{first_B}]) count = {safe_A_count}. total_moves = {total_moves}", file=sys.stderr)
        
        # 'B's after last_A are safe for Bob.
        safe_B_count = S[last_A+1:N].count('B')
        total_moves += safe_B_count
        print(f"DEBUG: Safe 'B's (S[{last_A+1}:{N}]) count = {safe_B_count}. total_moves = {total_moves}", file=sys.stderr)
        
        # The contested region is from first_B to last_A (inclusive).
        contested_length = (last_A - first_B + 1)
        total_moves += contested_length
        print(f"DEBUG: Contested region length (last_A - first_B + 1) = ({last_A} - {first_B} + 1) = {contested_length}. total_moves = {total_moves}", file=sys.stderr)
    
    print(f"DEBUG: Final total_moves before parity check = {total_moves}", file=sys.stderr)
    if total_moves % 2 == 1:
        print(f"DEBUG: total_moves is odd. Returning 'Alice'.", file=sys.stderr)
        return "Alice"
    else:
        print(f"DEBUG: total_moves is even. Returning 'Bob'.", file=sys.stderr)
        return "Bob"

T = int(input())
print(f"DEBUG: Total test cases T = {T}", file=sys.stderr)
for i in range(1, T + 1):
    print(f"DEBUG: --- Starting Case #{i} ---", file=sys.stderr)
    print(f"Case #{i}: {solve()}")
    print(f"DEBUG: --- Finished Case #{i} ---", file=sys.stderr)