from random import randint
from numpy import exp
from copy import deepcopy
import os

class simulated_annealing:
    def __init__(self, circuit, sa_max=3, alpha_rate=0.9):
        self.circuit = circuit
        self.sa_max = sa_max
        self.alpha = alpha_rate
        self.best_solution = self.solution()

    def solution(self):
        def neighbour(circuit):
            neighbour = deepcopy(circuit)
            while True:
                valid_circuit = True
                connection_index = randint(0, neighbour.connection_num-1)
                connection = neighbour.connection_list[connection_index]
                a_point = connection.a
                b_point = connection.b

                if a_point.num_connection == 1 or a_point.num_connection == neighbour.max_connection_per_point or b_point.num_connection == 1 or b_point.num_connection == neighbour.max_connection_per_point:
                    valid_circuit = False
                if valid_circuit:
                    while True:
                        c_index = randint(0, circuit.point_num-1)
                        d_index = randint(0, circuit.point_num-1)

                        if c_index != d_index:
                            c_point = neighbour.point_list[c_index]
                            d_point = neighbour.point_list[d_index]
                            if c_point.num_connection < circuit.max_connection_per_point and d_point.num_connection < circuit.max_connection_per_point:
                                break
                    break
            connection.switch(c_point, d_point)
            neighbour.cost = neighbour.cost_calc()
            return neighbour
        
        def initial_t():
            os.system("cls")
            print("Gerando os 3 primeiros vizinhos para o cálculo de temperatura inicial...")

            init1 = neighbour(self.circuit).cost
            init2 = neighbour(self.circuit).cost
            init3 = neighbour(self.circuit).cost
            t = (init1+init2+init3)/3

            return t
        
        t = initial_t()
        #t = 500
        best_circuit = deepcopy(self.circuit) # melhor solucao
        best_solution = best_circuit.cost
        initial_solution = best_solution

        os.system("cls")
        print(f"==> Circuito inicial com {self.circuit.point_num} pontos e {self.circuit.connection_num} conexões: ")
        self.circuit.print()
        counter = 0
        print("\n==> Solução: \n")
        while t > 0.0001:
            counter += 1
            print(f". {counter}° iter cost = {self.circuit.cost:.{3}f}")
            for i in range(self.sa_max):
                new_circuit = neighbour(self.circuit)
                new_solution = new_circuit.cost
                current_solution = self.circuit.cost
                delta = new_solution - current_solution
                if delta < 0:
                    self.circuit = new_circuit
                    if new_solution < best_solution:
                        best_circuit = new_circuit
                        best_solution = best_circuit.cost
                else:
                    if randint(0, 100) < exp(-delta/t)*100:
                        self.circuit = new_circuit
                t = t*self.alpha
        print("")
        print("=> Circuito final após solução por Simulated Annealing: ")
        self.circuit.print()
        print(f"\n===> A soma de distâncias (custo) de conexões do circuito foi de {initial_solution:.3f} para {best_solution:.3f}")
        
                
