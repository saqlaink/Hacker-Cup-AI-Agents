import sys

def solve():
    N = int(input())
    S = input()
    print(f"DEBUG: N = {N}, S = '{S}'", file=sys.stderr)

    # Find the leftmost 'B' and rightmost 'A'
    first_B = -1
    for i in range(N):
        if S[i] == 'B':
            first_B = i
            break
    print(f"DEBUG: first_B = {first_B}", file=sys.stderr)

    last_A = -1
    for i in range(N - 1, -1, -1):
        if S[i] == 'A':
            last_A = i
            break
    print(f"DEBUG: last_A = {last_A}", file=sys.stderr)

    # Case 1: No 'B's or no 'A's
    if first_B == -1:  # Only 'A's
        print(f"DEBUG: Case: No 'B's (first_B == -1). Returning 'Alice'.", file=sys.stderr)
        return "Alice"
    if last_A == -1:  # Only 'B's
        print(f"DEBUG: Case: No 'A's (last_A == -1). Returning 'Bob'.", file=sys.stderr)
        return "Bob"

    # Calculate "free" moves from the ends
    # Alice can eat all 'A's before the first 'B' without Bob being able to stop her.
    # Bob can eat all 'B's after the last 'A' without Alice being able to stop him.
    alice_free_moves = 0
    print(f"DEBUG: Calculating alice_free_moves (0 to first_B-1 = {first_B-1})", file=sys.stderr)
    for i in range(first_B):
        if S[i] == 'A':
            alice_free_moves += 1
            print(f"DEBUG:   S[{i}] = 'A', alice_free_moves incremented to {alice_free_moves}", file=sys.stderr)
    print(f"DEBUG: Final alice_free_moves = {alice_free_moves}", file=sys.stderr)

    bob_free_moves = 0
    print(f"DEBUG: Calculating bob_free_moves (last_A+1 = {last_A+1} to N-1 = {N-1})", file=sys.stderr)
    for i in range(last_A + 1, N):
        if S[i] == 'B':
            bob_free_moves += 1
            print(f"DEBUG:   S[{i}] = 'B', bob_free_moves incremented to {bob_free_moves}", file=sys.stderr)
    print(f"DEBUG: Final bob_free_moves = {bob_free_moves}", file=sys.stderr)
    
    # The segment between first_B and last_A (inclusive) is where players contest.
    # Its length is (last_A - first_B + 1). Each character in this segment is a move.
    # This segment includes the first 'B' and the last 'A'.
    contested_segment_length = last_A - first_B + 1
    print(f"DEBUG: Contested segment: S[{first_B}:{last_A+1}] = '{S[first_B:last_A+1]}'", file=sys.stderr)
    print(f"DEBUG: Contested segment length = {contested_segment_length}", file=sys.stderr)
    
    total_moves = alice_free_moves + bob_free_moves + contested_segment_length
    print(f"DEBUG: total_moves = alice_free_moves ({alice_free_moves}) + bob_free_moves ({bob_free_moves}) + contested_segment_length ({contested_segment_length}) = {total_moves}", file=sys.stderr)

    if total_moves % 2 == 1:
        print(f"DEBUG: total_moves ({total_moves}) is odd. Returning 'Alice'.", file=sys.stderr)
        return "Alice"
    else:
        print(f"DEBUG: total_moves ({total_moves}) is even. Returning 'Bob'.", file=sys.stderr)
        return "Bob"

T = int(input())
print(f"DEBUG: Total test cases T = {T}", file=sys.stderr)
for i in range(1, T + 1):
    print(f"DEBUG: --- Starting Case #{i} ---", file=sys.stderr)
    result = solve()
    print(f"Case #{i}: {result}")
    print(f"DEBUG: --- Finished Case #{i} ---", file=sys.stderr)