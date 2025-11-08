def solve():
    N = int(input())
    S = input()

    alice_count = S.count('A')
    bob_count = S.count('B')

    if alice_count == 0:
        return "Bob"
    if bob_count == 0:
        return "Alice"

    first_A = -1
    for i in range(N):
        if S[i] == 'A':
            first_A = i
            break

    last_B = -1
    for i in range(N - 1, -1, -1):
        if S[i] == 'B':
            last_B = i
            break
    
    if first_A == -1: # No 'A's, Alice skips
        return "Bob"
    if last_B == -1: # No 'B's, Bob skips
        return "Alice"

    if first_A < last_B:
        return "Alice"
    else:
        return "Bob"

T = int(input())
for i in range(1, T + 1):
    result = solve()
    print(f"Case #{i}: {result}")