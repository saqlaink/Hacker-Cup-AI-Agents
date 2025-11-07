def solve():
    N = int(input())
    S = input()

    a_count = S.count('A')
    b_count = S.count('B')

    if a_count == 0:
        return "Bob"
    if b_count == 0:
        return "Alice"

    first_a_idx = S.find('A')
    last_b_idx = S.rfind('B')

    if first_a_idx > last_b_idx:
        return "Alice"
    
    return "Bob" if (a_count + b_count) % 2 == 0 else "Alice"


T = int(input())
for i in range(1, T + 1):
    result = solve()
    print(f"Case #{i}: {result}")