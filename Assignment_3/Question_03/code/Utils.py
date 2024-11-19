def print_key(key, i):
    print(f"\nround {i} keys : \n")
    for i in range(len(key)):
        for j in range(len(key)):
            print(hex(key[i][j]), end=" ")
        print(end="\n")


def print_col(col):
    for i in range(len(col)):
        print(hex(col[i]), end=" ")
    print(end="\n")


def transpose_key(matrix):
    n = len(matrix)
    transposed = [[0] * n for _ in range(n)]
    for i in range(n):
        for j in range(n):
            transposed[i][j] = matrix[j][i]
    return transposed


def write_initialKey(initial_key):
    output_filename = "./texFiles/initial_key.tex"
    with open(output_filename, "w") as f:
        f.write("\\[\n")
        f.write("    \\text{Initial Key : }\n")
        f.write("    \\renewcommand{\\arraystretch}{1.5}\n")
        f.write("    \\setlength{\\arrayrulewidth}{0.6mm}\n")
        f.write("    \\setlength{\\tabcolsep}{0.5em}\n")
        f.write("    \\begin{array}{|>{\\centering\\arraybackslash}m{2em}|>{\\centering\\arraybackslash}m{2em}|>{\\centering\\arraybackslash}m{2em}|>{\\centering\\arraybackslash}m{2em}|}\n")
        f.write("        \\hline\n")
        for row in initial_key:
            latex_row = " & ".join(
                [f"\\text{{0x{value:02X}}}" for value in row])
            f.write(f"        {latex_row} \\\\\n")
            f.write("        \\hline\n")
        f.write("    \\end{array}\n")
        f.write("\\]\n")


def write_roundKeys(round_keys):
    output_filename = "./texFiles/round_keys.tex"
    with open(output_filename, "w") as f:
        f.write("\\[\n")
        f.write("    \\renewcommand{\\arraystretch}{1.5}\n")
        f.write("    \\setlength{\\arrayrulewidth}{0.6mm}\n")
        f.write("    \\setlength{\\tabcolsep}{0.5em}\n")
        f.write("    \\begin{tabular}{c c}\n")

        for i in range(0, len(round_keys), 2):

            f.write(f"        \\text{{Round {i+1} Key : }}\n")
            f.write(
                "        \\begin{array}{|>{\\centering\\arraybackslash}m{2em}|>{\\centering\\arraybackslash}m{2em}|>{\\centering\\arraybackslash}m{2em}|>{\\centering\\arraybackslash}m{2em}|}\n")
            f.write("            \\hline\n")
            for row in round_keys[i]:
                latex_row = " & ".join(
                    [f"\\text{{0x{value:02X}}}" for value in row])
                f.write(f"            {latex_row} \\\\\n")
                f.write("            \\hline\n")
            f.write("        \\end{array}\n")

            if i + 1 < len(round_keys):
                f.write("        &\n")
                f.write(f"        \\text{{Round {i+2} Key : }}\n")
                f.write(
                    "        \\begin{array}{|>{\\centering\\arraybackslash}m{2em}|>{\\centering\\arraybackslash}m{2em}|>{\\centering\\arraybackslash}m{2em}|>{\\centering\\arraybackslash}m{2em}|}\n")
                f.write("            \\hline\n")
                for row in round_keys[i + 1]:
                    latex_row = " & ".join(
                        [f"\\text{{0x{value:02X}}}" for value in row])
                    f.write(f"            {latex_row} \\\\\n")
                    f.write("            \\hline\n")
                f.write("        \\end{array}\n")
            else:
                f.write("        & \n")

            f.write("        \\\\\n")
            f.write("        \\vspace{1em} \\\\ \n")

        f.write("    \\end{tabular}\n")
        f.write("\\]\n")


def write_intermediate_steps(round_keys, steps_array):
    output_filename = "./texFiles/steps.tex"
    with open(output_filename, "w") as f:
        f.write("\\item \\textbf{Initial Fifth Round Key}\n\n")
        f.write(
            "The initial key is provided as a 4x4 matrix at the start of the fifth round:\n\n"
        )
        f.write("\\[\n")
        f.write("    \\text{Fifth Round Key : }\n")
        f.write("    \\renewcommand{\\arraystretch}{1.5}\n")
        f.write("    \\setlength{\\arrayrulewidth}{0.6mm}\n")
        f.write("    \\setlength{\\tabcolsep}{0.5em}\n")
        f.write(
            "    \\begin{array}{|>{\\centering\\arraybackslash}m{2em}|>{\\centering\\arraybackslash}m{2em}|>{\\centering\\arraybackslash}m{2em}|>{\\centering\\arraybackslash}m{2em}|}\n"
        )
        f.write("        \\hline\n")

        # Write the initial key matrix row by row
        for row in round_keys[5]:
            latex_row = " & ".join(
                [f"\\text{{0x{value:02X}}}" for value in row]
            )
            f.write(f"        {latex_row} \\\\\n")
            f.write("        \\hline\n")
        f.write("    \\end{array}\n")
        f.write("\\]\n\n")

        # Write steps for column rotation
        f.write("\\item \\textbf{Rotate the Last Column}\n\n")
        f.write("The last column is rotated as follows:\n")
        f.write(write_matrix(
            steps_array[:2],
            "Last Column Before Rotation",
            "Last Column After Rotation"
        ))
        f.write("\n\n")

        # Write steps for byte substitution
        f.write("\\item \\textbf{Substitute Bytes}\n\n")
        f.write("Apply the S-Box substitution to the rotated column:\n")
        f.write(write_matrix(
            steps_array[1:3],
            "Last Column Before Substitution",
            "Last Column After Substitution"
        ))
        f.write("\n")
        f.write(third_step(steps_array[2:5]))

        f.write(fourth_step(steps_array[5:]))

        f.write("\\item \\textbf{Next round Key(Sixth Round Key)}\n\n")
        f.write("\\[\n")
        f.write("    \\text{Sixth Round Key : }\n")
        f.write("    \\renewcommand{\\arraystretch}{1.5}\n")
        f.write("    \\setlength{\\arrayrulewidth}{0.6mm}\n")
        f.write("    \\setlength{\\tabcolsep}{0.5em}\n")
        f.write(
            "    \\begin{array}{|>{\\centering\\arraybackslash}m{2em}|>{\\centering\\arraybackslash}m{2em}|>{\\centering\\arraybackslash}m{2em}|>{\\centering\\arraybackslash}m{2em}|}\n"
        )
        f.write("        \\hline\n")

        # Write the initial key matrix row by row
        for row in round_keys[6]:
            latex_row = " & ".join(
                [f"\\text{{0x{value:02X}}}" for value in row]
            )
            f.write(f"        {latex_row} \\\\\n")
            f.write("        \\hline\n")
        f.write("    \\end{array}\n")
        f.write("\\]\n\n")


def write_matrix(matrix, title1, title2):
    latex_code = f"""
\\[
    \\begin{{array}}{{c@{{\\hskip 2cm}}c}}
        \\text{{{title1}}} & \\text{{{title2}}} \\\\[1em]
"""
    for row in matrix:
        latex_code += r"        \begin{array}{|c|}\n            \hline\n"
        latex_code += "            \\\\ \\hline\n".join(
            f"\\text{{0x{value:02X}}}" for value in row
        ) + r" \\ \hline\n"
        latex_code += r"        \end{array}\n"
        if row != matrix[-1]:
            latex_code += "        &\n"
    latex_code += r"    \end{array}\n\]"
    return latex_code.strip()


def third_step(arrays):
    latex_code = r"""
\pagebreak
\item \textbf{Apply Round Constant}

XOR the substituted column with the round constant.

\[
\begin{align*}
    & """ + f"""
    {format_as_grid(arrays[0])} 
    \\quad \\oplus \\quad
    {format_as_grid(arrays[1])} 
    \\quad = \\quad
    {format_as_grid(arrays[2])}
\end{{align*}}
\]
"""
    return latex_code.strip()


def format_as_grid(array):
    grid = r"\begin{array}{|c|}\hline\n"
    grid += r" \\ \hline\n".join(f"\\text{{0x{value:02X}}}" for value in array)
    grid += r" \\ \hline\n\end{array}"
    return grid


def fourth_step(array):
    def round(matrix):
        code = r"""
        \[
        \begin{align*}
            & """ + f"""
            {format_as_grid(matrix[1])} 
            \\quad \\oplus \\quad
            {format_as_grid(matrix[0])} 
            \\quad = \\quad
            {format_as_grid(matrix[2])}
        \end{{align*}}
        \]"""
        return code.strip()

    latex_code = r"""
\item \textbf{Generating the next round key }

The new key word is generated by XORing the resulting column with the previous column.
"""
    for i in range(0, 12, 3):
        latex_code += round(array[i:i+3])
    return latex_code.strip()
