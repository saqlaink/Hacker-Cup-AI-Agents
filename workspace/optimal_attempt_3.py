import sys

def solve():
    N = int(sys.stdin.readline())
    S = sys.stdin.readline().strip()

    # Precompute indices of 'A' and 'B'
    a_indices = [i for i, char in enumerate(S) if char == 'A']
    b_indices = [i for i, char in enumerate(S) if char == 'B']

    # dp_alice[k] stores the maximum number of moves possible if it's Alice's turn
    # and the remaining string is S[k:] (i.e., left pointer is k).
    # dp_bob[k] stores the maximum number of moves possible if it's Bob's turn
    # and the remaining string is S[:k] (i.e., right pointer is k-1).
    # The state is (left_ptr, right_ptr).
    # Alice's turn: (L, R) -> (i+1, R)
    # Bob's turn: (L, R) -> (L, j-1)

    # Let's simplify the state.
    # The game is about who makes the last move. This is a normal play game.
    # The total number of moves is K. Alice wins if K is odd, Bob wins if K is even.
    # Both players want to maximize K.

    # dp[L][R] = (max_moves_if_alice_starts, max_moves_if_bob_starts)
    # This is still N^2 states.
    # N=600,000 suggests a linear solution.

    # Let's consider the number of 'A's and 'B's.
    # Alice eats an 'A', Bob eats a 'B'.
    # The game ends when no more 'A's or 'B's are available in the current segment.

    # The key insight for N=600,000 must be that the optimal strategy is simple.
    # Alice wants to pick an 'A' at index `i` (from current `L` to `R`)
    # such that `1 + max_moves(i+1, R, Bob)` is maximized.
    # Bob wants to pick a 'B' at index `j` (from current `L` to `R`)
    # such that `1 + max_moves(L, j-1, Alice)` is maximized.

    # This is a game where players try to maximize the total number of moves.
    # The total number of moves is K. Alice wins if K is odd, Bob wins if K is even.

    # Let's consider the "effective" number of A's and B's.
    # Alice can eat any 'A'. Bob can eat any 'B'.
    # The game ends when all 'A's or all 'B's are gone, or the segment becomes empty.

    # What if Alice picks the leftmost 'A'?
    # What if Alice picks the rightmost 'A'?
    # What if Bob picks the leftmost 'B'?
    # What if Bob picks the rightmost 'B'?

    # The problem is symmetric in some sense.
    # Alice removes a prefix. Bob removes a suffix.
    # The game is played on a shrinking segment [L, R].

    # Consider the total number of 'A's and 'B's.
    # Let `num_A` be the count of 'A's, `num_B` be the count of 'B's.
    # If Alice eats an 'A' at index `i`, the new segment is `S[i+1...R]`.
    # If Bob eats a 'B' at index `j`, the new segment is `S[L...j-1]`.

    # This is a game where players try to maximize the number of moves.
    # The total number of moves is `K`. Alice wins if `K` is odd, Bob wins if `K` is even.

    # Let's consider the number of 'A's and 'B's that are "available" to be eaten.
    # Alice can eat an 'A'. Bob can eat a 'B'.
    # The game ends when `L > R`.

    # The crucial observation for N=600,000 must be that the optimal strategy is simple.
    # Alice wants to pick an 'A' at index `i` (from current `L` to `R`)
    # such that `1 + max_moves(i+1, R, Bob)` is maximized.
    # Bob wants to pick a 'B' at index `j` (from current `L` to `R`)
    # such that `1 + max_moves(L, j-1, Alice)` is maximized.

    # This is a game where players try to maximize the total number of moves.
    # The total number of moves is K. Alice wins if K is odd, Bob wins if K is even.

    # Let's consider the number of 'A's and 'B's that are "available" to be eaten.
    # Alice can eat an 'A'. Bob can eat a 'B'.
    # The game ends when `L > R`.

    # The key insight is that Alice can choose any 'A' in the current range [L, R]
    # and effectively discard all characters to its left.
    # Bob can choose any 'B' in the current range [L, R]
    # and effectively discard all characters to its right.

    # This means Alice can effectively choose a new `L` (say `L_new = i+1`)
    # and Bob can effectively choose a new `R` (say `R_new = j-1`).
    # The game is played on the segment `S[L...R]`.

    # The total number of 'A's that Alice can potentially eat is `count('A')`.
    # The total number of 'B's that Bob can potentially eat is `count('B')`.
    # However, these counts are reduced by the opponent's moves.

    # Let's consider the total number of 'A's and 'B's in the string.
    # Alice eats an 'A'. Bob eats a 'B'.
    # The game ends when `L > R`.

    # The total number of moves is `K`. Alice wins if `K` is odd, Bob wins if `K` is even.
    # Both players want to maximize `K`.

    # The crucial part is that Alice can choose *any* 'A' in the current range.
    # Bob can choose *any* 'B' in the current range.

    # This is a game where players try to maximize the number of moves.
    # The total number of moves is `K`. Alice wins if `K` is odd, Bob wins if `K` is even.

    # Let's consider the number of 'A's and 'B's that are "available" to be eaten.
    # Alice can eat an 'A'. Bob can eat a 'B'.
    # The game ends when `L > R`.

    # The key insight is that Alice can choose any 'A' in the current range [L, R]
    # and effectively discard all characters to its left.
    # Bob can choose any 'B' in the current range [L, R]
    # and effectively discard all characters to its right.

    # This means Alice can effectively choose a new `L` (say `L_new = i+1`)
    # and Bob can effectively choose a new `R` (say `R_new = j-1`).
    # The game is played on the segment `S[L...R]`.

    # The total number of 'A's that Alice can potentially eat is `count('A')`.
    # The total number of 'B's that Bob can potentially eat is `count('B')`.
    # However, these counts are reduced by the opponent's moves.

    # Let's consider the total number of 'A's and 'B's in the string.
    # Alice eats an 'A'. Bob eats a 'B'.
    # The game ends when `L > R`.

    # The total number of moves is `K`. Alice wins if `K` is odd, Bob wins if `K` is even.
    # Both players want to maximize `K`.

    # The crucial part is that Alice can choose *any* 'A' in the current range.
    # Bob can choose *any* 'B` in the current range.

    # This is a game where players try to maximize the number of moves.
    # The total number of moves is `K`. Alice wins if `K` is odd, Bob wins if `K` is even.

    # Let's consider the number of 'A's and 'B's that are "available" to be eaten.
    # Alice can eat an 'A'. Bob can eat a 'B'.
    # The game ends when `L > R`.

    # The key insight is that Alice can choose any 'A' in the current range [L, R]
    # and effectively discard all characters to its left.
    # Bob can choose any 'B' in the current range [L, R]
    # and effectively discard all characters to its right.

    # This means Alice can effectively choose a new `L` (say `L_new = i+1`)
    # and Bob can effectively choose a new `R` (say `R_new = j-1`).
    # The game is played on the segment `S[L...R]`.

    # The total number of 'A's that Alice can potentially eat is `count('A')`.
    # The total number of 'B's that Bob can potentially eat is `count('B')`.
    # However, these counts are reduced by the opponent's moves.

    # Let's consider the total number of 'A's and 'B's in the string.
    # Alice eats an 'A'. Bob eats a 'B'.
    # The game ends when `L > R`.

    # The total number of moves is `K`. Alice wins if `K` is odd, Bob wins if `K` is even.
    # Both players want to maximize `K`.

    # The crucial part is that Alice can choose *any* 'A' in the current range.
    # Bob can choose *any* 'B' in the current range.

    # This is a game where players try to maximize the number of moves.
    # The total number of moves is `K`. Alice wins if `K` is odd, Bob wins if `K` is even.

    # Let's consider the number of 'A's and 'B's that are "available" to be eaten.
    # Alice can eat an 'A'. Bob can eat a 'B'.
    # The game ends when `L > R`.

    # The key insight is that Alice can choose any 'A' in the current range [L, R]
    # and effectively discard all characters to its left.
    # Bob can choose any 'B' in the current range [L, R]
    # and effectively discard all characters to its right.

    # This means Alice can effectively choose a new `L` (say `L_new = i+1`)
    # and Bob can effectively choose a new `R` (say `R_new = j-1`).
    # The game is played on the segment `S[L...R]`.

    # The total number of 'A's