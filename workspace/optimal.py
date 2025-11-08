def solve():
    N = int(input())
    S = input()

    first_B = -1
    for i in range(N):
        if S[i] == 'B':
            first_B = i
            break

    last_A = -1
    for i in range(N - 1, -1, -1):
        if S[i] == 'A':
            last_A = i
            break

    if first_B == -1:  # No 'B's, Alice eats all 'A's
        return "Alice"
    if last_A == -1:  # No 'A's, Alice skips, Bob eats all 'B's
        return "Bob"

    # Count 'A's before the first 'B'
    alice_exclusive_moves = 0
    for i in range(first_B):
        if S[i] == 'A':
            alice_exclusive_moves += 1

    # Count 'B's after the last 'A'
    bob_exclusive_moves = 0
    for i in range(last_A + 1, N):
        if S[i] == 'B':
            bob_exclusive_moves += 1

    # The "contested" region is S[first_B : last_A+1]
    # In this region, Alice can eat an 'A' and Bob can eat a 'B'.
    # Each move by Alice shifts the left boundary right.
    contested_A_count = 0
    for i in range(first_B, last_A + 1):
        if S[i] == 'A':
            contested_A_count += 1
    
    contested_B_count = 0
    for i in range(first_B, last_A + 1):
        if S[i] == 'B':
            contested_B_count += 1

    total_alice_moves = alice_exclusive_moves + contested_A_count
    total_bob_moves = bob_exclusive_moves + contested_B_count

    if total_alice_moves >= total_bob_moves:
        return "Alice"
    else:
        return "Bob"

T = int(input())
for i in range(1, T + 1):
    result = solve()
    print(f"Case #{i}: {result}")