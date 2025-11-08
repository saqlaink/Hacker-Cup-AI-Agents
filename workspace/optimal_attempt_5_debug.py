import sys

def solve():
    N = int(input())
    S = input()
    print(f"DEBUG: N = {N}, S = '{S}'", file=sys.stderr)

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

    if first_B == -1:  # No 'B's, Alice eats all 'A's
        print(f"DEBUG: Case: No 'B's found. Returning 'Alice'.", file=sys.stderr)
        return "Alice"
    if last_A == -1:  # No 'A's, Alice skips, Bob eats all 'B's
        print(f"DEBUG: Case: No 'A's found. Returning 'Bob'.", file=sys.stderr)
        return "Bob"

    # Count 'A's before the first 'B'
    alice_exclusive_moves = 0
    print(f"DEBUG: Counting Alice exclusive moves (0 to {first_B-1})", file=sys.stderr)
    for i in range(first_B):
        if S[i] == 'A':
            alice_exclusive_moves += 1
            print(f"DEBUG:   S[{i}] = 'A', alice_exclusive_moves = {alice_exclusive_moves}", file=sys.stderr)
    print(f"DEBUG: alice_exclusive_moves = {alice_exclusive_moves}", file=sys.stderr)

    # Count 'B's after the last 'A'
    bob_exclusive_moves = 0
    print(f"DEBUG: Counting Bob exclusive moves ({last_A+1} to {N-1})", file=sys.stderr)
    for i in range(last_A + 1, N):
        if S[i] == 'B':
            bob_exclusive_moves += 1
            print(f"DEBUG:   S[{i}] = 'B', bob_exclusive_moves = {bob_exclusive_moves}", file=sys.stderr)
    print(f"DEBUG: bob_exclusive_moves = {bob_exclusive_moves}", file=sys.stderr)

    # The "contested" region is S[first_B : last_A+1]
    print(f"DEBUG: Contested region from index {first_B} to {last_A} (inclusive)", file=sys.stderr)
    contested_A_count = 0
    for i in range(first_B, last_A + 1):
        if S[i] == 'A':
            contested_A_count += 1
    print(f"DEBUG: contested_A_count = {contested_A_count}", file=sys.stderr)
    
    contested_B_count = 0
    for i in range(first_B, last_A + 1):
        if S[i] == 'B':
            contested_B_count += 1
    print(f"DEBUG: contested_B_count = {contested_B_count}", file=sys.stderr)

    total_alice_moves = alice_exclusive_moves + contested_A_count
    total_bob_moves = bob_exclusive_moves + contested_B_count
    print(f"DEBUG: total_alice_moves = {total_alice_moves} (exclusive_A={alice_exclusive_moves} + contested_A={contested_A_count})", file=sys.stderr)
    print(f"DEBUG: total_bob_moves = {total_bob_moves} (exclusive_B={bob_exclusive_moves} + contested_B={contested_B_count})", file=sys.stderr)

    if total_alice_moves >= total_bob_moves:
        print(f"DEBUG: total_alice_moves ({total_alice_moves}) >= total_bob_moves ({total_bob_moves}). Returning 'Alice'.", file=sys.stderr)
        return "Alice"
    else:
        print(f"DEBUG: total_alice_moves ({total_alice_moves}) < total_bob_moves ({total_bob_moves}). Returning 'Bob'.", file=sys.stderr)
        return "Bob"

T = int(input())
for i in range(1, T + 1):
    print(f"DEBUG: --- Starting Case #{i} ---", file=sys.stderr)
    result = solve()
    print(f"Case #{i}: {result}")
    print(f"DEBUG: --- End Case #{i} ---", file=sys.stderr)