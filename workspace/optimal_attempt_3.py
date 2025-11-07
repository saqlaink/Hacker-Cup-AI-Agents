import collections

def solve():
    N = int(input().strip())
    S = input().strip()

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

    while left <= right:
        if turn == 0: # Alice's turn

            available_a_indices = []
            while a_indices and a_indices[0] < left:
                a_indices.popleft() # Remove 'A's that are already knocked off
            
            for idx in a_indices:
                if left <= idx <= right:
                    available_a_indices.append(idx)
                elif idx > right: # 'A's beyond current right are not accessible
                    break

            if not available_a_indices:
                turn = 1 # Alice skips her turn
                continue








            # Let's use `left` and `right` to denote the current boundaries of the string.























            chosen_a_idx = -1
            while a_indices and a_indices[0] < left:
                a_indices.popleft() # 'A's that are now to the left of `left` are gone
            
            if a_indices and a_indices[0] <= right:
                chosen_a_idx = a_indices.popleft()
                alice_score += 1
                left = chosen_a_idx + 1
            
            turn = 1 # Switch to Bob's turn

        else: # Bob's turn
            chosen_b_idx = -1
            while b_indices and b_indices[-1] > right:
                b_indices.pop() # 'B's that are now to the right of `right` are gone
            
            if b_indices and b_indices[-1] >= left:
                chosen_b_idx = b_indices.pop()
                bob_score += 1
                right = chosen_b_idx - 1
            
            turn = 0 # Switch to Alice's turn
        



    if (alice_score + bob_score) % 2 == 1:
        return "Alice"
    else:
        return "Bob"


T = int(input().strip())
for i in range(1, T + 1):
    result = solve()
    print(f"Case #{i}: {result}")