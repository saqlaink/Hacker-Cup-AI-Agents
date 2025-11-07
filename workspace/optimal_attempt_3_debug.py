import collections
import sys

def solve():
    N = int(input().strip())
    S = input().strip()
    print(f"DEBUG: N = {N}, S = '{S}'", file=sys.stderr)

    alice_score = 0
    bob_score = 0
    left = 0
    right = N - 1
    turn = 0 # 0 for Alice, 1 for Bob

    a_indices = collections.deque()
    b_indices = collections.deque()
    for i in range(N):
        if S[i] == 'A':
            a_indices.append(i)
        else:
            b_indices.append(i)
    print(f"DEBUG: Initial state: alice_score={alice_score}, bob_score={bob_score}, left={left}, right={right}, turn={turn}", file=sys.stderr)
    print(f"DEBUG: Initial a_indices={list(a_indices)}, b_indices={list(b_indices)}", file=sys.stderr)

    while left <= right:
        print(f"DEBUG: --- Start of turn --- left={left}, right={right}, turn={turn}", file=sys.stderr)
        if turn == 0: # Alice's turn
            print(f"DEBUG: Alice's turn. Current a_indices={list(a_indices)}", file=sys.stderr)

            # First block: Check for available 'A's and handle skipping turn
            print(f"DEBUG: Alice (Pre-check): Cleaning a_indices for elements < left ({left}).", file=sys.stderr)
            while a_indices and a_indices[0] < left:
                popped_val = a_indices.popleft()
                print(f"DEBUG: Alice (Pre-check): Popped A at index {popped_val} because it's < left ({left}). Remaining a_indices={list(a_indices)}", file=sys.stderr)
            
            available_a_indices_in_range = []
            for idx in a_indices:
                if left <= idx <= right:
                    available_a_indices_in_range.append(idx)
                elif idx > right: # 'A's beyond current right are not accessible
                    break
            print(f"DEBUG: Alice (Pre-check): Available 'A's in [{left}, {right}] are {available_a_indices_in_range}", file=sys.stderr)

            if not available_a_indices_in_range:
                print(f"DEBUG: Alice: No available 'A's in [{left}, {right}]. Alice skips her turn.", file=sys.stderr)
                turn = 1 # Alice skips her turn
                continue # Skip the rest of Alice's turn logic and go to next loop iteration

            # Second block: Alice makes her move (if not skipped)
            print(f"DEBUG: Alice (Move): 'A's are available. Proceeding to make a move.", file=sys.stderr)
            chosen_a_idx = -1
            # This while loop is redundant if the first pre-check block already ran and popped.
            # But it's part of the original code, so we keep it and debug it.
            print(f"DEBUG: Alice (Move): Re-cleaning a_indices for elements < left ({left}). Current a_indices={list(a_indices)}", file=sys.stderr)
            while a_indices and a_indices[0] < left:
                popped_val = a_indices.popleft()
                print(f"DEBUG: Alice (Move): Popped A at index {popped_val} because it's < left ({left}). Remaining a_indices={list(a_indices)}", file=sys.stderr)
            
            if a_indices and a_indices[0] <= right: # This condition should always be true if not skipped above
                chosen_a_idx = a_indices.popleft()
                alice_score += 1
                left = chosen_a_idx + 1
                print(f"DEBUG: Alice: Chose 'A' at index {chosen_a_idx}. alice_score={alice_score}, new left={left}", file=sys.stderr)
            else:
                # This else branch should ideally not be hit if available_a_indices_in_range was not empty
                # unless a_indices was modified unexpectedly.
                print(f"DEBUG: Alice: ERROR/Unexpected: No 'A's found after pre-check indicated availability. a_indices={list(a_indices)}", file=sys.stderr)
            
            turn = 1 # Switch to Bob's turn
            print(f"DEBUG: Alice's turn ends. Next turn={turn}", file=sys.stderr)

        else: # Bob's turn
            print(f"DEBUG: Bob's turn. Current b_indices={list(b_indices)}", file=sys.stderr)
            chosen_b_idx = -1
            print(f"DEBUG: Bob: Cleaning b_indices for elements > right ({right}).", file=sys.stderr)
            while b_indices and b_indices[-1] > right:
                popped_val = b_indices.pop()
                print(f"DEBUG: Bob: Popped B at index {popped_val} because it's > right ({right}). Remaining b_indices={list(b_indices)}", file=sys.stderr)
            
            if b_indices and b_indices[-1] >= left:
                chosen_b_idx = b_indices.pop()
                bob_score += 1
                right = chosen_b_idx - 1
                print(f"DEBUG: Bob: Chose 'B' at index {chosen_b_idx}. bob_score={bob_score}, new right={right}", file=sys.stderr)
            else:
                print(f"DEBUG: Bob: No 'B's available in [{left}, {right}]. b_indices={list(b_indices)}. Bob skips his turn.", file=sys.stderr)
                # Bob implicitly skips if no B is found, as turn switches regardless.
                pass 
            
            turn = 0 # Switch to Alice's turn
            print(f"DEBUG: Bob's turn ends. Next turn={turn}", file=sys.stderr)
        
    print(f"DEBUG: --- Game End --- Final alice_score={alice_score}, bob_score={bob_score}", file=sys.stderr)

    total_moves = alice_score + bob_score
    print(f"DEBUG: Total moves = {total_moves}", file=sys.stderr)
    if total_moves % 2 == 1:
        print(f"DEBUG: Total moves ({total_moves}) is odd. Alice wins.", file=sys.stderr)
        return "Alice"
    else:
        print(f"DEBUG: Total moves ({total_moves}) is even. Bob wins.", file=sys.stderr)
        return "Bob"


T = int(input().strip())
print(f"DEBUG: Total test cases T = {T}", file=sys.stderr)
for i in range(1, T + 1):
    print(f"DEBUG: --- Starting Case #{i} ---", file=sys.stderr)
    result = solve()
    print(f"DEBUG: --- End of Case #{i} --- Result: {result}", file=sys.stderr)
    print(f"Case #{i}: {result}")