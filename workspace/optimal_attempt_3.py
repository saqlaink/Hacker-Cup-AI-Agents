def solve():
    N = int(input())
    S = input()

    first_A = -1
    last_A = -1
    first_B = -1
    last_B = -1

    for i in range(N):
        if S[i] == 'A':
            if first_A == -1:
                first_A = i
            last_A = i
        else: # S[i] == 'B'
            if first_B == -1:
                first_B = i
            last_B = i

    # Case 1: Only 'A's or no 'B's. Alice wins.
    if first_B == -1:
        return "Alice"
    
    # Case 2: Only 'B's or no 'A's. Bob wins.
    if first_A == -1:
        return "Bob"

    # Both 'A's and 'B's are present.
    # Alice wants to eat the last dish. Bob wants to eat the last dish.
    # This is a game where players try to maximize their own number of moves.












    










