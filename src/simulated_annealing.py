import lib

class simulated_annealing:
    def __innit__(self, sa_max, alpha_rate, circuit):
        self.sa_max = sa_max
        self.alpha_rate = alpha_rate
        self.circuit = circuit
    
    def cost_calc(self):
        distance = 0
        for i, edge in enumerate(self.circuit.connections_list):
            a_point = edge.a_point
            b_point = edge.b_point

