midori_sbox = [0xC, 0xA, 0xD, 0x3, 0xE, 0xB, 0xF, 0x7, 0x8, 0x9, 0x1, 0x5, 0x0, 0x2, 0x4, 0x6]


def generate_ddt(sbox=midori_sbox):
    n = len(sbox)  
    ddt = [[0] * n for _ in range(n)]  

    for x1 in range(n):
        for x2 in range(n):
            delta_in = x1 ^ x2  
            delta_out = sbox[x1] ^ sbox[x2]  
            ddt[delta_in][delta_out] += 1  

    return ddt


def generate_possible_points(ddt):
    prob_map = {
        16: (0, 0),
        2: (0, 1),
        4: (1, 0),
        0: (1, 1)
    }
    points = set()  
    n = len(ddt)
    for x in range(n):  
        for y in range(n):  
            if(ddt[x][y]!=0):
                x_bits = [(x >> i) & 1 for i in reversed(range(4))]
                y_bits = [(y >> i) & 1 for i in reversed(range(4))]
                p0, p1 = prob_map[ddt[x][y]]
                
                # point = tuple(x_bits + y_bits + [p0, p1])
                point = tuple(x_bits + y_bits)
                points.add(point)
    return list(points)


def generate_impossible_points(ddt):
    # all_points = generate_all_possible_points()
    # possible_points = generate_possible_points(ddt)

    # # The impossible points are those in all_points but not in possible_points
    # impossible_points = all_points - possible_points

    # return list(impossible_points)
    points = set()  
    n = len(ddt)
    for x in range(n):  
        for y in range(n):  
            if(ddt[x][y]==0):
                x_bits = [(x >> i) & 1 for i in reversed(range(4))]
                y_bits = [(y >> i) & 1 for i in reversed(range(4))]
                point = tuple(x_bits + y_bits)

                points.add(point)
    return list(points)


def removed_impossible_patterns(inequality, ID):
    coefficients = inequality[1:]  
    b = inequality[0]  
    
    removed_patterns = set()
    for point in ID:
        lhs = sum(coeff * bit for coeff, bit in zip(coefficients, point)) + b
        if lhs < 0:
            # print("point ",point,lhs)
            removed_patterns.add(point)
    return removed_patterns


def printInequlity(inequlites):
    for i, eq in enumerate(inequlites):
        print(i," ==> ",eq)