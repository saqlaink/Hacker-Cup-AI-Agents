def solve():
    N = int(input())
    S = input()

    first_A = S.find('A')
    last_A = S.rfind('A')
    first_B = S.find('B')
    last_B = S.rfind('B')

    if first_A == -1:
        return "Bob"
    if first_B == -1:
        return "Alice"

    total_moves = 0
    if last_A < first_B:
        # All 'A's are to the left of all 'B's. No contested region.
        # Each player eats all their preferred dishes.
        total_moves = S.count('A') + S.count('B')
    else:
        # 'A's and 'B's are interleaved.
        # 'A's before first_B are safe for Alice.
        total_moves += S[0:first_B].count('A')
        # 'B's after last_A are safe for Bob.
        total_moves += S[last_A+1:N].count('B')
        total_moves += (last_A - first_B + 1)
    
    if total_moves % 2 == 1:
        return "Alice"
    else:
        return "Bob"

T = int(input())
for i in range(1, T + 1):
    print(f"Case #{i}: {solve()}")