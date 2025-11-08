def solve():
    N = int(input())
    S = input()

    # Find the leftmost 'B' and rightmost 'A'
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

    # Case 1: No 'B's or no 'A's
    if first_B == -1:  # Only 'A's
        return "Alice"
    if last_A == -1:  # Only 'B's
        return "Bob"

    # Calculate "free" moves from the ends
    # Alice can eat all 'A's before the first 'B' without Bob being able to stop her.
    # Bob can eat all 'B's after the last 'A' without Alice being able to stop him.
    alice_free_moves = 0
    for i in range(first_B):
        if S[i] == 'A':
            alice_free_moves += 1

    bob_free_moves = 0
    for i in range(last_A + 1, N):
        if S[i] == 'B':
            bob_free_moves += 1

    
    
    total_moves = alice_free_moves + bob_free_moves + (last_A - first_B + 1)

    if total_moves % 2 == 1:
        return "Alice"
    else:
        return "Bob"

T = int(input())
for i in range(1, T + 1):
    result = solve()
    print(f"Case #{i}: {result}")