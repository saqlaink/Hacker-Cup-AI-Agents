import sys

def solve():
    N = int(sys.stdin.readline())
    S = sys.stdin.readline().strip()

    print(f"DEBUG: N = {N}, S = '{S}'", file=sys.stderr)

    # Find indices of all 'A's and 'B's
    a_indices = [i for i, char in enumerate(S) if char == 'A']
    b_indices = [i for i, char in enumerate(S) if char == 'B']

    num_A = len(a_indices)
    num_B = len(b_indices)

    print(f"DEBUG: a_indices = {a_indices}, num_A = {num_A}", file=sys.stderr)
    print(f"DEBUG: b_indices = {b_indices}, num_B = {num_B}", file=sys.stderr)

    # Case 1: No 'A's for Alice to eat
    if num_A == 0:
        print(f"DEBUG: Case 1: num_A == 0. Result: Bob", file=sys.stderr)
        return "Bob"

    # Case 2: No 'B's for Bob to eat
    if num_B == 0:
        print(f"DEBUG: Case 2: num_B == 0. Result: Alice", file=sys.stderr)
        return "Alice"

    # Both 'A's and 'B's are present.
    # The game is played on a segment [L, R] of the original string.
    # Alice picks an 'A' at index `i` (L <= i <= R), new segment is [i+1, R].
    # Bob picks a 'B' at index `j` (L <= j <= R), new segment is [L, j-1].
    # The player who eats the last dish wins. This is a normal play game.

    # The key insight for this problem type (from similar competitive programming problems)
    # is that Alice's moves only affect the left boundary (L), and Bob's moves only affect the right boundary (R).
    # They are effectively playing two independent games on the indices, but the game ends when L > R.
    # The total number of moves is fixed under optimal play where players try to maximize the game length.
    # Alice wants to pick an 'A' that leaves the most options for herself (smallest i).
    # Bob wants to pick a 'B' that leaves the most options for himself (largest j).

    # Let's simulate this greedy strategy to find the total number of moves.
    current_L = 0
    current_R = N - 1
    
    # Pointers for a_indices and b_indices to find available 'A's and 'B's efficiently
    a_ptr = 0
    b_ptr = num_B - 1

    total_moves = 0

    print(f"DEBUG: Starting game simulation. Initial L={current_L}, R={current_R}", file=sys.stderr)

    while True:
        # Alice's turn
        # Find the leftmost 'A' available in S[current_L ... current_R]
        alice_move_idx = -1
        while a_ptr < num_A and a_indices[a_ptr] < current_L:
            a_ptr += 1 # Skip 'A's that are to the left of current_L
        
        if a_ptr < num_A and a_indices[a_ptr] <= current_R:
            alice_move_idx = a_indices[a_ptr]
            print(f"DEBUG: Alice's turn. Found 'A' at index {alice_move_idx} (S[{alice_move_idx}]).", file=sys.stderr)
            current_L = alice_move_idx + 1
            a_ptr += 1
            total_moves += 1
            print(f"DEBUG: After Alice's move: L={current_L}, R={current_R}, total_moves={total_moves}", file=sys.stderr)
        else:
            print(f"DEBUG: Alice cannot make a move. No 'A's in S[{current_L}...{current_R}].", file=sys.stderr)
            break # Alice cannot move, Bob wins (as Alice couldn't make the last move)

        if current_L > current_R:
            print(f"DEBUG: Segment empty after Alice's move. L={current_L}, R={current_R}. Game ends.", file=sys.stderr)
            break

        # Bob's turn
        # Find the rightmost 'B' available in S[current_L ... current_R]
        bob_move_idx = -1
        while b_ptr >= 0 and b_indices[b_ptr] > current_R:
            b_ptr -= 1 # Skip 'B's that are to the right of current_R

        if b_ptr >= 0 and b_indices[b_ptr] >= current_L:
            bob_move_idx = b_indices[b_ptr]
            print(f"DEBUG: Bob's turn. Found 'B' at index {bob_move_idx} (S[{bob_move_idx}]).", file=sys.stderr)
            current_R = bob_move_idx - 1
            b_ptr -= 1
            total_moves += 1
            print(f"DEBUG: After Bob's move: L={current_L}, R={current_R}, total_moves={total_moves}", file=sys.stderr)
        else:
            print(f"DEBUG: Bob cannot make a move. No 'B's in S[{current_L}...{current_R}].", file=sys.stderr)
            break # Bob cannot move, Alice wins (as Bob couldn't make the last move)
        
        if current_L > current_R:
            print(f"DEBUG: Segment empty after Bob's move. L={current_L}, R={current_R}. Game ends.", file=sys.stderr)
            break

    print(f"DEBUG: Final total_moves = {total_moves}", file=sys.stderr)

    # The player who makes the last move wins.
    # If total_moves is odd, Alice (first player) wins.
    # If total_moves is even, Bob (second player) wins.
    if total_moves % 2 == 1:
        print(f"DEBUG: total_moves is odd. Result: Alice", file=sys.stderr)
        return "Alice"
    else:
        print(f"DEBUG: total_moves is even. Result: Bob", file=sys.stderr)
        return "Bob"


T = int(sys.stdin.readline())
for i in range(1, T + 1):
    result = solve()
    print(f"Case #{i}: {result}")