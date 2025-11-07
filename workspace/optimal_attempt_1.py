def solve():
    N = int(input())
    S = input()

    alice_score = 0
    bob_score = 0

    # Find the leftmost 'A' and rightmost 'B'
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

    # If no 'A's, Alice skips, Bob wins if there are 'B's.
    if first_A == -1:
        return "Bob" if last_B != -1 else "Alice" # If no 'B's either, Alice skips, Bob skips, no one eats. But N>=1, so one must exist.
    
    # If no 'B's, Bob skips, Alice wins if there are 'A's.
    if last_B == -1:
        return "Alice"

    # The game effectively plays on the segment between the leftmost 'A' and rightmost 'B'.
    # Alice can eat any 'A' at index k, leaving S[k+1:]























