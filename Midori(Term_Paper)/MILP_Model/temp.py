from sage import *

def bit_level_binary_matrix_multiplication(A_bits, B):
    bit_length = len(A_bits[0])  # Bit length of each entry (for 4-bit input, bit_length is 4)
    output = []

    for i in range(len(B)):
        W_bits = {j: [] for j in range(bit_length)}
        for j in range(len(B[i])):
            if B[i][j] == 1:
                for b in range(bit_length):
                    W_bits[b].append(f"Z{j}{b}")

        output.append({b: " + ".join(W_bits[b]) if W_bits[b] else "0" for b in range(bit_length)})

    return output


def convert_equations_to_flat_variables(results):
    converted_equations = []
    for i, W_bits in enumerate(results):
        for b, expr in W_bits.items():
            new_W_var = f"w_{i*4 + b}"
            new_expr = expr
            for j in range(4):
                for k in range(4):
                    old_Z_var = f"Z{j}{k}"
                    new_Z_var = f"z_{j*4 + k}"
                    new_expr = new_expr.replace(old_Z_var, new_Z_var)

            converted_equations.append(f"{new_W_var} = {new_expr}")
    return converted_equations


def introduce_intermediate_variables(flattened_equations):
    intermediate_vars = {}
    new_equations = []

    # Process for first 8 equations (w_0 to w_7)
    for eq in flattened_equations[:8]:
        lhs, rhs = eq.split(" = ")
        terms = rhs.split(" + ")

        if len(terms) > 2:
            t_var = f"t{len(intermediate_vars)}"
            intermediate_vars[t_var] = " + ".join(terms[:2])
            rhs = t_var + " + " + " + ".join(terms[2:])
            new_equations.append(f"{t_var} = {intermediate_vars[t_var]}")

        new_equations.append(f"{lhs} = {rhs}")

    # Process for the remaining equations
    for eq in flattened_equations[8:]:
        lhs, rhs = eq.split(" = ")
        terms = rhs.split(" + ")
        terms[0], terms[1] = terms[1], terms[0]
        rhs = " + ".join(terms)

        for t_var, t_expr in intermediate_vars.items():
            rhs = rhs.replace(t_expr, t_var)

        new_equations.append(f"{lhs} = {rhs}")

    return new_equations, intermediate_vars


def main(A_bits):
    results = bit_level_binary_matrix_multiplication(A_bits, B)
    flattened_equations = convert_equations_to_flat_variables(results)

    final_equations, intermediate_vars = introduce_intermediate_variables(flattened_equations)

    print("Final Equations with Intermediate Variables:")
    for eq in final_equations:
        print(eq)


if __name__ == "__main__":
    # Now passing all column matrices A_bits dynamically
    A_bits_col0 = [
        ["Z00", "Z01", "Z02", "Z03"],
        ["Z10", "Z11", "Z12", "Z13"],
        ["Z20", "Z21", "Z22", "Z23"],
        ["Z30", "Z31", "Z32", "Z33"],
    ]

    A_bits_col1 = [
        ["Z40", "Z41", "Z42", "Z43"],
        ["Z50", "Z51", "Z52", "Z53"],
        ["Z60", "Z61", "Z62", "Z63"],
        ["Z70", "Z71", "Z72", "Z73"],
    ]

    A_bits_col2 = [
        ["Z80", "Z81", "Z82", "Z83"],
        ["Z90", "Z91", "Z92", "Z93"],
        ["Za0", "Za1", "Za2", "Za3"],
        ["Zb0", "Zb1", "Zb2", "Zb3"],
    ]

    A_bits_col3 = [
        ["Zc0", "Zc1", "Zc2", "Zc3"],
        ["Zd0", "Zd1", "Zd2", "Zd3"],
        ["Ze0", "Ze1", "Ze2", "Ze3"],
        ["Zf0", "Zf1", "Zf2", "Zf3"],
    ]

    B = [[0, 1, 1, 1], [1, 0, 1, 1], [1, 1, 0, 1], [1, 1, 1, 0]]

    # Now process each column matrix individually
    main(A_bits_col0)
    main(A_bits_col1)
    main(A_bits_col2)
    main(A_bits_col3)
