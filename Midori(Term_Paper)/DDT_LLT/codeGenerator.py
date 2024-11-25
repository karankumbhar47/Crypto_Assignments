def generate_ddt_latex(ddt, filename="texFiles/ddt_table.tex"):
    n = len(ddt)
    
    latex_code = r"""
\begin{tabular}{c|""" + ("c" * n) + "}\n"
    latex_code += "in /\ out & " + " & ".join([hex(i)[2:].upper() for i in range(n)]) + r" \\" + "\n\\hline\n"
    
    for i, row in enumerate(ddt):
        latex_code += hex(i)[2:].upper() + " & "  
        formatted_row = " & ".join("-" if val == 0 else str(val) for val in row)
        latex_code += formatted_row + r" \\" + "\n"
    latex_code += r"\end{tabular}"
    
    with open(filename, "w") as file:
        file.write(latex_code)
    
    return latex_code


def generate_sbox_latex(sbox, filename="texFiles/sbox_table.tex"):
    n = len(sbox)
    cols = int(n)  
    
    latex_code = "\\begin{tabular}{|c|" + "c|" * cols + "}\n\\hline\n"
    row_x = "x & " + " & ".join(f"{hex(i)[2:].upper()}" for i in range(cols)) + " \\\\\n\\hline\n"
    latex_code += row_x
    row_sx = "S(x) & " + " & ".join(f"{hex(val)[2:].upper()}" for val in sbox) + " \\\\\n\\hline\n"
    latex_code += row_sx
    latex_code += "\\end{tabular}"
    
    with open(filename, "w") as file:
        file.write(latex_code)
    
    return latex_code


def generate_lat_table(data):
    filename = "texFiles/lat_table.tex"
    size = len(data)  
    if any(len(row) != size for row in data):
        raise ValueError("Input must be a square 2D array")

    headers = [hex(i)[2:] for i in range(size)]
    latex_code += "    \\begin{tabular}{|c|" + "c" * size + "|}\n"
    latex_code += "        \\hline\n"
    latex_code += "          & " + " & ".join(headers) + " \\\\\n"
    latex_code += "        \\hline\n"

    for i, row in enumerate(data):
        row_content = f"        {headers[i]} & " + " & ".join(
            str(cell) if cell != 0 else "." for cell in row
        )
        latex_code += row_content + " \\\\\n"
    
    latex_code += "        \\hline\n"
    latex_code += "    \\end{tabular}\n"
    
    with open(filename, "w") as file:
        file.write(latex_code)

    return latex_code
