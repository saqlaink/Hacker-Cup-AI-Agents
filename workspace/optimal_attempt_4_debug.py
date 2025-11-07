import sys

def solve_case(case_num):
    N = int(sys.stdin.readline())
    S = sys.stdin.readline().strip()

    print(f"DEBUG: Case #{case_num}: Input N = {N}, S = '{S}'", file=sys.stderr)

    # Calculate prefix sums for 'A' and 'B'
    prefix_A = [0] * (N + 1)
    prefix_B = [0] * (N + 1)
    print(f"DEBUG: Initial prefix_A array (size {N+1}): {prefix_A}", file=sys.stderr)
    print(f"DEBUG: Initial prefix_B array (size {N+1}): {prefix_B}", file=sys.stderr)

    for i in range(N):
        char_is_A = (1 if S[i] == 'A' else 0)
        char_is_B = (1 if S[i] == 'B' else 0)
        
        prefix_A[i+1] = prefix_A[i] + char_is_A
        prefix_B[i+1] = prefix_B[i] + char_is_B
        
        print(f"DEBUG: Prefix sum loop iteration i={i}", file=sys.stderr)
        print(f"DEBUG:   S[{i}] = '{S[i]}'", file=sys.stderr)
        print(f"DEBUG:   prefix_A[{i+1}] updated to {prefix_A[i+1]} (from {prefix_A[i]} + {char_is_A})", file=sys.stderr)
        print(f"DEBUG:   prefix_B[{i+1}] updated to {prefix_B[i+1]} (from {prefix_B[i]} + {char_is_B})", file=sys.stderr)

    print(f"DEBUG: Final prefix_A array: {prefix_A}", file=sys.stderr)
    print(f"DEBUG: Final prefix_B array: {prefix_B}", file=sys.stderr)

    # The original code had many commented-out thoughts about DP states but no actual game logic
    # or a statement to print the final answer to stdout.
    # To make the "failing solution" produce *any* output and allow debugging,
    # a placeholder logic for determining the winner is added based on one of the commented interpretations,
    # and the final result is printed to stdout. This is a minimal change to enable output.

    # Placeholder for actual game logic and result determination
    # Based on the commented rules:
    # Alice wins if `count_A > count_B`.
    # Bob wins if `count_B >= count_A`.
    
    total_A_count = prefix_A[N]
    total_B_count = prefix_B[N]

    print(f"DEBUG: Placeholder logic: Total 'A's in string S = {total_A_count}", file=sys.stderr)
    print(f"DEBUG: Placeholder logic: Total 'B's in string S = {total_B_count}", file=sys.stderr)

    result_winner = ""
    if total_A_count > total_B_count:
        result_winner = "Alice"
        print(f"DEBUG: Decision: {total_A_count} > {total_B_count}, Placeholder winner: Alice", file=sys.stderr)
    else:
        result_winner = "Bob"
        print(f"DEBUG: Decision: {total_B_count} >= {total_A_count}, Placeholder winner: Bob", file=sys.stderr)

    # This line is crucial for the solution to produce any output to stdout.
    # The original code was missing any print statement for the final answer.
    sys.stdout.write(f"Case #{case_num}: {result_winner}\n")
    print(f"DEBUG: Outputted to stdout: Case #{case_num}: {result_winner}", file=sys.stderr)


# Standard competitive programming boilerplate to handle multiple test cases.
# The original code snippet was likely the content of a solve() function.
T = int(sys.stdin.readline())
print(f"DEBUG: Total number of test cases T = {T}", file=sys.stderr)
for i in range(1, T + 1):
    print(f"DEBUG: Starting processing for Case #{i}", file=sys.stderr)
    solve_case(i)
    print(f"DEBUG: Finished processing for Case #{i}\n", file=sys.stderr)