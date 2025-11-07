import sys

def solve():
    N = int(input())
    print(f"DEBUG: N = {N}", file=sys.stderr)
    S = input()
    print(f"DEBUG: S = '{S}'", file=sys.stderr)

    alice_score = 0
    bob_score = 0
    print(f"DEBUG: Initial scores: alice_score = {alice_score}, bob_score = {bob_score}", file=sys.stderr)

    # Find the leftmost 'A' and rightmost 'B'
    first_A = -1
    print(f"DEBUG: Searching for first 'A'...", file=sys.stderr)
    for i in range(N):
        print(f"DEBUG: first_A loop: i = {i}, S[i] = '{S[i]}'", file=sys.stderr)
        if S[i] == 'A':
            first_A = i
            print(f"DEBUG: Found first 'A' at index {first_A}", file=sys.stderr)
            break
    print(f"DEBUG: Final first_A = {first_A}", file=sys.stderr)
    
    last_B = -1
    print(f"DEBUG: Searching for last 'B'...", file=sys.stderr)
    for i in range(N - 1, -1, -1):
        print(f"DEBUG: last_B loop: i = {i}, S[i] = '{S[i]}'", file=sys.stderr)
        if S[i] == 'B':
            last_B = i
            print(f"DEBUG: Found last 'B' at index {last_B}", file=sys.stderr)
            break
    print(f"DEBUG: Final last_B = {last_B}", file=sys.stderr)

    print(f"DEBUG: Checking edge cases based on first_A and last_B...", file=sys.stderr)
    # If no 'A's, Alice skips, Bob wins if there are 'B's.
    if first_A == -1:
        print(f"DEBUG: Decision: first_A == -1 (no 'A's found)", file=sys.stderr)
        if last_B != -1:
            print(f"DEBUG: Sub-decision: last_B != -1 (some 'B's found). Returning 'Bob'.", file=sys.stderr)
            return "Bob"
        else:
            print(f"DEBUG: Sub-decision: last_B == -1 (no 'B's found). Returning 'Alice'.", file=sys.stderr)
            return "Alice" # If no 'B's either, Alice skips, Bob skips, no one eats. But N>=1, so one must exist.
    
    # If no 'B's, Bob skips, Alice wins if there are 'A's.
    if last_B == -1:
        print(f"DEBUG: Decision: last_B == -1 (no 'B's found). Returning 'Alice'.", file=sys.stderr)
        return "Alice"

    print(f"DEBUG: Both 'A' and 'B' exist. first_A = {first_A}, last_B = {last_B}", file=sys.stderr)
    # The game effectively plays on the segment between the leftmost 'A' and rightmost 'B'.
    # Alice can eat any 'A' at index k, leaving S[k+1:]
    print(f"DEBUG: Core game logic for first_A != -1 and last_B != -1 is not implemented in the provided code.", file=sys.stderr)
    # The solution is incomplete here, so it will implicitly return None for these cases.


T = int(input())
print(f"DEBUG: Total test cases T = {T}", file=sys.stderr)
for i in range(1, T + 1):
    print(f"DEBUG: --- Starting Case #{i} ---", file=sys.stderr)
    result = solve()
    print(f"DEBUG: Result for Case #{i} = {result}", file=sys.stderr)
    print(f"Case #{i}: {result}")