import sys

def solve():
    N = int(sys.stdin.readline())
    S = sys.stdin.readline().strip()

    a_indices = [i for i, char in enumerate(S) if char == 'A']
    b_indices = [i for i, char in enumerate(S) if char == 'B']

    if not a_indices: # No 'A's, Alice skips all turns. Bob eats all 'B's.
        return "Bob"
    if not b_indices: # No 'B's, Bob skips all turns. Alice eats all 'A's.
        return "Alice"

    # The game is equivalent to a game where players try to maximize the number of their own pieces eaten,
    # and minimize the number of opponent's pieces eaten.
    # The winner is determined by the parity of the total number of dishes eaten.
    # Alice wants the total number of dishes eaten to be odd.
    # Bob wants the total number of dishes eaten to be even.

    # Let's find the first 'B' and the last 'A'.
    # Any 'A' before the first 'B' can be eaten by Alice without Bob being able to remove it
    # (unless Bob chooses a 'B' to its right, but that's not optimal for Bob if he wants to maximize his 'B's).
    # Any 'B' after the last 'A' can be eaten by Bob without Alice being able to remove it.

    first_b_idx = b_indices[0]
    last_a_idx = a_indices[-1]

    # Count 'A's that are definitely eaten by Alice (left of first 'B')
    # and 'B's that are definitely eaten by Bob (right of last 'A').
    alice_safe_count = 0
    for i in a_indices:
        if i < first_b_idx:
            alice_safe_count += 1
        else:
            break # A's are sorted, so we can stop

    bob_safe_count = 0
    for i in reversed(b_indices):
        if i > last_a_idx:
            bob_safe_count += 1
        else:
            break # B's are sorted, so we can stop

    # The "middle" part of the string is S[first_b_idx ... last_a_idx].
    # If first_b_idx > last_a_idx, it means all 'A's are to the left of all 'B's.
    # In this case, there's no contested middle section.
    # Alice eats all 'A's, Bob eats all 'B's. Total dishes = len(a_indices) + len(b_indices).
    if first_b_idx > last_a_idx:
        total_dishes_eaten = len(a_indices) + len(b_indices)
        return "Alice" if total_dishes_eaten % 2 == 1 else "Bob"

    # If there is an overlap (first_b_idx <= last_a_idx), the game is played on the middle segment.
    # In this middle segment, Alice can choose any 'A' and Bob can choose any 'B'.
    # Alice wants to maximize her 'A's and minimize Bob's 'B's.
    # Bob wants to maximize his 'B's and minimize Alice's 'A's.

    # The key insight is that in the contested middle segment, players will try to eat as many of their own dishes
    # as possible, while minimizing the opponent's dishes.
    # Alice can choose an 'A' at index `k`. This removes all dishes `S[0...k-1]`.
    # Bob can choose a 'B' at index `k`. This removes all dishes `S[k+1...N-1]`.
    # This means Alice can remove any 'B's to the left of her chosen 'A'.
    # Bob can remove any 'A's to the right of his chosen 'B'.

    # Consider the maximum number of 'A's Alice can eat from the middle segment, and 'B's Bob can eat.
    # Alice can eat all 'A's. Bob can eat all 'B's.
    # The total number of moves will be the sum of 'A's and 'B's that are *actually eaten*.
    # The players will try to eat as many of their own dishes as possible.
    # The number of 'A's Alice will eat is `len(a_indices)`.
    # The number of 'B's Bob will eat is `len(b_indices)`.
    # The total number of dishes eaten will be `len(a_indices) + len(b_indices)`.
    # This is because any 'A' Alice wants to eat, she can, by picking it.
    # Any 'B' Bob wants to eat, he can, by picking it.
    # The only way a dish is NOT eaten is if it's knocked off.
    # Alice's move at `i` removes `0...i-1`. Bob's move at `j` removes `j+1...N-1`.
    # If Alice picks `A` at `i`, she eats it. The new range is `[i+1, R]`.
    # If Bob picks `B` at `j`, he eats it. The new range is `[L, j-1]`.
    # This means the game is effectively about reducing the range `[L, R]`.
    # The total number of dishes eaten is `N_A + N_B`.
    # The player who makes the last move (eats the last dish) wins.
    # If `N_A + N_B` is odd, Alice wins. If even, Bob wins.

    # This simple parity argument holds if players can always make their preferred move without losing their own pieces.
    # But here, a player's move can remove opponent's pieces.
    # Alice can choose an 'A' that is far to the right to remove many 'B's to its left.
    # Bob can choose a 'B' that is far to the left to remove many 'A's to its right.

    # The game is about who can eat the last dish.
    # This means they want to be the one who makes the final move.
    # The total number of dishes eaten will be `len(a_indices) + len(b_indices)`.
    # The crucial part is that players can skip their turn if they have no preferred dishes.
    # This means the game might end with one player having dishes left, but no opponent dishes to eat.

    # Let's re-examine the sample case: ABBAAAB
    # N=7. A_indices = [0, 3, 4, 5], B_indices = [1, 2, 6].
    # Alice_count = 4, Bob_count = 3. Total = 7.
    # first_b_idx = 1. last_a_idx = 5.
    # Alice_safe_count: S[0]='A'. So 1.
    # Bob_safe_count: S[6]='B'. So 1.
    # Middle segment: S[1...5] = BBAAA.
    # Alice eats S[0]. Remaining: BBAAAB. L=1, R=6. Alice_count=3, Bob_count=3. Total=6.
    # Bob eats S[6]. Remaining: BBAAA. L=1, R=5. Alice_count=3, Bob_count=2. Total=5.
    # Alice eats S[3]. Remaining: AA. L=4, R=5. Alice_count=2, Bob_count=0. Total=2.
    # Bob skips.
    # Alice eats S[4]. Remaining: A. L=5, R=5. Alice_count=1, Bob_count=0. Total=1.
    # Bob skips.
    # Alice eats S[5]. Remaining: empty. L=6, R=5. Alice_count=0, Bob_count=0. Total=0.
    # Alice wins.

    # The total number of dishes eaten is not fixed.
    # It depends on the choices.
    # In the example, Alice ate 4 'A's, Bob ate 1 'B'. Total 5 dishes. Alice wins.
    # Initial: 4 'A's, 3 'B's.
    # Alice's first move: she chose S[3]. This removed S[0,1,2].
    # S[0] was 'A', S[1,2] were 'B'.
    # Alice ate S[3].
    # Dishes removed: S[0] (A), S[1] (B), S[2] (B).
    # Remaining: S[4,5,6] = AAB.
    # Alice has eaten 1 'A'. 0 'A's removed. 2 'B's removed.
    # Remaining 'A's: 2 (S[4], S[5]). Remaining 'B's: 1 (S[6]).
    # Total remaining dishes: 3.
    # Bob's turn. He eats S[6]. Remaining: S[4,5] = AA.
    # Bob has eaten 1 'B'. 0 'B's removed. 0 'A's removed.
    # Remaining 'A's: 2. Remaining 'B's: 0.
    # Total remaining dishes: 2.
    # Alice's turn. She eats S[4]. Remaining: S[5] = A.
    # Alice has eaten 1 'A'.
    # Remaining 'A's: 1. Remaining 'B's: 0.
    # Total remaining dishes: 1.
    # Bob skips.
    # Alice's turn. She eats S[5]. Remaining: empty.
    # Alice has eaten 1 'A'.
    # Total dishes eaten: (1+1+1) A's by Alice + (1) B's by Bob = 4 A's, 1 B. Total 5. Alice wins.

    # The total number of dishes eaten is `N_A_eaten + N_B_eaten`.
    # Alice wants this sum to be odd. Bob wants it to be even.

    # Let's count the number of 'A's and 'B's in the string.
    # Alice can always eat an 'A' if there is one.
    # Bob can always eat a 'B' if there is one.

    # The game ends when the current segment [L, R] has no 'A's for Alice or no 'B's for Bob.
    # Or when L > R.

    # Consider the number of 'A's and 'B's that are "interspersed".
    # These are the 'A's that are to the right of some 'B' and 'B's that are to the left of some 'A'.
    # The "middle" part of the string.
    # The dishes that are not in the initial `A...A` prefix or `B...B` suffix.

    # Let's find the first 'B' and the last 'A'.
    # `first_b_idx`: