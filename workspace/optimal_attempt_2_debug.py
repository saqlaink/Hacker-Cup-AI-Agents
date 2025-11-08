import sys

def solve():
    T = int(sys.stdin.readline())
    print(f"DEBUG: Total test cases T = {T}", file=sys.stderr)

    for i in range(1, T + 1):
        A, B, C = map(int, sys.stdin.readline().split())
        print(f"DEBUG: Case #{i}: Read A={A}, B={B}, C={C}", file=sys.stderr)

        result_parts = []
        for _ in range(A):
            result_parts.append("1")
            print(f"DEBUG: Case #{i}: Appended '1'. Current result_parts = {result_parts}", file=sys.stderr)

        product_ab = A * B
        print(f"DEBUG: Case #{i}: Calculated A * B = {product_ab}", file=sys.stderr)

        if product_ab >= C:
            print(f"DEBUG: Case #{i}: Condition A * B ({product_ab}) >= C ({C}) is TRUE. Appending C.", file=sys.stderr)
            result_parts.append(str(C))
        else:
            print(f"DEBUG: Case #{i}: Condition A * B ({product_ab}) >= C ({C}) is FALSE. Not appending C.", file=sys.stderr)

        final_result = " ".join(result_parts)
        print(f"DEBUG: Case #{i}: Final result string before output = '{final_result}'", file=sys.stderr)
        print(f"Case #{i}: {final_result}")

solve()