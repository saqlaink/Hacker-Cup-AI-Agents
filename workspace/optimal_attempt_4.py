def solve():
    N = int(input())
    S = input()

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

    if first_A == -1:  # No 'A's for Alice
        # Alice skips. Bob eats all 'B's.
        # Total moves = count of 'B's.
        # Alice wins if total moves is odd.
        return "Alice" if S.count('B') % 2 == 1 else "Bob"
    
    if last_B == -1:  # No 'B's for Bob
        # Bob skips. Alice eats all 'A's.
        # Total moves = count of 'A's.
        return "Alice" if S.count('A') % 2 == 1 else "Bob"


    if first_A > last_B:
        total_moves = S.count('A') + S.count('B')
        return "Alice" if total_moves % 2 == 1 else "Bob"
    
    total_moves = S.count('A') + S.count('B')
    return "Alice" if total_moves % 2 == 1 else "Bob"


T = int(input())
for i in range(1, T + 1):
    print(f"Case #{i}: {solve()}")