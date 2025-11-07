import sys

def solve():
    N = int(sys.stdin.readline())
    S = sys.stdin.readline().strip()

    # Find indices of all 'A's and 'B's
    a_indices = [i for i, char in enumerate(S) if char == 'A']
    b_indices = [i for i, char in enumerate(S) if char == 'B']

    num_A = len(a_indices)
    num_B = len(b_indices)

    # Case 1: No 'A's for Alice to eat
    if num_A == 0:
        # If there are 'B's, Bob eats them all. Bob wins.
        # If no 'B's either, no one moves, Alice skips, Bob skips, no last dish.
        # The problem implies there's always a last dish if there are any dishes.
        # If Alice skips, it's Bob's turn. If Bob has dishes, he eats one.
        # If Bob has no dishes, he skips. Then Alice skips again.
        # This means if num_A == 0, Alice can never make a move.
        # If num_B > 0, Bob will eat the last dish.
        # If num_B == 0, then num_A == 0 and num_B == 0, no dishes. This case should not happen if N > 0.
        # If N > 0 and num_A == 0, then num_B must be > 0. Bob wins.
        return "Bob"

    # Case 2: No 'B's for Bob to eat
    if num_B == 0:
        # Alice eats them all. Alice wins.
        return "Alice"

    # Both 'A's and 'B's are present.
    # The game is played on a segment [L, R] of the original string.
    # Alice picks an 'A' at index `i` (L <= i <= R), new segment is [i+1, R].
    # Bob picks a 'B' at index `j` (L <= j <= R), new segment is [L, j-1].
    # The player who eats the last dish wins. This is a normal play game.
    # The total number of moves will be k_A + k_B.
    # If (k_A + k_B) is odd, Alice wins. If even, Bob wins.

    # Alice wants to maximize the total number of moves.
    # Bob wants to maximize the total number of moves.
    # This is not a zero-sum game in terms of (k_A - k_B).
    # Both players want to maximize the total number of moves.
    # This is a common pattern in "last player to move wins" games.
    # The total number of moves is fixed under optimal play.

    # Let's consider the "critical" parts of the string.
    # Alice can choose any 'A'. To maximize moves, she should choose an 'A' that leaves the most pieces for future turns.
    # This means choosing the leftmost 'A'.
    # Bob can choose any 'B'. To maximize moves, he should choose a 'B' that leaves the most pieces for future turns.
    # This means choosing the rightmost 'B'.

    # Let's simulate the game with this greedy strategy.
    # Alice always picks the leftmost 'A'.
    # Bob always picks the rightmost 'B'.

    # The game state can be represented by (left_ptr, right_ptr) indicating the current active segment S[left_ptr ... right_ptr].
    # We need to find the actual indices of 'A's and 'B's within this segment.
    
    # This is equivalent to finding the number of 'A's that are to the left of the rightmost 'B'
    # and the number of 'B's that are to the right of the leftmost 'A'.
    
    # Let's find the index of the first 'B' from the left.
    first_B_idx = -1
    for i in range(N):
        if S[i] == 'B':
            first_B_idx = i
            break
    
    # Let's find the index of the last 'A' from the right.
    last_A_idx = -1
    for i in range(N - 1, -1, -1):
        if S[i] == 'A':
            last_A_idx = i
            break
            
    # If first_B_idx is -1, it means no 'B's, Alice wins (already handled).
    # If last_A_idx is -1, it means no 'A's, Bob wins (already handled).

    # Consider the segment S[0 ... first_B_idx-1]. All 'A's in this segment are "safe" for Alice.
    # Bob cannot remove them by pulling from the right, because he must pick a 'B' to move, and there are no 'B's in this segment.
    # Alice can eat all 'A's in S[0 ... first_B_idx-1].
    
    # Consider the segment S[last_A_idx+1 ... N-1]. All 'B's in this segment are "safe" for Bob.
    # Alice cannot remove them by pulling from the left, because she must pick an 'A' to move, and there are no 'A's in this segment.
    # Bob can eat all 'B's in S[last_A_idx+1 ... N-1].

    # The "contested" region is S[first_B_idx ... last_A_idx].
    # If first_B_idx > last_A_idx, it means all 'A's are to the left of all 'B's, or vice versa.
    # Example: AAAABBBB. first_B_idx = 4, last_A_idx = 3. first_B_idx > last_A_idx.
    # In this case, Alice eats all 'A's, then Bob eats all 'B's.
    # Total moves = num_A + num_B.
    # If (num_A + num_B) is odd, Alice wins. Else Bob wins.

    # Example: BBBBAAAA. first_B_idx = 0, last_A_idx = 7.
    # Alice's turn. She must pick an 'A'. She picks S[7]. New string S[8:]. No more 'A's.
    # Bob's turn. He must pick a 'B'. He picks S[0]. New string S[:0]. No more 'B's.
    # This is not a simple sum. The players can discard opponent's pieces.

    # The crucial observation is that Alice can only remove a prefix, Bob can only remove a suffix.
    # This means that the relative order of the remaining items is always preserved.
    # The game is effectively played on a subsegment `S[L...R]` of the original string.
    # Alice chooses an 'A' at `i` in `[L, R]`, new state `(i+1, R)`.
    # Bob chooses a 'B' at `j` in `[L, R]`, new state `(L, j-1)`.

    # This is a game where players are trying to maximize their own score (number of dishes eaten).
    # The total number of dishes eaten is `k_A + k_B`.
    # The winner is determined by the parity of `k_A + k_B`.
    # Alice wants `k_A + k_B` to be odd. Bob wants `k_A + k_B` to be even.

    # This is a game where players are trying to maximize their own score.
    # Let `score_A` be the number of 'A's Alice eats, `score_B` be the number of 'B's Bob eats.
    # Alice wants to maximize `score_A`. Bob wants to maximize `score_B`.
    # The total number of moves is `score_A + score_B`.
    # The winner is Alice if `(score_A + score_B)` is odd, Bob if `(score_A + score_B)` is even.

    # This is a game where players are trying to maximize their own score.
    # The total number of moves is `k_A + k_B`.
    # Alice wants `k_A + k_B` to be odd. Bob wants `k_A + k_B` to be even.
    # This is equivalent to Alice wanting to maximize `k_A - k_B` if `k_A+k_B` is odd, and minimize if even.
    # This is a complex game.

    # Let's re-examine the sample cases with this logic.
    # ABBAAAB (N=7)
    # A_indices = [0, 3, 4, 5]
    # B_indices = [1, 2, 6]
    # num_A = 4, num_B = 3

    # If Alice picks S[3] (A): new string S[4...6] = AAB.
    #   A_indices = [4, 5], B_indices = [6]
    #   Alice has 1 move.
    #   Bob's turn on AAB. Bob picks S[6] (B). new string S[4...5] = AA.
    #     Bob has 1 move.
    #     Alice's turn on AA. Alice picks S[4] (A). new string S[5...5] = A.
    #       Alice has 1 move.
    #       Bob's turn on A. No B's. Bob skips.
    #       Alice's turn on A. Alice picks S[5] (A). new string S[6...5] (empty).
    #         Alice has 1 move.
    #         Game ends.
    # Total moves: Alice 1+1+1 = 3, Bob 1 = 1. Total = 4. Even. Bob wins.
    # But sample says Alice wins. My interpretation of optimal play is wrong.

    # "If each player wants nothing more than the satisfaction of eating the last remaining dish on table, and both choose which dish to eat based on that, who will eat the final dish?"
    # This means they play optimally to be the one who makes the last move.
    # This is a standard normal play game. The player who makes the last move wins.

    # The game is equivalent to this:
    # There are `num_A` 'A' tokens and `num_B` 'B' tokens.
    # Alice takes an 'A' token.
    # Bob takes a 'B' token.
    # Additionally, if Alice takes `S[i]`, she removes all 'B's at `S[0...i-1]`.
    # If Bob takes `S[j]`, he removes all 'A's at `S[j+1...N-1]`.

    # This is a game on a single pile of items, but items are of two types.
    # The state can be simplified.
    # The game is played on a segment `S[L...R]`.
    # Alice picks an 'A' at `i`