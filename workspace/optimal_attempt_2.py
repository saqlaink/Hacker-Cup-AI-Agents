import sys

def solve():
    N = int(sys.stdin.readline())
    S = sys.stdin.readline().strip()

    # Precompute indices of 'A's and 'B's
    a_indices = [i for i, char in enumerate(S) if char == 'A']
    b_indices = [i for i, char in enumerate(S) if char == 'B']

    # dp[l][r][turn] stores the maximum total dishes eaten from S[l...r]
    # if it's 'turn's turn.
    # turn = 0 for Alice, turn = 1 for Bob
    # We only need to store the result for the current length and previous length
    # to optimize space, but N=600000 means N^2 states are too many.
    # The problem must have a greedy or O(N) solution.

    # Let's re-evaluate the game. Players want to eat the *last* dish.
    # This means they want to maximize the total number of dishes eaten.
    # If total_dishes_eaten is odd, Alice wins. If even, Bob wins.
    # This is a standard game theory problem where players maximize their score
    # (in this case, total dishes eaten).

    # The key insight for N=600,000 must be that the choices are limited.
    # Alice can pick any 'A' at index k. This makes the new left boundary k+1.
    # Bob can pick any 'B' at index k. This makes the new right boundary k-1.
    # This means Alice can choose any 'A' in the current range [L, R]
    # to set the new L' = k+1.
    # Bob can choose any 'B' in the current range [L, R]
    # to set the new R' = k-1.

    # This is a game on an interval [L, R].
    # Alice chooses k in [L, R] such that S[k] == 'A', new state is [k+1, R].
    # Bob chooses k in [L, R] such that S[k] == 'B', new state is [L, k-1].

    # The critical observation for N=600,000 problems with interval DP structure
    # is often that only a few choices for k are optimal.
    # For Alice, she can pick the leftmost 'A' or the rightmost 'A'.
    # For Bob, he can pick the leftmost 'B' or the rightmost 'B'.
    # Let's test this hypothesis.

    # Precompute next_A[i], prev_A[i], next_B[i], prev_B[i]
    # next_A[i]: smallest index j >= i such that S[j] == 'A'
    # prev_A[i]: largest index j <= i such that S[j] == 'A'
    # Similarly for 'B'
    
    next_A = [N] * (N + 1)
    prev_A = [-1] * (N + 1)
    next_B = [N] * (N + 1)
    prev_B = [-1] * (N + 1)

    last_a = N
    last_b = N
    for i in range(N - 1, -1, -1):
        if S[i] == 'A':
            last_a = i
        else: # S[i] == 'B'
            last_b = i
        next_A[i] = last_a
        next_B[i] = last_b
    
    first_a = -1
    first_b = -1
    for i in range(N):
        if S[i] == 'A':
            first_a = i
        else: # S[i] == 'B'
            first_b = i
        prev_A[i+1] = first_a
        prev_B[i+1] = first_b

    # dp[i][j][turn] = max dishes eaten from S[i...j]
    # turn 0 for Alice, 1 for Bob
    # We need to compute for increasing length of segments.
    # dp[len][i][turn] where j = i + len - 1
    # This is still N^2 states.

    # The problem is that the state space is too large for N=600,000.
    # This implies that the game is not played on arbitrary subsegments [L, R].
    # The crucial part is that Alice pulls from the left, Bob from the right.
    # This means Alice's move changes the effective left boundary.
    # Bob's move changes the effective right boundary.

    # Let's consider the total number of 'A's and 'B's.
    # Alice can eat at most len(a_indices) 'A's.
    # Bob can eat at most len(b_indices) 'B's.

    # The game is about who gets to eat the *last* dish.
    # This is equivalent to finding the total number of dishes eaten, K.
    # If K is odd, Alice wins. If K is even, Bob wins.

    # Let's simplify the game.
    # Alice can pick any 'A'. This means she can choose to remove any prefix S[0...k-1]
    # by picking S[k].
    # Bob can pick any 'B'. This means he can choose to remove any suffix S[k+1...N-1]
    # by picking S[k].

    # The game is equivalent to this:
    # Alice picks an 'A' at index `i`. This 'A' is eaten. All plates `S[0...i-1]` are discarded.
    # Bob picks a 'B' at index `j`. This 'B' is eaten. All plates `S[j+1...N-1]` are discarded.
    # The remaining plates are `S[i+1...j-1]` (if Alice picked `i` and Bob picked `j` and `i < j`).
    # But they take turns.

    # Let's trace the game with the sample again: ABBAAAB
    # Alice's turn. She can pick any 'A'.
    # If she picks S[0] ('A'): remaining S[1...6] (BBAAB).
    # If she picks S[3] ('A'): remaining S[4...6] (AAB).
    # If she picks S[4] ('A'): remaining S[5...6] (AB).
    # If she picks S[5] ('A'): remaining S[6...6] (B).
    # If she picks S[6] ('A'): remaining S[7...6] (empty).

    # The sample explanation says Alice picks S[3].
    # This means Alice wants to maximize `1 + (max_dishes_Bob_can_force_on_S[4...6])`.
    # This is exactly the N^2 DP.

    # The only way N=600,000 works is if the choices for k are very limited,
    # or the game reduces to a simpler form.
    # What if only the leftmost 'A' and rightmost 'A' matter for Alice?
    # And only leftmost 'B' and rightmost 'B' matter for Bob?

    # Let's define `f(L, R, turn)` as the maximum total dishes eaten from `S[L...R]`.
    # `memo = {}`
    # `def f(L, R, turn):`
    #   `if L > R: return 0`
    #   `if (L, R, turn) in memo: return memo[(L, R, turn)]`

    #   `res = 0`
    #   `if turn == 0: # Alice's turn`
    #     `# Find all 'A's in S[L...R]`
    #     `current_a_indices = []`
    #     `curr = next_A[L]`
    #     `while curr <= R:`
    #       `current_a_indices.append(curr)`
    #       `curr = next_A[curr + 1]`
        
    #     `if not current_a_indices:`
    #       `res = f(L, R, 1) # Alice skips`
    #     `else:`
    #       `for k in current_a_indices:`
    #         `res = max(res, 1 + f(k + 1, R, 1))`
    #   `else: # Bob's turn`
    #     `# Find all 'B's in S[L...R]`
    #     `current_b_indices = []`
    #     `curr = prev_B[R+1]`
    #     `while curr >= L:`
    #       `current_b_indices.append(curr)`
    #       `curr = prev_B[curr]`
    #     `current_b_indices.reverse()` # Process from left to right for consistency, though order doesn't matter for max
        
    #     `if not current_b_indices:`
    #       `res = f(L, R, 0) # Bob skips`
    #     `else:`
    #       `for k in current_b_indices:`
    #         `res = max(res, 1 + f(L, k - 1, 0))`
    
    #   `memo[(L, R, turn)] = res`
    #   `return res`

    # `total_dishes = f(0, N-1, 0)`
    # `if total_dishes % 2 == 1: print("Alice")`
    # `else: print("Bob")`

    # The above is the correct DP formulation. The issue is N^2 states.
    # The only way to make this O(N) is if the number of choices for `k` is constant.
    # For example, if Alice only considers `next_A[L]` and `prev_A[R]`.
    # And Bob only considers `next_B[L]` and `prev_B[R]`.

    # Let's re-examine the sample case: ABBAAAB
    # Alice picks S[3]. This is not next_A[0] (which is S[0]) nor prev_A[6] (which is S[6]).
    # This means the "only two choices" hypothesis is false.
    # Alice can pick any 'A' in the range.

    # The problem is a variant of Nim.
    # The key must be that the choices of 'A' and 'B' are independent in some way.
    # Alice's choice of 'A' at `k` removes `S[0...k-1]`.
    # Bob's choice of 'B' at `k'` removes `S[k'+1...N-1]`.
    # The remaining segment is `S[k+1...k'-1]`.

    # This means Alice effectively chooses a new left boundary `L_new = k+1`.
    # Bob effectively chooses a new right boundary `R_new = k'-1`.