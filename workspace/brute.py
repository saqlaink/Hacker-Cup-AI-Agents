def solve():
    N = int(input())
    A = list(map(int, input().split()))

    max_diff = 0
    for i in range(N - 1):
        diff = abs(A[i] - A[i+1])
        if diff > max_diff:
            max_diff = diff
    
    return max_diff

T = int(input())
for i in range(1, T + 1):
    result = solve()
    print(f"Case #{i}: {result}")