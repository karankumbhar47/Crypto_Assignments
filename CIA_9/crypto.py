from sympy import symbols, Poly, GF
from sympy.polys.galoistools import gf_degree, gf_pow_mod

def is_primitive_polynomial(poly_int):

    binary_representation = bin(poly_int)[2:]
    degree = len(binary_representation) - 1
    
    x = symbols('x')
    coefficients = [int(bit) for bit in binary_representation]
    poly = Poly(coefficients, x, domain=GF(2))

    if not poly.is_irreducible:
        return False

    order = 2**degree - 1
    test_result = gf_pow_mod([0, 1], order, poly.all_coeffs(), 2, GF(2) )
    
    return gf_degree(test_result) == 0 and test_result == [1]

# Example usage:
poly_int = int(input("Enter the feedback polynomial as an integer: "))
print(is_primitive_polynomial(poly_int))
