import sys

def solve():
    N = int(input())
    S = input()

    print(f"DEBUG: N = {N}, S = '{S}'", file=sys.stderr)

    first_A = -1
    print(f"DEBUG: Searching for first 'A'...", file=sys.stderr)
    for i in range(N):
        print(f"DEBUG:   first_A loop i = {i}, S[i] = '{S[i]}'", file=sys.stderr)
        if S[i] == 'A':
            first_A = i
            print(f"DEBUG:   Found first 'A' at index {first_A}", file=sys.stderr)
            break
    print(f"DEBUG: Final first_A = {first_A}", file=sys.stderr)

    last_B = -1
    print(f"DEBUG: Searching for last 'B'...", file=sys.stderr)
    for i in range(N - 1, -1, -1):
        print(f"DEBUG:   last_B loop i = {i}, S[i] = '{S[i]}'", file=sys.stderr)
        if S[i] == 'B':
            last_B = i
            print(f"DEBUG:   Found last 'B' at index {last_B}", file=sys.stderr)
            break
    print(f"DEBUG: Final last_B = {last_B}", file=sys.stderr)

    if first_A == -1:  # No 'A's for Alice
        print(f"DEBUG: Branch: No 'A's found (first_A == -1)", file=sys.stderr)
        count_B = S.count('B')
        print(f"DEBUG:   S.count('B') = {count_B}", file=sys.stderr)
        # Alice skips. Bob eats all 'B's.
        # Total moves = count of 'B's.
        # Alice wins if total moves is odd.
        result = "Alice" if count_B % 2 == 1 else "Bob"
        print(f"DEBUG:   Calculated result = {result}", file=sys.stderr)
        return result
    
    if last_B == -1:  # No 'B's for Bob
        print(f"DEBUG: Branch: No 'B's found (last_B == -1)", file=sys.stderr)
        count_A = S.count('A')
        print(f"DEBUG:   S.count('A') = {count_A}", file=sys.stderr)
        # Bob skips. Alice eats all 'A's.
        # Total moves = count of 'A's.
        result = "Alice" if count_A % 2 == 1 else "Bob"
        print(f"DEBUG:   Calculated result = {result}", file=sys.stderr)
        return result

    print(f"DEBUG: first_A = {first_A}, last_B = {last_B}", file=sys.stderr)
    if first_A > last_B:
        print(f"DEBUG: Branch: first_A ({first_A}) > last_B ({last_B})", file=sys.stderr)
        count_A = S.count('A')
        count_B = S.count('B')
        total_moves = count_A + count_B
        print(f"DEBUG:   S.count('A') = {count_A}, S.count('B') = {count_B}, total_moves = {total_moves}", file=sys.stderr)
        result = "Alice" if total_moves % 2 == 1 else "Bob"
        print(f"DEBUG:   Calculated result = {result}", file=sys.stderr)
        return result
    
    print(f"DEBUG: Branch: Default case (first_A <= last_B)", file=sys.stderr)
    count_A = S.count('A')
    count_B = S.count('B')
    total_moves = count_A + count_B
    print(f"DEBUG:   S.count('A') = {count_A}, S.count('B') = {count_B}, total_moves = {total_moves}", file=sys.stderr)
    result = "Alice" if total_moves % 2 == 1 else "Bob"
    print(f"DEBUG:   Calculated result = {result}", file=sys.stderr)
    return result


T = int(input())
print(f"DEBUG: Total test cases T = {T}", file=sys.stderr)
for i in range(1, T + 1):
    print(f"DEBUG: --- Starting Case #{i} ---", file=sys.stderr)
    print(f"Case #{i}: {solve()}")
    print(f"DEBUG: --- Finished Case #{i} ---", file=sys.stderr)