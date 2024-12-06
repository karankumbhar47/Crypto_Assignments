from sage import *

def bit_level_binary_matrix_multiplication(A_bits, B):
    n = len(A_bits)
    bit_length = len(A_bits[0])
    output = []

    for i in range(len(B)):
        W_bits = {j: [] for j in range(bit_length)}
        for j in range(len(B[i])):
            if B[i][j] == 1:
                for b in range(bit_length):
                    W_bits[b].append(f"Z{j}{b}")

        output.append(
            {b: " + ".join(W_bits[b]) if W_bits[b] else "0" for b in range(bit_length)}
        )

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


# A_bits = [
#     ["Z00", "Z01", "Z02", "Z03"],
#     ["Z10", "Z11", "Z12", "Z13"],
#     ["Z20", "Z21", "Z22", "Z23"],
#     ["Z30", "Z31", "Z32", "Z33"],
# ]

# A_bits = [
#     ["Z40", "Z41", "Z42", "Z43"],
#     ["Z50", "Z51", "Z52", "Z53"],
#     ["Z60", "Z61", "Z62", "Z63"],
#     ["Z70", "Z71", "Z72", "Z73"],
# ]

# B = [[0, 1, 1, 1], [1, 0, 1, 1], [1, 1, 0, 1], [1, 1, 1, 0]]


# results = bit_level_binary_matrix_multiplication(A_bits, B)


# for i, W_bits in enumerate(results):
#     print(f"W_{i} bits:")
#     for b, expr in W_bits.items():
#         print(f"  W{i}{b} = {expr}")

# flattened_equations = convert_equations_to_flat_variables(results)

# # Print converted equations
# for eq in flattened_equations:
#     print(eq)



def bit_level_binary_matrix_multiplication(A_bits, B):
    n = len(A_bits)
    bit_length = len(A_bits[0])
    output = []

    for i in range(len(B)):
        W_bits = {j: [] for j in range(bit_length)}
        for j in range(len(B[i])):
            if B[i][j] == 1:
                for b in range(bit_length):
                    W_bits[b].append(f"Z{j}{b}")

        output.append(
            {b: " + ".join(W_bits[b]) if W_bits[b] else "0" for b in range(bit_length)}
        )

    return output


def introduce_intermediate_variables(flattened_equations):
    intermediate_vars = {}
    new_equations = []

    for eq in flattened_equations[:4]:  # First 8 equations for w_0 to w_7
        lhs, rhs = eq.split(" = ")
        terms = rhs.split(" + ")

        if len(terms) > 2:  # Create intermediate variables for terms
            t_var = f"t{len(intermediate_vars)}"
            intermediate_vars[t_var] = " + ".join(terms[:2])  # First two terms
            rhs = t_var + " + " + " + ".join(terms[2:])
            new_equations.append(f"{t_var} = {intermediate_vars[t_var]}")

        new_equations.append(f"{lhs} = {rhs}")

    print(len(intermediate_vars))

    for eq in flattened_equations[4:]:  # First 8 equations for w_0 to w_7
        lhs, rhs = eq.split(" = ")
        terms = rhs.split(" + ")

        if len(terms) > 2:  # Create intermediate variables for terms
            t_var = f"t{len(intermediate_vars)}"
            intermediate_vars[t_var] = " + ".join([terms[0],terms[2]])  # First two terms
            rhs = t_var + " + " + " + ".join([terms[1]])
            new_equations.append(f"{t_var} = {intermediate_vars[t_var]}")

        new_equations.append(f"{lhs} = {rhs}")

    print(len(intermediate_vars))

    for eq in flattened_equations[8:]:  # Remaining equations for w_8 to w_15
        lhs, rhs = eq.split(" = ")
        for t_var, t_expr in intermediate_vars.items():
            # print(lhs,",",rhs,",",t_var,",",t_expr)
            rhs = rhs.replace(t_expr, t_var)  # Replace terms with intermediate vars
            # print(rhs)
        new_equations.append(f"{lhs} = {rhs}")

    return new_equations, intermediate_vars


def convert_equations_to_flat_variables(results):
    converted_equations = []
    for i, W_bits in enumerate(results):
        for b, expr in W_bits.items():
            new_W_var = f"w_{i*4 + b}"
            new_expr = expr
            for j in range(4):  # Adjust Z variables
                for k in range(4):
                    old_Z_var = f"Z{j}{k}"
                    new_Z_var = f"z_{j*4 + k}"
                    new_expr = new_expr.replace(old_Z_var, new_Z_var)

            converted_equations.append(f"{new_W_var} = {new_expr}")
    return converted_equations


# Define input bit matrix and binary mix column matrix
A_bits = [
    ["Z00", "Z01", "Z02", "Z03"],
    ["Z10", "Z11", "Z12", "Z13"],
    ["Z20", "Z21", "Z22", "Z23"],
    ["Z30", "Z31", "Z32", "Z33"],
]

B = [[0, 1, 1, 1], [1, 0, 1, 1], [1, 1, 0, 1], [1, 1, 1, 0]]

# Compute equations for Wi
results = bit_level_binary_matrix_multiplication(A_bits, B)
flattened_equations = convert_equations_to_flat_variables(results)

# Introduce intermediate variables
final_equations, intermediate_vars = introduce_intermediate_variables(flattened_equations)

# Print final equations with intermediate variables
print("Final Equations with Intermediate Variables:")
for eq in final_equations:
    print(eq)

# Print intermediate variables
print("\nIntermediate Variables:")
for var, expr in intermediate_vars.items():
    print(f"{var} = {expr}")
