import sys

def solve():
    N = int(sys.stdin.readline())
    S = sys.stdin.readline().strip()

    A_indices = [i for i, char in enumerate(S) if char == 'A']
    B_indices = [i for i, char in enumerate(S) if char == 'B']

    L = 0
    R = N - 1
    alice_turn = True
    last_player_moved = None
    consecutive_skips = 0

    a_left_ptr = 0
    a_right_ptr = len(A_indices) - 1
    b_left_ptr = 0
    b_right_ptr = len(B_indices) - 1

    while L <= R:
        if alice_turn:
            found_A_move = False
            
            # Adjust a_left_ptr to skip A's that are now to the left of L
            while a_left_ptr <= a_right_ptr and A_indices[a_left_ptr] < L:
                a_left_ptr += 1
            
            # Adjust a_right_ptr to skip A's that are now to the right of R
            while a_left_ptr <= a_right_ptr and A_indices[a_right_ptr] > R:
                a_right_ptr -= 1
            
            if a_left_ptr <= a_right_ptr: # There is an 'A' in S[L..R]
                # Alice picks the rightmost available 'A'
                i = A_indices[a_right_ptr]
                L = i + 1
                last_player_moved = 'Alice'
                consecutive_skips = 0
                found_A_move = True
            
            if not found_A_move:
                consecutive_skips += 1
                if consecutive_skips == 2:
                    break # Both players skipped consecutively
            else:
                consecutive_skips = 0 # Reset skips if a move was made
            
            alice_turn = False
        else: # Bob's turn
            found_B_move = False

            # Adjust b_left_ptr to skip B's that are now to the left of L
            while b_left_ptr <= b_right_ptr and B_indices[b_left_ptr] < L:
                b_left_ptr += 1
            
            # Adjust b_right_ptr to skip B's that are now to the right of R
            while b_left_ptr <= b_right_ptr and B_indices[b_right_ptr] > R:
                b_right_ptr -= 1

            if b_left_ptr <= b_right_ptr: # There is a 'B' in S[L..R]
                # Bob picks the leftmost available 'B'
                j = B_indices[b_left_ptr]
                R = j - 1
                last_player_moved = 'Bob'
                consecutive_skips = 0
                found_B_move = True
            
            if not found_B_move:
                consecutive_skips += 1
                if consecutive_skips == 2:
                    break # Both players skipped consecutively
            else:
                consecutive_skips = 0 # Reset skips if a move was made
            
            alice_turn = True
    
    return last_player_moved

T = int(sys.stdin.readline())
for i in range(1, T + 1):
    result = solve()
    sys.stdout.write(f"Case #{i}: {result}\n")