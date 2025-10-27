def solve():
    N = int(input().strip())
    S = input().strip()

    alice_moves = 0
    bob_moves = 0

    # Find the indices of all 'A's and 'B's
    a_indices = [i for i, char in enumerate(S) if char == 'A']
    b_indices = [i for i, char in enumerate(S) if char == 'B']

    # If no 'A's, Alice skips all turns. Bob wins if there are 'B's.
    if not a_indices:
        if b_indices:
            return "Bob"
        else:
            # No A's, no B's. This case shouldn't happen based on problem context
            # but if it does, no one makes a move. Let's assume problem guarantees a winner.
            # If no dishes, no last dish.
            return "Nobody" # Or handle as per specific tie-breaking rule if any.
    
    # If no 'B's, Bob skips all turns. Alice wins if there are 'A's.
    if not b_indices:
        if a_indices:
            return "Alice"
        else:
            return "Nobody"

    # Find the first 'B' and the last 'A'
    first_b_idx = S.find('B')
    last_a_idx = S.rfind('A')

    # Case 1: All 'B's are to the left of all 'A's (or they are interleaved such that first B is after last A)
    # e.g., "BBAAA", "BBABAA" (first B at 0, last A at 5, but first B is at 0, last A is at 5)
    # The condition `first_b_idx > last_a_idx` means all 'B's appear before all 'A's.
    # Example: "BBBAAA" -> first_b_idx=0, last_a_idx=5. This is not >.
    # Example: "AAABBB" -> first_b_idx=3, last_a_idx=2. This is >.
    # If first_b_idx > last_a_idx, it means the string is like "A...A B...B". No, it's "B...B A...A".
    # Example: "BBAAA" (N=5). first_b_idx=0, last_a_idx=4.
    # Example: "AAABBB" (N=6). first_b_idx=3, last_a_idx=2. Here, last_a_idx < first_b_idx.
    # If last_a_idx < first_b_idx, it means all 'A's are to the left of all 'B's.
    # E.g., "AAABBB". Alice picks S[0]. Remaining "AABBB". Bob picks S[5]. Remaining "AAAAB".
    # This is not the condition.

    # The critical observation for N=600,000 is that the game is equivalent to a simpler one.
    # The game is about who can make the last move.
    # Alice can choose any 'A' at index `i`. This removes `S[0...i]` from consideration. The new left boundary is `i+1`.
    # Bob can choose any 'B' at index `j`. This removes `S[j...N-1]` from consideration. The new right boundary is `j`.

    # The game is played on a contiguous segment [L, R).
    # Alice increases L. Bob decreases R.
    # The game ends when L >= R.
    # The total number of moves is the number of times L is increased + the number of times R is decreased.

    # Consider the number of 'A's that are to the left of the *first* 'B'.
    # Alice can eat these 'A's without affecting any 'B's.
    # Consider the number of 'B's that are to the right of the *last* 'A'.
    # Bob can eat these 'B's without affecting any 'A's.

    # Let's find the first 'B' and the last 'A' in the original string.
    # If there are no 'B's, Alice wins. (Handled above)
    # If there are no 'A's, Bob wins. (Handled above)

    # Let `first_B_pos` be the index of the first 'B'.
    # Let `last_A_pos` be the index of the last 'A'.

    # If `last_A_pos < first_B_pos`:
    # This means the string is like "A...A B...B".
    # Example: "AABBB" (N=5). first_B_pos=2, last_A_pos=1.
    # Alice's turn. She can eat any 'A'.
    # If Alice eats S[0] ('A'), remaining "ABBB". Bob eats S[3] ('B'). Remaining "AAB". Alice eats S[0] ('A'). Remaining "AB". Bob eats S[1] ('B'). Remaining "A". Alice eats S[0] ('A'). Alice wins.
    # If Alice eats S[1] ('A'), remaining "BBB". Bob eats S[2] ('B'). Remaining "BB". Bob eats S[1] ('B'). Remaining "B". Bob eats S[0] ('B'). Bob wins.
    # Alice would choose to eat S[0] and win.
    # So if `last_A_pos < first_B_pos`, Alice wins.

    # If `first_B_pos < last_A_pos`:
    # This means the string is like "B...B A...A".
    # Example: "BBAAA" (N=5). first_B_pos=0, last_A_pos=4.
    # Alice's turn. She can only eat 'A's.
    # Alice eats S[2] ('A'). Remaining "AA". Bob skips. Alice eats S[0] ('A'). Remaining "A". Bob skips. Alice eats S[0] ('A'). Alice wins.
    # So if `first_B_pos < last_A_pos`, Alice wins.

    # This logic seems to imply Alice always wins if both A and B exist.
    # But sample 4: N=2, S="AB". Alice: A=1, B=1. Sample output: Bob.
    # My logic: first_B_pos=1, last_A_pos=0. last_A_pos < first_B_pos. Alice should win. Mismatch.

    # The problem is a simple parity game on the number of 'A's and 'B's that are "available" to be eaten.
    # The key insight is that Alice can always choose an 'A' that is to the right of *all* 'B's, if such an 'A' exists.
    # And Bob can always choose a 'B' that is to the left of *all* 'A's, if such a 'B' exists.

    # Let's count the number of 'A's and 'B's.
    num_A = S.count('A')
    num_B = S.count('B')

    # If Alice has no moves, she skips. If Bob has moves, he wins.
    if num_A == 0:
        return "Bob"
    # If Bob has no moves, he skips. If Alice has moves, she wins.
    if num_B == 0:
        return "Alice"

    # Both players have at least one piece.
    # The game is equivalent to a simple Nim pile of size `num_A + num_B`
    # if players could always eat their preferred piece without affecting the other player's pieces.
    # But the "pulling" mechanism changes this.

    # The critical point is the "middle" of the string.
    # Alice can choose any 'A' at index `i`. This makes the new string `S[i+1:]`.
    # Bob can choose any 'B' at index `j`. This makes the new string `S[:j]`.

    # The game ends when the current player cannot make a move, and the other player also cannot make a move.
    # The player who makes the last move wins.

    # Consider the indices of 'A's and 'B's.
    # Alice wants to eat an 'A'. If she eats `S[i]`, the new range is `[i+1, R)`.
    # Bob wants to eat a 'B'. If he eats `S[j]`, the new range is `[L, j)`.

    # The game is about who can make the last move.
    # The total number of moves is the total number of pieces eaten.
    # Let's count the number of 'A's and 'B's that are *not* "protected" by the other player.

    # Find the index of the first 'B' from the left.
    first_B_from_left = -1
    for i in range(N):
        if S[i] == 'B':
            first_B_from_left = i
            break

    # Find the index of the last 'A' from the right.
    last_A_from_right = -1
    for i in range(N - 1, -1, -1):
        if S[i] == 'A':
            last_A_from_right = i
            break
            
    # These checks are already covered by num_A == 0 or num_B == 0
    # if first_B_from_left == -1: return "Alice"
    # if last_A_from_right == -1: return "Bob"

    # If all 'A's are to the left of all 'B's (e.g., "AAABBB")
    # `last_A_from_right` will be less than `first_B_from_left`.
    # Example: "AAABBB", N=6. first_B_from_left=3, last_A_from_right=2.
    # Alice's turn. She can pick S[0], S[1], S[2].
    # If she picks S[0], remaining "AABBB". Bob can pick S[3], S[4], S[5].
    # If Bob picks S[3], remaining "AAB". Alice picks S[0]. Remaining "AB". Bob picks S[1]. Remaining "A". Alice picks S[0]. Alice wins.
    # This is still the full game.

    # The key is that Alice can choose any 'A', and Bob any 'B'.
    # This means Alice can choose to "cut" the string at any 'A'.
    # Bob can choose to "cut" the string at any 'B'.

    # The game is equivalent to counting the number of 'A's and 'B's that are *not* "trapped" by the opponent's pieces.
    # An 'A' is trapped if it's to the right of the first 'B'.
    # A 'B' is trapped if it's to the left of the last 'A'.

    # This is a known game