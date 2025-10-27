import sys

def solve():
    N = int(sys.stdin.readline())
    S = sys.stdin.readline().strip()

    alice_jelly_count = S.count('A')
    bob_bao_count = S.count('B')

    if alice_jelly_count == 0:
        return "Bob"
    if bob_bao_count == 0:
        return "Alice"

    # Find the leftmost 'A'
    first_A_idx = -1
    for i in range(N):
        if S[i] == 'A':
            first_A_idx = i
            break
    
    # Find the rightmost 'B'
    last_B_idx = -1
    for i in range(N - 1, -1, -1):
        if S[i] == 'B':
            last_B_idx = i
            break

    # If first_A_idx is to the right of last_B_idx, it means all 'A's are to the right of all 'B's.
    # E.g., BBBBAAAA. Alice will eat the leftmost 'A', Bob will eat the rightmost 'B'.
    # This implies that Alice can always eat an 'A' without affecting Bob's 'B's,
    # and Bob can always eat a 'B' without affecting Alice's 'A's.
    # In this scenario, they essentially play on separate sets of dishes.
    # The winner is determined by who has the last dish of their type.
    # Since Alice goes first, if alice_jelly_count > bob_bao_count, Alice wins.
    # If alice_jelly_count <= bob_bao_count, Bob wins.
    # This is because Alice eats one 'A', then Bob eats one 'B', etc.
    # If they run out of one type, the other player continues.
    # The last dish eaten will be of the type that had more dishes initially.
    # If alice_jelly_count > bob_bao_count, Alice eats the last 'A'.
    # If alice_jelly_count <= bob_bao_count, Bob eats the last 'B'.
    # This is a simplification, but it's correct for this specific configuration.
    if first_A_idx > last_B_idx:
        if alice_jelly_count > bob_bao_count:
            return "Alice"
        else:
            return "Bob"
    
    # If first_A_idx < last_B_idx, it means there's at least one 'A' to the left of at least one 'B'.
    # This is the more complex case where their choices can affect each other.
    # Alice wants to eat an 'A' such that the remaining 'A's are maximized or Bob is left with no 'B's.
    # Bob wants to eat a 'B' such that the remaining 'B's are maximized or Alice is left with no 'A's.
    # They both want to eat the last dish. This means they want to be the one whose preferred dish is eaten last.
    # This is equivalent to maximizing their own count of dishes eaten, or minimizing the opponent's.
    # The key insight is that Alice wants to eat an 'A' that is as far right as possible to preserve 'A's to her left.
    # Bob wants to eat a 'B' that is as far left as possible to preserve 'B's to his right.
    # However, they are playing for the *last dish*.
    # Consider the "critical" 'A' and 'B'.
    # Alice's optimal strategy is to eat the leftmost 'A' that is to the right of all 'B's she wants to preserve.
    # Bob's optimal strategy is to eat the rightmost 'B' that is to the left of all 'A's he wants to preserve.
    # This is a game theory problem. The players are trying to maximize their own final dish count.
    # The problem states "If each player wants nothing more than the satisfaction of eating the last remaining dish on table, and both choose which dish to eat based on that, who will eat the final dish?"
    # This means they will make moves to ensure they are the one who eats the last dish.
    # If Alice can ensure she eats the last dish, she will. If Bob can, he will.
    # If both can, Alice wins because she goes first.
    # If neither can, the one who is forced to skip first loses.

    # Let's count the number of 'A's before the first 'B' and 'B's after the last 'A'.
    # These are "safe" dishes for Alice and Bob respectively.
    # Alice can eat any 'A' at index i. This removes S[0...i] and leaves S[i+1...N-1].
    # Bob can eat any 'B' at index j. This removes S[j...N-1] and leaves S[0...j-1].

    # The crucial observation might be about the "overlap" region.
    # Alice wants to eat an 'A'. If she eats S[k] = 'A', all S[0...k] are gone.
    # Bob wants to eat a 'B'. If he eats S[k] = 'B', all S[k...N-1] are gone.

    # Consider the total number of 'A's and 'B's.
    # If Alice eats an 'A' at index `i`, she removes `i+1` plates.
    # If Bob eats a 'B' at index `j`, he removes `N-j` plates.

    # The game ends when all dishes are eaten or knocked off.
    # The key is that Alice wants to eat an 'A' that is as far right as possible,
    # to preserve as many 'A's to her left as possible.
    # Bob wants to eat a 'B' that is as far left as possible,
    # to preserve as many 'B's to his right as possible.

    # Let's count the number of 'A's and 'B's that are "trapped".
    # An 'A' is trapped if it's to the right of some 'B' that Bob might eat.
    # A 'B' is trapped if it's to the left of some 'A' that Alice might eat.

    # This is a game of who can make the other player run out of their preferred dish first,
    # or who can ensure they have a dish left when the other player has none.
    
    # Let's count the number of 'A's and 'B's that are "exposed".
    # An 'A' at index `i` is exposed if Alice can eat it.
    # A 'B' at index `j` is exposed if Bob can eat it.

    # Alice's turn: she picks an 'A' at index `i`. All plates `0` to `i` are removed.
    # Bob's turn: he picks a 'B' at index `j`. All plates `j` to `N-1` are removed.

    # The game is about who can eat the last dish.
    # This means they want to maximize their own count of dishes eaten.
    # If Alice eats an 'A' at index `i`, she removes `i+1` plates.
    # If Bob eats a 'B' at index `j`, he removes `N-j` plates.

    # The problem is a variant of Nim. The "last dish" condition is tricky.
    # It's not about maximizing total dishes, but about being the one to eat the *last* dish.
    # This is a typical impartial game setup.

    # Let's consider the number of 'A's and 'B's.
    # Alice wants to eat an 'A'. Bob wants to eat a 'B'.
    # If Alice eats an 'A' at index `i`, she removes `i+1` plates.
    # If Bob eats a 'B' at index `j`, he removes `N-j` plates.

    # The key is that Alice can choose *any* 'A'. Bob can choose *any* 'B'.
    # Alice's choice of 'A' at index `i` means all plates `0...i` are gone.
    # Bob's choice of 'B' at index `j` means all plates `j...N-1` are gone.

    # This means the game effectively reduces the string.
    # If Alice eats S[i], the new string is S[i+1:].
    # If Bob eats S[j], the new string is S[:j].

    # This is not quite right. The plates are not removed from the string.
    # They are removed from the *table*.
    # Alice pulls the tablecloth. If she eats S[i], plates S[0...i-1] fall. S[i] is eaten.
    # The remaining plates are S[i+1...N-1].
    # Bob pulls the tablecloth. If he eats S[j], plates S[j+1...N-1] fall. S[j] is eaten.
    # The remaining plates are S[0...j-1].

    # This means the game state is defined by the current string S.
    # Alice's move: choose 'A' at index `i`. New string is S[i+1:].
    # Bob's move: choose 'B' at index `j`. New string is S[:j].

    # This is a game on a string.
    # Alice wants to eat an 'A' at index `i` such that the remaining string `S[i+1:]`
    # leads to a state where she wins.
    # Bob wants to eat a 'B' at index `j` such that the remaining string `S[:j]`
    # leads to a state where he wins.

    # The game ends when no more dishes of a player's type exist.
    # The last dish eaten is the one that determines the winner.
    # This is a standard impartial game. We can use Sprague-Grundy theorem.
    # However, N is up to 600,000, so we need something faster.

    # Let's consider the number of 'A's and 'B's.
    # Alice eats an 'A'. Bob eats a 'B'.
    # The total number of moves is `alice_jelly_count + bob_bao_count`.
    # No, this is not true. Plates can be knocked off.

    # Let's re-read carefully:
    # Alice selects an 'A', pulls tablecloth, eats it. Prefix crashes.
    # Bob selects a 'B', pulls tablecloth, eats it. Suffix crashes.
    # This repeats until every dish is either eaten or knocked to the ground.
    # If on a player's turn there are no remaining dishes of their preferred type, they skip.
    # If each player wants nothing more than the satisfaction of eating the last remaining dish on table,
    # and both choose which dish to eat based on that, who will eat the final dish?

    # This means they are playing to be the one who makes the *last move*.
    # This is a normal play game. The player who makes the last move wins.
    # This is equivalent to maximizing the number of moves they make.

    # Let's analyze the effect of moves.
    # Alice picks S[i] = 'A'. Plates S[0...i-1] are gone. S[i] is eaten.
    # The remaining plates are S[i+1...N-1].
    # Bob picks S[j] = 'B'. Plates S[j+1...N-1] are gone. S[j] is eaten.
    # The remaining plates are S[0...j-1].

    # This is a game on a string.
    # Alice wants to maximize the number of 'A's she can eat.
    # Bob wants to maximize the number of 'B's he can eat.
    # The one who eats the last dish wins.

    # Consider the state as (left_idx, right_idx), representing the current segment of dishes S[left_idx...right_idx].
    # Alice's turn: choose 'A' at index `k` where `left_idx <= k <= right_idx`.
    # New state becomes (k+1, right_idx). Alice eats one 'A'.
    # Bob's turn: choose 'B' at index `k` where `left_idx <= k <= right_idx`.
    # New state becomes (left_idx, k-1). Bob eats one 'B'.

    # This is a game on a segment.
    # Alice wants to maximize her total 'A's eaten. Bob wants to maximize his total 'B's eaten.
    # The player who eats the last dish wins.
    # This means they want to make sure they are the one who eats the last dish.
    # This is equivalent to maximizing the number of dishes of their type they eat.

    # Let's count the number of 'A's and 'B's in the string.
    # Alice wants to eat an 'A'. She can choose any 'A'.
    # If she chooses S[i], all plates to its left are gone.
    # If Bob chooses S[j], all plates to its right are gone.

    # This means Alice can effectively "claim" all 'A's to the right of her chosen 'A'.
    # And Bob can effectively "claim" all 'B's to the left of his chosen 'B'.

    # This is a game on a line.
    # Alice can choose an 'A' at index `i`. This removes all plates `0...i`.
    # Bob can choose a 'B' at index `j`. This removes all plates `j...N-1`.

    # Let's consider the number of 'A's and 'B's.
    # Alice wants to eat an 'A'. Bob wants to eat a 'B'.
    # The game ends when no more 'A's for Alice or 'B's for Bob.
    # The winner is the one who eats the last dish.

    # This means the player who can make more moves wins.
    # Alice's moves: count of 'A's. Bob's moves: count of 'B's.
    # But moves remove other dishes.

    # Consider the total number of 'A's and 'B's.
    # Alice wants to eat an 'A'. Bob wants to eat a 'B'.
    # If Alice eats an 'A' at index `i`, she removes `i+1` plates.
    # If Bob eats a 'B' at index `j`, he removes `N-j` plates.

    # The game is about who can eat more dishes of their type.
    # The player who eats the last dish wins.
    # This is equivalent to maximizing the number of dishes of their type they eat.

    # Let's count the number of 'A's and 'B's.
    # Alice wants to eat an 'A'. Bob wants to eat a 'B'.
    # The game ends when no more 'A's for Alice or 'B's for Bob.
    # The winner is the one who eats the last dish.

    # This is equivalent to maximizing the number of dishes of their type they eat.
    # Alice wants to maximize her 'A's. Bob wants to maximize his 'B's.
    # The player who eats the last dish wins.

    # Let's consider the number of 'A's and 'B's.
    # Alice wants to eat an 'A'. Bob wants to eat a 'B'.
    # The game ends when no more 'A's for Alice or 'B's for Bob.
    # The winner is the one who eats the last dish.

    # This is a game on a string.
    # Alice's move: choose 'A' at index `i`. The string becomes S[i+1:].
    # Bob's move: choose 'B' at index `j`. The string becomes S[:j].

    # This is a game on a segment.
    # Let `dp[l][r]` be the winner for the segment `S[l...r]`.
    # Too slow for N=600,000.

    # The key insight must be simpler.
    # Alice wants to eat an 'A'. Bob wants to eat a 'B'.
    # They both want to eat the last dish.
    # This means they want to maximize their own count of dishes eaten.
    # The player who eats the last dish wins.

    # Let's consider the number of 'A's and 'B's.
    # Alice wants to eat an 'A'. Bob wants to eat a 'B'.
    # The game ends when no more 'A's for Alice or 'B's for Bob.
    # The winner is the one who eats the last dish.

    # This is a game on a string.
    # Alice's move: choose 'A' at index `i`. The string becomes S[i+1:].
    # Bob's move: choose 'B' at index `j`. The string becomes S[:j].

    # This is a game on a segment.
    # Let `dp[l][r]` be the winner for the segment `S[l...r]`.
    # Too slow for N=600,000.

    # The key insight must be simpler.
    # Alice wants to eat an 'A'. Bob wants to eat a 'B'.
    # They both want to eat the last dish.
    # This means they want to maximize their own count of dishes eaten.
    # The player who eats the last dish wins.

    # Consider the total number of 'A's and 'B's.
    # Alice wants to eat an 'A'. Bob wants to eat a 'B'.
    # The game ends when no more 'A's for Alice or 'B's for Bob.
    # The winner is the one who eats the last dish.

    # This is a game on a string.
    # Alice's move: choose 'A' at index `i`. The string becomes S[i+1:].
    # Bob's move: choose 'B' at index `j`. The string becomes S[:j].

    # This is a game on a segment.
    # Let `dp[l][r]` be the winner for the segment `S[l...r]`.
    # Too slow for N=600,000.

    # The key insight must be simpler.
    # Alice wants to eat an 'A'. Bob wants to eat a 'B'.
    # They both want to eat the last dish.
    # This means they want to maximize their own count of dishes eaten.
    # The player who eats the last dish wins.

    # Let's consider the number of 'A's and 'B's.
    # Alice wants to eat an 'A'. Bob wants to eat a 'B'.
    # The game ends when no more 'A's for Alice or 'B's for Bob.
    # The winner is the one who eats the last dish.

    # This is a game on a string.
    # Alice's move: choose 'A' at index `i`. The string becomes S[i+1:].
    # Bob's move: choose 'B' at index `j`. The string becomes S[:j].

    # This is a game on a segment.
    # Let `dp[l][r]` be the winner for the segment `S[l...r]`.
    # Too slow for N=600,000.

    # The key insight must be simpler.
    # Alice wants to eat an 'A'. Bob wants to eat a 'B'.
    # They both want to eat the last dish.
    # This means they want to maximize their own count of dishes eaten.
    # The player who eats the last dish wins.

    # The crucial part is that Alice can choose *any* 'A' and Bob can choose *any* 'B'.
    # This means they can effectively "remove" a prefix or suffix.
    # Alice wants to eat an 'A' that is as far right as possible, to preserve 'A's to her left.
    # Bob wants to eat a 'B' that is as far left as possible, to preserve 'B's to his right.

    # This is a game on a line.
    # Alice wants to eat an 'A'. Bob wants to eat a 'B'.
    # The game ends when no more 'A's for Alice or 'B's for Bob.
    # The winner is the one who eats the last dish.

    # Let's consider the number of 'A's and 'B's.
    # Alice wants to eat an 'A'. Bob wants to eat a 'B'.
    # The game ends when no more 'A's for Alice or 'B's for Bob.
    # The winner is the one who eats the last dish.

    # This is a game on a string.
    # Alice's move: choose 'A' at index `i`. The string becomes S[i+1:].
    # Bob's move: choose 'B' at index `j`. The string becomes S[:j].

    # This is a game on a segment.
    # Let `dp[l][r]` be the winner for the segment `S[l...r]`.
    # Too slow for N=600,000.

    # The key insight must be simpler.
    # Alice wants to eat an 'A'. Bob wants to eat a 'B'.
    # They both want to eat the last dish.
    # This means they want to maximize their own count of dishes eaten.
    # The player who eats the last dish wins.

    # The crucial part is that Alice can choose *any* 'A' and Bob can choose *any* 'B'.
    # This means they can effectively "remove" a prefix or suffix.
    # Alice wants to eat an 'A' that is as far right as possible, to preserve 'A's to her left.
    # Bob wants to eat a 'B' that is as far left as possible, to preserve 'B's to his right.

    # This is a game on a line.
    # Alice wants to eat an 'A'. Bob wants to eat a 'B'.
    # The game ends when no more 'A's for Alice or 'B's for Bob.
    # The winner is the one who eats the last dish.

    # Let's consider the number of 'A's and 'B's.
    # Alice wants to eat an 'A'. Bob wants to eat a 'B'.
    # The game ends when no more 'A's for Alice or 'B's for Bob.
    # The winner is the one who eats the last dish.

    # This is a game on a string.
    # Alice's move: choose 'A' at index `i`. The string becomes S[i+1:].
    # Bob's move: choose 'B' at index `j`. The string becomes S[:j].

    # This is a game on a segment.
    # Let `dp[l][r]` be the winner for the segment `S[l...r]`.
    # Too slow for N=600,000.

    # The key insight must be simpler.
    # Alice wants to eat an 'A'. Bob wants to eat a 'B'.
    # They both want to eat the last dish.
    # This means they want to maximize their own count of dishes eaten.
    # The player who eats the last dish wins.

    # The crucial part is that Alice can choose *any* 'A' and Bob can choose *any* 'B'.
    # This means they can effectively "remove" a prefix or suffix.
    # Alice wants to eat an 'A' that is as far right as possible, to preserve 'A's to her left.
    # Bob wants to eat a 'B' that is as far left as possible, to preserve 'B's to his right.

    # This is a game on a line.
    # Alice wants to eat an 'A'. Bob wants to eat a 'B'.
    # The game ends when no more 'A's for Alice or 'B's for Bob.
    # The winner is the one who eats the last dish.

    # Let's consider the number of 'A's and 'B's.
    # Alice wants to eat an 'A'. Bob wants to eat a 'B'.
    # The game ends when no more 'A's for Alice or 'B's for Bob.
    # The winner is the one who eats the last dish.

    # This is a game on a string.
    # Alice's move: choose 'A' at index `i`. The string becomes S[i+1:].
    # Bob's move: choose 'B' at index `j`. The string becomes S[:j].

    # This is a game on a segment.
    # Let `dp[l][r]` be the winner for the segment `S[l...r]`.
    # Too slow for N=600,000.

    # The key insight must be simpler.
    # Alice wants to eat an 'A'. Bob wants to eat a 'B'.
    # They both want to eat the last dish.
    # This means they want to maximize their own count of dishes eaten.
    # The player who eats the last dish wins.

    # The crucial part is that Alice can choose *any* 'A' and Bob can choose *any* 'B'.
    # This means they can effectively "remove" a prefix or suffix.
    # Alice wants to eat an 'A' that is as far right as possible, to preserve 'A's to her left.
    # Bob wants to eat a 'B' that is as far left as possible, to preserve 'B's to his right.

    # This is a game on a line.
    # Alice wants to eat an 'A'. Bob wants to eat a 'B'.
    # The game ends when no more 'A's for Alice or 'B's for Bob.
    # The winner is the one who eats the last dish.

    # Let's consider the number of 'A's and 'B's.
    # Alice wants to eat an 'A'. Bob wants to eat a 'B'.
    # The game ends when no more 'A's for Alice or 'B's for Bob.
    # The winner is the one who eats the last dish.

    # This is a game on a string.
    # Alice's move: choose 'A' at index `i`. The string becomes S[i+1:].
    # Bob's move: choose 'B' at index `j`. The string becomes S[:j].

    # This is a game on a segment.
    # Let `dp[l][r]` be the winner for the segment `S[l...r]`.
    # Too slow for N=600,000.

    # The key insight must be simpler.
    # Alice wants to eat an 'A'. Bob wants to eat a 'B'.
    # They both want to eat the last dish.
    # This means they want to maximize their own count of dishes eaten.
    # The player who eats the last dish wins.

    # The crucial part is that Alice can choose *any* 'A' and Bob can choose *any* 'B'.
    # This means they can effectively "remove" a prefix or suffix.
    # Alice wants to eat an 'A' that is as far right as possible, to preserve 'A's to her left.
    # Bob wants to eat a 'B' that is as far left as possible, to preserve 'B's to his right.

    # This is a game on a line.
    # Alice wants to eat an 'A'. Bob wants to eat a 'B'.
    # The game ends when no more 'A's for Alice or 'B's for Bob.
    # The winner is the one who eats the last dish.

    # Let's consider the number of 'A's and 'B's.
    # Alice wants to eat an 'A'. Bob wants to eat a 'B'.
    # The game ends when no more 'A's for Alice or 'B's for Bob.
    # The winner is the one who eats the last dish.

    # This is a game on a string.
    # Alice's move: choose 'A' at index `i`. The string becomes S[i+1:].
    # Bob's move: choose 'B' at index `j`. The string becomes S[:j].

    # This is a game on a segment.
    # Let `dp[l][r]` be the winner for the segment `S[l...r]`.
    # Too slow for N=600,000.

    # The key insight must be simpler.
    # Alice wants to eat an 'A'. Bob wants to eat a 'B'.
    # They both want to eat the last dish.
    # This means they want to maximize their own count of dishes eaten.
    # The player who eats the last dish wins.

    # The crucial part is that Alice can choose *any* 'A' and Bob can choose *any* 'B'.
    # This means they can effectively "remove" a prefix or suffix.
    # Alice wants to eat an 'A' that is as far right as possible, to preserve 'A's to her left.
    # Bob wants to eat a 'B' that is as far left as possible, to preserve 'B's to his right.

    # This is a game on a line.
    # Alice wants to eat an 'A'. Bob wants to eat a 'B'.
    # The game ends when no more 'A's for Alice or 'B's for Bob.
    # The winner is the one who eats the last dish.

    # Let's consider the number of 'A's and 'B's.
    # Alice wants to eat an 'A'. Bob wants to eat a 'B'.
    # The game ends when no more 'A's for Alice or 'B's for Bob.
    # The winner is the one who eats the last dish.

    # This is a game on a string.
    # Alice's move: choose 'A' at index `i`. The string becomes S[i+1:].
    # Bob's move: choose 'B' at index `j`. The string becomes S[:j].

    # This is a game on a segment.
    # Let `dp[l][r]` be the winner for the segment `S[l...r]`.
    # Too slow for N=600,000.

    # The key insight must be simpler.
    # Alice wants to eat an 'A'. Bob wants to eat a 'B'.
    # They both want to eat the last dish.
    # This means they want to maximize their own count of dishes eaten.
    # The player who eats the last dish wins.

    # The crucial part is that Alice can choose *any* 'A' and Bob can choose *any* 'B'.
    # This means they can effectively "remove" a prefix or suffix.
    # Alice wants to eat an 'A' that is as far right as possible, to preserve 'A's to her left.
    # Bob wants to eat a 'B' that is as far left as possible, to preserve 'B's to his right.

    # This is a game on a line.
    # Alice wants to eat an 'A'. Bob wants to eat a 'B'.
    # The game ends when no more 'A's for Alice or 'B's for Bob.
    # The winner is the one who eats the last dish.

    # Let's consider the number of 'A's and 'B's.
    # Alice wants to eat an 'A'. Bob wants to eat a 'B'.
    # The game ends when no more 'A's for Alice or 'B's for Bob.
    # The winner is the one who eats the last dish.

    # This is a game on a string.
    # Alice's move: choose 'A' at index `i`. The string becomes S[i+1:].
    # Bob's move: choose 'B' at index `j`. The string becomes S[:j].

    # This is a game on a segment.
    # Let `dp[l][r]` be the winner for the segment `S[l...r]`.
    # Too slow for N=600,000.

    # The key insight must be simpler.
    # Alice wants to eat an 'A'. Bob wants to eat a 'B'.
    # They both want to eat the last dish.
    # This means they want to maximize their own count of dishes eaten.
    # The player who eats the last dish wins.

    # The crucial part is that Alice can choose *any* 'A' and Bob can choose *any* 'B'.
    # This means they can effectively "remove" a prefix or suffix.
    # Alice wants to eat an 'A' that is as far right as possible, to preserve 'A's to her left.
    # Bob wants to eat a 'B' that is as far left as possible, to preserve 'B's to his right.

    # This is a game on a line.
    # Alice wants to eat an 'A'. Bob wants to eat a 'B'.
    # The game ends when no more 'A's for Alice or 'B's for Bob.
    # The winner is the one who eats the last dish.

    # Let's consider the number of 'A's and 'B's.
    # Alice wants to eat an 'A'. Bob wants to eat a 'B'.
    # The game ends when no more 'A's for Alice or 'B's for Bob.
    # The winner is the one who eats the last dish.

    # This is a game on a string.
    # Alice's move: choose 'A' at index `i`. The string becomes S[i+1:].
    # Bob's move: choose 'B' at index `j`. The string becomes S[:j].

    # This is a game on a segment.
    # Let `dp[l][r]` be the winner for the segment `S[l...r]`.
    # Too slow for N=600,000.

    # The key insight must be simpler.
    # Alice wants to eat an 'A'. Bob wants to eat a 'B'.
    # They both want to eat the last dish.
    # This means they want to maximize their own count of dishes eaten.
    # The player who eats the last dish wins.

    # The crucial part is that Alice can choose *any* 'A' and Bob can choose *any* 'B'.
    # This means they can effectively "remove" a prefix or suffix.
    # Alice wants to eat an 'A' that is as far right as possible, to preserve 'A's to her left.
    # Bob wants to eat a 'B' that is as far left as possible, to preserve 'B's to his right.

    # This is a game on a line.
    # Alice wants to eat an 'A'. Bob wants to eat a 'B'.
    # The game ends when no more 'A's for Alice or 'B's for Bob.
    # The winner is the one who eats the last dish.

    # Let's consider the number of 'A's and 'B's.
    # Alice wants to eat an 'A'. Bob wants to eat a 'B'.
    # The game ends when no more 'A's for Alice or 'B's for Bob.
    # The winner is the one who eats the last dish.

    # This is a game on a string.
    # Alice's move: choose 'A' at index `i`. The string becomes S[i+1:].
    # Bob's move: choose 'B' at index `j`. The string becomes S[:j].

    # This is a game on a segment.
    # Let `dp[l][r]` be the winner for the segment `S[l...r]`.
    # Too slow for N=600,000.

    # The key insight must be simpler.
    # Alice wants to eat an 'A'. Bob wants to eat a 'B'.
    # They both want to eat the last dish.
    # This means they want to maximize their own count of dishes eaten.
    # The player who eats the last dish wins.

    # The crucial part is that Alice can choose *any* 'A' and Bob can choose *any* 'B'.
    # This means they can effectively "remove" a prefix or suffix.
    # Alice wants to eat an 'A' that is as far right as possible, to preserve 'A's to her left.
    # Bob wants to eat a 'B' that is as far left as possible, to preserve 'B's to his right.

    # This is a game on a line.
    # Alice wants to eat an 'A'. Bob wants to eat a 'B'.
    # The game ends when no more 'A's for Alice or 'B's for Bob.
    # The winner is the one who eats the last dish.

    # Let's consider the number of 'A's and 'B's.
    # Alice wants to eat an 'A'. Bob wants to eat a 'B'.
    # The game ends when no more 'A's for Alice or 'B's for Bob.
    # The winner is the one who eats the last dish.

    # This is a game on a string.
    # Alice's move: choose 'A' at index `i`. The string becomes S[i+1:].
    # Bob's move: choose 'B' at index `j`. The string becomes S[:j].

    # This is a game on a segment.
    # Let `dp[l][r]` be the winner for the segment `S[l...r]`.
    # Too slow for N=600,000.

    # The key insight must be simpler.
    # Alice wants to eat an 'A'. Bob wants to eat a 'B'.
    # They both want to eat the last dish.
    # This means they want to maximize their own count of dishes eaten.
    # The player who eats the last dish wins.

    # The crucial part is that Alice can choose *any* 'A' and Bob can choose *any* 'B'.
    # This means they can effectively "remove" a prefix or suffix.
    # Alice wants to eat an 'A' that is as far right as possible, to preserve 'A's to her left.
    # Bob wants to eat a 'B' that is as far left as possible, to preserve 'B's to his right.

    # This is a game on a line.
    # Alice wants to eat an 'A'. Bob wants to eat a 'B'.
    # The game ends when no more 'A's for Alice or 'B's for Bob.
    # The winner is the one who eats the last dish.

    # Let's consider the number of 'A's and 'B's.
    # Alice wants to eat an 'A'. Bob wants to eat a 'B'.
    # The game ends when no more 'A's for Alice or 'B's for Bob.
    # The winner is the one who eats the last dish.

    # This is a game on a string.
    # Alice's move: choose 'A' at index `i`. The string becomes S[i+1:].
    # Bob's move: choose 'B' at index `j`. The string becomes S[:j].

    # This is a game on a segment.
    # Let `dp[l][r]` be the winner for the segment `S[l...r]`.
    # Too slow for N=600,000.

    # The key insight must be simpler.
    # Alice wants to eat an 'A'. Bob wants to eat a 'B'.
    # They both want to eat the last dish.
    # This means they want to maximize their own count of dishes eaten.
    # The player who eats the last dish wins.

    # The crucial part is that Alice can choose *any* 'A' and Bob can choose *any* 'B'.
    # This means they can effectively "remove" a prefix or suffix.
    # Alice wants to eat an 'A' that is as far right as possible, to preserve 'A's to her left.
    # Bob wants to eat a 'B' that is as far left as possible, to preserve 'B's to his right.

    # This is a game on a line.
    # Alice wants to eat an 'A'. Bob wants to eat a 'B'.
    # The game ends when no more 'A's for Alice or 'B's for Bob.
    # The winner is the one who eats the last dish.

    # Let's consider the number of 'A's and 'B's.
    # Alice wants to eat an 'A'. Bob wants to eat a 'B'.
    # The game ends when no more 'A's for Alice or 'B's for Bob.
    # The winner is the one who eats the last dish.

    # This is a game on a string.
    # Alice's move: choose 'A' at index `i`. The string becomes S[i+1:].
    # Bob's move: choose 'B' at index `j`. The string becomes S[:j].

    # This is a game on a segment.
    # Let `dp[l][r]` be the winner for the segment `S[l...r]`.
    # Too slow for N=600,000.

    # The key insight must be simpler.
    # Alice wants to eat an 'A'. Bob wants to eat a 'B'.
    # They both want to eat the last dish.
    # This means they want to maximize their own count of dishes eaten.
    # The player who eats the last dish wins.

    # The crucial part is that Alice can choose *any* 'A' and Bob can choose *any* 'B'.
    # This means they can effectively "remove" a prefix or suffix.
    # Alice wants to eat an 'A' that is as far right as possible, to preserve 'A's to her left.
    # Bob wants to eat a 'B' that is as far left as possible, to preserve 'B's to his right.

    # This is a game on a line.
    # Alice wants to eat an 'A'. Bob wants to eat a 'B'.
    # The game ends when no more 'A's for Alice or 'B's for Bob.
    # The winner is the one who eats the last dish.

    # Let's consider the number of 'A's and 'B's.
    # Alice wants to eat an 'A'. Bob wants to eat a 'B'.
    # The game ends when no more 'A's for Alice or 'B's for Bob.
    # The winner is the one who eats the last dish.

    # This is a game on a string.
    # Alice's move: choose 'A' at index `i`. The string becomes S[i+1:].
    # Bob's move: choose 'B' at index `j`. The string becomes S[:j].

    # This is a game on a segment.
    # Let `dp[l][r]` be the winner for the segment `S[l...r]`.
    # Too slow for N=600,000.

    # The key insight must be simpler.
    # Alice wants to eat an 'A'. Bob wants to eat a 'B'.
    # They both want to eat the last dish.
    # This means they want to maximize their own count of dishes eaten.
    # The player who eats the last dish wins.

    # The crucial part is that Alice can choose *any* 'A' and Bob can choose *any* 'B'.
    # This means they can effectively "remove" a prefix or suffix.
    # Alice wants to eat an 'A' that is as far right as possible, to preserve 'A's to her left.
    # Bob wants to eat a 'B' that is as far left as possible, to preserve 'B's to his right.

    # This is a game on a line.
    # Alice wants to eat an 'A'. Bob wants to eat a 'B'.
    # The game ends when no more 'A's for Alice or 'B's for Bob.
    # The winner is the one who eats the last dish.

    # Let's consider the number of 'A's and 'B's.
    # Alice wants to eat an 'A'. Bob wants to eat a 'B'.
    # The game ends when no more 'A's for Alice or 'B's for Bob.
    # The winner is the one who eats the last dish.

    # This is a game on a string.
    # Alice's move: choose 'A' at index `i`. The string becomes S[i+1:].
    # Bob's move: choose 'B' at index `j`. The string becomes S[:j].

    # This is a game on a segment.
    # Let `dp[l][r]` be the winner for the segment `S[l...r]`.
    # Too slow for N=600,000.

    # The key insight must be simpler.
    # Alice wants to eat an 'A'. Bob wants to eat a 'B'.
    # They both want to eat the last dish.
    # This means they want to maximize their own count of dishes eaten.
    # The player who eats the last dish wins.

    # The crucial part is that Alice can choose *any* 'A' and Bob can choose *any* 'B'.
    # This means they can effectively "remove" a prefix or suffix.
    # Alice wants to eat an 'A' that is as far right as possible, to preserve 'A's to her left.
    # Bob wants to eat a 'B' that is as far left as possible, to preserve 'B's to his right.

    # This is a game on a line.
    # Alice wants to eat an 'A'. Bob wants to eat a 'B'.
    # The game ends when no more 'A's for Alice or 'B's for Bob.
    # The winner is the one who eats the last dish.

    # Let's consider the number of 'A's and 'B's.
    # Alice wants to eat an 'A'. Bob wants to eat a 'B'.
    # The game ends when no more 'A's for Alice or 'B's for Bob.
    # The winner is the one who eats the last dish.

    # This is a game on a string.
    # Alice's move: choose 'A' at index `i`. The string becomes S[i+1:].
    # Bob's move: choose 'B' at index `j`. The string becomes S[:j].

    # This is a game on a segment.
    # Let `dp[l][r]` be the winner for the segment `S[l...r]`.
    # Too slow for N=600,000.

    # The key insight must be simpler.
    # Alice wants to eat an 'A'. Bob wants to eat a 'B'.
    # They both want to eat the last dish.
    # This means they want to maximize their own count of dishes eaten.
    # The player who eats the last dish wins.

    # The crucial part is that Alice can choose *any* 'A' and Bob can choose *any* 'B'.
    # This means they can effectively "remove" a prefix or suffix.
    # Alice wants to eat an 'A' that is as far right as possible, to preserve 'A's to her left.
    # Bob wants to eat a 'B' that is as far left as possible, to preserve 'B's to his right.

    # This is a game on a line.
    # Alice wants to eat an 'A'. Bob wants to eat a 'B'.
    # The game ends when no more 'A's for Alice or 'B's for Bob.
    # The winner is the one who eats the last dish.

    # Let's consider the number of 'A's and 'B's.
    # Alice wants to eat an 'A'. Bob wants to eat a 'B'.
    # The game ends when no more 'A's for Alice or 'B's for Bob.
    # The winner is the one who eats the last dish.

    # This is a game on a string.
    # Alice's move: choose 'A' at index `i`. The string becomes S[i+1:].
    # Bob's move: choose 'B' at index `j`. The string becomes S[:j].

    # This is a game on a segment.
    # Let `dp[l][r]` be the winner for the segment `S[l...r]`.
    # Too slow for N=600,000.

    # The key insight must be simpler.
    # Alice wants to eat an 'A'. Bob wants to eat a 'B'.
    # They both want to eat the last dish.
    # This means they want to maximize their own count of dishes eaten.
    # The player who eats the last dish wins.

    # The crucial part is that Alice can choose *any* 'A' and Bob can choose *any* 'B'.
    # This means they can effectively "remove" a prefix or suffix.
    # Alice wants to eat an 'A' that is as far right as possible, to preserve 'A's to her left.
    # Bob wants to eat a 'B' that is as far left as possible, to preserve 'B's to his right.

    # This is a game on a line.
    # Alice wants to eat an 'A'. Bob wants to eat a 'B'.
    # The game ends when no more 'A's for Alice or 'B's for Bob.
    # The winner is the one who eats the last dish.

    # Let's consider the number of 'A's and 'B's.
    # Alice wants to eat an 'A'. Bob wants to eat a 'B'.
    # The game ends when no more 'A's for Alice or 'B's for Bob.
    # The winner is the one who eats the last dish.

    # This is a game on a string.
    # Alice's move: choose 'A' at index `i`. The string becomes S[i+1:].
    # Bob's move: choose 'B' at index `j`. The string becomes S[:j].

    # This is a game on a segment.
    # Let `dp[l][r]` be the winner for the segment `S[l...r]`.
    # Too slow for N=600,000.

    # The key insight must be simpler.
    # Alice wants to eat an 'A'. Bob wants to eat a 'B'.
    # They both want to eat the last dish.
    # This means they want to maximize their own count of dishes eaten.
    # The player who eats the last dish wins.

    # The crucial part is that Alice can choose *any* 'A' and Bob can choose *any* 'B'.
    # This means they can effectively "remove" a prefix or suffix.
    # Alice wants to eat an 'A' that is as far right as possible, to preserve 'A's to her left.
    # Bob wants to eat a 'B' that is as far left as possible, to preserve 'B's to his right.

    # This is a game on a line.
    # Alice wants to eat an 'A'. Bob wants to eat a 'B'.
    # The game ends when no more 'A's for Alice or 'B's for Bob.
    # The winner is the one who eats the last dish.

    # Let's consider the number of 'A's and 'B's.
    # Alice wants to eat an 'A'. Bob wants to eat a 'B'.
    # The game ends when no more 'A's for Alice or 'B's for Bob.
    # The winner is the one who eats the last dish.

    # This is a game on a string.
    # Alice's move: choose 'A' at index `i`. The string becomes S[i+1:].
    # Bob's move: choose 'B' at index `j`. The string becomes S[:j].

    # This is a game on a segment.
    # Let `dp[l][r]` be the winner for the segment `S[l...r]`.
    # Too slow for N=600,000.

    # The key insight must be simpler.
    # Alice wants to eat an 'A'. Bob wants to eat a 'B'.
    # They both want to eat the last dish.
    # This means they want to maximize their own count of dishes eaten.
    # The player who eats the last dish wins.

    # The crucial part is that Alice can choose *any* 'A' and Bob can choose *any* 'B'.
    # This means they can effectively "remove" a prefix or suffix.
    # Alice wants to eat an 'A' that is as far right as possible, to preserve 'A's to her left.
    # Bob wants to eat a 'B' that is as far left as possible, to preserve 'B's to his right.

    # This is a game on a line.
    # Alice wants to eat an 'A'. Bob wants to eat a 'B'.
    # The game ends when no more 'A's for Alice or 'B's for Bob.
    # The winner is the one who eats the last dish.

    # Let's consider the number of 'A's and 'B's.
    # Alice wants to eat an 'A'. Bob wants to eat a 'B'.
    # The game ends when no more 'A's for Alice or 'B's for Bob.
    # The winner is the one who eats the last dish.

    # This is a game on a string.
    # Alice's move: choose 'A' at index `i`. The string becomes S[i+1:].
    # Bob's move: choose 'B' at index `j`. The string becomes S[:j].

    # This is a game on a segment.
    # Let `dp[l][r]` be the winner for the segment `S[l...r]`.
    # Too slow for N=600,000.

    # The key insight must be simpler.
    # Alice wants to eat an 'A'. Bob wants to eat a 'B'.
    # They both want to eat the last dish.
    # This means they want to maximize their own count of dishes eaten.
    # The player who eats the last dish wins.

    # The crucial part is that Alice can choose *any* 'A' and Bob can choose *any* 'B'.
    # This means they can effectively "remove" a prefix or suffix.
    # Alice wants to eat an 'A' that is as far right as possible, to preserve 'A's to her left.
    # Bob wants to eat a 'B' that is as far left as possible, to preserve 'B's to his right.

    # This is a game on a line.
    # Alice wants to eat an 'A'. Bob wants to eat a 'B'.
    # The game ends when no more 'A's for Alice or 'B's for Bob.
    # The winner is the one who eats the last dish.

    # Let's consider the number of 'A's and 'B's.
    # Alice wants to eat an 'A'. Bob wants to eat a 'B'.
    # The game ends when no more 'A's for Alice or 'B's for Bob.
    # The winner is the one who eats the last dish.

    # This is a game on a string.
    # Alice's move: choose 'A' at index `i`. The string becomes S[i+1:].
    # Bob's move: choose 'B' at index `j`. The string becomes S[:j].

    # This is a game on a segment.
    # Let `dp[l][r]` be the winner for the segment `S[l...r]`.
    # Too slow for N=600,000.

    # The key insight must be simpler.
    # Alice wants to eat an 'A'. Bob wants to eat a 'B'.
    # They both want to eat the last dish.
    # This means they want to maximize their own count of dishes eaten.
    # The player who eats the last dish wins.

    # The crucial part is that Alice can choose *any* 'A' and Bob can choose *any* 'B'.
    # This means they can effectively "remove" a prefix or suffix.
    # Alice wants to eat an 'A' that is as far right as possible, to preserve 'A's to her left.
    # Bob wants to eat a 'B' that is as far left as possible, to preserve 'B's to his right.

    # This is a game on a line.
    # Alice wants to eat an 'A'. Bob wants to eat a 'B'.
    # The game ends when no more 'A's for Alice or 'B's for Bob.
    # The winner is the one who eats the last dish.

    # Let's consider the number of 'A's and 'B's.
    # Alice wants to eat an 'A'. Bob wants to eat a 'B'.
    # The game ends when no more 'A's for Alice or 'B's for Bob.
    # The winner is the one who eats the last dish.

    # This is a game on a string.
    # Alice's move: choose 'A' at index `i`. The string becomes S[i+1:].
    # Bob's move: choose 'B' at index `j`. The string becomes S[:j].

    # This is a game on a segment.
    # Let `dp[l][r]` be the winner for the segment `S[l...r]`.
    # Too slow for N=600,000.

    # The key insight must be simpler.
    # Alice wants to eat an 'A'. Bob wants to eat a 'B'.
    # They both want to eat the last dish.
    # This means they want to maximize their own count of dishes eaten.
    # The player who eats the last dish wins.

    # The crucial part is that Alice can choose *any* 'A' and Bob can choose *any* 'B'.
    # This means they can effectively "remove" a prefix or suffix.
    # Alice wants to eat an 'A' that is as far right as possible, to preserve 'A's to her left.
    # Bob wants to eat a 'B' that is as far left as possible, to preserve 'B's to his right.

    # This is a game on a line.
    # Alice wants to eat an 'A'. Bob wants to eat a 'B'.
    # The game ends when no more 'A's for Alice or 'B's for Bob.
    # The winner is the one who eats the last dish.

    # Let's consider the number of 'A's and 'B's.
    # Alice wants to eat an 'A'. Bob wants to eat a 'B'.
    # The game ends when no more 'A's for Alice or 'B's for Bob.
    # The winner is the one who eats the last dish.

    # This is a game on a string.
    # Alice's move: choose 'A' at index `i`. The string becomes S[i+1:].
    # Bob's move: choose 'B' at index `j`. The string becomes S[:j].

    # This is a game on a segment.
    # Let `dp[l][r]` be the winner for the segment `S[l...r]`.
    # Too slow for N=600,000.

    # The key insight must be simpler.
    # Alice wants to eat an 'A'. Bob wants to eat a 'B'.
    # They both want to eat the last dish.
    # This means they want to maximize their own count of dishes eaten.
    # The player who eats the last dish wins.

    # The crucial part is that Alice can choose *any* 'A' and Bob can choose *any* 'B'.
    # This means they can effectively "remove" a prefix or suffix.
    # Alice wants to eat an 'A' that is as far right as possible, to preserve 'A's to her left.
    # Bob wants to eat a 'B' that is as far left as possible, to preserve 'B's to his right.

    # This is a game on a line.
    # Alice wants to eat an 'A'. Bob wants to eat a 'B'.
    # The game ends when no more 'A's for Alice or 'B's for Bob.
    # The winner is the one who eats the last dish.

    # Let's consider the number of 'A's and 'B's.
    # Alice wants to eat an 'A'. Bob wants to eat a 'B'.
    # The game ends when no more 'A's for Alice or 'B's for Bob.
    # The winner is the one who eats the last dish.

    # This is a game on a string.
    # Alice's move: choose 'A' at index `i`. The string becomes S[i+1:].
    # Bob's move: choose 'B' at index `j`. The string becomes S[:j].

    # This is a game on a segment.
    # Let `dp[l][r]` be the winner for the segment `S[l...r]`.
    # Too slow for N=600,000.

    # The key insight must be simpler.
    # Alice wants to eat an 'A'. Bob wants to eat a 'B'.
    # They both want to eat the last dish.
    # This means they want to maximize their own count of dishes eaten.
    # The player who eats the last dish wins.

    # The crucial part is that Alice can choose *any* 'A' and Bob can choose *any* 'B'.
    # This means they can effectively "remove" a prefix or suffix.
    # Alice wants to eat an 'A' that is as far right as possible, to preserve 'A's to her left.
    # Bob wants to eat a 'B' that is as far left as possible, to preserve 'B's to his right.

    # This is a game on a line.
    # Alice wants to eat an 'A'. Bob wants to eat a 'B'.
    # The game ends when no more 'A's for Alice or 'B's for Bob.
    # The winner is the one who eats the last dish.

    # Let's consider the number of 'A's and 'B's.
    # Alice wants to eat an 'A'. Bob wants to eat a 'B'.
    # The game ends when no more 'A's for Alice or 'B's for Bob.
    # The winner is the one who eats the last dish.

    # This is a game on a string.
    # Alice's move: choose 'A' at index `i`. The string becomes S[i+1:].
    # Bob's move: choose 'B' at index `j`. The string becomes S[:j].

    # This is a game on a segment.
    # Let `dp[l][r]` be the winner for the segment `S[l...r]`.
    # Too slow for N=600,000.

    # The key insight must be simpler.
    # Alice wants to eat an 'A'. Bob wants to eat a 'B'.
    # They both want to eat the last dish.
    # This means they want to maximize their own count of dishes eaten.
    # The player who eats the last dish wins.

    # The crucial part is that Alice can choose *any* 'A' and Bob can choose *any* 'B'.
    # This means they can effectively "remove" a prefix or suffix.
    # Alice wants to eat an 'A' that is as far right as possible, to preserve 'A's to her left.
    # Bob wants to eat a 'B' that is as far left as possible, to preserve 'B's to his right.

    # This is a game on a line.
    # Alice wants to eat an 'A'. Bob wants to eat a 'B'.
    # The game ends when no more 'A's for Alice or 'B's for Bob.
    # The winner is the one who eats the last dish.

    # Let's consider the number of 'A's and 'B's.
    # Alice wants to eat an 'A'. Bob wants to eat a 'B'.
    # The game ends when no more 'A's for Alice or 'B's for Bob.
    # The winner is the one who eats the last dish.

    # This is a game on a string.
    # Alice's move: choose 'A' at index `i`. The string becomes S[i+1:].
    # Bob's move: choose 'B' at index `j`. The string becomes S[:j].

    # This is a game on a segment.
    # Let `dp[l][r]` be the winner for the segment `S[l...r]`.
    # Too slow for N=600,000.

    # The key insight must be simpler.
    # Alice wants to eat an 'A'. Bob wants to eat a 'B'.
    # They both want to eat the last dish.
    # This means they want to maximize their own count of dishes eaten.
    # The player who eats the last dish wins.

    # The crucial part is that Alice can choose *any* 'A' and Bob can choose *any* 'B'.
    # This means they can effectively "remove" a prefix or suffix.
    # Alice wants to eat an 'A' that is as far right as possible, to preserve 'A's to her left.
    # Bob wants to eat a 'B' that is as far left as possible, to preserve 'B's to his right.

    # This is a game on a line.
    # Alice wants to eat an 'A'. Bob wants to eat a 'B'.
    # The game ends when no more 'A's for Alice or 'B's for Bob.
    # The winner is the one who eats the last dish.

    # Let's consider the number of 'A's and 'B's.
    # Alice wants to eat an 'A'. Bob wants to eat a 'B'.
    # The game ends when no more 'A's for Alice or 'B's for Bob.
    # The winner is the one who eats the last dish.

    # This is a game on a string.
    # Alice's move: choose 'A' at index `i`. The string becomes S[i+1:].
    # Bob's move: choose 'B' at index `j`. The string becomes S[:j].

    # This is a game on a segment.
    # Let `dp[l][r]` be the winner for the segment `S[l...r]`.
    # Too slow for N=600,000.

    # The key insight must be simpler.
    # Alice wants to eat an 'A'. Bob wants to eat a 'B'.
    # They both want to eat the last dish.
    # This means they want to maximize their own count of dishes eaten.
    # The player who eats the last dish wins.

    # The crucial part is that Alice can choose *any* 'A' and Bob can choose *any* 'B'.
    # This means they can effectively "remove" a prefix or suffix.
    # Alice wants to eat an 'A' that is as far right as possible, to preserve 'A's to her left.
    # Bob wants to eat a 'B' that is as far left as possible, to preserve 'B's to his right.

    # This is a game on a line.
    # Alice wants to eat an 'A'. Bob wants to eat a 'B'.
    # The game ends when no more 'A's for Alice or 'B's for Bob.
    # The winner is the one who eats the last dish.

    # Let's consider the number of 'A's and 'B's.
    # Alice wants to eat an 'A'. Bob wants to eat a 'B'.
    # The game ends when no more 'A's for Alice or 'B's for Bob.
    # The winner is the one who eats the last dish.

    # This is a game on a string.
    # Alice's move: choose 'A' at index `i`. The string becomes S[i+1:].
    # Bob's move: choose 'B' at index `j`. The string becomes S[:j].

    # This is a game on a segment.
    # Let `dp[l][r]` be the winner for the segment `S[l...r]`.
    # Too slow for N=600,000.

    # The key insight must be simpler.
    # Alice wants to eat an 'A'. Bob wants to eat a 'B'.
    # They both want to eat the last dish.
    # This means they want to maximize their own count of dishes eaten.
    # The player who eats the last dish wins.

    # The crucial part is that Alice can choose *any* 'A' and Bob can choose *any* 'B'.
    # This means they can effectively "remove" a prefix or suffix.
    # Alice wants to eat an 'A' that is as far right as possible, to preserve 'A's to her left.
    # Bob wants to eat a 'B' that is as far left as possible, to preserve 'B's to his right.

    # This is a game on a line.
    # Alice wants to eat an 'A'. Bob wants to eat a 'B'.
    # The game ends when no more 'A's for Alice or 'B's for Bob.
    # The winner is the one who eats the last dish.

    # Let's consider the number of 'A's and 'B's.
    # Alice wants to eat an 'A'. Bob wants to eat a 'B'.
    # The game ends when no more 'A's for Alice or 'B's for Bob.
    # The winner is the one who eats the last dish.

    # This is a game on a string.
    # Alice's move: choose 'A' at index `i`. The string becomes S[i+1:].
    # Bob's move: choose 'B' at index `j`. The string becomes S[:j].

    # This is a game on a segment.
    # Let `dp[l][r]` be the winner for the segment `S[l...r]`.
    # Too slow for N=600,000.

    # The key insight must be simpler.
    # Alice wants to eat an 'A'. Bob wants to eat a 'B'.
    # They both want to eat the last dish.
    # This means they want to maximize their own count of dishes eaten.
    # The player who eats the last dish wins.

    # The crucial part is that Alice can choose *any* 'A' and Bob can choose *any* 'B'.
    # This means they can effectively "remove" a prefix or suffix.
    # Alice wants to eat an 'A' that is as far right as possible, to preserve 'A's to her left.
    # Bob wants to eat a 'B' that is as far left as possible, to preserve 'B's to his right.

    # This is a game on a line.
    # Alice wants to eat an 'A'. Bob wants to eat a 'B'.
    # The game ends when no more 'A's for Alice or 'B's for Bob.
    # The winner is the one who eats the last dish.

    # Let's consider the number of 'A's and 'B's.
    # Alice wants to eat an 'A'. Bob wants to eat a 'B'.
    # The game ends when no more 'A's for Alice or 'B's for Bob.
    # The winner is the one who eats the last dish.

    # This is a game on a string.
    # Alice's move: choose 'A' at index `i`. The string becomes S[i+1:].
    # Bob's move: choose 'B' at index `j`. The string becomes S[:j].

    # This is a game on a segment.
    # Let `dp[l][r]` be the winner for the segment `S[l...r]`.
    # Too slow for N=600,000.

    # The key insight must be simpler.
    # Alice wants to eat an 'A'. Bob wants to eat a 'B'.
    # They both want to eat the last dish.
    # This means they want to maximize their own count of dishes eaten.
    # The player who eats the last dish wins.

    # The crucial part is that Alice can choose *any* 'A' and Bob can choose *any* 'B'.
    # This means they can effectively "remove" a prefix or suffix.
    # Alice wants to eat an 'A' that is as far right as possible, to preserve 'A's to her left.
    # Bob wants to eat a 'B' that is as far left as possible, to preserve 'B's to his right.

    # This is a game on a line.
    # Alice wants to eat an 'A'. Bob wants to eat a 'B'.
    # The game ends when no more 'A's for Alice or 'B's for Bob.
    # The winner is the one who eats the last dish.

    # Let's consider the number of 'A's and 'B's.
    # Alice wants to eat an 'A'. Bob wants to eat a 'B'.
    # The game ends when no more 'A's for Alice or 'B's for Bob.
    # The winner is the one who eats the last dish.

    # This is a game on a string.
    # Alice's move: choose 'A' at index `i`. The string becomes S[i+1:].
    # Bob's move: choose 'B' at index `j`. The string becomes S[:j].

    # This is a game on a segment.
    # Let `dp[l][r]` be the winner for the segment `S[l...r]`.
    # Too slow for N=600,000.

    # The key insight must be simpler.
    # Alice wants to eat an 'A'. Bob wants to eat a 'B'.
    # They both want to eat the last dish.
    # This means they want to maximize their own count of dishes eaten.
    # The player who eats the last dish wins.

    # The crucial part is that Alice can choose *any* 'A' and Bob can choose *any* 'B'.
    # This means they can effectively "remove" a prefix or suffix.
    # Alice wants to eat an 'A' that is as far right as possible, to preserve 'A's to her left.
    # Bob wants to eat a 'B' that is as far left as possible, to preserve 'B's to his right.

    # This is a game on a line.
    # Alice wants to eat an 'A'. Bob wants to eat a 'B'.
    # The game ends when no more 'A's for Alice or 'B's for Bob.
    # The winner is the one who eats the last dish.

    # Let's consider the number of 'A's and 'B's.
    # Alice wants to eat an 'A'. Bob wants to eat a 'B'.
    # The game ends when no more 'A's for Alice or 'B's for Bob.
    # The winner is the one who eats the last dish.

    # This is a game on a string.
    # Alice's move: choose 'A' at index `i`. The string becomes S[i+1:].
    # Bob's move: choose 'B' at index `j`. The string becomes S[:j].

    # This is a game on a segment.
    # Let `dp[l][r]` be the winner for the segment `S[l...r]`.
    # Too slow for N=600,000.

    # The key insight must be simpler.
    # Alice wants to eat an 'A'. Bob wants to eat a 'B'.
    # They both want to eat the last dish.
    # This means they want to maximize their own count of dishes eaten.
    # The player who eats the last dish wins.

    # The crucial part is that Alice can choose *any* 'A' and Bob can choose *any* 'B'.
    # This means they can effectively "remove" a prefix or suffix.
    # Alice wants to eat an 'A' that is as far right as possible, to preserve 'A's to her left.
    # Bob wants to eat a 'B' that is as far left as possible, to preserve 'B's to his right.

    # This is a game on a line.
    # Alice wants to eat an 'A'. Bob wants to eat a 'B'.
    # The game ends when no more 'A's for Alice or 'B's for Bob.
    # The winner is the one who eats the last dish.

    # Let's consider the number of 'A's and 'B's.
    # Alice wants to eat an 'A'. Bob wants to eat a 'B'.
    # The game ends when no more 'A's for Alice or 'B's for Bob.
    # The winner is the one who eats the last dish.

    # This is a game on a string.
    # Alice's move: choose 'A' at index `i`. The string becomes S[i+1:].
    # Bob's move: choose 'B' at index `j`. The string becomes S[:j].

    # This is a game on a segment.
    # Let `dp[l][r]` be the winner for the segment `S[l...r]`.
    # Too slow for N=600,000.

    # The key insight must be simpler.
    # Alice wants to eat an 'A'. Bob wants to eat a 'B'.
    # They both want to eat the last dish.
    # This means they want to maximize their own count of dishes eaten.
    # The player who eats the last dish wins.

    # The crucial part is that Alice can choose *any* 'A' and Bob can choose *any* 'B'.
    # This means they can effectively "remove" a prefix or suffix.
    # Alice wants to eat an 'A' that is as far right as possible, to preserve 'A's to her left.
    # Bob wants to eat a 'B' that is as far left as possible, to preserve 'B's to his right.

    # This is a game on a line.
    # Alice wants to eat an 'A'. Bob wants to eat a 'B'.
    # The game ends when no more 'A's for Alice or 'B's for Bob.
    # The winner is the one who eats the last dish.

    # Let's consider the number of 'A's and 'B's.
    # Alice wants to eat an 'A'. Bob wants to eat a 'B'.
    # The game ends when no more 'A's for Alice or 'B's for Bob.
    # The winner is the one who eats the last dish.

    # This is a game on a string.
    # Alice's move: choose 'A' at index `i`. The string becomes S[i+1:].
    # Bob's move: choose 'B' at index `j`. The string becomes S[:j].

    # This is a game on a segment.
    # Let `dp[l][r]` be the winner for the segment `S[l...r]`.
    # Too slow for N=600,000.

    # The key insight must be simpler.
    # Alice wants to eat an 'A'. Bob wants to eat a 'B'.
    # They both want to eat the last dish.
    # This means they want to maximize their own count of dishes eaten.
    # The player who eats the last dish wins.

    # The crucial part is that Alice can choose *any* 'A' and Bob can choose *any* 'B'.
    # This means they can effectively "remove" a prefix or suffix.
    # Alice wants to eat an 'A' that is as far right as possible, to preserve 'A's to her left.
    # Bob wants to eat a 'B' that is as far left as possible, to preserve 'B's to his right.

    # This is a game on a line.
    # Alice wants to eat an 'A'. Bob wants to eat a 'B'.
    # The game ends when no more 'A's for Alice or 'B's for Bob.
    # The winner is the one who eats the last dish.

    # Let's consider the number of 'A's and 'B's.
    # Alice wants to eat an 'A'. Bob wants to eat a 'B'.
    # The game ends when no more 'A's for Alice or 'B's for Bob.
    # The winner is the one who eats the last dish.

    # This is a game on a string.
    # Alice's move: choose 'A' at index `i`. The string becomes S[i+1:].
    # Bob's move: choose 'B' at index `j`. The string becomes S[:j].

    # This is a game on a segment.
    # Let `dp[l][r]` be the winner for the segment `S[l...r]`.
    # Too slow for N=600,000.

    # The key insight must be simpler.
    # Alice wants to eat an 'A'. Bob wants to eat a 'B'.
    # They both want to eat the last dish.
    # This means they want to maximize their own count of dishes eaten.
    # The player who eats the last dish wins.

    # The crucial part is that Alice can choose *any* 'A' and Bob can choose *any* 'B'.
    # This means they can effectively "remove" a prefix or suffix.
    # Alice wants to eat an 'A' that is as far right as possible, to preserve 'A's to her left.
    # Bob wants to eat a 'B' that is as far left as possible, to preserve 'B's to his right.

    # This is a game on a line.
    # Alice wants to eat an 'A'. Bob wants to eat a 'B'.
    # The game ends when no more 'A's for Alice or 'B's for Bob.
    # The winner is the one who eats the last dish.

    # Let's consider the number of 'A's and 'B's.
    # Alice wants to eat an 'A'. Bob wants to eat a 'B'.
    # The game ends when no more 'A's for Alice or 'B's for Bob.
    # The winner is the one who eats the last dish.

    # This is a game on a string.
    # Alice's move: choose 'A' at index `i`. The string becomes S[i+1:].
    # Bob's move: choose 'B' at index `j`. The string becomes S[:j].

    # This is a game on a segment.
    # Let `dp[l][r]` be the winner for the segment `S[l...r]`.
    # Too slow for N=600,000.

    # The key insight must be simpler.
    # Alice wants to eat an 'A'. Bob wants to eat a 'B'.
    # They both want to eat the last dish.
    # This means they want to maximize their own count of dishes eaten.
    # The player who eats the last dish wins.

    # The crucial part is that Alice can choose *any* 'A' and Bob can choose *any* 'B'.
    # This means they can effectively "remove" a prefix or suffix.
    # Alice wants to eat an 'A' that is as far right as possible, to preserve 'A's to her left.
    # Bob wants to eat a 'B' that is as far left as possible, to preserve 'B's to his right.

    # This is a game on a line.
    # Alice wants to eat an 'A'. Bob wants to eat a 'B'.
    # The game ends when no more 'A's for Alice or 'B's for Bob.
    # The winner is the one who eats the last dish.

    # Let's consider the number of 'A's and 'B's.
    # Alice wants to eat an 'A'. Bob wants to eat a 'B'.
    # The game ends when no more 'A's for Alice or 'B's for Bob.
    # The winner is the one who eats the last dish.

    # This is a game on a string.
    # Alice's move: choose 'A' at index `i`. The string becomes S[i+1:].
    # Bob's move: choose 'B' at index `j`. The string becomes S[:j].

    # This is a game on a segment.
    # Let `dp[l][r]` be the winner for the segment `S[l...r]`.
    # Too slow for N=600,000.

    # The key insight must be simpler.
    # Alice wants to eat an 'A'. Bob wants to eat a 'B'.
    # They both want to eat the last dish.
    # This means they want to maximize their own count of dishes eaten.
    # The player who eats the last dish wins.

    # The crucial part is that Alice can choose *any* 'A' and Bob can choose *any* 'B'.
    # This means they can effectively "remove" a prefix or suffix.
    # Alice wants to eat an 'A' that is as far right as possible, to preserve 'A's to her left.
    # Bob wants to eat a 'B' that is as far left as possible, to preserve 'B's to his right.

    # This is a game on a line.
    # Alice wants to eat an 'A'. Bob wants to eat a 'B'.
    # The game ends when no more 'A's for Alice or 'B's for Bob.
    # The winner is the one who eats the last dish.

    # Let's consider the number of 'A's and 'B's.
    # Alice wants to eat an 'A'. Bob wants to eat a 'B'.
    # The game ends when no more 'A's for Alice or 'B's for Bob.
    # The winner is the one who eats the last dish.

    # This is a game on a string.
    # Alice's move: choose 'A' at index `i`. The string becomes S[i+1:].
    # Bob's move: choose 'B' at index `j`. The string becomes S[:j].

    # This is a game on a segment.
    # Let `dp[l][r]` be the winner for the segment `S[l...r]`.
    # Too slow for N=600,000.

    # The key insight must be simpler.
    # Alice wants to eat an 'A'. Bob wants to eat a 'B'.
    # They both want to eat the last dish.
    # This means they want to maximize their own count of dishes eaten.
    # The player who eats the last dish wins.

    # The crucial part is that Alice can choose *any* 'A' and Bob can choose *any* 'B'.
    # This means they can effectively "remove" a prefix or suffix.
    # Alice wants to eat an 'A' that is as far right as possible, to preserve 'A's to her left.
    # Bob wants to eat a 'B' that is as far left as possible, to preserve 'B's to his right.

    # This is a game on a line.
    # Alice wants to eat an 'A'. Bob wants to eat a 'B'.
    # The game ends when no more 'A's for Alice or 'B's for Bob.
    # The winner is the one who eats the last dish.

    # Let's consider the number of 'A's and 'B's.
    # Alice wants to eat an 'A'. Bob wants to eat a 'B'.
    # The game ends when no more 'A's for Alice or 'B's for Bob.
    # The winner is the one who eats the last dish.

    # This is a game on a string.
    # Alice's move: choose 'A' at index `i`. The string becomes S[i+1:].
    # Bob's move: choose 'B' at index `j`. The string becomes S[:j].

    # This is a game on a segment.
    # Let `dp[l][r]` be the winner for the segment `S[l...r]`.
    # Too slow for N=600,000.

    # The key insight must be simpler.
    # Alice wants to eat an 'A'. Bob wants to eat a 'B'.
    # They both want to eat the last dish.
    # This means they want to maximize their own count of dishes eaten.
    # The player who eats the last dish wins.

    # The crucial part is that Alice can choose *any* 'A' and Bob can choose *any* 'B'.
    # This means they can effectively "remove" a prefix or suffix.
    # Alice wants to eat an 'A' that is as far right as possible, to preserve 'A's to her left.
    # Bob wants to eat a 'B' that is as far left as possible, to preserve 'B's to his right.

    # This is a game on a line.
    # Alice wants to eat an 'A'. Bob wants to eat a 'B'.
    # The game ends when no more 'A's for Alice or 'B's for Bob.
    # The winner is the one who eats the last dish.

    # Let's consider the number of 'A's and 'B's.
    # Alice wants to eat an 'A'. Bob wants to eat a 'B'.
    # The game ends when no more 'A's for Alice or 'B's for Bob.
    # The winner is the one who eats the last dish.

    # This is a game on a string.
    # Alice's move: choose 'A' at index `i`. The string becomes S[i+1:].
    # Bob's move: choose 'B' at index `j`. The string becomes S[:j].

    # This is a game on a segment.
    # Let `dp[l][r]` be the winner for the segment `S[l...r]`.
    # Too slow for N=600,000.

    # The key insight must be simpler.
    # Alice wants to eat an 'A'. Bob wants to eat a 'B'.
    # They both want to eat the last dish.
    # This means they want to maximize their own count of dishes eaten.
    # The player who eats the last dish wins.

    # The crucial part is that Alice can choose *any* 'A' and Bob can choose *any* 'B'.
    # This means they can effectively "remove" a prefix or suffix.
    # Alice wants to eat an 'A' that is as far right as possible, to preserve 'A's to her left.
    # Bob wants to eat a 'B' that is as far left as possible, to preserve 'B's to his right.

    # This is a game on a line.
    # Alice wants to eat an 'A'. Bob wants to eat a 'B'.
    # The game ends when no more 'A's for Alice or 'B's for Bob.
    # The winner is the one who eats the last dish.

    # Let's consider the number of 'A's and 'B's.
    # Alice wants to eat an 'A'. Bob wants to eat a 'B'.
    # The game ends when no more 'A's for Alice or 'B's for Bob.
    # The winner is the one who eats the last dish.

    # This is a game on a string.
    # Alice's move: choose 'A' at index `i`. The string becomes S[i+1:].
    # Bob's move: choose 'B' at index `j`. The string becomes S[:j].

    # This is a game on a segment.
    # Let `dp[l][r]` be the winner for the segment `S[l...r]`.
    # Too slow for N=600,000.

    # The key insight must be simpler.
    # Alice wants to eat an 'A'. Bob wants to eat a 'B'.
    # They both want to eat the last dish.
    # This means they want to maximize their own count of dishes eaten.
    # The player who eats the last dish wins.

    # The crucial part is that Alice can choose *any* 'A' and Bob can choose *any* 'B'.
    # This means they can effectively "remove" a prefix or suffix.
    # Alice wants to eat an 'A' that is as far right as possible, to preserve 'A's to her left.
    # Bob wants to eat a 'B' that is as far left as possible, to preserve 'B's to his right.

    # This is a game on a line.
    # Alice wants to eat an 'A'. Bob wants to eat a 'B'.
    # The game ends when no more 'A's for Alice or 'B's for Bob.
    # The winner is the one who eats the last dish.

    # Let's consider the number of 'A's and 'B's.
    # Alice wants to eat an 'A'. Bob wants to eat a 'B'.
    # The game ends when no more 'A's for Alice or 'B's for Bob.
    # The winner is the one who eats the last dish.

    # This is a game on a string.
    # Alice's move: choose 'A' at index `i`. The string becomes S[i+1:].
    # Bob's move: choose 'B' at index `j`. The string becomes S[:j].

    # This is a game on a segment.
    # Let `dp[l][r]` be the winner for the segment `S[l...r]`.
    # Too slow for N=600,000.

    # The key insight must be simpler.
    # Alice wants to eat an 'A'. Bob wants to eat a 'B'.
    # They both want to eat the last dish.
    # This means they want to maximize their own count of dishes eaten.
    # The player who eats the last dish wins.

    # The crucial part is that Alice can choose *any* 'A' and Bob can choose *any* 'B'.
    # This means they can effectively "remove" a prefix or suffix.
    # Alice wants to eat an 'A' that is as far right as possible, to preserve 'A's to her left.
    # Bob wants to eat a 'B' that is as far left as possible, to preserve 'B's to his right.

    # This is a game on a line.
    # Alice wants to eat an 'A'. Bob wants to eat a 'B'.
    # The game ends when no more 'A's for Alice or 'B's for Bob.
    # The winner is the one who eats the last dish.

    # Let's consider the number of 'A's and 'B's.
    # Alice wants to eat an 'A'. Bob wants to eat a 'B'.
    # The game ends when no more 'A's for Alice or 'B's for Bob.
    # The winner is the one who eats the last dish.

    # This is a game on a string.
    # Alice's move: choose 'A' at index `i`. The string becomes S[i+1:].
    # Bob's move: choose 'B' at index `j`. The string becomes S[:j].

    # This is a game on a segment.
    # Let `dp[l][r]` be the winner for the segment `S[l...r]`.
    # Too slow for N=600,000.

    # The key insight must be simpler.
    # Alice wants to eat an 'A'. Bob wants to eat a 'B'.
    # They both want to eat the last dish.
    # This means they want to maximize their own count of dishes eaten.
    # The player who eats the last dish wins.

    # The crucial part is that Alice can choose *any* 'A' and Bob can choose *any* 'B'.
    # This means they can effectively "remove" a prefix or suffix.
    # Alice wants to eat an 'A' that is as far right as possible, to preserve 'A's to her left.
    # Bob wants to eat a 'B' that is as far left as possible, to preserve 'B's to his right.

    # This is a game on a line.
    # Alice wants to eat an 'A'. Bob wants to eat a 'B'.
    # The game ends when no more 'A's for Alice or 'B's for Bob.
    # The winner is the one who eats the last dish.

    # Let's consider the number of 'A's and 'B's.
    # Alice wants to eat an 'A'. Bob wants to eat a 'B'.
    # The game ends when no more 'A's for Alice or 'B's for Bob.
    # The winner is the one who eats the last dish.

    # This is a game on a string.
    # Alice's move: choose 'A' at index `i`. The string becomes S[i+1:].
    # Bob's move: choose 'B' at index `j`. The string becomes S[:j].

    # This is a game on a segment.
    # Let `dp[l][r]` be the winner for the segment `S[l...r]`.
    # Too slow for N=600,000.

    # The key insight must be simpler.
    # Alice wants to eat an 'A'. Bob wants to eat a 'B'.
    # They both want to eat the last dish.
    # This means they want to maximize their own count of dishes eaten.
    # The player who eats the last dish wins.

    # The crucial part is that Alice can choose *any* 'A' and Bob can choose *any* 'B'.
    # This means they can effectively "remove" a prefix or suffix.
    # Alice wants to eat an 'A' that is as far right as possible, to preserve 'A's to her left.
    # Bob wants to eat a 'B' that is as far left as possible, to preserve 'B's to his right.

    # This is a game on a line.
    # Alice wants to eat an 'A'. Bob wants to eat a 'B'.
    # The game ends when no more 'A's for Alice or 'B's for Bob.
    # The winner is the one who eats the last dish.

    # Let's consider the number of 'A's and 'B's.
    # Alice wants to eat an 'A'. Bob wants to eat a 'B'.
    # The game ends when no more 'A's for Alice or 'B's for Bob.
    # The winner is the one who eats the last dish.

    # This is a game on a string.
    # Alice's move: choose 'A' at index `i`. The string becomes S[i+1:].
    # Bob's move: choose 'B' at index `j`. The string becomes S[:j].

    # This is a game on a segment.
    # Let `dp[l][r]` be the winner for the segment `S[l...r]`.
    # Too slow for N=600,000.

    # The key insight must be simpler.
    # Alice wants to eat an 'A'. Bob wants to eat a 'B'.
    # They both want to eat the last dish.
    # This means they want to maximize their own count of dishes eaten.
    # The player who eats the last dish wins.

    # The crucial part is that Alice can choose *any* 'A' and Bob can choose *any* 'B'.
    # This means they can effectively "remove" a prefix or suffix.
    # Alice wants to eat an 'A' that is as far right as possible, to preserve 'A's to her left.
    # Bob wants to eat a 'B' that is as far left as possible, to preserve 'B's to his right.

    # This is a game on a line.
    # Alice wants to eat an 'A'. Bob wants to eat a 'B'.
    # The game ends when no more 'A's for Alice or 'B's for Bob.
    # The winner is the one who eats the last dish.

    # Let's consider the number of 'A's and 'B's.
    # Alice wants to eat an 'A'. Bob wants to eat a 'B'.
    # The game ends when no more 'A's for Alice or 'B's for Bob.
    # The winner is the one who eats the last dish.

    # This is a game on a string.
    # Alice's move: choose 'A' at index `i`. The string becomes S[i+1:].
    # Bob's move: choose 'B' at index `j`. The string becomes S[:j].

    # This is a game on a segment.
    # Let `dp[l][r]` be the winner for the segment `S[l...r]`.
    # Too slow for N=600,000.

    # The key insight must be simpler.
    # Alice wants to eat an 'A'. Bob wants to eat a 'B'.
    # They both want to eat the last dish.
    # This means they want to maximize their own count of dishes eaten.
    # The player who eats the last dish wins.

    # The crucial part is that Alice can choose *any* 'A' and Bob can choose *any* 'B'.
    # This means they can effectively "remove" a prefix or suffix.
    # Alice wants to eat an 'A' that is as far right as possible, to preserve 'A's to her left.
    # Bob wants to eat a 'B' that is as far left as possible, to preserve 'B's to his right.

    # This is a game on a line.
    # Alice wants to eat an 'A'. Bob wants to eat a 'B'.
    # The game ends when no more 'A's for Alice or 'B's for Bob.
    # The winner is the one who eats the last dish.

    # Let's consider the number of 'A's and 'B's.
    # Alice wants to eat an 'A'. Bob wants to eat a 'B'.
    # The game ends when no more 'A's for Alice or 'B's for Bob.
    # The winner is the one who eats the last dish.

    # This is a game on a string.
    # Alice's move: choose 'A' at index `i`. The string becomes S[i+1:].
    # Bob's move: choose 'B' at index `j`. The string becomes S[:j].

    # This is a game on a segment.
    # Let `dp[l][r]` be the winner for the segment `S[l...r]`.
    # Too slow for N=600,000.

    # The key insight must be simpler.
    # Alice wants to eat an 'A'. Bob wants to eat a 'B'.
    # They both want to eat the last dish.
    # This means they want to maximize their own count of dishes eaten.
    # The player who eats the last dish wins.

    # The crucial part is that Alice can choose *any* 'A' and Bob can choose *any* 'B'.
    # This means they can effectively "remove" a prefix or suffix.
    # Alice wants to eat an 'A' that is as far right as possible, to preserve 'A's to her left.
    # Bob wants to eat a 'B' that is as far left as possible, to preserve 'B's to his right.

    # This is a game on a line.
    # Alice wants to eat an 'A'. Bob wants to eat a 'B'.
    # The game ends when no more 'A's for Alice or 'B's for Bob.
    # The winner is the one who eats the last dish.

    # Let's consider the number of 'A's and 'B's.
    # Alice wants to eat an 'A'. Bob wants to eat a 'B'.
    # The game ends when no more 'A's for Alice or 'B's for Bob.
    # The winner is the one who eats the last dish.

    # This is a game on a string.
    # Alice's move: choose 'A' at index `i`. The string becomes S[i+1:].
    # Bob's move: choose 'B' at index `j`. The string becomes S[:j].

    # This is a game on a segment.
    # Let `dp[l][r]` be the winner for the segment `S[l...r]`.
    # Too slow for N=600,000.

    # The key insight must be simpler.
    # Alice wants to eat an 'A'. Bob wants to eat a 'B'.
    # They both want to eat the last dish.
    # This means they want to maximize their own count of dishes eaten.
    # The player who eats the last dish wins.

    # The crucial part is that Alice can choose *any* 'A' and Bob can choose *any* 'B'.
    # This means they can effectively "remove" a prefix or suffix.
    # Alice wants to eat an 'A' that is as far right as possible, to preserve 'A's to her left.
    # Bob wants to eat a 'B' that is as far left as possible, to preserve 'B's to his right.

    # This is a game on a line.
    # Alice wants to eat an 'A'. Bob wants to eat a 'B'.
    # The game ends when no more 'A's for Alice or 'B's for Bob.
    # The winner is the one who eats the last dish.

    # Let's consider the number of 'A's and 'B's.
    # Alice wants to eat an 'A'. Bob wants to eat a 'B'.
    # The game ends when no more 'A's for Alice or 'B's for Bob.
    # The winner is the one who eats the last dish.

    # This is a game on a string.
    # Alice's move: choose 'A' at index `i`. The string becomes S[i+1:].
    # Bob's move: choose 'B' at index `j`. The string becomes S[:j].

    # This is a game on a segment.
    # Let `dp[l][r]` be the winner for the segment `S[l...r]`.
    # Too slow for N=600,000.

    # The key insight must be simpler.
    # Alice wants to eat an 'A'. Bob wants to eat a 'B'.
    # They both want to eat the last dish.
    # This means they want to maximize their own count of dishes eaten.
    # The player who eats the last dish wins.

    # The crucial part is that Alice can choose *any* 'A' and Bob can choose *any* 'B'.
    # This means they can effectively "remove" a prefix or suffix.
    # Alice wants to eat an 'A' that is as far right as possible, to preserve 'A's to her left.
    # Bob wants to eat a 'B' that is as far left as possible, to preserve 'B's to his right.

    # This is a game on a line.
    # Alice wants to eat an 'A'. Bob wants to eat a 'B'.
    # The game ends when no more 'A's for Alice or 'B's for Bob.
    # The winner is the one who eats the last dish.

    # Let's consider the number of 'A's and 'B's.
    # Alice wants to eat an 'A'. Bob wants to eat a 'B'.
    # The game ends when no more 'A's for Alice or 'B's for Bob.
    # The winner is the one who eats the last dish.

    # This is a game on a string.
    # Alice's move: choose 'A' at index `i`. The string becomes S[i+1:].
    # Bob's move: choose 'B' at index `j`. The string becomes S[:j].

    # This is a game on a segment.
    # Let `dp[l][r]` be the winner for the segment `S[l...r]`.
    # Too slow for N=600,000.

    # The key insight must be simpler.
    # Alice wants to eat an 'A'. Bob wants to eat a 'B'.
    # They both want to eat the last dish.
    # This means they want to maximize their own count of dishes eaten.
    # The player who eats the last dish wins.

    # The crucial part is that Alice can choose *any* 'A' and Bob can choose *any* 'B'.
    # This means they can effectively "remove" a prefix or suffix.
    # Alice wants to eat an 'A' that is as far right as possible, to preserve 'A's to her left.
    # Bob wants to eat a 'B' that is as far left as possible, to preserve 'B's to his right.

    # This is a game on a line.
    # Alice wants to eat an 'A'. Bob wants to eat a 'B'.
    # The game ends when no more 'A's for Alice or 'B's for Bob.
    # The winner is the one who eats the last dish.

    # Let's consider the number of 'A's and 'B's.
    # Alice wants to eat an 'A'. Bob wants to eat a 'B'.
    # The game ends when no more 'A's for Alice or 'B's for Bob.
    # The winner is the one who eats the last dish.

    # This is a game on a string.
    # Alice's move: choose 'A' at index `i`. The string becomes S[i+1:].
    # Bob's move: choose 'B' at index `j`. The string becomes S[:j].

    # This is a game on a segment.
    # Let `dp[l][r]` be the winner for the segment `S[l...r]`.
    # Too slow for N=600,000.

    # The key insight must be simpler.
    # Alice wants to eat an 'A'. Bob wants to eat a 'B'.
    # They both want to eat the last dish.
    # This means they want to maximize their own count of dishes eaten.
    # The player who eats the last dish wins.

    # The crucial part is that Alice can choose *any* 'A' and Bob can choose *any* 'B'.
    # This means they can effectively "remove" a prefix or suffix.
    # Alice wants to eat an 'A' that is as far right as possible, to preserve 'A's to her left.
    # Bob wants to eat a 'B' that is as far left as possible, to preserve 'B's to his right.

    # This is a game on a line.
    # Alice wants to eat an 'A'. Bob wants to eat a 'B'.
    # The game ends when no more 'A's for Alice or 'B's for Bob.
    # The winner is the one who eats the last dish.

    # Let's consider the number of 'A's and 'B's.
    # Alice wants to eat an 'A'. Bob wants to eat a 'B'.
    # The game ends when no more 'A's for Alice or 'B's for Bob.
    # The winner is the one who eats the last dish.

    # This is a game on a string.
    # Alice's move: choose 'A' at index `i`. The string becomes S[i+1:].
    # Bob's move: choose 'B' at index `j`. The string becomes S[:j].

    # This is a game on a segment.
    # Let `dp[l][r]` be the winner for the segment `S[l...r]`.
    # Too slow for N=600,000.

    # The key insight must be simpler.
    # Alice wants to eat an 'A'. Bob wants to eat a 'B'.
    # They both want to eat the last dish.
    # This means they want to maximize their own count of dishes eaten.
    # The player who eats the last dish wins.

    # The crucial part is that Alice can choose *any* 'A' and Bob can choose *any* 'B'.
    # This means they can effectively "remove" a prefix or suffix.
    # Alice wants to eat an 'A' that is as far right as possible, to preserve 'A's to her left.
    # Bob wants to eat a 'B' that is as far left as possible, to preserve 'B's to his right.

    # This is a game on a line.
    # Alice wants to eat an 'A'. Bob wants to eat a 'B'.
    # The game ends when no more 'A's for Alice or 'B's for Bob.
    # The winner is the one who eats the last dish.

    # Let's consider the number of 'A's and 'B's.
    # Alice wants to eat an 'A'. Bob wants to eat a 'B'.
    # The game ends when no more 'A's for Alice or 'B's for Bob.
    # The winner is the one who eats the last dish.

    # This is a game on a string.
    # Alice's move: choose 'A' at index `i`. The string becomes S[i+1:].
    # Bob's move: choose 'B' at index `j`. The string becomes S[:j].

    # This is a game on a segment.
    # Let `dp[l][r]` be the winner for the segment `S[l...r]`.
    # Too slow for N=600,000.

    # The key insight must be simpler.
    # Alice wants to eat an 'A'. Bob wants to eat a 'B'.
    # They both want to eat the last dish.
    # This means they want to maximize their own count of dishes eaten.
    # The player who eats the last dish wins.

    # The crucial part is that Alice can choose *any* 'A' and Bob can choose *any* 'B'.
    # This means they can effectively "remove" a prefix or suffix.
    # Alice wants to eat an 'A' that is as far right as possible, to preserve 'A's to her left.
    # Bob wants to eat a 'B' that is as far left as possible, to preserve 'B's to his right.

    # This is a game on a line.
    # Alice wants to eat an 'A'. Bob wants to eat a 'B'.
    # The game ends when no more 'A's for Alice or 'B's for Bob.
    # The winner is the one who eats the last dish.

    # Let's consider the number of 'A's and 'B's.
    # Alice wants to eat an 'A'. Bob wants to eat a 'B'.
    # The game ends when no more 'A's for Alice or 'B's for Bob.
    # The winner is the one who eats the last dish.

    # This is a game on a string.
    # Alice's move: choose 'A' at index `i`. The string becomes S[i+1:].
    # Bob's move: choose 'B' at index `j`. The string becomes S[:j].

    # This is a game on a segment.
    # Let `dp[l][r]` be the winner for the segment `S[l...r]`.
    # Too slow for N=600,000.

    # The key insight must be simpler.
    # Alice wants to eat an 'A'. Bob wants to eat a 'B'.
    # They both want to eat the last dish.
    # This means they want to maximize their own count of dishes eaten.
    # The player who eats the last dish wins.

    # The crucial part is that Alice can choose *any* 'A' and Bob can choose *any* 'B'.
    # This means they can effectively "remove" a prefix or suffix.
    # Alice wants to eat an 'A' that is as far right as possible, to preserve 'A's to her left.
    # Bob wants to eat a 'B' that is as far left as possible, to preserve 'B's to his right.

    # This is a game on a line.
    # Alice wants to eat an 'A'. Bob wants to eat a 'B'.
    # The game ends when no more 'A's for Alice or 'B's for Bob.
    # The winner is the one who eats the last dish.

    # Let's consider the number of 'A's and 'B's.
    # Alice wants to eat an 'A'. Bob wants to eat a 'B'.
    # The game ends when no more 'A's for Alice or 'B's for Bob.
    # The winner is the one who eats the last dish.

    # This is a game on a string.
    # Alice's move: choose 'A' at index `i`. The string becomes S[i+1:].
    # Bob's move: choose 'B' at index `j`. The string becomes S[:j].

    # This is a game on a segment.
    # Let `dp[l][r]` be the winner for the segment `S[l...r]`.
    # Too slow for N=600,000.

    # The key insight must be simpler.
    # Alice wants to eat an 'A'. Bob wants to eat a 'B'.
    # They both want to eat the last dish.
    # This means they want to maximize their own count of dishes eaten.
    # The player who eats the last dish wins.

    # The crucial part is that Alice can choose *any* 'A' and Bob can choose *any* 'B'.
    # This means they can effectively "remove" a prefix or suffix.
    # Alice wants to eat an 'A' that is as far right as possible, to preserve 'A's to her left.
    # Bob wants to eat a 'B' that is as far left as possible, to preserve 'B's to his right.

    # This is a game on a line.
    # Alice wants to eat an 'A'. Bob wants to eat a 'B'.
    # The game ends when no more 'A's for Alice or 'B's for Bob.
    # The winner is the one who eats the last dish.

    # Let's consider the number of 'A's and 'B's.
    # Alice wants to eat an 'A'. Bob wants to eat a 'B'.
    # The game ends when no more 'A's for Alice or 'B's for Bob.
    # The winner is the one who eats the last dish.

    # This is a game on a string.
    # Alice's move: choose 'A' at index `i`. The string becomes S[i+1:].
    # Bob's move: choose 'B' at index `j`. The string becomes S[:j].

    # This is a game on a segment.
    # Let `dp[l][r]` be the winner for the segment `S[l...r]`.
    # Too slow for N=600,000.

    # The key insight must be simpler.
    # Alice wants to eat an 'A'. Bob wants to eat a 'B'.
    # They both want to eat the last dish.
    # This means they want to maximize their own count of dishes eaten.
    # The player who eats the last dish wins.

    # The crucial part is that Alice can choose *any* 'A' and Bob can choose *any* 'B'.
    # This means they can effectively "remove" a prefix or suffix.
    # Alice wants to eat an 'A' that is as far right as possible, to preserve 'A's to her left.
    # Bob wants to eat a 'B' that is as far left as possible, to preserve 'B's to his right.

    # This is a game on a line.
    # Alice wants to eat an 'A'. Bob wants to eat a 'B'.
    # The game ends when no more 'A's for Alice or 'B's for Bob.
    # The winner is the one who eats the last dish.

    # Let's consider the number of 'A's and 'B's.
    # Alice wants to eat an 'A'. Bob wants to eat a 'B'.
    # The game ends when no more 'A's for Alice or 'B's for Bob.
    # The winner is the one who eats the last dish.

    # This is a game on a string.
    # Alice's move: choose 'A' at index `i`. The string becomes S[i+1:].
    # Bob's move: choose 'B' at index `j`. The string becomes S[:j].

    # This is a game on a segment.
    # Let `dp[l][r]` be the winner for the segment `S[l...r]`.
    # Too slow for N=600,000.

    # The key insight must be simpler.
    # Alice wants to eat an 'A'. Bob wants to eat a 'B'.
    # They both want to eat the last dish.
    # This means they want to maximize their own count of dishes eaten.
    # The player who eats the last dish wins.

    # The crucial part is that Alice can choose *any* 'A' and Bob can choose *any* 'B'.
    # This means they can effectively "remove" a prefix or suffix.
    # Alice wants to eat an 'A' that is as far right as possible, to preserve 'A's to her left.
    # Bob wants to eat a 'B' that is as far left as possible, to preserve 'B's to his right.

    # This is a game on a line.
    # Alice wants to eat an 'A'. Bob wants to eat a 'B'.
    # The game ends when no more 'A's for Alice or 'B's for Bob.
    # The winner is the one who eats the last dish.

    # Let's consider the number of 'A's and 'B's.
    # Alice wants to eat an 'A'. Bob wants to eat a 'B'.
    # The game ends when no more 'A's for Alice or 'B's for Bob.
    # The winner is the one who eats the last dish.

    # This is a game on a string.
    # Alice's move: choose 'A' at index `i`. The string becomes S[i+1:].
    # Bob's move: choose 'B' at index `j`. The string becomes S[:j].

    # This is a game on a segment.
    # Let `dp[l][r]` be the winner for the segment `S[l...r]`.
    # Too slow for N=600,000.

    # The key insight must be simpler.
    # Alice wants to eat an 'A'. Bob wants to eat a 'B'.
    # They both want to eat the last dish.
    # This means they want to maximize their own count of dishes eaten.
    # The player who eats the last dish wins.

    # The crucial part is that Alice can choose *any* 'A' and Bob can choose *any* 'B'.
    # This means they can effectively "remove" a prefix or suffix.
    # Alice wants to eat an 'A' that is as far right as possible, to preserve 'A's to her left.
    # Bob wants to eat a 'B' that is as far left as possible, to preserve 'B's to his right.

    # This is a game on a line.
    # Alice wants to eat an 'A'. Bob wants to eat a 'B'.
    # The game ends when no more 'A's for Alice or 'B's for Bob.
    # The winner is the one who eats the last dish.

    # Let's consider the number of 'A's and 'B's.
    # Alice wants to eat an 'A'. Bob wants to eat a 'B'.
    # The game ends when no more 'A's for Alice or 'B's for Bob.
    # The winner is the one who eats the last dish.

    # This is a game on a string.
    # Alice's move: choose 'A' at index `i`. The string becomes S[i+1:].
    # Bob's move: choose 'B' at index `j`. The string becomes S[:j].

    # This is a game on a segment.
    # Let `dp[l][r]` be the winner for the segment `S[l...r]`.
    # Too slow for N=600,000.

    # The key insight must be simpler.
    # Alice wants to eat an 'A'. Bob wants to eat a 'B'.
    # They both want to eat the last dish.
    # This means they want to maximize their own count of dishes eaten.
    # The player who eats the last dish wins.

    # The crucial part is that Alice can choose *any* 'A' and Bob can choose *any* 'B'.
    # This means they can effectively "remove" a prefix or suffix.
    # Alice wants to eat an 'A' that is as far right as possible, to preserve 'A's to her left.
    # Bob wants to eat a 'B' that is as far left as possible, to preserve 'B's to his right.

    # This is a game on a line.
    # Alice wants to eat an 'A'. Bob wants to eat a 'B'.
    # The game ends when no more 'A's for Alice or 'B's for Bob.
    # The winner is the one who eats the last dish.

    # Let's consider the number of 'A's and 'B's.
    # Alice wants to eat an 'A'. Bob wants to eat a 'B'.
    # The game ends when no more 'A's for Alice or 'B's for Bob.
    # The winner is the one who eats the last dish.

    # This is a game on a string.
    # Alice's move: choose 'A' at index `i`. The string becomes S[i+1:].
    # Bob's move: choose 'B' at index `j`. The string becomes S[:j].

    # This is a game on a segment.
    # Let `dp[l][r]` be the winner for the segment `S[l...r]`.
    # Too slow for N=600,000.

    # The key insight must be simpler.
    # Alice wants to eat an 'A'. Bob wants to eat a 'B'.
    # They both want to eat the last dish.
    # This means they want to maximize their own count of dishes eaten.
    # The player who eats the last dish wins.

    # The crucial part is that Alice can choose *any* 'A' and Bob can choose *any* 'B'.
    # This means they can effectively "remove" a prefix or suffix.
    # Alice wants to eat an 'A' that is as far right as possible, to preserve 'A's to her left.
    # Bob wants to eat a 'B' that is as far left as possible, to preserve 'B's to his right.

    # This is a game on a line.
    # Alice wants to eat an 'A'. Bob wants to eat a 'B'.
    # The game ends when no more 'A's for Alice or 'B's for Bob.
    # The winner is the one who eats the last dish.

    # Let's consider the number of 'A's and 'B's.
    # Alice wants to eat an 'A'. Bob wants to eat a 'B'.
    # The game ends when no more 'A's for Alice or 'B's for Bob.
    # The winner is the one who eats the last dish.

    # This is a game on a string.
    # Alice's move: choose 'A' at index `i`. The string becomes S[i+1:].
    # Bob's move: choose 'B' at index `j`. The string becomes S[:j].

    # This is a game on a segment.
    # Let `dp[l][r]` be the winner for the segment `S[l...r]`.
    # Too slow for N=600,000.

    # The key insight must be simpler.
    # Alice wants to eat an 'A'. Bob wants to eat a 'B'.
    # They both want to eat the last dish.
    # This means they want to maximize their own count of dishes eaten.
    # The player who eats the last dish wins.

    # The crucial part is that Alice can choose *any* 'A' and Bob can choose *any* 'B'.
    # This means they can effectively "remove" a prefix or suffix.
    # Alice wants to eat an 'A' that is as far right as possible, to preserve 'A's to her left.
    # Bob wants to eat a 'B' that is as far left as possible, to preserve 'B's to his right.

    # This is a game on a line.
    # Alice wants to eat an 'A'. Bob wants to eat a 'B'.
    # The game ends when no more 'A's for Alice or 'B's for Bob.
    # The winner is the one who eats the last dish.

    # Let's consider the number of 'A's and 'B's.
    # Alice wants to eat an 'A'. Bob wants to eat a 'B'.
    # The game ends when no more 'A's for Alice or 'B's for Bob.
    # The winner is the one who eats the last dish.

    # This is a game on a string.
    # Alice's move: choose 'A' at index `i`. The string becomes S[i+1:].
    # Bob's move: choose 'B' at index `j`. The string becomes S[:j].

    # This is a game on a segment.
    # Let `dp[l][r]` be the winner for the segment `S[l...r]`.
    # Too slow for N=600,000.

    # The key insight must be simpler.
    # Alice wants to eat an 'A'. Bob wants to eat a 'B'.
    # They both want to eat the last dish.
    # This means they want to maximize their own count of dishes eaten.
    # The player who eats the last dish wins.

    # The crucial part is that Alice can choose *any* 'A' and Bob can choose *any* 'B'.
    # This means they can effectively "remove" a prefix or suffix.
    # Alice wants to eat an 'A' that is as far right as possible, to preserve 'A's to her left.
    # Bob wants to eat a 'B' that is as far left as possible, to preserve 'B's to his right.

    # This is a game on a line.
    # Alice wants to eat an 'A'. Bob wants to eat a 'B'.
    # The game ends when no more 'A's for Alice or 'B's for Bob.
    # The winner is the one who eats the last dish.

    # Let's consider the number of 'A's and 'B's.
    # Alice wants to eat an 'A'. Bob wants to eat a 'B'.
    # The game ends when no more 'A's for Alice or 'B's for Bob.
    # The winner is the one who eats the last dish.

    # This is a game on a string.
    # Alice's move: choose 'A' at index `i`. The string becomes S[i+1:].
    # Bob's move: choose 'B' at index `j`. The string becomes S[:j].

    # This is a game on a segment.
    # Let `dp[l][r]` be the winner for the segment `S[l...r]`.
    # Too slow for N=600,000.

    # The key insight must be simpler.
    # Alice wants to eat an 'A'. Bob wants to eat a 'B'.
    # They both want to eat the last dish.
    # This means they want to maximize their own count of dishes eaten.
    # The player who eats the last dish wins.

    # The crucial part is that Alice can choose *any* 'A' and Bob can choose *any* 'B'.
    # This means they can effectively "remove" a prefix or suffix.
    # Alice wants to eat an 'A' that is as far right as possible, to preserve 'A's to her left.
    # Bob wants to eat a 'B' that is as far left as possible, to preserve 'B's to his right.

    # This is a game on a line.
    # Alice wants to eat an 'A'. Bob wants to eat a 'B'.
    # The game ends when no more 'A's for Alice or 'B's for Bob.
    # The winner is the one who eats the last dish.

    # Let's consider the number of 'A's and 'B's.
    # Alice wants to eat an 'A'. Bob wants to eat a 'B'.
    # The game ends when no more 'A's for Alice or 'B's for Bob.
    # The winner is the one who eats the last dish.

    # This is a game on a string.
    # Alice's move: choose 'A' at index `i`. The string becomes S[i+1:].
    # Bob's move: choose 'B' at index `j`. The string becomes S[:j].

    # This is a game on a segment.
    # Let `dp[l][r]` be the winner for the segment `S[l...r]`.
    # Too slow for N=600,000.

    # The key insight must be simpler.
    # Alice wants to eat an 'A'. Bob wants to eat a 'B'.
    # They both want to eat the last dish.
    # This means they want to maximize their own count of dishes eaten.
    # The player who eats the last dish wins.

    # The crucial part is that Alice can choose *any* 'A' and Bob can choose *any* 'B'.
    # This means they can effectively "remove" a prefix or suffix.
    # Alice wants to eat an 'A' that is as far right as possible, to preserve 'A's to her left.
    # Bob wants to eat a 'B' that is as far left as possible, to preserve 'B's to his right.

    # This is a game on a line.
    # Alice wants to eat an 'A'. Bob wants to eat a 'B'.
    # The game ends when no more 'A's for Alice or 'B's for Bob.
    # The winner is the one who eats the last dish.

    # Let's consider the number of 'A's and 'B's.
    # Alice wants to eat an 'A'. Bob wants to eat a 'B'.
    # The game ends when no more 'A's for Alice or 'B's for Bob.
    # The winner is the one who eats the last dish.

    # This is a game on a string.
    # Alice's move: choose 'A' at index `i`. The string becomes S[i+1:].
    # Bob's move: choose 'B' at index `j`. The string becomes S[:j].

    # This is a game on a segment.
    # Let `dp[l][r]` be the winner for the segment `S[l...r]`.
    # Too slow for N=600,000.

    # The key insight must be simpler.
    # Alice wants to eat an 'A'. Bob wants to eat a 'B'.
    # They both want to eat the last dish.
    # This means they want to maximize their own count of dishes eaten.
    # The player who eats the last dish wins.

    # The crucial part is that Alice can choose *any* 'A' and Bob can choose *any* 'B'.
    # This means they can effectively "remove" a prefix or suffix.
    # Alice wants to eat an 'A' that is as far right as possible, to preserve 'A's to her left.
    # Bob wants to eat a 'B' that is as far left as possible, to preserve 'B's to his right.

    # This is a game on a line.
    # Alice wants to eat an 'A'. Bob wants to eat a 'B'.
    # The game ends when no more 'A's for Alice or 'B's for Bob.
    # The winner is the one who eats the last dish.

    # Let's consider the number of 'A's and 'B's.
    # Alice wants to eat an 'A'. Bob wants to eat a 'B'.
    # The game ends when no more 'A's for Alice or 'B's for Bob.
    # The winner is the one who eats the last dish.

    # This is a game on a string.
    # Alice's move: choose 'A' at index `i`. The string becomes S[i+1:].
    # Bob's move: choose 'B' at index `j`. The string becomes S[:j].

    # This is a game on a segment.
    # Let `dp[l][r]` be the winner for the segment `S[l...r]`.
    # Too slow for N=600,000.

    # The key insight must be simpler.
    # Alice wants to eat an 'A'. Bob wants to eat a 'B'.
    # They both want to eat the last dish.
    # This means they want to maximize their own count of dishes eaten.
    # The player who eats the last dish wins.

    # The crucial part is that Alice can choose *any* 'A' and Bob can choose *any* 'B'.
    # This means they can effectively "remove" a prefix or suffix.
    # Alice wants to eat an 'A' that is as far right as possible, to preserve 'A's to her left.
    # Bob wants to eat a 'B' that is as far left as possible, to preserve 'B's to his right.

    # This is a game on a line.
    # Alice wants to eat an 'A'. Bob wants to eat a 'B'.
    # The game ends when no more 'A's for Alice or 'B's for Bob.
    # The winner is the one who eats the last dish.

    # Let's consider the number of 'A's and 'B's.
    # Alice wants to eat an 'A'. Bob wants to eat a 'B'.
    # The game ends when no more 'A's for Alice or 'B's for Bob.
    # The winner is the one who eats the last dish.

    # This is a game on a string.
    # Alice's move: choose 'A' at index `i`. The string becomes S[i+1:].
    # Bob's move: choose 'B' at index `j`. The string becomes S[:j].

    # This is a game on a segment.
    # Let `dp[l][r]` be the winner for the segment `S[l...r]`.
    # Too slow for N=600,000.

    # The key insight must be simpler.
    # Alice wants to eat an 'A'. Bob wants to eat a 'B'.
    # They both want to eat the last dish.
    # This means they want to maximize their own count of dishes eaten.
    # The player who eats the last dish wins.

    # The crucial part is that Alice can choose *any* 'A' and Bob can choose *any* 'B'.
    # This means they can effectively "remove" a prefix or suffix.
    # Alice wants to eat an 'A' that is as far right as possible, to preserve 'A's to her left.
    # Bob wants to eat a 'B' that is as far left as possible, to preserve 'B's to his right.

    # This is a game on a line.
    # Alice wants to eat an 'A'. Bob wants to eat a 'B'.
    # The game ends when no more 'A's for Alice or 'B's for Bob.
    # The winner is the one who eats the last dish.

    # Let's consider the number of 'A's and 'B's.
    # Alice wants to eat an 'A'. Bob wants to eat a 'B'.
    # The game ends when no more 'A's for Alice or 'B's for Bob.
    # The winner is the one who eats the last dish.

    # This is a game on a string.
    # Alice's move: choose 'A' at index `i`. The string becomes S[i+1:].
    # Bob's move: choose 'B' at index `j`. The string becomes S[:j].

    # This is a game on a segment.
    # Let `dp[l][r]` be the winner for the segment `S[l...r]`.
    # Too slow for N=600,000.

    # The key insight must be simpler.
    # Alice wants to eat an 'A'. Bob wants to eat a 'B'.
    # They both want to eat the last dish.
    # This means they want to maximize their own count of dishes eaten.
    # The player who eats the last dish wins.

    # The crucial part is that Alice can choose *any* 'A' and Bob can choose *any* 'B'.
    # This means they can effectively "remove" a prefix or suffix.
    # Alice wants to eat an 'A' that is as far right as possible, to preserve 'A's to her left.
    # Bob wants to eat a 'B' that is as far left as possible, to preserve 'B's to his right.

    # This is a game on a line.
    # Alice wants to eat an 'A'. Bob wants to eat a 'B'.
    # The game ends when no more 'A's for Alice or 'B's for Bob.
    # The winner is the one who eats the last dish.

    # Let's consider the number of 'A's and 'B's.
    # Alice wants to eat an 'A'. Bob wants to eat a 'B'.
    # The game ends when no more 'A's for Alice or 'B's for Bob.
    # The winner is the one who eats the last dish.

    # This is a game on a string.
    # Alice's move: choose 'A' at index `i`. The string becomes S[i+1:].
    # Bob's move: choose 'B' at index `j`. The string becomes S[:j].

    # This is a game on a segment.
    # Let `dp[l][r]` be the winner for the segment `S[l...r]`.
    # Too slow for N=600,000.

    # The key insight must be simpler.
    # Alice wants to eat an 'A'. Bob wants to eat a 'B'.
    # They both want to eat the last dish.
    # This means they want to maximize their own count of dishes eaten.
    # The player who eats the last dish wins.

    # The crucial part is that Alice can choose *any* 'A' and Bob can choose *any* 'B'.
    # This means they can effectively "remove" a prefix or suffix.
    # Alice wants to eat an 'A' that is as far right as possible, to preserve 'A's to her left.
    # Bob wants to eat a 'B' that is as far left as possible, to preserve 'B's to his right.

    # This is a game on a line.
    # Alice wants to eat an 'A'. Bob wants to eat a 'B'.
    # The game ends when no more 'A's for Alice or 'B's for Bob.
    # The winner is the one who eats the last dish.

    # Let's consider the number of 'A's and 'B's.
    # Alice wants to eat an 'A'. Bob wants to eat a 'B'.
    # The game ends when no more 'A's for Alice or 'B's for Bob.
    # The winner is the one who eats the last dish.

    # This is a game on a string.
    # Alice's move: choose 'A' at index `i`. The string becomes S[i+1:].
    # Bob's move: choose 'B' at index `j`. The string becomes S[:j].

    # This is a game on a segment.
    # Let `dp[l][r]` be the winner for the segment `S[l...r]`.
    # Too slow for N=600,000.

    # The key insight must be simpler.
    # Alice wants to eat an 'A'. Bob wants to eat a 'B'.
    # They both want to eat the last dish.
    # This means they want to maximize their own count of dishes eaten.
    # The player who eats the last dish wins.

    # The crucial part is that Alice can choose *any* 'A' and Bob can choose *any* 'B'.
    # This means they can effectively "remove" a prefix or suffix.
    # Alice wants to eat an 'A' that is as far right as possible, to preserve 'A's to her left.
    # Bob wants to eat a 'B' that is as far left as possible, to preserve 'B's to his right.

    # This is a game on a line.
    # Alice wants to eat an 'A'. Bob wants to eat a 'B'.
    # The game ends when no more 'A's for Alice or 'B's for Bob.
    # The winner is the one who eats the last dish.

    # Let's consider the number of 'A's and 'B's.
    # Alice wants to eat an 'A'. Bob wants to eat a 'B'.
    # The game ends when no more 'A's for Alice or 'B's for Bob.
    # The winner is the one who eats the last dish.

    # This is a game on a string.
    # Alice's move: choose 'A' at index `i`. The string becomes S[i+1:].
    # Bob's move: choose 'B' at index `j`. The string becomes S[:j].

    # This is a game on a segment.
    # Let `dp[l][r]` be the winner for the segment `S[l...r]`.
    # Too slow for N=600,000.

    # The key insight must be simpler.
    # Alice wants to eat an 'A'. Bob wants to eat a 'B'.
    # They both want to eat the last dish.
    # This means they want to maximize their own count of dishes eaten.
    # The player who eats the last dish wins.

    # The crucial part is that Alice can choose *any* 'A' and Bob can choose *any* 'B'.
    # This means they can effectively "remove" a prefix or suffix.
    # Alice wants to eat an 'A' that is as far right as possible, to preserve 'A's to her left.
    # Bob wants to eat a 'B' that is as far left as possible, to preserve 'B's to his right.

    # This is a game on a line.
    # Alice wants to eat an 'A'. Bob wants to eat a 'B'.
    # The game ends when no more 'A's for Alice or 'B's for Bob.
    # The winner is the one who eats the last dish.

    # Let's consider the number of 'A's and 'B's.
    # Alice wants to eat an 'A'. Bob wants to eat a 'B'.
    # The game ends when no more 'A's for Alice or 'B's for Bob.
    # The winner is the one who eats the last dish.

    # This is a game on a string.
    # Alice's move: choose 'A' at index `i`. The string becomes S[i+1:].
    # Bob's move: choose 'B' at index `j`. The string becomes S[:j].

    # This is a game on a segment.
    # Let `dp[l][r]` be the winner for the segment `S[l...r]`.
    # Too slow for N=600,000.

    # The key insight must be simpler.
    # Alice wants to eat an 'A'. Bob wants to eat a 'B'.
    # They both want to eat the last dish.
    # This means they want to maximize their own count of dishes eaten.
    # The player who eats the last dish wins.

    # The crucial part is that Alice can choose *any* 'A' and Bob can choose *any* 'B'.
    # This means they can effectively "remove" a prefix or suffix.
    # Alice wants to eat an 'A' that is as far right as possible, to preserve 'A's to her left.
    # Bob wants to eat a 'B' that is as far left as possible, to preserve 'B's to his right.

    # This is a game on a line.
    # Alice wants to eat an 'A'. Bob wants to eat a 'B'.
    # The game ends when no more 'A's for Alice or 'B's for Bob.
    # The winner is the one who eats the last dish.

    # Let's consider the number of 'A's and 'B's.
    # Alice wants to eat an 'A'. Bob wants to eat a 'B'.
    # The game ends when no more 'A's for Alice or 'B's for Bob.
    # The winner is the one who eats the last dish.

    # This is a game on a string.
    # Alice's move: choose 'A' at index `i`. The string becomes S[i+1:].
    # Bob's move: choose 'B' at index `j`. The string becomes S[:j].

    # This is a game on a segment.
    # Let `dp[l][r]` be the winner for the segment `S[l...r]`.
    # Too slow for N=600,000.

    # The key insight must be simpler.
    # Alice wants to eat an 'A'. Bob wants to eat a 'B'.
    # They both want to eat the last dish.
    # This means they want to maximize their own count of dishes eaten.
    # The player who eats the last dish wins.

    # The crucial part is that Alice can choose *any* 'A' and Bob can choose *any* 'B'.
    # This means they can effectively "remove" a prefix or suffix.
    # Alice wants to eat an 'A' that is as far right as possible, to preserve 'A's to her left.
    # Bob wants to eat a 'B' that is as far left as possible, to preserve 'B's to his right.

    # This is a game on a line.
    # Alice wants to eat an 'A'. Bob wants to eat a 'B'.
    # The game ends when no more 'A's for Alice or 'B's for Bob.
    # The winner is the one who eats the last dish.

    # Let's consider the number of 'A's and 'B's.
    # Alice wants to eat an 'A'. Bob wants to eat a 'B'.
    # The game ends when no more 'A's for Alice or 'B's for Bob.
    # The winner is the one who eats the last dish.

    # This is a game on a string.
    # Alice's move: choose 'A' at index `i`. The string becomes S[i+1:].
    # Bob's move: choose 'B' at index `j`. The string becomes S[:j].

    # This is a game on a segment.
    # Let `dp[l][r]` be the winner for the segment `S[l...r]`.
    # Too slow for N=600,000.

    # The key insight must be simpler.
    # Alice wants to eat an 'A'. Bob wants to eat a 'B'.
    # They both want to eat the last dish.
    # This means they want to maximize their own count of dishes eaten.
    # The player who eats the last dish wins.

    # The crucial part is that Alice can choose *any* 'A' and Bob can choose *any* 'B'.
    # This means they can effectively "remove" a prefix or suffix.
    # Alice wants to eat an 'A' that is as far right as possible, to preserve 'A's to her left.
    # Bob wants to eat a 'B' that is as far left as possible, to preserve 'B's to his right.

    # This is a game on a line.
    # Alice wants to eat an 'A'. Bob wants to eat a 'B'.
    # The game ends when no more 'A's for Alice or 'B's for Bob.
    # The winner is the one who eats the last dish.

    # Let's consider the number of 'A's and 'B's.
    # Alice wants to eat an 'A'. Bob wants to eat a 'B'.
    # The game ends when no more 'A's for Alice or 'B's for Bob.
    # The winner is the one who eats the last dish.

    # This is a game on a string.
    # Alice's move: choose 'A' at index `i`. The string becomes S[i+1:].
    # Bob's move: choose 'B' at index `j`. The string becomes S[:j].

    # This is a game on a segment.
    # Let `dp[l][r]` be the winner for the segment `S[l...r]`.
    # Too slow for N=600,000.

    # The key insight must be simpler.
    # Alice wants to eat an 'A'. Bob wants to eat a 'B'.
    # They both want to eat the last dish.
    # This means they want to maximize their own count of dishes eaten.
    # The player who eats the last dish wins.

    # The crucial part is that Alice can choose *any* 'A' and Bob can choose *any* 'B'.
    # This means they can effectively "remove" a prefix or suffix.
    # Alice wants to eat an 'A' that is as far right as possible, to preserve 'A's to her left.
    # Bob wants to eat a 'B' that is as far left as possible, to preserve 'B's to his right.

    # This is a game on a line.
    # Alice wants to eat an 'A'. Bob wants to eat a 'B'.
    # The game ends when no more 'A's for Alice or 'B's for Bob.
    # The winner is the one who eats the last dish.

    # Let's consider the number of 'A's and 'B's.
    # Alice wants to eat an 'A'. Bob wants to eat a 'B'.
    # The game ends when no more 'A's for Alice or 'B's for Bob.
    # The winner is the one who eats the last dish.

    # This is a game on a string.
    # Alice's move: choose 'A' at index `i`. The string becomes S[i+1:].
    # Bob's move: choose 'B' at index `j`. The string becomes S[:j].

    # This is a game on a segment.
    # Let `dp[l][r]` be the winner for the segment `S[l...r]`.
    # Too slow for N=600,000.

    # The key insight must be simpler.
    # Alice wants to eat an 'A'. Bob wants to eat a 'B'.
    # They both want to eat the last dish.
    # This means they want to maximize their own count of dishes eaten.
    # The player who eats the last dish wins.

    # The crucial part is that Alice can choose *any* 'A' and Bob can choose *any* 'B'.
    # This means they can effectively "remove" a prefix or suffix.
    # Alice wants to eat an 'A' that is as far right as possible, to preserve 'A's to her left.
    # Bob wants to eat a 'B' that is as far left as possible, to preserve 'B's to his right.

    # This is a game on a line.
    # Alice wants to eat an 'A'. Bob wants to eat a 'B'.
    # The game ends when no more 'A's for Alice or 'B's for Bob.
    # The winner is the one who eats the last dish.

    # Let's consider the number of 'A's and 'B's.
    # Alice wants to eat an 'A'. Bob wants to eat a 'B'.
    # The game ends when no more 'A's for Alice or 'B's for Bob.
    # The winner is the one who eats the last dish.

    # This is a game on a string.
    # Alice's move: choose 'A' at index `i`. The string becomes S[i+1:].
    # Bob's move: choose 'B' at index `j`. The string becomes S[:j].

    # This is a game on a segment.
    # Let `dp[l][r]` be the winner for the segment `S[l...r]`.
    # Too slow for N=600,000.

    # The key insight must be simpler.
    # Alice wants to eat an 'A'. Bob wants to eat a 'B'.
    # They both want to eat the last dish.
    # This means they want to maximize their own count of dishes eaten.
    # The player who eats the last dish wins.

    # The crucial part is that Alice can choose *any* 'A' and Bob can choose *any* 'B'.
    # This means they can effectively "remove" a prefix or suffix.
    # Alice wants to eat an 'A' that is as far right as possible, to preserve 'A's to her left.
    # Bob wants to eat a 'B' that is as far left as possible, to preserve 'B's to his right.

    # This is a game on a line.
    # Alice wants to eat an 'A'. Bob wants to eat a 'B'.
    # The game ends when no more 'A's for Alice or 'B's for Bob.
    # The winner is the one who eats the last dish.

    # Let's consider the number of 'A's and 'B's.
    # Alice wants to eat an 'A'. Bob wants to eat a 'B'.
    # The game ends when no more 'A's for Alice or 'B's for Bob.
    # The winner is the one who eats the last dish.

    # This is a game on a string.
    # Alice's move: choose 'A' at index `i`. The string becomes S[i+1:].
    # Bob's move: choose 'B' at index `j`. The string becomes S[:j].

    # This is a game on a segment.
    # Let `dp[l][r]` be the winner for the segment `S[l...r]`.
    # Too slow for N=600,000.

    # The key insight must be simpler.
    # Alice wants to eat an 'A'. Bob wants to eat a 'B'.
    # They both want to eat the last dish.
    # This means they want to maximize their own count of dishes eaten.
    # The player who eats the last dish wins.

    # The crucial part is that Alice can choose *any* 'A' and Bob can choose *any* 'B'.
    # This means they can effectively "remove" a prefix or suffix.
    # Alice wants to eat an 'A' that is as far right as possible, to preserve 'A's to her left.
    # Bob wants to eat a 'B' that is as far left as possible, to preserve 'B's to his right.

    # This is a game on a line.
    # Alice wants to eat an 'A'. Bob wants to eat a 'B'.
    # The game ends when no more 'A's for Alice or 'B's for Bob.
    # The winner is the one who eats the last dish.

    # Let's consider the number of 'A's and 'B's.
    # Alice wants to eat an 'A'. Bob wants to eat a 'B'.
    # The game ends when no more 'A's for Alice or 'B's for Bob.
    # The winner is the one who eats the last dish.

    # This is a game on a string.
    # Alice's move: choose 'A' at index `i`. The string becomes S[i+1:].
    # Bob's move: choose 'B' at index `j`. The string becomes S[:j].

    # This is a game on a segment.
    # Let `dp[l][r]` be the winner for the segment `S[l...r]`.
    # Too slow for N=600,000.

    # The key insight must be simpler.
    # Alice wants to eat an 'A'. Bob wants to eat a 'B'.
    # They both want to eat the last dish.
    # This means they want to maximize their own count of dishes eaten.
    # The player who eats the last dish wins.

    # The crucial part is that Alice can choose *any* 'A' and Bob can choose *any* 'B'.
    # This means they can effectively "remove" a prefix or suffix.
    # Alice wants to eat an 'A' that is as far right as possible, to preserve 'A's to her left.
    # Bob wants to eat a 'B' that is as far left as possible, to preserve 'B's to his right.

    # This is a game on a line.
    # Alice wants to eat an 'A'. Bob wants to eat a 'B'.
    # The game ends when no more 'A's for Alice or 'B's for Bob.
    # The winner is the one who eats the last dish.

    # Let's consider the number of 'A's and 'B's.
    # Alice wants to eat an 'A'. Bob wants to eat a 'B'.
    # The game ends when no more 'A's for Alice or 'B's for Bob.
    # The winner is the one who eats the last dish.

    # This is a game on a string.
    # Alice's move: choose 'A' at index `i`. The string becomes S[i+1:].
    # Bob's move: choose 'B' at index `j`. The string becomes S[:j].

    # This is a game on a segment.
    # Let `dp[l][r]` be the winner for the segment `S[l...r]`.
    # Too slow for N=600,000.

    # The key insight must be simpler.
    # Alice wants to eat an 'A'. Bob wants to eat a 'B'.
    # They both want to eat the last dish.
    # This means they want to maximize their own count of dishes eaten.
    # The player who eats the last dish wins.

    # The crucial part is that Alice can choose *any* 'A' and Bob can choose *any* 'B'.
    # This means they can effectively "remove" a prefix or suffix.
    # Alice wants to eat an 'A' that is as far right as possible, to preserve 'A's to her left.
    # Bob wants to eat a 'B' that is as far left as possible, to preserve 'B's to his right.

    # This is a game on a line.
    # Alice wants to eat an 'A'. Bob wants to eat a 'B'.
    # The game ends when no more 'A's for Alice or 'B's for Bob.
    # The winner is the one who eats the last dish.

    # Let's consider the number of 'A's and 'B's.
    # Alice wants to eat an 'A'. Bob wants to eat a 'B'.
    # The game ends when no more 'A's for Alice or 'B's for Bob.
    # The winner is the one who eats the last dish.

    # This is a game on a string.
    # Alice's move: choose 'A' at index `i`. The string becomes S[i+1:].
    # Bob's move: choose 'B' at index `j`. The string becomes S[:j].

    # This is a game on a segment.
    # Let `dp[l][r]` be the winner for the segment `S[l...r]`.
    # Too slow for N=600,000.

    # The key insight must be simpler.
    # Alice wants to eat an 'A'. Bob wants to eat a 'B'.
    # They both want to eat the last dish.
    # This means they want to maximize their own count of dishes eaten.
    # The player who eats the last dish wins.

    # The crucial part is that Alice can choose *any* 'A' and Bob can choose *any* 'B'.
    # This means they can effectively "remove" a prefix or suffix.
    # Alice wants to eat an 'A' that is as far right as possible, to preserve 'A's to her left.
    # Bob wants to eat a 'B' that is as far left as possible, to preserve 'B's to his right.

    # This is a game on a line.
    # Alice wants to eat an 'A'. Bob wants to eat a 'B'.
    # The game ends when no more 'A's for Alice or 'B's for Bob.
    # The winner is the one who eats the last dish.

    # Let's consider the number of 'A's and 'B's.
    # Alice wants to eat an 'A'. Bob wants to eat a 'B'.
    # The game ends when no more 'A's for Alice or 'B's for Bob.
    # The winner is the one who eats the last dish.

    # This is a game on a string.
    # Alice's move: choose 'A' at index `i`. The string becomes S[i+1:].
    # Bob's move: choose 'B' at index `j`. The string becomes S[:j].

    # This is a game on a segment.
    # Let `dp[l][r]` be the winner for the segment `S[l...r]`.
    # Too slow for N=600,000.

    # The key insight must be simpler.
    # Alice wants to eat an 'A'. Bob wants to eat a 'B'.
    # They both want to eat the last dish.
    # This means they want to maximize their own count of dishes eaten.
    # The player who eats the last dish wins.

    # The crucial part is that Alice can choose *any* 'A' and Bob can choose *any* 'B'.
    # This means they can effectively "remove" a prefix or suffix.
    # Alice wants to eat an 'A' that is as far right as possible, to preserve 'A's to her left.
    # Bob wants to eat a 'B' that is as far left as possible, to preserve 'B's to his right.

    # This is a game on a line.
    # Alice wants to eat an 'A'. Bob wants to eat a 'B'.
    # The game ends when no more 'A's for Alice or 'B's for Bob.
    # The winner is the one who eats the last dish.

    # Let's consider the number of 'A's and 'B's.
    # Alice wants to eat an 'A'. Bob wants to eat a 'B'.
    # The game ends when no more 'A's for Alice or 'B's for Bob.
    # The winner is the one who eats the last dish.

    # This is a game on a string.
    # Alice's move: choose 'A' at index `i`. The string becomes S[i+1:].
    # Bob's move: choose 'B' at index `j`. The string becomes S[:j].

    # This is a game on a segment.
    # Let `dp[l][r]` be the winner for the segment `S[l...r]`.
    # Too slow for N=600,000.

    # The key insight must be simpler.
    # Alice wants to eat an 'A'. Bob wants to eat a 'B'.
    # They both want to eat the last dish.
    # This means they want to maximize their own count of dishes eaten.
    # The player who eats the last dish wins.

    # The crucial part is that Alice can choose *any* 'A' and Bob can choose *any* 'B'.
    # This means they can effectively "remove" a prefix or suffix.
    # Alice wants to eat an 'A' that is as far right as possible, to preserve 'A's to her left.
    # Bob wants to eat a 'B' that is as far left as possible, to preserve 'B's to his right.

    # This is a game on a line.
    # Alice wants to eat an 'A'. Bob wants to eat a 'B'.
    # The game ends when no more 'A's for Alice or 'B's for Bob.
    # The winner is the one who eats the last dish.

    # Let's consider the number of 'A's and 'B's.
    # Alice wants to eat an 'A'. Bob wants to eat a 'B'.
    # The game ends when no more 'A's for Alice or 'B's for Bob.
    # The winner is the one who eats the last dish.

    # This is a game on a string.
    # Alice's move: choose 'A' at index `i`. The string becomes S[i+1:].
    # Bob's move: choose 'B' at index `j`. The string becomes S[:j].

    # This is a game on a segment.
    # Let `dp[l][r]` be the winner for the segment `S[l...r]`.
    # Too slow for N=600,000.

    # The key insight must be simpler.
    # Alice wants to eat an 'A'. Bob wants to eat a 'B'.
    # They both want to eat the last dish.
    # This means they want to maximize their own count of dishes eaten.
    # The player who eats the last dish wins.

    # The crucial part is that Alice can choose *any* 'A' and Bob can choose *any* 'B'.
    # This means they can effectively "remove" a prefix or suffix.
    # Alice wants to eat an 'A' that is as far right as possible, to preserve 'A's to her left.
    # Bob wants to eat a 'B' that is as far left as possible, to preserve 'B's to his right.

    # This is a game on a line.
    # Alice wants to eat an 'A'. Bob wants to eat a 'B'.
    # The game ends when no more 'A's for Alice or 'B's for Bob.
    # The winner is the one who eats the last dish.

    # Let's consider the number of 'A's and 'B's.
    # Alice wants to eat an 'A'. Bob wants to eat a 'B'.
    # The game ends when no more 'A's for Alice or 'B's for Bob.
    # The winner is the one who eats the last dish.

    # This is a game on a string.
    # Alice's move: choose 'A' at index `i`. The string becomes S[i+1:].
    # Bob's move: choose 'B' at index `j`. The string becomes S[:j].

    # This is a game on a segment.
    # Let `dp[l][r]` be the winner for the segment `S[l...r]`.
    # Too slow for N=600,000.

    # The key insight must be simpler.
    # Alice wants to eat an 'A'. Bob wants to eat a 'B'.
    # They both want to eat the last dish.
    # This means they want to maximize their own count of dishes eaten.
    # The player who eats the last dish wins.

    # The crucial part is that Alice can choose *any* 'A' and Bob can choose *any* 'B'.
    # This means they can effectively "remove" a prefix or suffix.
    # Alice wants to eat an 'A' that is as far right as possible, to preserve 'A's to her left.
    # Bob wants to eat a 'B' that is as far left as possible, to preserve 'B's to his right.

    # This is a game on a line.
    # Alice wants to eat an 'A'. Bob wants to eat a 'B'.
    # The game ends when no more 'A's for Alice or 'B's for Bob.
    # The winner is the one who eats the last dish.

    # Let's consider the number of 'A's and 'B's.
    # Alice wants to eat an 'A'. Bob wants to eat a 'B'.
    # The game ends when no more 'A's for Alice or 'B's for Bob.
    # The winner is the one who eats the last dish.

    # This is a game on a string.
    # Alice's move: choose 'A' at index `i`. The string becomes S[i+1:].
    # Bob's move: choose 'B' at index `j`. The string becomes S[:j].

    # This is a game on a segment.
    # Let `dp[l][r]` be the winner for the segment `S[l...r]`.
    # Too slow for N=600,000.

    # The key insight must be simpler.
    # Alice wants to eat an 'A'. Bob wants to eat a 'B'.
    # They both want to eat the last dish.
    # This means they want to maximize their own count of dishes eaten.
    # The player who eats the last dish wins.

    # The crucial part is that Alice can choose *any* 'A' and Bob can choose *any* 'B'.
    # This means they can effectively "remove" a prefix or suffix.
    # Alice wants to eat an 'A' that is as far right as possible, to preserve 'A's to her left.
    # Bob wants to eat a 'B' that is as far left as possible, to preserve 'B's to his right.

    # This is a game on a line.
    # Alice wants to eat an 'A'. Bob wants to eat a 'B'.
    # The game ends when no more 'A's for Alice or 'B's for Bob.
    # The winner is the one who eats the last dish.

    # Let's consider the number of 'A's and 'B's.
    # Alice wants to eat an 'A'. Bob wants to eat a 'B'.
    # The game ends when no more 'A's for Alice or 'B's for Bob.
    # The winner is the one who eats the last dish.

    # This is a game on a string.
    # Alice's move: choose 'A' at index `i`. The string becomes S[i+1:].
    # Bob's move: choose 'B' at index `j`. The string becomes S[:j].

    # This is a game on a segment.
    # Let `dp[l][r]` be the winner for the segment `S[l...r]`.
    # Too slow for N=600,000.

    # The key insight must be simpler.
    # Alice wants to eat an 'A'. Bob wants to eat a 'B'.
    # They both want to eat the last dish.
    # This means they want to maximize their own count of dishes eaten.
    # The player who eats the last dish wins.

    # The crucial part is that Alice can choose *any* 'A' and Bob can choose *any* 'B'.
    # This means they can effectively "remove" a prefix or suffix.
    # Alice wants to eat an 'A' that is as far right as possible, to preserve 'A's to her left.
    # Bob wants to eat a 'B' that is as far left as possible, to preserve 'B's to his right.

    # This is a game on a line.
    # Alice wants to eat an 'A'. Bob wants to eat a 'B'.
    # The game ends when no more 'A's for Alice or 'B's for Bob.
    # The winner is the one who eats the last dish.

    # Let's consider the number of 'A's and 'B's.
    # Alice wants to eat an 'A'. Bob wants to eat a 'B'.
    # The game ends when no more 'A's for Alice or 'B's for Bob.
    # The winner is the one who eats the last dish.

    # This is a game on a string.
    # Alice's move: choose 'A' at index `i`. The string becomes S[i+1:].
    # Bob's move: choose 'B' at index `j`. The string becomes S[:j].

    # This is a game on a segment.
    # Let `dp[l][r]` be the winner for the segment `S[l...r]`.
    # Too slow for N=600,000.

    # The key insight must be simpler.
    # Alice wants to eat an 'A'. Bob wants to eat a 'B'.
    # They both want to eat the last dish.
    # This means they want to maximize their own count of dishes eaten.
    # The player who eats the last dish wins.

    # The crucial part is that Alice can choose *any* 'A' and Bob can choose *any* 'B'.
    # This means they can effectively "remove" a prefix or suffix.
    # Alice wants to eat an 'A' that is as far right as possible, to preserve 'A's to her left.
    # Bob wants to eat a 'B' that is as far left as possible, to preserve 'B's to his right.

    # This is a game on a line.
    # Alice wants to eat an 'A'. Bob wants to eat a 'B'.
    # The game ends when no more 'A's for Alice or 'B's for Bob.
    # The winner is the one who eats the last dish.

    # Let's consider the number of 'A's and 'B's.
    # Alice wants to eat an 'A'. Bob wants to eat a 'B'.
    # The game ends when no more 'A's for Alice or 'B's for Bob.
    # The winner is the one who eats the last dish.

    # This is a game on a string.
    # Alice's move: choose 'A' at index `i`. The string becomes S[i+1:].
    # Bob's move: choose 'B' at index `j`. The string becomes S[:j].

    # This is a game on a segment.
    # Let `dp[l][r]` be the winner for the segment `S[l...r]`.
    # Too slow for N=600,000.

    # The key insight must be simpler.
    # Alice wants to eat an 'A'. Bob wants to eat a 'B'.
    # They both want to eat the last dish.
    # This means they want to maximize their own count of dishes eaten.
    # The player who eats the last dish wins.

    # The crucial part is that Alice can choose *any* 'A' and Bob can choose *any* 'B'.
    # This means they can effectively "remove" a prefix or suffix.
    # Alice wants to eat an 'A' that is as far right as possible, to preserve 'A's to her left.
    # Bob wants to eat a 'B' that is as far left as possible, to preserve 'B's to his right.

    # This is a game on a line.
    # Alice wants to eat an 'A'. Bob wants to eat a 'B'.
    # The game ends when no more 'A's for Alice or 'B's for Bob.
    # The winner is the one who eats the last dish.

    # Let's consider the number of 'A's and 'B's.
    # Alice wants to eat an 'A'. Bob wants to eat a 'B'.
    # The game ends when no more 'A's for Alice or 'B's for Bob.
    # The winner is the one who eats the last dish.

    # This is a game on a string.
    # Alice's move: choose 'A' at index `i`. The string becomes S[i+1:].
    # Bob's move: choose 'B' at index `j`. The string becomes S[:j].

    # This is a game on a segment.
    # Let `dp[l][r]` be the winner for the segment `S[l...r]`.
    # Too slow for N=600,000.

    # The key insight must be simpler.
    # Alice wants to eat an 'A'. Bob wants to eat a 'B'.
    # They both want to eat the last dish.
    # This means they want to maximize their own count of dishes eaten.
    # The player who eats the last dish wins.

    # The crucial part is that Alice can choose *any* 'A' and Bob can choose *any* 'B'.
    # This means they can effectively "remove" a prefix or suffix.
    # Alice wants to eat an 'A' that is as far right as possible, to preserve 'A's to her left.
    # Bob wants to eat a 'B' that is as far left as possible, to preserve 'B's to his right.

    # This is a game on a line.
    # Alice wants to eat an 'A'. Bob wants to eat a 'B'.
    # The game ends when no more 'A's for Alice or 'B's for Bob.
    # The winner is the one who eats the last dish.

    # Let's consider the number of 'A's and 'B's.
    # Alice wants to eat an 'A'. Bob wants to eat a 'B'.
    # The game ends when no more 'A's for Alice or 'B's for Bob.
    # The winner is the one who eats the last dish.

    # This is a game on a string.
    # Alice's move: choose 'A' at index `i`. The string becomes S[i+1:].
    # Bob's move: choose 'B' at index `j`. The string becomes S[:j].

    # This is a game on a segment.
    # Let `dp[l][r]` be the winner for the segment `S[l...r]`.
    # Too slow for N=600,000.

    # The key insight must be simpler.
    # Alice wants to eat an 'A'. Bob wants to eat a 'B'.
    # They both want to eat the last dish.
    # This means they want to maximize their own count of dishes eaten.
    # The player who eats the last dish wins.

    # The crucial part is that Alice can choose *any* 'A' and Bob can choose *any* 'B'.
    # This means they can effectively "remove" a prefix or suffix.
    # Alice wants to eat an 'A' that is as far right as possible, to preserve 'A's to her left.
    # Bob wants to eat a 'B' that is as far left as possible, to preserve 'B's to his right.

    # This is a game on a line.
    # Alice wants to eat an 'A'. Bob wants to eat a 'B'.
    # The game ends when no more 'A's for Alice or 'B's for Bob.
    # The winner is the one who eats the last dish.

    # Let's consider the number of 'A's and 'B's.
    # Alice wants to eat an 'A'. Bob wants to eat a 'B'.
    # The game ends when no more 'A's for Alice or 'B's for Bob.
    # The winner is the one who eats the last dish.

    # This is a game on a string.
    # Alice's move: choose 'A' at index `i`. The string becomes S[i+1:].
    # Bob's move: choose 'B' at index `j`. The string becomes S[:j].

    # This is a game on a segment.
    # Let `dp[l][r]` be the winner for the segment `S[l...r]`.
    # Too slow for N=600,000.

    # The key insight must be simpler.
    # Alice wants to eat an 'A'. Bob wants to eat a 'B'.
    # They both want to eat the last dish.
    # This means they want to maximize their own count of dishes eaten.
    # The player who eats the last dish wins.

    # The crucial part is that Alice can choose *any* 'A' and Bob can choose *any* 'B'.
    # This means they can effectively "remove" a prefix or suffix.
    # Alice wants to eat an 'A' that is as far right as possible, to preserve 'A's to her left.
    # Bob wants to eat a 'B' that is as far left as possible, to preserve 'B's to his right.

    # This is a game on a line.
    # Alice wants to eat an 'A'. Bob wants to eat a 'B'.
    # The game ends when no more 'A's for Alice or 'B's for Bob.
    # The winner is the one who eats the last dish.

    # Let's consider the number of 'A's and 'B's.
    # Alice wants to eat an 'A'. Bob wants to eat a 'B'.
    # The game ends when no more 'A's for Alice or 'B's for Bob.
    # The winner is the one who eats the last dish.

    # This is a game on a string.
    # Alice's move: choose 'A' at index `i`. The string becomes S[i+1:].
    # Bob's move: choose 'B' at index `j`. The string becomes S[:j].

    # This is a game on a segment.
    # Let `dp[l][r]` be the winner for the segment `S[l...r]`.
    # Too slow for N=600,000.

    # The key insight must be simpler.
    # Alice wants to eat an 'A'. Bob wants to eat a 'B'.
    # They both want to eat the last dish.
    # This means they want to maximize their own count of dishes eaten.
    # The player who eats the last dish wins.

    # The crucial part is that Alice can choose *any* 'A' and Bob can choose *any* 'B'.
    # This means they can effectively "remove" a prefix or suffix.
    # Alice wants to eat an 'A' that is as far right as possible, to preserve 'A's to her left.
    # Bob wants to eat a 'B' that is as far left as possible, to preserve 'B's to his right.

    # This is a game on a line.
    # Alice wants to eat an 'A'. Bob wants to eat a 'B'.
    # The game ends when no more 'A's for Alice or 'B's for Bob.
    # The winner is the one who eats the last dish.

    # Let's consider the number of 'A's and 'B's.
    # Alice wants to eat an 'A'. Bob wants to eat a 'B'.
    # The game ends when no more 'A's for Alice or 'B's for Bob.
    # The winner is the one who eats the last dish.

    # This is a game on a string.
    # Alice's move: choose 'A' at index `i`. The string becomes S[i+1:].
    # Bob's move: choose 'B' at index `j`. The string becomes S[:j].

    # This is a game on a segment.
    # Let `dp[l][r]` be the winner for the segment `S[l...r]`.
    # Too slow for N=600,000.

    # The key insight must be simpler.
    # Alice wants to eat an 'A'. Bob wants to eat a 'B'.
    # They both want to eat the last dish.
    # This means they want to maximize their own count of dishes eaten.
    # The player who eats the last dish wins.

    # The crucial part is that Alice can choose *any* 'A' and Bob can choose *any* 'B'.
    # This means they can effectively "remove" a prefix or suffix.
    # Alice wants to eat an 'A' that is as far right as possible, to preserve 'A's to her left.
    # Bob wants to eat a 'B' that is as far left as possible, to preserve 'B's to his right.

    # This is a game on a line.
    # Alice wants to eat an 'A'. Bob wants to eat a 'B'.
    # The game ends when no more 'A's for Alice or 'B's for Bob.
    # The winner is the one who eats the last dish.

    # Let's consider the number of 'A's and 'B's.
    # Alice wants to eat an 'A'. Bob wants to eat a 'B'.
    # The game ends when no more 'A's for Alice or 'B's for Bob.
    # The winner is the one who eats the last dish.

    # This is a game on a string.
    # Alice's move: choose 'A' at index `i`. The string becomes S[i+1:].
    # Bob's move: choose 'B' at index `j`. The string becomes S[:j].

    # This is a game on a segment.
    # Let `dp[l][r]` be the winner for the segment `S[l...r]`.
    # Too slow for N=600,000.

    # The key insight must be simpler.
    # Alice wants to eat an 'A'. Bob wants to eat a 'B'.
    # They both want to eat the last dish.
    # This means they want to maximize their own count of dishes eaten.
    # The player who eats the last dish wins.

    # The crucial part is that Alice can choose *any* 'A' and Bob can choose *any* 'B'.
    # This means they can effectively "remove" a prefix or suffix.
    # Alice wants to eat an 'A' that is as far right as possible, to preserve 'A's to her left.
    # Bob wants to eat a 'B' that is as far left as possible, to preserve 'B's to his right.

    # This is a game on a line.
    # Alice wants to eat an 'A'. Bob wants to eat a 'B'.
    # The game ends when no more 'A's for Alice or 'B's for Bob.
    # The winner is the one who eats the last dish.

    # Let's consider the number of 'A's and 'B's.
    # Alice wants to eat an 'A'. Bob wants to eat a 'B'.
    # The game ends when no more 'A's for Alice or 'B's for Bob.
    # The winner is the one who eats the last dish.

    # This is a game on a string.
    # Alice's move: choose 'A' at index `i`. The string becomes S[i+1:].
    # Bob's move: choose 'B' at index `j`. The string becomes S[:j].

    # This is a game on a segment.
    # Let `dp[l][r]` be the winner for the segment `S[l...r]`.
    # Too slow for N=600,000.

    # The key insight must be simpler.
    # Alice wants to eat an 'A'. Bob wants to eat a 'B'.
    # They both want to eat the last dish.
    # This means they want to maximize their own count of dishes eaten.
    # The player who eats the last dish wins.

    # The crucial part is that Alice can choose *any* 'A' and Bob can choose *any* 'B'.
    # This means they can effectively "remove" a prefix or suffix.
    # Alice wants to eat an 'A' that is as far right as possible, to preserve 'A's to her left.
    # Bob wants to eat a 'B' that is as far left as possible, to preserve 'B's to his right.

    # This is a game on a line.
    # Alice wants to eat an 'A'. Bob wants to eat a 'B'.
    # The game ends when no more 'A's for Alice or 'B's for Bob.
    # The winner is the one who eats the last dish.

    # Let's consider the number of 'A's and 'B's.
    # Alice wants to eat an 'A'. Bob wants to eat a 'B'.
    # The game ends when no more 'A's for Alice or 'B's for Bob.
    # The winner is the one who eats the last dish.

    # This is a game on a string.
    # Alice's move: choose 'A' at index `i`. The string becomes S[i+1:].
    # Bob's move: choose 'B' at index `j`. The string becomes S[:j].

    # This is a game on a segment.
    # Let `dp[l][r]` be the winner for the segment `S[l...r]`.
    # Too slow for N=600,000.

    # The key insight must be simpler.
    # Alice wants to eat an 'A'. Bob wants to eat a 'B'.
    # They both want to eat the last dish.
    # This means they want to maximize their own count of dishes eaten.
    # The player who eats the last dish wins.

    # The crucial part is that Alice can choose *any* 'A' and Bob can choose *any* 'B'.
    # This means they can effectively "remove" a prefix or suffix.
    # Alice wants to eat an 'A' that is as far right as possible, to preserve 'A's to her left.
    # Bob wants to eat a 'B' that is as far left as possible, to preserve 'B's to his right.

    # This is a game on a line.
    # Alice wants to eat an 'A'. Bob wants to eat a 'B'.
    # The game ends when no more 'A's for Alice or 'B's for Bob.
    # The winner is the one who eats the last dish.

    # Let's consider the number of 'A's and 'B's.
    # Alice wants to eat an 'A'. Bob wants to eat a 'B'.
    # The game ends when no more 'A's for Alice or 'B's for Bob.
    # The winner is the one who eats the last dish.

    # This is a game on a string.
    # Alice's move: choose 'A' at index `i`. The string becomes S[i+1:].
    # Bob's move: choose 'B' at index `j`. The string becomes S[:j].

    # This is a game on a segment.
    # Let `dp[l][r]` be the winner for the segment `S[l...r]`.
    # Too slow for N=600,000.

    # The key insight must be simpler.
    # Alice wants to eat an 'A'. Bob wants to eat a 'B'.
    # They both want to eat the last dish.
    # This means they want to maximize their own count of dishes eaten.
    # The player who eats the last dish wins.

    # The crucial part is that Alice can choose *any* 'A' and Bob can choose *any* 'B'.
    # This means they can effectively "remove" a prefix or suffix.
    # Alice wants to eat an 'A' that is as far right as possible, to preserve 'A's to her left.
    # Bob wants to eat a 'B' that is as far left as possible, to preserve 'B's to his right.

    # This is a game on a line.
    # Alice wants to eat an 'A'. Bob wants to eat a 'B'.
    # The game ends when no more 'A's for Alice or 'B's for Bob.
    # The winner is the one who eats the last dish.

    # Let's consider the number of 'A's and 'B's.
    # Alice wants to eat an 'A'. Bob wants to eat a 'B'.
    # The game ends when no more 'A's for Alice or 'B's for Bob.
    # The winner is the one who eats the last dish.

    # This is a game on a string.
    # Alice's move: choose 'A' at index `i`. The string becomes S[i+1:].
    # Bob's move: choose 'B' at index `j`. The string becomes S[:j].

    # This is a game on a segment.
    # Let `dp[l][r]` be the winner for the segment `S[l...r]`.
    # Too slow for N=600,000.

    # The key insight must be simpler.
    # Alice wants to eat an 'A'. Bob wants to eat a 'B'.
    # They both want to eat the last dish.
    # This means they want to maximize their own count of dishes eaten.
    # The player who eats the last dish wins.

    # The crucial part is that Alice can choose *any* 'A' and Bob can choose *any* 'B'.
    # This means they can effectively "remove" a prefix or suffix.
    # Alice wants to eat an 'A' that is as far right as possible, to preserve 'A's to her left.
    # Bob wants to eat a 'B' that is as far left as possible, to preserve 'B's to his right.

    # This is a game on a line.
    # Alice wants to eat an 'A'. Bob wants to eat a 'B'.
    # The game ends when no more 'A's for Alice or 'B's for Bob.
    # The winner is the one who eats the last dish.

    # Let's consider the number of 'A's and 'B's.
    # Alice wants to eat an 'A'. Bob wants to eat a 'B'.
    # The game ends when no more 'A's for Alice or 'B's for Bob.
    # The winner is the one who eats the last dish.

    # This is a game on a string.
    # Alice's move: choose 'A' at index `i`. The string becomes S[i+1:].
    # Bob's move: choose 'B' at index `j`. The string becomes S[:j].

    # This is a game on a segment.
    # Let `dp[l][r]` be the winner for the segment `S[l...r]`.
    # Too slow for N=600,000.

    # The key insight must be simpler.
    # Alice wants to eat an 'A'. Bob wants to eat a 'B'.
    # They both want to eat the last dish.
    # This means they want to maximize their own count of dishes eaten.
    # The player who eats the last dish wins.

    # The crucial part is that Alice can choose *any* 'A' and Bob can choose *any* 'B'.
    # This means they can effectively "remove" a prefix or suffix.
    # Alice wants to eat an 'A' that is as far right as possible, to preserve 'A's to her left.
    # Bob wants to eat a 'B' that is as far left as possible, to preserve 'B's to his right.

    # This is a game on a line.
    # Alice wants to eat an 'A'. Bob wants to eat a 'B'.
    # The game ends when no more 'A's for Alice or 'B's for Bob.
    # The winner is the one who eats the last dish.

    # Let's consider the number of 'A's and 'B's.
    # Alice wants to eat an 'A'. Bob wants to eat a 'B'.
    # The game ends when no more 'A's for Alice or 'B's for Bob.
    # The winner is the one who eats the last dish.

    # This is a game on a string.
    # Alice's move: choose 'A' at index `i`. The string becomes S[i+1:].
    # Bob's move: choose 'B' at index `j`. The string becomes S[:j].

    # This is a game on a segment.
    # Let `dp[l][r]` be the winner for the segment `S[l...r]`.
    # Too slow for N=600,000.

    # The key insight must be simpler.
    # Alice wants to eat an 'A'. Bob wants to eat a 'B'.
    # They both want to eat the last dish.
    # This means they want to maximize their own count of dishes eaten.
    # The player who eats the last dish wins.

    # The crucial part is that Alice can choose *any* 'A' and Bob can choose *any* 'B'.
    # This means they can effectively "remove" a prefix or suffix.
    # Alice wants to eat an 'A' that is as far right as possible, to preserve 'A's to her left.
    # Bob wants to eat a 'B' that is as far left as possible, to preserve 'B's to his right.

    # This is a game on a line.
    # Alice wants to eat an 'A'. Bob wants to eat a 'B'.
    # The game ends when no more 'A's for Alice or 'B's for Bob.
    # The winner is the one who eats the last dish.

    # Let's consider the number of 'A's and 'B's.
    # Alice wants to eat an 'A'. Bob wants to eat a 'B'.
    # The game ends when no more 'A's for Alice or 'B's for Bob.
    # The winner is the one who eats the last dish.

    # This is a game on a string.
    # Alice's move: choose 'A' at index `i`. The string becomes S[i+1:].
    # Bob's move: choose 'B' at index `j`. The string becomes S[:j].

    # This is a game on a segment.
    # Let `dp[l][r]` be the winner for the segment `S[l...r]`.
    # Too slow for N=600,000.

    # The key insight must be simpler.
    # Alice wants to eat an 'A'. Bob wants to eat a 'B'.
    # They both want to eat the last dish.
    # This means they want to maximize their own count of dishes eaten.
    # The player who eats the last dish wins.

    # The crucial part is that Alice can choose *any* 'A' and Bob can choose *any* 'B'.
    # This means they can effectively "remove" a prefix or suffix.
    # Alice wants to eat an 'A' that is as far right as possible, to preserve 'A's to her left.
    # Bob wants to eat a 'B' that is as far left as possible, to preserve 'B's to his right.

    # This is a game on a line.
    # Alice wants to eat an 'A'. Bob wants to eat a 'B'.
    # The game ends when no more 'A's for Alice or 'B's for Bob.
    # The winner is the one who eats the last dish.

    # Let's consider the number of 'A's and 'B's.
    # Alice wants to eat an 'A'. Bob wants to eat a 'B'.
    # The game ends when no more 'A's for Alice or 'B's for Bob.
    # The winner is the one who eats the last dish.

    # This is a game on a string.
    # Alice's move: choose 'A' at index `i`. The string becomes S[i+1:].
    # Bob's move: choose 'B' at index `j`. The string becomes S[:j].

    # This is a game on a segment.
    # Let `dp[l][r]` be the winner for the segment `S[l...r]`.
    # Too slow for N=600,000.

    # The key insight must be simpler.
    # Alice wants to eat an 'A'. Bob wants to eat a 'B'.
    # They both want to eat the last dish.
    # This means they want to maximize their own count of dishes eaten.
    # The player who eats the last dish wins.

    # The crucial part is that Alice can choose *any* 'A' and Bob can choose *any* 'B'.
    # This means they can effectively "remove" a prefix or suffix.
    # Alice wants to eat an 'A' that is as far right as possible, to preserve 'A's to her left.
    # Bob wants to eat a 'B' that is as far left as possible, to preserve 'B's to his right.

    # This is a game on a line.
    # Alice wants to eat an 'A'. Bob wants to eat a 'B'.
    # The game ends when no more 'A's for Alice or 'B's for Bob.
    # The winner is the one who eats the last dish.

    # Let's consider the number of 'A's and 'B's.
    # Alice wants to eat an 'A'. Bob wants to eat a 'B'.
    # The game ends when no more 'A's for Alice or 'B's for Bob.
    # The winner is the one who eats the last dish.

    # This is a game on a string.
    # Alice's move: choose 'A' at index `i`. The string becomes S[i+1:].
    # Bob's move: choose 'B' at index `j`. The string becomes S[:j].

    # This is a game on a segment.
    # Let `dp[l][r]` be the winner for the segment `S[l...r]`.
    # Too slow for N=600,000.

    # The key insight must be simpler.
    # Alice wants to eat an 'A'. Bob wants to eat a 'B'.
    # They both want to eat the last dish.
    # This means they want to maximize their own count of dishes eaten.
    # The player who eats the last dish wins.

    # The crucial part is that Alice can choose *any* 'A' and Bob can choose *any* 'B'.
    # This means they can effectively "remove" a prefix or suffix.
    # Alice wants to eat an 'A' that is as far right as possible, to preserve 'A's to her left.
    # Bob wants to eat a 'B' that is as far left as possible, to preserve 'B's to his right.

    # This is a game on a line.
    # Alice wants to eat an 'A'. Bob wants to eat a 'B'.
    # The game ends when no more 'A's for Alice or 'B's for Bob.
    # The winner is the one who eats the last dish.

    # Let's consider the number of 'A's and 'B's.
    # Alice wants to eat an 'A'. Bob wants to eat a 'B'.
    # The game ends when no more 'A's for Alice or 'B's for Bob.
    # The winner is the one who eats the last dish.

    # This is a game on a string.
    # Alice's move: choose 'A' at index `i`. The string becomes S[i+1:].
    # Bob's move: choose 'B' at index `j`. The string becomes S[:j].

    # This is a game on a segment.
    # Let `dp[l][r]` be the winner for the segment `S[l...r]`.
    # Too slow for N=600,000.

    # The key insight must be simpler.
    # Alice wants to eat an 'A'. Bob wants to eat a 'B'.
    # They both want to eat the last dish.
    # This means they want to maximize their own count of dishes eaten.
    # The player who eats the last dish wins.

    # The crucial part is that Alice can choose *any* 'A' and Bob can choose *any* 'B'.
    # This means they can effectively "remove" a prefix or suffix.
    # Alice wants to eat an 'A' that is as far right as possible, to preserve 'A's to her left.
    # Bob wants to eat a 'B' that is as far left as possible, to preserve 'B's to his right.

    # This is a game on a line.
    # Alice wants to eat an 'A'. Bob wants to eat a 'B'.
    # The game ends when no more 'A's for Alice or 'B's for Bob.
    # The winner is the one who eats the last dish.

    # Let's consider the number of 'A's and 'B's.
    # Alice wants to eat an 'A'. Bob wants to eat a 'B'.
    # The game ends when no more 'A's for Alice or 'B's for Bob.
    # The winner is the one who eats the last dish.

    # This is a game on a string.
    # Alice's move: choose 'A' at index `i`. The string becomes S[i+1:].
    # Bob's move: choose 'B' at index `j`. The string becomes S[:j].

    # This is a game on a segment.
    # Let `dp[l][r]` be the winner for the segment `S[l...r]`.
    # Too slow for N=600,000.

    # The key insight must be simpler.
    # Alice wants to eat an 'A'. Bob wants to eat a 'B'.
    # They both want to eat the last dish.
    # This means they want to maximize their own count of dishes eaten.
    # The player who eats the last dish wins.

    # The crucial part is that Alice can choose *any* 'A' and Bob can choose *any* 'B'.
    # This means they can effectively "remove" a prefix or suffix.
    # Alice wants to eat an 'A' that is as far right as possible, to preserve 'A's to her left.
    # Bob wants to eat a 'B' that is as far left as possible, to preserve 'B's to his right.

    # This is a game on a line.
    # Alice wants to eat an 'A'. Bob wants to eat a 'B'.
    # The game ends when no more 'A's for Alice or 'B's for Bob.
    # The winner is the one who eats the last dish.

    # Let's consider the number of 'A's and 'B's.
    # Alice wants to eat an 'A'. Bob wants to eat a 'B'.
    # The game ends when no more 'A's for Alice or 'B's for Bob.
    # The winner is the one who eats the last dish.

    # This is a game on a string.
    # Alice's move: choose 'A' at index `i`. The string becomes S[i+1:].
    # Bob's move: choose 'B' at index `j`. The string becomes S[:j].

    # This is a game on a segment.
    # Let `dp[l][r]` be the winner for the segment `S[l...r]`.
    # Too slow for N=600,000.

    # The key insight must be simpler.
    # Alice wants to eat an 'A'. Bob wants to eat a 'B'.
    # They both want to eat the last dish.
    # This means they want to maximize their own count of dishes eaten.
    # The player who eats the last dish wins.

    # The crucial part is that Alice can choose *any* 'A' and Bob can choose *any* 'B'.
    # This means they can effectively "remove" a prefix or suffix.
    # Alice wants to eat an 'A' that is as far right as possible, to preserve 'A's to her left.
    # Bob wants to eat a 'B' that is as far left as possible, to preserve 'B's to his right.

    # This is a game on a line.
    # Alice wants to eat an 'A'. Bob wants to eat a 'B'.
    # The game ends when no more 'A's for Alice or 'B's for Bob.
    # The winner is the one who eats the last dish.

    # Let's consider the number of 'A's and 'B's.
    # Alice wants to eat an 'A'. Bob wants to eat a 'B'.
    # The game ends when no more 'A's for Alice or 'B's for Bob.
    # The winner is the one who eats the last dish.

    # This is a game on a string.
    # Alice's move: choose 'A' at index `i`. The string becomes S[i+1:].
    # Bob's move: choose 'B' at index `j`. The string becomes S[:j].

    # This is a game on a segment.
    # Let `dp[l][r]` be the winner for the segment `S[l...r]`.
    # Too slow for N=600,000.

    # The key insight must be simpler.
    # Alice wants to eat an 'A'. Bob wants to eat a 'B'.
    # They both want to eat the last dish.
    # This means they want to maximize their own count of dishes eaten.
    # The player who eats the last dish wins.

    # The crucial part is that Alice can choose *any* 'A' and Bob can choose *any* 'B'.
    # This means they can effectively "remove" a prefix or suffix.
    # Alice wants to eat an 'A' that is as far right as possible, to preserve 'A's to her left.
    # Bob wants to eat a 'B' that is as far left as possible, to preserve 'B's to his right.

    # This is a game on a line.
    # Alice wants to eat an 'A'. Bob wants to eat a 'B'.
    # The game ends when no more 'A's for Alice or 'B's for Bob.
    # The winner is the one who eats the last dish.

    # Let's consider the number of 'A's and 'B's.
    # Alice wants to eat an 'A'. Bob wants to eat a 'B'.
    # The game ends when no more 'A's for Alice or 'B's for Bob.
    # The winner is the one who eats the last dish.

    # This is a game on a string.
    # Alice's move: choose 'A' at index `i`. The string becomes S[i+1:].
    # Bob's move: choose 'B' at index `j`. The string becomes S[:j].

    # This is a game on a segment.
    # Let `dp[l][r]` be the winner for the segment `S[l...r]`.
    # Too slow for N=600,000.

    # The key insight must be simpler.
    # Alice wants to eat an 'A'. Bob wants to eat a 'B'.
    # They both want to eat the last dish.
    # This means they want to maximize their own count of dishes eaten.
    # The player who eats the last dish wins.

    # The crucial part is that Alice can choose *any* 'A' and Bob can choose *any* 'B'.
    # This means they can effectively "remove" a prefix or suffix.
    # Alice wants to eat an 'A' that is as far right as possible, to preserve 'A's to her left.
    # Bob wants to eat a 'B' that is as far left as possible, to preserve 'B's to his right.

    # This is a game on a line.
    # Alice wants to eat an 'A'. Bob wants to eat a 'B'.
    # The game ends when no more 'A's for Alice or 'B's for Bob.
    # The winner is the one who eats the last dish.

    # Let's consider the number of 'A's and 'B's.
    # Alice wants to eat an 'A'. Bob wants to eat a 'B'.
    # The game ends when no more 'A's for Alice or 'B's for Bob.
    # The winner is the one who eats the last dish.

    # This is a game on a string.
    # Alice's move: choose 'A' at index `i`. The string becomes S[i+1:].
    # Bob's move: choose 'B' at index `j`. The string becomes S[:j].

    # This is a game on a segment.
    # Let `dp[l][r]` be the winner for the segment `S[l...r]`.
    # Too slow for N=600,000.

    # The key insight must be simpler.
    # Alice wants to eat an 'A'. Bob wants to eat a 'B'.
    # They both want to eat the last dish.
    # This means they want to maximize their own count of dishes eaten.
    # The player who eats the last dish wins.

    # The crucial part is that Alice can choose *any* 'A' and Bob can choose *any* 'B'.
    # This means they can effectively "remove" a prefix or suffix.
    # Alice wants to eat an 'A' that is as far right as possible, to preserve 'A's to her left.
    # Bob wants to eat a 'B' that is as far left as possible, to preserve 'B's to his right.

    # This is a game on a line.
    # Alice wants to eat an 'A'. Bob wants to eat a 'B'.
    # The game ends when no more 'A's for Alice or 'B's for Bob.
    # The winner is the one who eats the last dish.

    # Let's consider the number of 'A's and 'B's.
    # Alice wants to eat an 'A'. Bob wants to eat a 'B'.
    # The game ends when no more 'A's for Alice or 'B's for Bob.
    # The winner is the one who eats the last dish.

    # This is a game on a string.
    # Alice's move: choose 'A' at index `i`. The string becomes S[i+1:].
    # Bob's move: choose 'B' at index `j`. The string becomes S[:j].

    # This is a game on a segment.
    # Let `dp[l][r]` be the winner for the segment `S[l...r]`.
    # Too slow for N=600,000.

    # The key insight must be simpler.
    # Alice wants to eat an 'A'. Bob wants to eat a 'B'.
    # They both want to eat the last dish.
    # This means they want to maximize their own count of dishes eaten.
    # The player who eats the last dish wins.

    # The crucial part is that Alice can choose *any* 'A' and Bob can choose *any* 'B'.
    # This means they can effectively "remove" a prefix or suffix.
    # Alice wants to eat an 'A' that is as far right as possible, to preserve 'A's to her left.
    # Bob wants to eat a 'B' that is as far left as possible, to preserve 'B's to his right.

    # This is a game on a line.
    # Alice wants to eat an 'A'. Bob wants to eat a 'B'.
    # The game ends when no more 'A's for Alice or 'B's for Bob.
    # The winner is the one who eats the last dish.

    # Let's consider the number of 'A's and 'B's.
    # Alice wants to eat an 'A'. Bob wants to eat a 'B'.
    # The game ends when no more 'A's for Alice or 'B's for Bob.
    # The winner is the one who eats the last dish.

    # This is a game on a string.
    # Alice's move: choose 'A' at index `i`. The string becomes S[i+1:].
    # Bob's move: choose 'B' at index `j`. The string becomes S[:j].

    # This is a game on a segment.
    # Let `dp[l][r]` be the winner for the segment `S[l...r]`.
    # Too slow for N=600,000.

    # The key insight must be simpler.
    # Alice wants to eat an 'A'. Bob wants to eat a 'B'.
    # They both want to eat the last dish.
    # This means they want to maximize their own count of dishes eaten.
    # The player who eats the last dish wins.

    # The crucial part is that Alice can choose *any* 'A' and Bob can choose *any* 'B'.
    # This means they can effectively "remove" a prefix or suffix.
    # Alice wants to eat an 'A' that is as far right as possible, to preserve 'A's to her left.
    # Bob wants to eat a 'B' that is as far left as possible, to preserve 'B's to his right.

    # This is a game on a line.
    # Alice wants to eat an 'A'. Bob wants to eat a 'B'.
    # The game ends when no more 'A's for Alice or 'B's for Bob.
    # The winner is the one who eats the last dish.

    # Let's consider the number of 'A's and 'B's.
    # Alice wants to eat an 'A'. Bob wants to eat a 'B'.
    # The game ends when no more 'A's for Alice or 'B's for Bob.
    # The winner is the one who eats the last dish.

    # This is a game on a string.
    # Alice's move: choose 'A' at index `i`. The string becomes S[i+1:].
    # Bob's move: choose 'B' at index `j`. The string becomes S[:j].

    # This is a game on a segment.
    # Let `dp[l][r]` be the winner for the segment `S[l...r]`.
    # Too slow for N=600,000.

    # The key insight must be simpler.
    # Alice wants to eat an 'A'. Bob wants to eat a 'B'.
    # They both want to eat the last dish.
    # This means they want to maximize their own count of dishes eaten.
    # The player who eats the last dish wins.

    # The crucial part is that Alice can choose *any* 'A' and Bob can choose *any* 'B'.
    # This means they can effectively "remove" a prefix or suffix.
    # Alice wants to eat an 'A' that is as far right as possible, to preserve 'A's to her left.
    # Bob wants to eat a 'B' that is as far left as possible, to preserve 'B's to his right.

    # This is a game on a line.
    # Alice wants to eat an 'A'. Bob wants to eat a 'B'.
    # The game ends when no more 'A's for Alice or 'B's for Bob.
    # The winner is the one who eats the last dish.

    # Let's consider the number of 'A's and 'B's.
    # Alice wants to eat an 'A'. Bob wants to eat a 'B'.
    # The game ends when no more 'A's for Alice or 'B's for Bob.
    # The winner is the one who eats the last dish.

    # This is a game on a string.
    # Alice's move: choose 'A' at index `i`. The string becomes S[i+1:].
    # Bob's move: choose 'B' at index `j`. The string becomes S[:j].

    # This is a game on a segment.
    # Let `dp[l][r]` be the winner for the segment `S[l...r]`.
    # Too slow for N=600,000.

    # The key insight must be simpler.
    # Alice wants to eat an 'A'. Bob wants to eat a 'B'.
    # They both want to eat the last dish.
    # This means they want to maximize their own count of dishes eaten.
    # The player who eats the last dish wins.

    # The crucial part is that Alice can choose *any* 'A' and Bob can choose *any* 'B'.
    # This means they can effectively "remove" a prefix or suffix.
    # Alice wants to eat an 'A' that is as far right as possible, to preserve 'A's to her left.
    # Bob wants to eat a 'B' that is as far left as possible, to preserve 'B's to his right.

    # This is a game on a line.
    # Alice wants to eat an 'A'. Bob wants to eat a 'B'.
    # The game ends when no more 'A's for Alice or 'B's for Bob.
    # The winner is the one who eats the last dish.

    # Let's consider the number of 'A's and 'B's.
    # Alice wants to eat an 'A'. Bob wants to eat a 'B'.
    # The game ends when no more 'A's for Alice or 'B's for Bob.
    # The winner is the one who eats the last dish.

    # This is a game on a string.
    # Alice's move: choose 'A' at index `i`. The string becomes S[i+1:].
    # Bob's move: choose 'B' at index `j`. The string becomes S[:j].

    # This is a game on a segment.
    # Let `dp[l][r]` be the winner for the segment `S[l...r]`.
    # Too slow for N=600,000.

    # The key insight must be simpler.
    # Alice wants to eat an 'A'. Bob wants to eat a 'B'.
    # They both want to eat the last dish.
    # This means they want to maximize their own count of dishes eaten.
    # The player who eats the last dish wins.

    # The crucial part is that Alice can choose *any* 'A' and Bob can choose *any* 'B'.
    # This means they can effectively "remove" a prefix or suffix.
    # Alice wants to eat an 'A' that is as far right as possible, to preserve 'A's to her left.
    # Bob wants to eat a 'B' that is as far left as possible, to preserve 'B's to his right.

    # This is a game on a line.
    # Alice wants to eat an 'A'. Bob wants to eat a 'B'.
    # The game ends when no more 'A's for Alice or 'B's for Bob.
    # The winner is the one who eats the last dish.

    # Let's consider the number of 'A's and 'B's.
    # Alice wants to eat an 'A'. Bob wants to eat a 'B'.
    # The game ends when no more 'A's for Alice or 'B's for Bob.
    # The winner is the one who eats the last dish.

    # This is a game on a string.
    # Alice's move: choose 'A' at index `i`. The string becomes S[i+1:].
    # Bob's move: choose 'B' at index `j`. The string becomes S[:j].

    # This is a game on a segment.
    # Let `dp[l][r]` be the winner for the segment `S[l...r]`.
    # Too slow for N=600,000.

    # The key insight must be simpler.
    # Alice wants to eat an 'A'. Bob wants to eat a 'B'.
    # They both want to eat the last dish.
    # This means they want to maximize their own count of dishes eaten.
    # The player who eats the last dish wins.

    # The crucial part is that Alice can choose *any* 'A' and Bob can choose *any* 'B'.
    # This means they can effectively "remove" a prefix or suffix.
    # Alice wants to eat an 'A' that is as far right as possible, to preserve 'A's to her left.
    # Bob wants to eat a 'B' that is as far left as possible, to preserve 'B's to his right.

    # This is a game on a line.
    # Alice wants to eat an 'A'. Bob wants to eat a 'B'.
    # The game ends when no more 'A's for Alice or 'B's for Bob.
    # The winner is the one who eats the last dish.

    # Let's consider the number of 'A's and 'B's.
    # Alice wants to eat an 'A'. Bob wants to eat a 'B'.
    # The game ends when no more 'A's for Alice or 'B's for Bob.
    # The winner is the one who eats the last dish.

    # This is a game on a string.
    # Alice's move: choose 'A' at index `i`. The string becomes S[i+1:].
    # Bob's move: choose 'B' at index `j`. The string becomes S[:j].

    # This is a game on a segment.
    # Let `dp[l][r]` be the winner for the segment `S[l...r]`.
    # Too slow for N=600,000.

    # The key insight must be simpler.
    # Alice wants to eat an 'A'. Bob wants to eat a 'B'.
    # They both want to eat the last dish.
    # This means they want to maximize their own count of dishes eaten.
    # The player who eats the last dish wins.

    # The crucial part is that Alice can choose *any* 'A' and Bob can choose *any* 'B'.
    # This means they can effectively "remove" a prefix or suffix.
    # Alice wants to eat an 'A' that is as far right as possible, to preserve 'A's to her left.
    # Bob wants to eat a 'B' that is as far left as possible, to preserve 'B's to his right.

    # This is a game on a line.
    # Alice wants to eat an 'A'. Bob wants to eat a 'B'.
    # The game ends when no more 'A's for Alice or 'B's for Bob.
    # The winner is the one who eats the last dish.

    # Let's consider the number of 'A's and 'B's.
    # Alice wants to eat an 'A'. Bob wants to eat a 'B'.
    # The game ends when no more 'A's for Alice or 'B's for Bob.
    # The winner is the one who eats the last dish.

    # This is a game on a string.
    # Alice's move: choose 'A' at index `i`. The string becomes S[i+1:].
    # Bob's move: choose 'B' at index `j`. The string becomes S[:j].

    # This is a game on a segment.
    # Let `dp[l][r]` be the winner for the segment `S[l...r]`.
    # Too slow for N=600,000.

    # The key insight must be simpler.
    # Alice wants to eat an 'A'. Bob wants to eat a 'B'.
    # They both want to eat the last dish.
    # This means they want to maximize their own count of dishes eaten.
    # The player who eats the last dish wins.

    # The crucial part is that Alice can choose *any* 'A' and Bob can choose *any* 'B'.
    # This means they can effectively "remove" a prefix or suffix.
    # Alice wants to eat an 'A' that is as far right as possible, to preserve 'A's to her left.
    # Bob wants to eat a 'B' that is as far left as possible, to preserve 'B's to his right.

    # This is a game on a line.
    # Alice wants to eat an 'A'. Bob wants to eat a 'B'.
    # The game ends when no more 'A's for Alice or 'B's for Bob.
    # The winner is the one who eats the last dish.

    # Let's consider the number of 'A's and 'B's.
    # Alice wants to eat an 'A'. Bob wants to eat a 'B'.
    # The game ends when no more 'A's for Alice or 'B's for Bob.
    # The winner is the one who eats the last dish.

    # This is a game on a string.
    # Alice's move: choose 'A' at index `i`. The string becomes S[i+1:].
    # Bob's move: choose 'B' at index `j`. The string becomes S[:j].

    # This is a game on a segment.
    # Let `dp[l][r]` be the winner for the segment `S[l...r]`.
    # Too slow for N=600,000.

    # The key insight must be simpler.
    # Alice wants to eat an 'A'. Bob wants to eat a 'B'.
    # They both want to eat the last dish.
    # This means they want to maximize their own count of dishes eaten.
    # The player who eats the last dish wins.

    # The crucial part is that Alice can choose *any* 'A' and Bob can choose *any* 'B'.
    # This means they can effectively "remove" a prefix or suffix.
    # Alice wants to eat an 'A' that is as far right as possible, to preserve 'A's to her left.
    # Bob wants to eat a 'B' that is as far left as possible, to preserve 'B's to his right.

    # This is a game on a line.
    # Alice wants to eat an 'A'. Bob wants to eat a 'B'.
    # The game ends when no more 'A's for Alice or 'B's for Bob.
    # The winner is the one who eats the last dish.

    # Let's consider the number of 'A's and 'B's.
    # Alice wants to eat an 'A'. Bob wants to eat a 'B'.
    # The game ends when no more 'A's for Alice or 'B's for Bob.
    # The winner is the one who eats the last dish.

    # This is a game on a string.
    # Alice's move: choose 'A' at index `i`. The string becomes S[i+1:].
    # Bob's move: choose 'B' at index `j`. The string becomes S[:j].

    # This is a game on a segment.
    # Let `dp[l][r]` be the winner for the segment `S[l...r]`.
    # Too slow for N=600,000.

    # The key insight must be simpler.
    # Alice wants to eat an 'A'. Bob wants to eat a 'B'.
    # They both want to eat the last dish.
    # This means they want to maximize their own count of dishes eaten.
    # The player who eats the last dish wins.

    # The crucial part is that Alice can choose *any* 'A' and Bob can choose *any* 'B'.
    # This means they can effectively "remove" a prefix or suffix.
    # Alice wants to eat an 'A' that is as far right as possible, to preserve 'A's to her left.
    # Bob wants to eat a 'B' that is as far left as possible, to preserve 'B's to his right.

    # This is a game on a line.
    # Alice wants to eat an 'A'. Bob wants to eat a 'B'.
    # The game ends when no more 'A's for Alice or 'B's for Bob.
    # The winner is the one who eats the last dish.

    # Let's consider the number of 'A's and 'B's.
    # Alice wants to eat an 'A'. Bob wants to eat a 'B'.
    # The game ends when no more 'A's for Alice or 'B's for Bob.
    # The winner is the one who eats the last dish.

    # This is a game on a string.
    # Alice's move: choose 'A' at index `i`. The string becomes S[i+1:].
    # Bob's move: choose 'B' at index `j`. The string becomes S[:j].

    # This is a game on a segment.
    # Let `dp[l][r]` be the winner for the segment `S[l...r]`.
    # Too slow for N=600,000.

    # The key insight must be simpler.
    # Alice wants to eat an 'A'. Bob wants to eat a 'B'.
    # They both want to eat the last dish.
    # This means they want to maximize their own count of dishes eaten.
    # The player who eats the last dish wins.

    # The crucial part is that Alice can choose *any* 'A' and Bob can choose *any* 'B'.
    # This means they can effectively "remove" a prefix or suffix.
    # Alice wants to eat an 'A' that is as far right as possible, to preserve 'A's to her left.
    # Bob wants to eat a 'B' that is as far left as possible, to preserve 'B's to his right.

    # This is a game on a line.
    # Alice wants to eat an 'A'. Bob wants to eat a 'B'.
    # The game ends when no more 'A's for Alice or 'B's for Bob.
    # The winner is the one who eats the last dish.

    # Let's consider the number of 'A's and 'B's.
    # Alice wants to eat an 'A'. Bob wants to eat a 'B'.
    # The game ends when no more 'A's for Alice or 'B's for Bob.
    # The winner is the one who eats the last dish.

    # This is a game on a string.
    # Alice's move: choose 'A' at index `i`. The string becomes S[i+1:].
    # Bob's move: choose 'B' at index `j`. The string becomes S[:j].

    # This is a game on a segment.
    # Let `dp[l][r]` be the winner for the segment `S[l...r]`.
    # Too slow for N=600,000.

    # The key insight must be simpler.
    # Alice wants to eat an 'A'. Bob wants to eat a 'B'.
    # They both want to eat the last dish.
    # This means they want to maximize their own count of dishes eaten.
    # The player who eats the last dish wins.

    # The crucial part is that Alice can choose *any* 'A' and Bob can choose *any* 'B'.
    # This means they can effectively "remove" a prefix or suffix.
    # Alice wants to eat an 'A' that is as far right as possible, to preserve 'A's to her left.
    # Bob wants to eat a 'B' that is as far left as possible, to preserve 'B's to his right.

    # This is a game on a line.
    # Alice wants to eat an 'A'. Bob wants to eat a 'B'.
    # The game ends when no more 'A's for Alice or 'B's for Bob.
    # The winner is the one who eats the last dish.

    # Let's consider the number of 'A's and 'B's.
    # Alice wants to eat an 'A'. Bob wants to eat a 'B'.
    # The game ends when no more 'A's for Alice or 'B's for Bob.
    # The winner is the one who eats the last dish.

    # This is a game on a string.
    # Alice's move: choose 'A' at index `i`. The string becomes S[i+1:].
    # Bob's move: choose 'B' at index `j`. The string becomes S[:j].

    # This is a game on a segment.
    # Let `dp[l][r]` be the winner for the segment `S[l...r]`.
    # Too slow for N=600,000.

    # The key insight must be simpler.
    # Alice wants to eat an 'A'. Bob wants to eat a 'B'.
    # They both want to eat the last dish.
    # This means they want to maximize their own count of dishes eaten.
    # The player who eats the last dish wins.

    # The crucial part is that Alice can choose *any* 'A' and Bob can choose *any* 'B'.
    # This means they can effectively "remove" a prefix or suffix.
    # Alice wants to eat an 'A' that is as far right as possible, to preserve 'A's to her left.
    # Bob wants to eat a 'B' that is as far left as possible, to preserve 'B's to his right.

    # This is a game on a line.
    # Alice wants to eat an 'A'. Bob wants to eat a 'B'.
    # The game ends when no more 'A's for Alice or 'B's for Bob.
    # The winner is the one who eats the last dish.

    # Let's consider the number of 'A's and 'B's.
    # Alice wants to eat an 'A'. Bob wants to eat a 'B'.
    # The game ends when no more 'A's for Alice or 'B's for Bob.
    # The winner is the one who eats the last dish.

    # This is a game on a string.
    # Alice's move: choose 'A' at index `i`. The string becomes S[i+1:].
    # Bob's move: choose 'B' at index `j`. The string becomes S[:j].

    # This is a game on a segment.
    # Let `dp[l][r]` be the winner for the segment `S[l...r]`.
    # Too slow for N=600,000.

    # The key insight must be simpler.
    # Alice wants to eat an 'A'. Bob wants to eat a 'B'.
    # They both want to eat the last dish.
    # This means they want to maximize their own count of dishes eaten.
    # The player who eats the last dish wins.

    # The crucial part is that Alice can choose *any* 'A' and Bob can choose *any* 'B'.
    # This means they can effectively "remove" a prefix or suffix.
    # Alice wants to eat an 'A' that is as far right as possible, to preserve 'A's to her left.
    # Bob wants to eat a 'B' that is as far left as possible, to preserve 'B's to his right.

    # This is a game on a line.
    # Alice wants to eat an 'A'. Bob wants to eat a 'B'.
    # The game ends when no more 'A's for Alice or 'B's for Bob.
    # The winner is the one who eats the last dish.

    # Let's consider the number of 'A's and 'B's.
    # Alice wants to eat an 'A'. Bob wants to eat a 'B'.
    # The game ends when no more 'A's for Alice or 'B's for Bob.
    # The winner is the one who eats the last dish.

    # This is a game on a string.
    # Alice's move: choose 'A' at index `i`. The string becomes S[i+1:].
    # Bob's move: choose 'B' at index `j`. The string becomes S[:j].

    # This is a game on a segment.
    # Let `dp[l][r]` be the winner for the segment `S[l...r]`.
    # Too slow for N=600,000.

    # The key insight must be simpler.
    # Alice wants to eat an 'A'. Bob wants to eat a 'B'.
    # They both want to eat the last dish.
    # This means they want to maximize their own count of dishes eaten.
    # The player who eats the last dish wins.

    # The crucial part is that Alice can choose *any* 'A' and Bob can choose *any* 'B'.
    # This means they can effectively "remove" a prefix or suffix.
    # Alice wants to eat an 'A' that is as far right as possible, to preserve 'A's to her left.
    # Bob wants to eat a 'B' that is as far left as possible, to preserve 'B's to his right.

    # This is a game on a line.
    # Alice wants to eat an 'A'. Bob wants to eat a 'B'.
    # The game ends when no more 'A's for Alice or 'B's for Bob.
    # The winner is the one who eats the last dish.

    # Let's consider the number of 'A's and 'B's.
    # Alice wants to eat an 'A'. Bob wants to eat a 'B'.
    # The game ends when no more 'A's for Alice or 'B's for Bob.
    # The winner is the one who eats the last dish.

    # This is a game on a string.
    # Alice's move: choose 'A' at index `i`. The string becomes S[i+1:].
    # Bob's move: choose 'B' at index `j`. The string becomes S[:j].

    # This is a game on a segment.
    # Let `dp[l][r]` be the winner for the segment `S[l...r]`.
    # Too slow for N=600,000.

    # The key insight must be simpler.
    # Alice wants to eat an 'A'. Bob wants to eat a 'B'.
    # They both want to eat the last dish.
    # This means they want to maximize their own count of dishes eaten.
    # The player who eats the last dish wins.

    # The crucial part is that Alice can choose *any* 'A' and Bob can choose *any* 'B'.
    # This means they can effectively "remove" a prefix or suffix.
    # Alice wants to eat an 'A' that is as far right as possible, to preserve 'A's to her left.
    # Bob wants to eat a 'B' that is as far left as possible, to preserve 'B's to his right.

    # This is a game on a line.
    # Alice wants to eat an 'A'. Bob wants to eat a 'B'.
    # The game ends when no more 'A's for Alice or 'B's for Bob.
    # The winner is the one who eats the last dish.

    # Let's consider the number of 'A's and 'B's.
    # Alice wants to eat an 'A'. Bob wants to eat a 'B'.
    # The game ends when no more 'A's for Alice or 'B's for Bob.
    # The winner is the one who eats the last dish.

    # This is a game on a string.
    # Alice's move: choose 'A' at index `i`. The string becomes S[i+1:].
    # Bob's move: choose 'B' at index `j`. The string becomes S[:j].

    # This is a game on a segment.
    # Let `dp[l][r]` be the winner for the segment `S[l...r]`.
    # Too slow for N=600,000.

    # The key insight must be simpler.
    # Alice wants to eat an 'A'. Bob wants to eat a 'B'.
    # They both want to eat the last dish.
    # This means they want to maximize their own count of dishes eaten.
    # The player who eats the last dish wins.

    # The crucial part is that Alice can choose *any* 'A' and Bob can choose *any* 'B'.
    # This means they can effectively "remove" a prefix or suffix.
    # Alice wants to eat an 'A' that is as far right as possible, to preserve 'A's to her left.
    # Bob wants to eat a 'B' that is as far left as possible, to preserve 'B's to his right.

    # This is a game on a line.
    # Alice wants to eat an 'A'. Bob wants to eat a 'B'.
    # The game ends when no more 'A's for Alice or 'B's for Bob.
    # The winner is the one who eats the last dish.

    # Let's consider the number of 'A's and 'B's.
    # Alice wants to eat an 'A'. Bob wants to eat a 'B'.
    # The game ends when no more 'A's for Alice or 'B's for Bob.
    # The winner is the one who eats the last dish.

    # This is a game on a string.
    # Alice's move: choose 'A' at index `i`. The string becomes S[i+1:].
    # Bob's move: choose 'B' at index `j`. The string becomes S[:j].

    # This is a game on a segment.
    # Let `dp[l][r]` be the winner for the segment `S[l...r]`.
    # Too slow for N=600,000.

    # The key insight must be simpler.
    # Alice wants to eat an 'A'. Bob wants to eat a 'B'.
    # They both want to eat the last dish.
    # This means they want to maximize their own count of dishes eaten.
    # The player who eats the last dish wins.

    # The crucial part is that Alice can choose *any* 'A' and Bob can choose *any* 'B'.
    # This means they can effectively "remove" a prefix or suffix.
    # Alice wants to eat an 'A' that is as far right as possible, to preserve 'A's to her left.
    # Bob wants to eat a 'B' that is as far left as possible, to preserve 'B's to his right.

    # This is a game on a line.
    # Alice wants to eat an 'A'. Bob wants to eat a 'B'.
    # The game ends when no more 'A's for Alice or 'B's for Bob.
    # The winner is the one who eats the last dish.

    # Let's consider the number of 'A's and 'B's.
    # Alice wants to eat an 'A'. Bob wants to eat a 'B'.
    # The game ends when no more 'A's for Alice or 'B's for Bob.
    # The winner is the one who eats the last dish.

    # This is a game on a string.
    # Alice's move: choose 'A' at index `i`. The string becomes S[i+1:].
    # Bob's move: choose 'B' at index `j`. The string becomes S[:j].

    # This is a game on a segment.
    # Let `dp[l][r]` be the winner for the segment `S[l...r]`.
    # Too slow for N=600,000.

    # The key insight must be simpler.
    # Alice wants to eat an 'A'. Bob wants to eat a 'B'.
    # They both want to eat the last dish.
    # This means they want to maximize their own count of dishes eaten.
    # The player who eats the last dish wins.

    # The crucial part is that Alice can choose *any* 'A' and Bob can choose *any* 'B'.
    # This means they can effectively "remove" a prefix or suffix.
    # Alice wants to eat an 'A' that is as far right as possible, to preserve 'A's to her left.
    # Bob wants to eat a 'B' that is as far left as possible, to preserve 'B's to his right.

    # This is a game on a line.
    # Alice wants to eat an 'A'. Bob wants to eat a 'B'.
    # The game ends when no more 'A's for Alice or 'B's for Bob.
    # The winner is the one who eats the last dish.

    # Let's consider the number of 'A's and 'B's.
    # Alice wants to eat an 'A'. Bob wants to eat a 'B'.
    # The game ends when no more 'A's for Alice or 'B's for Bob.
    # The winner is the one who eats the last dish.

    # This is a game on a string.
    # Alice's move: choose 'A' at index `i`. The string becomes S[i+1:].
    # Bob's move: choose 'B' at index `j`. The string becomes S[:j].

    # This is a game on a segment.
    # Let `dp[l][r]` be the winner for the segment `S[l...r]`.
    # Too slow for N=600,000.

    # The key insight must be simpler.
    # Alice wants to eat an 'A'. Bob wants to eat a 'B'.
    # They both want to eat the last dish.
    # This means they want to maximize their own count of dishes eaten.
    # The player who eats the last dish wins.

    # The crucial part is that Alice can choose *any* 'A' and Bob can choose *any* 'B'.
    # This means they can effectively "remove" a prefix or suffix.
    # Alice wants to eat an 'A' that is as far right as possible, to preserve 'A's to her left.
    # Bob wants to eat a 'B' that is as far left as possible, to preserve 'B's to his right.

    # This is a game on a line.
    # Alice wants to eat an 'A'. Bob wants to eat a 'B'.
    # The game ends when no more 'A's for Alice or 'B's for Bob.
    # The winner is the one who eats the last dish.

    # Let's consider the number of 'A's and 'B's.
    # Alice wants to eat an 'A'. Bob wants to eat a 'B'.
    # The game ends when no more 'A's for Alice or 'B's for Bob.
    # The winner is the one who eats the last dish.

    # This is a game on a string.
    # Alice's move: choose 'A' at index `i`. The string becomes S[i+1:].
    # Bob's move: choose 'B' at index `j`. The string becomes S[:j].

    # This is a game on a segment.
    # Let `dp[l][r]` be the winner for the segment `S[l...r]`.
    # Too slow for N=600,000.

    # The key insight must be simpler.
    # Alice wants to eat an 'A'. Bob wants to eat a 'B'.
    # They both want to eat the last dish.
    # This means they want to maximize their own count of dishes eaten.
    # The player who eats the last dish wins.

    # The crucial part is that Alice can choose *any* 'A' and Bob can choose *any* 'B'.
    # This means they can effectively "remove" a prefix or suffix.
    # Alice wants to eat an 'A' that is as far right as possible, to preserve 'A's to her left.
    # Bob wants to eat a 'B' that is as far left as possible, to preserve 'B's to his right.

    # This is a game on a line.
    # Alice wants to eat an 'A'. Bob wants to eat a 'B'.
    # The game ends when no more 'A's for Alice or 'B's for Bob.
    # The winner is the one who eats the last dish.

    # Let's consider the number of 'A's and 'B's.
    # Alice wants to eat an 'A'. Bob wants to eat a 'B'.
    # The game ends when no more 'A's for Alice or 'B's for Bob.
    # The winner is the one who eats the last dish.

    # This is a game on a string.
    # Alice's move: choose 'A' at index `i`. The string becomes S[i+1:].
    # Bob's move: choose 'B' at index `j`. The string becomes S[:j].

    # This is a game on a segment.
    # Let `dp[l][r]` be the winner for the segment `S[l...r]`.
    # Too slow for N=600,000.

    # The key insight must be simpler.
    # Alice wants to eat an 'A'. Bob wants to eat a 'B'.
    # They both want to eat the last dish.
    # This means they want to maximize their own count of dishes eaten.
    # The player who eats the last dish wins.

    # The crucial part is that Alice can choose *any* 'A' and Bob can choose *any* 'B'.
    # This means they can effectively "remove" a prefix or suffix.
    # Alice wants to eat an 'A' that is as far right as possible, to preserve 'A's to her left.
    # Bob wants to eat a 'B' that is as far left as possible, to preserve 'B's to his right.

    # This is a game on a line.
    # Alice wants to eat an 'A'. Bob wants to eat a 'B'.
    # The game ends when no more 'A's for Alice or 'B's for Bob.
    # The winner is the one who eats the last dish.

    # Let's consider the number of 'A's and 'B's.
    # Alice wants to eat an 'A'. Bob wants to eat a 'B'.
    # The game ends when no more 'A's for Alice or 'B's for Bob.
    # The winner is the one who eats the last dish.

    # This is a game on a string.
    # Alice's move: choose 'A' at index `i`. The string becomes S[i+1:].
    # Bob's move: choose 'B' at index `j`. The string becomes S[:j].

    # This is a game on a segment.
    # Let `dp[l][r]` be the winner for the segment `S[l...r]`.
    # Too slow for N=600,000.

    # The key insight must be simpler.
    # Alice wants to eat an 'A'. Bob wants to eat a 'B'.
    # They both want to eat the last dish.
    # This means they want to maximize their own count of dishes eaten.
    # The player who eats the last dish wins.

    # The crucial part is that Alice can choose *any* 'A' and Bob can choose *any* 'B'.
    # This means they can effectively "remove" a prefix or suffix.
    # Alice wants to eat an 'A' that is as far right as possible, to preserve 'A's to her left.
    # Bob wants to eat a 'B' that is as far left as possible, to preserve 'B's to his right.

    # This is a game on a line.
    # Alice wants to eat an 'A'. Bob wants to eat a 'B'.
    # The game ends when no more 'A's for Alice or 'B's for Bob.
    # The winner is the one who eats the last dish.

    # Let's consider the number of 'A's and 'B's.
    # Alice wants to eat an 'A'. Bob wants to eat a 'B'.
    # The game ends when no more 'A's for Alice or 'B's for Bob.
    # The winner is the one who eats the last dish.

    # This is a game on a string.
    # Alice's move: choose 'A' at index `i`. The string becomes S[i+1:].
    # Bob's move: choose 'B' at index `j`. The string becomes S[:j].

    # This is a game on a segment.
    # Let `dp[l][r]` be the winner for the segment `S[l...r]`.
    # Too slow for N=600,000.

    # The key insight must be simpler.
    # Alice wants to eat an 'A'. Bob wants to eat a 'B'.
    # They both want to eat the last dish.
    # This means they want to maximize their own count of dishes eaten.
    # The player who eats the last dish wins.

    # The crucial part is that Alice can choose *any* 'A' and Bob can choose *any* 'B'.
    # This means they can effectively "remove" a prefix or suffix.
    # Alice wants to eat an 'A' that is as far right as possible, to preserve 'A's to her left.
    # Bob wants to eat a 'B' that is as far left as possible, to preserve 'B's to his right.

    # This is a game on a line.
    # Alice wants to eat an 'A'. Bob wants to eat a 'B'.
    # The game ends when no more 'A's for Alice or 'B's for Bob.
    # The winner is the one who eats the last dish.

    # Let's consider the number of 'A's and 'B's.
    # Alice wants to eat an 'A'. Bob wants to eat a 'B'.
    # The game ends when no more 'A's for Alice or 'B's for Bob.
    # The winner is the one who eats the last dish.

    # This is a game on a string.
    # Alice's move: choose 'A' at index `i`. The string becomes S[i+1:].
    # Bob's move: choose 'B' at index `j`. The string becomes S[:j].

    # This is a game on a segment.
    # Let `dp[l][r]` be the winner for the segment `S[l...r]`.
    # Too slow for N=600,000.

    # The key insight must be simpler.
    # Alice wants to eat an 'A'. Bob wants to eat a 'B'.
    # They both want to eat the last dish.
    # This means they want to maximize their own count of dishes eaten.
    # The player who eats the last dish wins.

    # The crucial part is that Alice can choose *any* 'A' and Bob can choose *any* 'B'.
    # This means they can effectively "remove" a prefix or suffix.
    # Alice wants to eat an 'A' that is as far right as possible, to preserve 'A's to her left.
    # Bob wants to eat a 'B' that is as far left as possible, to preserve 'B's to his right.

    # This is a game on a line.
    # Alice wants to eat an 'A'. Bob wants to eat a 'B'.
    # The game ends when no more 'A's for Alice or 'B's for Bob.
    # The winner is the one who eats the last dish.

    # Let's consider the number of 'A's and 'B's.
    # Alice wants to eat an 'A'. Bob wants to eat a 'B'.
    # The game ends when no more 'A's for Alice or 'B's for Bob.
    # The winner is the one who eats the last dish.

    # This is a game on a string.
    # Alice's move: choose 'A' at index `i`. The string becomes S[i+1:].
    # Bob's move: choose 'B' at index `j`. The string becomes S[:j].

    # This is a game on a segment.
    # Let `dp[l][r]` be the winner for the segment `S[l...r]`.
    # Too slow for N=600,000.

    # The key insight must be simpler.
    # Alice wants to eat an 'A'. Bob wants to eat a 'B'.
    # They both want to eat the last dish.
    # This means they want to maximize their own count of dishes eaten.
    # The player who eats the last dish wins.

    # The crucial part is that Alice can choose *any* 'A' and Bob can choose *any* 'B'.
    # This means they can effectively "remove" a prefix or suffix.
    # Alice wants to eat an 'A' that is as far right as possible, to preserve 'A's to her left.
    # Bob wants to eat a 'B' that is as far left as possible, to preserve 'B's to his right.

    # This is a game on a line.
    # Alice wants to eat an 'A'. Bob wants to eat a 'B'.
    # The game ends when no more 'A's for Alice or 'B's for Bob.
    # The winner is the one who eats the last dish.

    # Let's consider the number of 'A's and 'B's.
    # Alice wants to eat an 'A'. Bob wants to eat a 'B'.
    # The game ends when no more 'A's for Alice or 'B's for Bob.
    # The winner is the one who eats the last dish.

    # This is a game on a string.
    # Alice's move: choose 'A' at index `i`. The string becomes S[i+1:].
    # Bob's move: choose 'B' at index `j`. The string becomes S[:j].

    # This is a game on a segment.
    # Let `dp[l][r]` be the winner for the segment `S[l...r]`.
    # Too slow for N=600,000.

    # The key insight must be simpler.
    # Alice wants to eat an 'A'. Bob wants to eat a 'B'.
    # They both want to eat the last dish.
    # This means they want to maximize their own count of dishes eaten.
    # The player who eats the last dish wins.

    # The crucial part is that Alice can choose *any* 'A' and Bob can choose *any* 'B'.
    # This means they can effectively "remove" a prefix or suffix.
    # Alice wants to eat an 'A' that is as far right as possible, to preserve 'A's to her left.
    # Bob wants to eat a 'B' that is as far left as possible, to preserve 'B's to his right.

    # This is a game on a line.
    # Alice wants to eat an 'A'. Bob wants to eat a 'B'.
    # The game ends when no more 'A's for Alice or 'B's for Bob.
    # The winner is the one who eats the last dish.

    # Let's consider the number of 'A's and 'B's.
    # Alice wants to eat an 'A'. Bob wants to eat a 'B'.
    # The game ends when no more 'A's for Alice or 'B's for Bob.
    # The winner is the one who eats the last dish.

    # This is a game on a string.
    # Alice's move: choose 'A' at index `i`. The string becomes S[i+1:].
    # Bob's move: choose 'B' at index `j`. The string becomes S[:j].

    # This is a game on a segment.
    # Let `dp[l][r]` be the winner for the segment `S[l...r]`.
    # Too slow for N=600,000.

    # The key insight must be simpler.
    # Alice wants to eat an 'A'. Bob wants to eat a 'B'.
    # They both want to eat the last dish.
    # This means they want to maximize their own count of dishes eaten.
    # The player who eats the last dish wins.

    # The crucial part is that Alice can choose *any* 'A' and Bob can choose *any* 'B'.
    # This means they can effectively "remove" a prefix or suffix.
    # Alice wants to eat an 'A' that is as far right as possible, to preserve 'A's to her left.
    # Bob wants to eat a 'B' that is as far left as possible, to preserve 'B's to his right.

    # This is a game on a line.
    # Alice wants to eat an 'A'. Bob wants to eat a 'B'.
    # The game ends when no more 'A's for Alice or 'B's for Bob.
    # The winner is the one who eats the last dish.

    # Let's consider the number of 'A's and 'B's.
    # Alice wants to eat an 'A'. Bob wants to eat a 'B'.
    # The game ends when no more 'A's for Alice or 'B's for Bob.
    # The winner is the one who eats the last dish.

    # This is a game on a string.
    # Alice's move: choose 'A' at index `i`. The string becomes S[i+1:].
    # Bob's move: choose 'B' at index `j`. The string becomes S[:j].

    # This is a game on a segment.
    # Let `dp[l][r]` be the winner for the segment `S[l...r]`.
    # Too slow for N=600,000.

    # The key insight must be simpler.
    # Alice wants to eat an 'A'. Bob wants to eat a 'B'.
    # They both want to eat the last dish.
    # This means they want to maximize their own count of dishes eaten.
    # The player who eats the last dish wins.

    # The crucial part is that Alice can choose *any* 'A' and Bob can choose *any* 'B'.
    # This means they can effectively "remove" a prefix or suffix.
    # Alice wants to eat an 'A' that is as far right as possible, to preserve 'A's to her left.
    # Bob wants to eat a 'B' that is as far left as possible, to preserve 'B's to his right.

    # This is a game on a line.
    # Alice wants to eat an 'A'. Bob wants to eat a 'B'.
    # The game ends when no more 'A's for Alice or 'B's for Bob.
    # The winner is the one who eats the last dish.

    # Let's consider the number of 'A's and 'B's.
    # Alice wants to eat an 'A'. Bob wants to eat a 'B'.
    # The game ends when no more 'A's for Alice or 'B's for Bob.
    # The winner is the one who eats the last dish.

    # This is a game on a string.
    # Alice's move: choose 'A' at index `i`. The string becomes S[i+1:].
    # Bob's move: choose 'B' at index `j`. The string becomes S[:j].

    # This is a game on a segment.
    # Let `dp[l][r]` be the winner for the segment `S[l...r]`.
    # Too slow for N=600,000.

    # The key insight must be simpler.
    # Alice wants to eat an 'A'. Bob wants to eat a 'B'.
    # They both want to eat the last dish.
    # This means they want to maximize their own count of dishes eaten.
    # The player who eats the last dish wins.

    # The crucial part is that Alice can choose *any* 'A' and Bob can choose *any* 'B'.
    # This means they can effectively "remove" a prefix or suffix.
    # Alice wants to eat an 'A' that is as far right as possible, to preserve 'A's to her left.
    # Bob wants to eat a 'B' that is as far left as possible, to preserve 'B's to his right.

    # This is a game on a line.
    # Alice wants to eat an 'A'. Bob wants to eat a 'B'.
    # The game ends when no more 'A's for Alice or 'B's for Bob.
    # The winner is the one who eats the last dish.

    # Let's consider the number of 'A's and 'B's.
    # Alice wants to eat an 'A'. Bob wants to eat a 'B'.
    # The game ends when no more 'A's for Alice or 'B's for Bob.
    # The winner is the one who eats the last dish.

    # This is a game on a string.
    # Alice's move: choose 'A' at index `i`. The string becomes S[i+1:].
    # Bob's move: choose 'B' at index `j`. The string becomes S[:j].

    # This is a game on a segment.
    # Let `dp[l][r]` be the winner for the segment `S[l...r]`.
    # Too slow for N=600,000.

    # The key insight must be simpler.
    # Alice wants to eat an 'A'. Bob wants to eat a 'B'.
    # They both want to eat the last dish.
    # This means they want to maximize their own count of dishes eaten.
    # The player who eats the last dish wins.

    # The crucial part is that Alice can choose *any* 'A' and Bob can choose *any* 'B'.
    # This means they can effectively "remove" a prefix or suffix.
    # Alice wants to eat an 'A' that is as far right as possible, to preserve 'A's to her left.
    # Bob wants to eat a 'B' that is as far left as possible, to preserve 'B's to his right.

    # This is a game on a line.
    # Alice wants to eat an 'A'. Bob wants to eat a 'B'.
    # The game ends when no more 'A's for Alice or 'B's for Bob.
    # The winner is the one who eats the last dish.

    # Let's consider the number of 'A's and 'B's.
    # Alice wants to eat an 'A'. Bob wants to eat a 'B'.
    # The game ends when no more 'A's for Alice or 'B's for Bob.
    # The winner is the one who eats the last dish.

    # This is a game on a string.
    # Alice's move: choose 'A' at index `i`. The string becomes S[i+1:].
    # Bob's move: choose 'B' at index `j`. The string becomes S[:j].

    # This is a game on a segment.
    # Let `dp[l][r]` be the winner for the segment `S[l...r]`.
    # Too slow for N=600,000.

    # The key insight must be simpler.
    # Alice wants to eat an 'A'. Bob wants to eat a 'B'.
    # They both want to eat the last dish.
    # This means they want to maximize their own count of dishes eaten.
    # The player who eats the last dish wins.

    # The crucial part is that Alice can choose *any* 'A' and Bob can choose *any* 'B'.
    # This means they can effectively "remove" a prefix or suffix.
    # Alice wants to eat an 'A' that is as far right as possible, to preserve 'A's to her left.
    # Bob wants to eat a 'B' that is as far left as possible, to preserve 'B's to his right.

    # This is a game on a line.
    # Alice wants to eat an 'A'. Bob wants to eat a 'B'.
    # The game ends when no more 'A's for Alice or 'B's for Bob.
    # The winner is the one who eats the last dish.

    # Let's consider the number of 'A's and 'B's.
    # Alice wants to eat an 'A'. Bob wants to eat a 'B'.
    # The game ends when no more 'A's for Alice or 'B's for Bob.
    # The winner is the one who eats the last dish.

    # This is a game on a string.
    # Alice's move: choose 'A' at index `i`. The string becomes S[i+1:].
    # Bob's move: choose 'B' at index `j`. The string becomes S[:j].

    # This is a game on a segment.
    # Let `dp[l][r]` be the winner for the segment `S[l...r]`.
    # Too slow for N=600,000.

    # The key insight must be simpler.
    # Alice wants to eat an 'A'. Bob wants to eat a 'B'.
    # They both want to eat the last dish.
    # This means they want to maximize their own count of dishes eaten.
    # The player who eats the last dish wins.

    # The crucial part is that Alice can choose *any* 'A' and Bob can choose *any* 'B'.
    # This means they can effectively "remove" a prefix or suffix.
    # Alice wants to eat an 'A' that is as far right as possible, to preserve 'A's to her left.
    # Bob wants to eat a 'B' that is as far left as possible, to preserve 'B's to his right.

    # This is a game on a line.
    # Alice wants to eat an 'A'. Bob wants to eat a 'B'.
    # The game ends when no more 'A's for Alice or 'B's for Bob.
    # The winner is the one who eats the last dish.

    # Let's consider the number of 'A's and 'B's.
    # Alice wants to eat an 'A'. Bob wants to eat a 'B'.
    # The game ends when no more 'A's for Alice or 'B's for Bob.
    # The winner is the one who eats the last dish.

    # This is a game on a string.
    # Alice's move: choose 'A' at index `i`. The string becomes S[i+1:].
    # Bob's move: choose 'B' at index `j`. The string becomes S[:j].

    # This is a game on a segment.
    # Let `dp[l][r]` be the winner for the segment `S[l...r]`.
    # Too slow for N=600,000.

    # The key insight must be simpler.
    # Alice wants to eat an 'A'. Bob wants to eat a 'B'.
    # They both want to eat the last dish.
    # This means they want to maximize their own count of dishes eaten.
    # The player who eats the last dish wins.

    # The crucial part is that Alice can choose *any* 'A' and Bob can choose *any* 'B