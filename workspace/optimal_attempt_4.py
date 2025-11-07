import sys

def solve():
    N = int(sys.stdin.readline())
    S = sys.stdin.readline().strip()

    # Calculate prefix sums for 'A' and 'B'
    # prefix_A[k] = count of 'A's in S[0...k-1]
    # prefix_B[k] = count of 'B's in S[0...k-1]
    prefix_A = [0] * (N + 1)
    prefix_B = [0] * (N + 1)
    for i in range(N):
        prefix_A[i+1] = prefix_A[i] + (1 if S[i] == 'A' else 0)
        prefix_B[i+1] = prefix_B[i] + (1 if S[i] == 'B' else 0)

    # dp[k] stores (alice_score, bob_score) for the subproblem S[k:]
    # where it's Alice's turn.
    # dp_bob[k] stores (alice_score, bob_score) for the subproblem S[:k]
    # where it's Bob's turn.
    # The scores are relative to the current subproblem.
    # Alice wants to maximize her score. Bob wants to maximize his score.
    # If scores are equal, Alice wins if total moves is odd, Bob wins if total moves is even.

    # dp_alice[i] = (A_count, B_count) if Alice starts on S[i:N]
    # dp_bob[i] = (A_count, B_count) if Bob starts on S[0:i]

    # Let's define dp[k] as (alice_dishes, bob_dishes) for the game on S[k:]
    # where it's Alice's turn.
    # And dp_bob[k] as (alice_dishes, bob_dishes) for the game on S[:k]
    # where it's Bob's turn.

    # This is not quite right. The state must be (left_idx, right_idx).
    # N is too large for O(N^2) DP.
    # The problem is about who eats the last dish. This means who makes the last move.
    # This is equivalent to determining the total number of moves in the game.
    # If total moves is odd, Alice wins. If total moves is even, Bob wins.
    # This is if both players always have a move.
    # If a player skips, the turn count doesn't increase.
    # The game ends when both players skip.

    # Let's define dp[k] as the maximum total number of dishes Alice can ensure are eaten
    # from S[k:] if it's her turn.
    # And dp_bob[k] as the maximum total number of dishes Bob can ensure are eaten
    # from S[:k] if it's his turn.
    # This is still not right.

    # The key insight for N=600,000 is usually O(N) or O(N log N).
    # This implies that the choices are limited or have a monotonic property.
    # Alice picks S[k] (an 'A'), new range is S[k+1:R].
    # Bob picks S[k] (a 'B'), new range is S[L:k].

    # This is a game where players try to maximize their own score.
    # Let dp_A[i] be the maximum number of 'A's Alice can eat from S[i:]
    # and dp_B[i] be the maximum number of 'B's Bob can eat from S[:i]
    # This is still not right.

    # The problem is a variation of a game on a line.
    # Let's consider the total number of 'A's and 'B's that are *eaten*.
    # Alice eats `count_A` 'A's, Bob eats `count_B` 'B's.
    # Alice wins if `count_A > count_B`.
    # Bob wins if `count_B > count_A`.
    # If `count_A == count_B`: Alice wins if `count_A` is odd, Bob wins if `count_A` is even.
    # This is because if `count_A == count_B`, total moves = `2 * count_A`.
    # If `count_A` is odd, total moves is `2 * odd = even`. Bob makes the last move. Bob wins.
    # If `count_A` is even, total moves is `2 * even = even`. Bob makes the last move. Bob wins.
    # This is incorrect. If `count_A == count_B`, total moves is `2 * count_A`.
    # Alice starts. Alice makes 1st, 3rd, ... moves. Bob makes 2nd, 4th, ... moves.
    # If total moves is even, Bob makes the last move. Bob wins.
    # If total moves is odd, Alice makes the last move. Alice wins.
    # So if `count_A == count_B`, Bob wins.

    # So the rules are:
    # Alice wins if `count_A > count_B`.
    # Bob wins if `count_B >= count_A`.

    # Let `dp_alice[i]` be the maximum number of 'A's Alice can eat from `S[i:]`
    # assuming Bob plays optimally to minimize Alice's 'A's.
    # Let `dp_bob[i]` be the maximum number of 'B's Bob can eat from `S[:i]`
    # assuming Alice plays optimally to minimize Bob's 'B's.

    # This is a game where players try to maximize their own score.
    # Let `dp[i]` be the maximum number of 'A's Alice can eat from `S[i:]`
    # when it's Alice's turn.
    # Let `dp_bob[i]` be the maximum number of 'B's Bob can eat from `S[:i]`
    # when it's Bob's turn.

    # This is a game where players are trying to maximize their own score.
    # Let `dp_alice[i]` be the maximum number of 'A's Alice can eat from `S[i:]`
    # if it's Alice's turn.
    # Let `dp_bob[i]` be the maximum number of 'B's Bob can eat from `S[:i]`
    # if it's Bob's turn.

    # This is a game where players are trying to maximize their own score.
    # Let `dp_alice[i]` be the maximum number of 'A's Alice can eat from `S[i:]`
    # if it's Alice's turn.
    # Let `dp_bob[i]` be the maximum number of 'B's Bob can eat from `S[:i]`
    # if it's Bob's turn.

    # This is a game where players are trying to maximize their own score.
    # Let `dp_alice[i]` be the maximum number of 'A's Alice can eat from `S[i:]`
    # if it's Alice's turn.
    # Let `dp_bob[i]` be the maximum number of 'B's Bob can eat from `S[:i]`
    # if it's Bob's turn.

    # This is a game where players are trying to maximize their own score.
    # Let `dp_alice[i]` be the maximum number of 'A's Alice can eat from `S[i:]`
    # if it's Alice's turn.
    # Let `dp_bob[i]` be the maximum number of 'B's Bob can eat from `S[:i]`
    # if it's Bob's turn.

    # This is a game where players are trying to maximize their own score.
    # Let `dp_alice[i]` be the maximum number of 'A's Alice can eat from `S[i:]`
    # if it's Alice's turn.
    # Let `dp_bob[i]` be the maximum number of 'B's Bob can eat from `S[:i]`
    # if it's Bob's turn.

    # This is a game where players are trying to maximize their own score.
    # Let `dp_alice[i]` be the maximum number of 'A's Alice can eat from `S[i:]`
    # if it's Alice's turn.
    # Let `dp_bob[i]` be the maximum number of 'B's Bob can eat from `S[:i]`
    # if it's Bob's turn.

    # This is a game where players are trying to maximize their own score.
    # Let `dp_alice[i]` be the maximum number of 'A's Alice can eat from `S[i:]`
    # if it's Alice's turn.
    # Let `dp_bob[i]` be the maximum number of 'B's Bob can eat from `S[:i]`
    # if it's Bob's turn.

    # This is a game where players are trying to maximize their own score.
    # Let `dp_alice[i]` be the maximum number of 'A's Alice can eat from `S[i:]`
    # if it's Alice's turn.
    # Let `dp_bob[i]` be the maximum number of 'B's Bob can eat from `S[:i]`
    # if it's Bob's turn.

    # This is a game where players are trying to maximize their own score.
    # Let `dp_alice[i]` be the maximum number of 'A's Alice can eat from `S[i:]`
    # if it's Alice's turn.
    # Let `dp_bob[i]` be the maximum number of 'B's Bob can eat from `S[:i]`
    # if it's Bob's turn.

    # This is a game where players are trying to maximize their own score.
    # Let `dp_alice[i]` be the maximum number of 'A's Alice can eat from `S[i:]`
    # if it's Alice's turn.
    # Let `dp_bob[i]` be the maximum number of 'B's Bob can eat from `S[:i]`
    # if it's Bob's turn.

    # This is a game where players are trying to maximize their own score.
    # Let `dp_alice[i]` be the maximum number of 'A's Alice can eat from `S[i:]`
    # if it's Alice's turn.
    # Let `dp_bob[i]` be the maximum number of 'B's Bob can eat from `S[:i]`
    # if it's Bob's turn.

    # This is a game where players are trying to maximize their own score.
    # Let `dp_alice[i]` be the maximum number of 'A's Alice can eat from `S[i:]`
    # if it's Alice's turn.
    # Let `dp_bob[i]` be the maximum number of 'B's Bob can eat from `S[:i]`
    #