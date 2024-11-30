from sympy import symbols, Poly, GF, is_irreducible

def is_primitive_polynomial(poly_int):
    """
    Determines if the polynomial represented by the integer poly_int is primitive
    over GF(2).
    
    Args:
    - poly_int (int): An integer representing the binary form of the polynomial coefficients.

    Returns:
    - bool: True if the polynomial is primitive, False otherwise.
    """
    # Convert integer to binary and get the degree of the polynomial
    binary_representation = bin(poly_int)[2:]
    degree = len(binary_representation) - 1
    
    # Generate the polynomial over GF(2)
    x = symbols('x')
    coefficients = [int(bit) for bit in binary_representation]
    poly = Poly(coefficients, x, domain=GF(2))
    
    # Check if the polynomial is irreducible
    if not is_irreducible(poly):
        return False

    # Check if the polynomial has order 2^degree - 1
    order = 2**degree - 1
    if poly.order() == order:
        return True
    
    return False

# Example usage:
poly_int = int(input("Enter the feedback polynomial as an integer: "))
print(is_primitive_polynomial(poly_int))
