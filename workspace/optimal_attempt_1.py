def solve():
    N = int(input())
    A = list(map(int, input().split()))

    if N == 1:
        return 0

    max_diff = 0
    for i in range(N - 1):
        diff = abs(A[i] - A[i+1])
        max_diff = max(max_diff, diff)
    
    return max_diff

T = int(input())
for i in range(1, T + 1):
    result = solve()
    print(f"Case #{i}: {result}")