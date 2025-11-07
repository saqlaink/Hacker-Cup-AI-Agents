def solve():
    N = int(input())
    S = input()

    count_A = S.count('A')
    count_B = S.count('B')

    if count_A == 0:
        return "Bob"
    if count_B == 0:
        return "Alice"

    # Find the first 'A' from the left and the last 'B' from the right.
    # These are the "critical" plates that define the contested region.
    first_A_idx = -1
    for i in range(N):
        if S[i] == 'A':
            first_A_idx = i
            break
    
    last_B_idx = -1
    for i in range(N - 1, -1, -1):
        if S[i] == 'B':
            last_B_idx = i
            break

    # If all 'A's are to the right of all 'B's, Alice can always pick an 'A'
    # that is to the right of all 'B's, effectively making Bob skip.
    # Example: BBBBAAA. Alice picks any A, say S[4]. String becomes S[5:]. No B's left. Alice wins.
    if first_A_idx > last_B_idx:
        return "Alice"
    
    
    distance = last_B_idx - first_A_idx
    if distance % 2 == 0:
        return "Alice"
    else:
        return "Bob"

T = int(input())
for i in range(1, T + 1):
    print(f"Case #{i}: {solve()}")