def solve():
    N = int(input())
    S = input()

    first_B_idx = S.find('B')
    last_A_idx = S.rfind('A')

    if first_B_idx == -1:
        return "Alice"
    if last_A_idx == -1:
        return "Bob"

    if first_B_idx > last_A_idx:
        num_A = S.count('A')
        num_B = S.count('B')
        if num_A > num_B:
            return "Alice"
        else:
            return "Bob"
    else:
        return "Alice"

T = int(input())
for i in range(1, T + 1):
    result = solve()
    print(f"Case #{i}: {result}")