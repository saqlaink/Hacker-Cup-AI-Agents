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

    print(f"DEBUG: Initial state: alice_score={alice_score}, bob_score={bob_score}, left={left}, right={right}, turn={turn}", file=sys.stderr)

    iteration_count = 0
    while left <= right:
        iteration_count += 1
        print(f"DEBUG: --- Iteration {iteration_count} ---", file=sys.stderr)
        print(f"DEBUG: Current state at start of loop: left={left}, right={right}, turn={turn}, S[{left}:{right+1}]='{S[left:right+1]}'", file=sys.stderr)

        if turn == 0: # Alice's turn
            print(f"DEBUG: Alice's turn (turn=0)", file=sys.stderr)
            available_a_indices = []
            for i in range(left, right + 1):
                if S[i] == 'A':
                    available_a_indices.append(i)
            print(f"DEBUG: Alice: available_a_indices = {available_a_indices}", file=sys.stderr)
            
            if not available_a_indices:
                print(f"DEBUG: Alice: No 'A' available in S[{left}:{right+1}]. Switching turn to Bob (turn=1).", file=sys.stderr)
                turn = 1
                continue
            
            chosen_k = available_a_indices[-1]
            print(f"DEBUG: Alice: Chose index {chosen_k} (S[{chosen_k}]='A')", file=sys.stderr)
            alice_score += 1
            left = chosen_k + 1
            print(f"DEBUG: Alice: After move: alice_score={alice_score}, new left={left}", file=sys.stderr)
            
        else: # Bob's turn
            print(f"DEBUG: Bob's turn (turn=1)", file=sys.stderr)
            available_b_indices = []
            for i in range(left, right + 1):
                if S[i] == 'B':
                    available_b_indices.append(i)
            print(f"DEBUG: Bob: available_b_indices = {available_b_indices}", file=sys.stderr)
            
            if not available_b_indices:
                print(f"DEBUG: Bob: No 'B' available in S[{left}:{right+1}]. Switching turn to Alice (turn=0).", file=sys.stderr)
                turn = 0
                continue
            
            chosen_k = available_b_indices[0]
            print(f"DEBUG: Bob: Chose index {chosen_k} (S[{chosen_k}]='B')", file=sys.stderr)
            bob_score += 1
            right = chosen_k - 1
            print(f"DEBUG: Bob: After move: bob_score={bob_score}, new right={right}", file=sys.stderr)
        
        turn = 1 - turn # Switch turn
        print(f"DEBUG: Turn switched to {turn}", file=sys.stderr)

    print(f"DEBUG: Loop finished. Final scores: alice_score={alice_score}, bob_score={bob_score}", file=sys.stderr)
    if alice_score >= bob_score:
        print(f"DEBUG: Alice wins (alice_score={alice_score} >= bob_score={bob_score})", file=sys.stderr)
        return "Alice"
    else:
        print(f"DEBUG: Bob wins (bob_score={bob_score} > alice_score={alice_score})", file=sys.stderr)
        return "Bob"

T = int(input().strip())
print(f"DEBUG: Total test cases T = {T}", file=sys.stderr)
for i in range(1, T + 1):
    print(f"DEBUG: --- Starting Case #{i} ---", file=sys.stderr)
    result = solve()
    print(f"Case #{i}: {result}")