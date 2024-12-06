def bit_level_binary_matrix_multiplication(A_bits, B, level):
    n = len(A_bits)
    bit_length = len(A_bits[0])
    output = []

    for i in range(len(B)):
        W_bits = {j+level: [] for j in range(bit_length)}
        for j in range(len(B[i])):
            if B[i][j] == 1:
                for b in range(bit_length):
                    W_bits[b+level].append(f"Z{hex(j+level)[-1]}{b}")

        output.append(
            {b: " + ".join(W_bits[b+level]) if W_bits[b+level] else "0" for b in range(bit_length)}
        )

    return output


def introduce_intermediate_variables(flattened_equations,level):
    intermediate_vars = {}
    new_equations = []

    for eq in flattened_equations[:4]:
        lhs, rhs = eq.split(" = ")
        terms = rhs.split(" + ")

        if len(terms) > 2:
            t_var = f"t{len(intermediate_vars)+level}"
            intermediate_vars[t_var] = " + ".join(terms[:2])
            rhs = t_var + " + " + " + ".join(terms[2:])
            new_equations.append(f"{t_var} = {intermediate_vars[t_var]}")

        new_equations.append(f"{lhs} = {rhs}")

    for eq in flattened_equations[4:8]:
        lhs, rhs = eq.split(" = ")
        terms = rhs.split(" + ")

        if len(terms) > 2:
            t_var = f"t{len(intermediate_vars)}"
            intermediate_vars[t_var] = " + ".join([terms[0], terms[2]])
            rhs = t_var + " + " + " + ".join([terms[1]])
            new_equations.append(f"{t_var} = {intermediate_vars[t_var]}")

        new_equations.append(f"{lhs} = {rhs}")

    for eq in flattened_equations[8:12]:
        lhs, rhs = eq.split(" = ")
        terms = rhs.split(" + ")
        terms[0], terms[1] = terms[1], terms[0]
        rhs = " + ".join(terms)
        for t_var, t_expr in intermediate_vars.items():

            rhs = rhs.replace(t_expr, t_var)

        new_equations.append(f"{lhs} = {rhs}")

    for eq in flattened_equations[12:]:
        lhs, rhs = eq.split(" = ")
        for t_var, t_expr in intermediate_vars.items():

            rhs = rhs.replace(t_expr, t_var)

        new_equations.append(f"{lhs} = {rhs}")

    return new_equations, intermediate_vars


def convert_equations_to_flat_variables(results,level):
    converted_equations = []
    for i, W_bits in enumerate(results):
        for b, expr in W_bits.items():
            new_W_var = f"w_{level*4 + (i*4)+b}"
            new_expr = expr
            for j in range(level,level+4):
                for k in range(4):
                    old_Z_var = f"Z{hex(j)[-1]}{k}"
                    new_Z_var = f"z_{j*4 + k}"
                    new_expr = new_expr.replace(old_Z_var, new_Z_var)

            converted_equations.append(f"{new_W_var} = {new_expr}")
    return converted_equations


def main(A_bits,level):
    results = bit_level_binary_matrix_multiplication(A_bits, B, level*4)
    flattened_equations = convert_equations_to_flat_variables(results,level*4)

    final_equations, _ = introduce_intermediate_variables(
        flattened_equations,level*8
    )

    print("Inequlity for coloumn ",level)
    for eq in final_equations:
        print(eq)
    print(len(final_equations))

if __name__ == "__main__":
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

    main(A_bits_col0,0)
    main(A_bits_col1,1)
    main(A_bits_col2,2)
    main(A_bits_col3,3)