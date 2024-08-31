import gurobipy as gp
from gurobipy import *

class Sypher004:

    def __init__(self, rounds, state_size):
        self.rounds = rounds

        self.state_size = state_size

    def create_bit_var(self, model):
        bit_grb_var = [[ 0 for i in range(self.state_size)] for j in range(self.rounds + 1)]

        for i in range(self.rounds + 1):
            for j in range(self.state_size):
                bit_grb_var[i][j] = model.addVar(name='x'+str(i)+str(hex(j)[-1]), vtype='B')

        return bit_grb_var

    def create_sbox_var(self, model):
        sbox_grb_var = [[ 0 for i in range(self.state_size//4)] for j in range(self.rounds + 1)]

        for i in range(self.rounds + 1):
            for j in range(self.state_size//4):
                sbox_grb_var[i][j] = model.addVar(name='a'+str(i)+str(j), vtype='B')

        return sbox_grb_var

    def create_obj_func(self, model, sbox_grb_var):
        eqn = LinExpr(0.0)
        for i in range(self.rounds):
            for j in range(self.state_size//4):
                eqn += sbox_grb_var[i][j]

        model.setObjective(eqn, GRB.MINIMIZE)  

    def create_constraints(self, model, rnd, bit_grb_var, sbox_grb_var):
        for sbox in range(0,self.state_size//4):
            for bit in range(0, 4):
                model.addConstr(bit_grb_var[rnd][4*sbox + bit] - sbox_grb_var[rnd][sbox] <= 0)

        for sbox in range(0,self.state_size//4):
            eqn = LinExpr(0.0)
            for bit in range(0, 4):
                eqn += bit_grb_var[rnd][4*sbox + bit]

            model.addConstr(eqn - sbox_grb_var[rnd][sbox] >= 0)

        for sbox in range(0,self.state_size//4):
            model.addConstr(4 * bit_grb_var[rnd+1][4*sbox] + 4 * bit_grb_var[rnd+1][4*sbox + 1] + 4 * bit_grb_var[rnd+1][4*sbox + 2] + 4 * bit_grb_var[rnd+1][4*sbox + 3]
                - bit_grb_var[rnd][4*sbox] - bit_grb_var[rnd][4*sbox + 1] - bit_grb_var[rnd][4*sbox + 2] - bit_grb_var[rnd][4*sbox + 3] >= 0)


        for sbox in range(0,self.state_size//4):
            model.addConstr(4 * bit_grb_var[rnd][4*sbox] + 4 * bit_grb_var[rnd][4*sbox + 1] + 4 * bit_grb_var[rnd][4*sbox + 2] + 4 * bit_grb_var[rnd][4*sbox + 3]
                - bit_grb_var[rnd+1][4*sbox] - bit_grb_var[rnd+1][4*sbox + 1] - bit_grb_var[rnd+1][4*sbox + 2] - bit_grb_var[rnd+1][4*sbox + 3] >= 0)



    def linear_layer(self, model, bit_grb_var):
        array = [0 for i in range(0,self.state_size)]

        array_index = [0, 4, 8, 12, 1, 5, 9, 13, 2, 6, 10, 14, 3, 7, 11, 15]
        for i in range(0, self.state_size):
            array[array_index[i]] = bit_grb_var[i]

        return array

    def create_last_dummy_constraints(self, model, sbox_grb_var):
        eqn = LinExpr(0.0)
        for rnd in range(self.rounds):
            for sbox in range(0,self.state_size//4):
                eqn += sbox_grb_var[rnd][sbox]

        model.addConstr(eqn >= 1)

    def make_model(self, model, bit_grb_var, sbox_grb_var):
        Sypher004.create_obj_func(self, model, sbox_grb_var)

        for rnd in range(self.rounds):
            if (rnd != 0):
                bit_grb_var[rnd] = Sypher004.linear_layer(self, model, bit_grb_var[rnd])
            Sypher004.create_constraints(self, model, rnd, bit_grb_var, sbox_grb_var)

        Sypher004.create_last_dummy_constraints(self, model, sbox_grb_var)


if __name__=='__main__':
    cipher = "sypher004"

    Round = int(input("Number of Round : "))
    state_size = 16

    model_name = cipher+ "_" + str(Round)
    model = gp.Model(model_name)

    sypher004 = Sypher004(Round, state_size)

    bit_grb_var = sypher004.create_bit_var(model) 
    sbox_grb_var = sypher004.create_sbox_var(model) 

    sypher004.make_model(model, bit_grb_var, sbox_grb_var) 

    model.optimize()

    model.write(model_name + ".lp")
    model.write(model_name + ".sol")
