import lib
import numpy as np
from random import randint

class sim_annealing:
    def __init__(self, circuit, sa_max=3, alpha_rate=0.9):
        self.sa_max = sa_max
        self.alpha_rate = alpha_rate
        self.circuit = circuit
        self.best_solution = circuit.cost_calc()
        self.t0 = self.initial_temperature()

    def switch_edge(self, circuit, edge_i):
        edge = self.circuit.connections_list[edge_i]
        old_a = edge.a_point.id
        old_b = edge.b_point.id
        while True:
            valid_switch = True
            new_a = randint(0, self.circuit.num_points-1)
            new_b = randint(0, self.circuit.num_points-1)
            if new_a == new_b or new_a == old_a and new_b == old_b or new_a == old_b and new_b == old_a or self.circuit.points_list[new_a].connection_num == self.circuit.max_connection or self.circuit.points_list[new_b].connection_num == self.circuit.max_connection:
                valid_switch = False
            if valid_switch:
                break
        circuit.connections_list[edge_i].a_point = self.circuit.points_list[new_a]
        circuit.connections_list[edge_i].b_point = self.circuit.points_list[new_b]
        return circuit

    def gen_neighbour(self):
        neighbour = self.circuit
        while True:
            elim_index = randint(0, self.circuit.num_connections-1)
            a_point = self.circuit.connections_list[elim_index].a_point
            b_point = self.circuit.connections_list[elim_index].b_point
            if a_point.connection_num > 1 and b_point.connection_num > 1:
                break
        self.switch_edge(neighbour, elim_index)
        return neighbour
    
    def initial_temperature(self):
        for i in range(3):
            n_0 = self.gen_neighbour()
            n_1 = self.gen_neighbour()
            n_2 = self.gen_neighbour()

            t0 = (n_0.cost_calc() + n_1.cost_calc() + n_2.cost_calc())/3
        return t0
    
    def solution(self):
        solution = self.best_solution
        t = self.initial_temperature()

        while t > 0.05:
            for i in range(self.sa_max):
                neighbour = self.gen_neighbour()
                new_solution = neighbour.cost_calc()
                if new_solution < solution:
                    solution = new_solution
                    if solution < self.best_solution:
                        self.best_solution = solution
                else:
                    if np.exp(-(new_solution-solution)/t)*100 >= randint(0, 100):
                        solution = new_solution
            t = self.alpha_rate*t
            print(self.best_solution)

