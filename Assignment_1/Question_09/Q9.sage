from sage.all import *
def euclidean_gcd(a, b):
    while b != 0:
        a, b = b, a % b
    return a

def extended_euclidean_gcd(a, b):
    old_r, r = a, b
    old_s, s = 1, 0
    old_t, t = 0, 1
    
    while r != 0:
        quotient = old_r // r
        old_r, r = r, old_r - quotient * r
        old_s, s = s, old_s - quotient * s
        old_t, t = t, old_t - quotient * t
    
    return old_r, old_s, old_t


def num_invertible_elements(m):
    count = 0
    for i in range(1, m):
        if euclidean_gcd(i, m) == 1:
            count += 1
    return count

def find_inverse(a, m):
    gcd, x, _ = extended_euclidean_gcd(a, m)
    if gcd != 1:
        raise ValueError(f"{a} has no inverse in Z_{m}")
    else:
        return x % m

# Using Sage's In-Built Functions
def num_invertible_elements_sage(m):
    return euler_phi(m)

def find_inverse_sage(a, m):
    if gcd(a, m) != 1:
        raise ValueError(f"{a} has no inverse in Z_{m}")
    else:
        return inverse_mod(a, m)

# Example Usage
# invertible
m = 12
a = 5

# non-invertible values in 
# m = 12 
# a = 2

print("Number of invertible elements in Z_", m, ":", num_invertible_elements(m))
print("Inverse of", a, "in Z_", m, ":", find_inverse(a, m))

# Using Sage's in-built functions
print("Number of invertible elements in Z_", m, "using Sage:", num_invertible_elements_sage(m))
print("Inverse of", a, "in Z_", m, "using Sage:", find_inverse_sage(a, m))
