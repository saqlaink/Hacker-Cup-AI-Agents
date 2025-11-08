import sys

# Constants for modulo arithmetic and maximum exponent
MOD = 10**9 + 7
MAX_EXP = 60 # Maximum exponent for prime factors of B (B <= 10^14, 2^46 is ~7*10^13)

# Precomputed inverse factorials for combinations
inv_fact = [1] * (MAX_EXP + 1)
# C_vals[exp] stores C(exp + N - 1, exp) mod MOD for the current N
C_vals = [1] * (MAX_EXP + 1)

def precompute_inv_factorials():
    """Precomputes inverse factorials modulo MOD up to MAX_EXP."""
    fact = [1] * (MAX_EXP + 1)
    for i in range(1, MAX_EXP + 1):
        fact[i] = (fact[i-1] * i) % MOD
    
    inv_fact[MAX_EXP] = pow(fact[MAX_EXP], MOD - 2, MOD)
    for i in range(MAX_EXP - 1, -1, -1):
        inv_fact[i] = (inv_fact[i+1] * (i+1)) % MOD

precompute_inv_factorials()

def calculate_C_term(exp, N_minus_1_mod):
    """
    Calculates C(exp + N - 1, exp) mod MOD.
    This is the number of ways to express a prime factor p^exp as a product of N integers.
    """
    if exp == 0:
        return 1
    numerator = 1
    for j in range(exp):
        term = (exp + N_minus_1_mod - j + MOD) % MOD
        numerator = (numerator * term) % MOD
    return (numerator * inv_fact[exp]) % MOD

def get_prime_factors(num):
    """Returns a dictionary of prime factors and their exponents for a given number."""
    factors = {}
    d = 2
    temp_num = num
    while d * d <= temp_num:
        while temp_num % d == 0:
            factors[d] = factors.get(d, 0) + 1
            temp_num //= d
        d += 1
    if temp_num > 1:
        factors[temp_num] = factors.get(temp_num, 0) + 1
    return factors

# Global variables for the DFS to avoid passing them repeatedly
memo = {}
prime_factors_B_list = []
A_global = 0

def dfs(idx, current_d_val):
    """
    Recursively calculates the sum of ways for divisors.
    idx: current index in prime_factors_B_list
    current_d_val: product of prime factors processed so far (p_0^e_0 * ... * p_{idx-1}^e_{idx-1})
    """
    if (idx, current_d_val) in memo:
        return memo[(idx, current_d_val)]

    if idx == len(prime_factors_B_list):
        return 1 # Base case: product of empty set of terms is 1

    p, b_exp = prime_factors_B_list[idx]
    res = 0
    p_power = 1
    
    for e in range(b_exp + 1):
        # Pruning: if current_d_val * p_power exceeds A_global,
        if current_d_val > A_global // p_power: 
            break
        
        ways_d_prime_factor = C_vals[e]
        ways_B_over_d_prime_factor = C_vals[b_exp - e]
        
        g_val = (ways_d_prime_factor * ways_B_over_d_prime_factor) % MOD
        
        res = (res + g_val * dfs(idx + 1, current_d_val * p_power)) % MOD
        
        p_power *= p
    
    memo[(idx, current_d_val)] = res
    return res

def solve():
    global prime_factors_B_list, A_global, memo, C_vals

    N, A, B = map(int, sys.stdin.readline().split())

    N_minus_1_mod = (N - 1) % MOD
    A_global = A
    
    for exp_val in range(MAX_EXP + 1):
        C_vals[exp_val] = calculate_C_term(exp_val, N_minus_1_mod)

    prime_factors_B_dict = get_prime_factors(B)
    prime_factors_B_list = list(prime_factors_B_dict.items())
    
    memo.clear() # Clear memoization table for each test case
    
    return dfs(0, 1)

T = int(sys.stdin.readline())
for i in range(1, T + 1):
    print(f"Case #{i}: {solve()}")