import gurobipy as gp
from gurobipy import GRB


class Midori64:
    def __init__(self, num_round, model):
        self.num_round = num_round
        self.model = model
        self.state_size = 64
        self.all_xi = []
        self.all_yi = []
        self.all_zi = []
        self.all_wi = []
        self.all_ti = []
        self.all_ai = []
        self.all_pi = []

    def create_vars(self):
        sbox_count = self.state_size // 4

        for round_num in range(self.num_round):
            x_vars = [
                self.model.addVar(vtype=GRB.BINARY, name=f"x_{round_num}_{j}")
                for j in range(self.state_size)
            ]
            y_vars = [
                self.model.addVar(vtype=GRB.BINARY, name=f"y_{round_num}_{j}")
                for j in range(self.state_size)
            ]
            z_vars = [
                self.model.addVar(vtype=GRB.BINARY, name=f"z_{round_num}_{j}")
                for j in range(self.state_size)
            ]
            w_vars = [
                self.model.addVar(vtype=GRB.BINARY, name=f"w_{round_num}_{j}")
                for j in range(self.state_size)
            ]
            t_vars = [
                self.model.addVar(
                    vtype=GRB.BINARY, name=f"t_{round_num}_{round_num*8+j}"
                )
                for j in range(self.state_size // 2)
            ]
            a_vars = [
                self.model.addVar(vtype=GRB.BINARY, name=f"a_{round_num}_{j}")
                for j in range(sbox_count)
            ]
            p_vars = [
                [
                    self.model.addVar(vtype=GRB.BINARY, name=f"p_{round_num}_{j}_{k}")
                    for k in range(2)
                ]
                for j in range(sbox_count)
            ]
            self.all_xi.append(x_vars)
            self.all_yi.append(y_vars)
            self.all_ai.append(a_vars)
            self.all_pi.append(p_vars)
            self.all_zi.append(z_vars)
            self.all_ti.append(t_vars)
            self.all_wi.append(w_vars)

    def add_substitution_constraints(self, x_vars, y_vars, a_vars, p_vars):
        sbox_count = self.state_size // 4

        for j in range(sbox_count):
            x_nibbles = [x_vars[4 * j + k] for k in range(4)]
            y_nibbles = [y_vars[4 * j + k] for k in range(4)]
            a_var = a_vars[j]
            p_sbox = p_vars[j]

            for x in x_nibbles:
                self.model.addConstr(x - a_var <= 0)
            self.model.addConstr(sum(x_nibbles) - a_var >= 0)
            self.model.addConstr(4 * sum(x_nibbles) - sum(y_nibbles) >= 0)
            self.model.addConstr(4 * sum(y_nibbles) - sum(x_nibbles) >= 0)

            ddt_constraints = [
                [0, -1, 0, -1, 0, -1, 0, -1, 4, 3],
                [0, 1, 2, 1, 0, -3, -2, -3, 6, 5],
                [0, -2, -1, 1, -2, 1, 0, -1, 4, 5],
                [-2, -2, 1, 2, -1, 1, -2, -3, 6, 8],
                [-5, -4, -7, -1, 8, -1, -2, 2, 11, 20],
                [-2, -1, -2, 3, -2, 3, -1, -3, 7, 8],
                [-2, 1, 0, -1, 0, -2, -1, 1, 4, 5],
                [3, 3, -1, 3, 0, 1, -2, 1, 0, -2],
                [0, 2, 6, 2, -2, -1, 0, -1, -2, 3],
                [-1, 3, -2, -1, -2, -2, -1, 3, 6, 6],
                [0, 1, -2, 1, 3, 3, -1, 3, 0, -2],
                [0, 1, -2, 1, 0, 1, -2, 1, 4, 1],
                [-2, -1, 0, -1, 0, 2, 6, 2, -2, 3],
                [0, -1, -2, 1, 2, -2, 2, 0, 4, 3],
                [0, -3, -1, -1, 2, -1, 1, 4, 2, 5],
                [0, 0, 0, 0, 0, 0, 0, 0, -1, -1],
                [-4, -2, 1, -2, 2, 1, 5, 1, 1, 4],
                [0, 0, 0, 0, 0, 1, -1, 1, 1, 0],
                [8, 2, -2, -1, -5, -1, -7, -4, 11, 20],
                [0, -3, -2, -3, 0, 1, 2, 1, 6, 5],
                [2, 0, 2, -2, 0, 1, -2, -1, 4, 3],
                [1, 2, -1, 2, 1, -1, 1, -1, 2, 0],
                [0, 1, 2, 1, -1, 1, 1, 1, -2, 0],
                [0, 1, -3, -2, 3, 1, 2, -2, 5, 4],
                [2, -2, 2, 0, 0, -1, -2, 1, 4, 3],
                [2, 1, 4, 1, -3, -2, 1, -2, 1, 3],
            ]

            for ddt_row in ddt_constraints:
                xi_coeffs = ddt_row[:4]
                yi_coeffs = ddt_row[4:8]
                pi_coeffs = ddt_row[8:]
                self.model.addConstr(
                    sum(xi_coeffs[k] * x_nibbles[k] for k in range(4))
                    + sum(yi_coeffs[k] * y_nibbles[k] for k in range(4))
                    + sum(pi_coeffs[k] * p_sbox[k] for k in range(2))
                    >= 0
                )

        return

    def add_shufflecell_constraints(self, y_vars, z_vars):

        shuffle_map = [0, 10, 5, 15, 14, 4, 11, 1, 9, 3, 12, 6, 7, 13, 2, 8]
        for k, r in enumerate(shuffle_map):
            for b in range(4):
                self.model.addConstr(y_vars[4 * r + b] - z_vars[4 * k + b] == 0)

    def add_mixcolumn_constraints(self, z_vars, w_vars, t_vars):
        mix_column_matrix = [
            [4, 8, 12, 0],
            [5, 9, 13, 1],
            [6, 10, 14, 2],
            [7, 11, 15, 3],
            [0, 12, 8, 4],
            [1, 13, 9, 5],
            [2, 14, 10, 6],
            [3, 15, 11, 7],
        ]

        second_matrix = [
            [8, 4, 4],
            [9, 5, 5],
            [10, 6, 6],
            [11, 7, 7],
            [12, 0, 0],
            [13, 1, 1],
            [14, 2, 2],
            [15, 3, 3],
        ]

        for col_idx in range(4):
            for idx, mix_row in enumerate(mix_column_matrix):

                ti_idx = mix_row[3] + 8 * col_idx
                z_idx_a = mix_row[0] + 16 * col_idx
                z_idx_b = mix_row[1] + 16 * col_idx
                z_idx_c = mix_row[2] + 16 * col_idx

                self.model.addConstr(
                    z_vars[z_idx_a] + z_vars[z_idx_b] - t_vars[ti_idx] >= 0
                )
                self.model.addConstr(
                    z_vars[z_idx_a] - z_vars[z_idx_b] + t_vars[ti_idx] >= 0
                )
                self.model.addConstr(
                    -z_vars[z_idx_a] + z_vars[z_idx_b] + t_vars[ti_idx] >= 0
                )
                self.model.addConstr(
                    z_vars[z_idx_a] + z_vars[z_idx_b] + t_vars[ti_idx] <= 2
                )

                self.model.addConstr(
                    t_vars[ti_idx] + z_vars[z_idx_c] - w_vars[idx] >= 0
                )
                self.model.addConstr(
                    t_vars[ti_idx] - z_vars[z_idx_c] + w_vars[idx] >= 0
                )
                self.model.addConstr(
                    -t_vars[ti_idx] + z_vars[z_idx_c] + w_vars[idx] >= 0
                )
                self.model.addConstr(
                    t_vars[ti_idx] + z_vars[z_idx_c] + w_vars[idx] <= 2
                )

            for idx, row in enumerate(second_matrix):
                ti_idx = row[2] + 8 * col_idx

                z_idx_a = mix_row[0] + 16 * col_idx
                z_idx_b = mix_row[1] + 16 * col_idx
                z_idx_c = mix_row[2] + 16 * col_idx

                z_idx = row[0] + 16 * col_idx
                w_idx = row[1] + 16 * col_idx

                self.model.addConstr(
                    t_vars[ti_idx] + z_vars[z_idx] - w_vars[w_idx] >= 0
                )
                self.model.addConstr(
                    t_vars[ti_idx] - z_vars[z_idx] + w_vars[w_idx] >= 0
                )
                self.model.addConstr(
                    -t_vars[ti_idx] + z_vars[z_idx] + w_vars[w_idx] >= 0
                )
                self.model.addConstr(
                    t_vars[ti_idx] + z_vars[z_idx] + w_vars[w_idx] <= 2
                )

    def create_model(self):
        self.create_vars()
        self.objectiveFunction(self.all_pi)
        for i in range(self.num_round):
            self.add_substitution_constraints(
                self.all_xi[i], self.all_yi[i], self.all_ai[i], self.all_pi[i]
            )
            self.add_shufflecell_constraints(self.all_yi[i], self.all_zi[i])
            self.add_mixcolumn_constraints(
                self.all_zi[i], self.all_wi[i], self.all_ti[i]
            )

        self.model.optimize()

    def objectiveFunction(self, all_pVars):
        objective = gp.LinExpr()
        for i in range(self.num_round):
            for j, p_sbox in enumerate(all_pVars[i]):
                objective += 2 * p_sbox[0] + 3 * p_sbox[1]

        self.model.setObjective(objective, GRB.MINIMIZE)
        self.model.addConstr(self.all_xi[0][0] == 1)  # Example input difference
        self.model.addConstr(self.all_xi[0][40] == 1)  # Example input difference


def main():
    model_name = "Midori64_Cipher"
    num_round = 6
    model = gp.Model("Cipher_Midori")

    midori64_model = Midori64(num_round, model)
    midori64_model.create_model()

    try:
        midori64_model.model.write(model_name + ".lp")
        midori64_model.model.write(model_name + ".sol")
    except:
        pass


if __name__ == "__main__":
    main()
