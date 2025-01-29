import lib
import numpy as np
from random import randint

class sim_annealing:
    def __init__(self, circuit, sa_max=3, alpha_rate=0.1):
        self.sa_max = sa_max
        self.alpha_rate = alpha_rate
        self.circuit = circuit
        self.best_solution = self.cost_calc()
    
    def cost_calc(self):
        distance = 0
        for edge in self.circuit.connections_list:
            a_point = edge.a_point
            b_point = edge.b_point

            a_x = a_point.x
            a_y = a_point.y
            b_x = b_point.x
            b_y = b_point.y

            edge_cost = np.sqrt((a_x-b_x)**2+(a_y-b_y)**2)
            #print(f"{a_x} {b_x} {edge_cost}")
            distance += edge_cost
        return distance

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