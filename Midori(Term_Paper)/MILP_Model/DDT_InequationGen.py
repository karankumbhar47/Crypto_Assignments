from MILP_Model.DDT_Utils import *
from sage.all import Polyhedron
from sage.geometry.polyhedron.representation import Inequality 


def reduce_inequalites(inequalities,impossible_points):
    reduced_set = set()

    while impossible_points:
        print("length of impossible Points : ",len(impossible_points))
        best_inequality = None
        max_removed_patterns = 0

        for inequality in inequalities:
            removed_patterns = removed_impossible_patterns(inequality, impossible_points)

            if len(removed_patterns) > max_removed_patterns:
                max_removed_patterns = len(removed_patterns)
                best_inequality = inequality

        if best_inequality is not None:
            removed_patterns = removed_impossible_patterns(best_inequality, impossible_points)
            impossible_points = [point for point in impossible_points if point not in removed_patterns]

            reduced_set.add(best_inequality)
            inequalities.remove(best_inequality)

    return reduced_set


def main():
    ddt = generate_ddt()
    possible_points = generate_possible_points(ddt)
    impossible_points = generate_impossible_points(ddt)  

    poly = Polyhedron(vertices=possible_points)
    inequalities = list(poly.inequality_generator())
    reduced_set = reduce_inequalites(inequalities,impossible_points)

    for inequality in reduced_set:
        print(inequality)

    print(len(reduced_set))


if __name__ == "__main__":
    main()