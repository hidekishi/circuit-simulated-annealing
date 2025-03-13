from circuit import circuit, point, connection, is_circuit_connected
from random import randint
from copy import deepcopy
import matplotlib.pyplot as plt
import numpy as np

class simulated_annealing:
    def __init__(self, circuit, sa_max=3, alpha_rate=0.9):
        self.circuit = circuit
        self.original_circuit = deepcopy(circuit)
        self.sa_max = sa_max
        self.alpha = alpha_rate
        self.best_solution = self.solution()
    def solution(self):
        # EXIBICAO DA SOLUCAO INICIAL
        print("Circuito inicial: ")
        self.circuit.print_circuit()
        self.circuit.print_points_stats()
        print(f"Custo da solução inicial = {self.circuit.cost}")
        self.plot_graph("./grafico/inicial.png")
        # GERA UM VIZINHO COM BASE NO CIRCUITO ATUAL
        def generate_neighbour(original_circuit):
            neighbour_circuit = deepcopy(original_circuit)
            # SELECIONA A CONEXAO QUE VAI SER RETIRADA
            while True:
                switch_connection_index = randint(0, len(neighbour_circuit.connections_list)-1)
                switch_connection = neighbour_circuit.connections_list[switch_connection_index]
                if switch_connection.a_point.connection_num > 1 or switch_connection.b_point.connection_num > 1:
                    break
            # GERA A NOVA CONEXAO
            while True:
                c_index = randint(0, neighbour_circuit.point_num-1)
                d_index = randint(0, neighbour_circuit.point_num-1)
                c_point = neighbour_circuit.points_list[c_index]
                d_point = neighbour_circuit.points_list[d_index]
                if c_index != d_index:
                        if neighbour_circuit.points_list[c_index].connection_num < neighbour_circuit.max_connection_per_point and neighbour_circuit.points_list[d_index].connection_num < neighbour_circuit.max_connection_per_point:
                            break
            switch_connection.switch(c_point, d_point)
            neighbour_circuit.cost_calc()
            #print(f"\nVizinho criado retirando a conexao {switch_connection_index} e criando uma nova entre {c_point.id} --- {d_point.id}")
            #neighbour_circuit.print_circuit()
            #neighbour_circuit.print_points_stats()
            #print(f"Custo atualizado = {neighbour_circuit.cost}")
            return neighbour_circuit
        # DEFINE A TEMPERATURA INICIAL COM BASE NA MEDIA DE CUSTO DE 3 VIZINHOS
        def initial_t():
            v1 = generate_neighbour(self.circuit).cost
            v2 = generate_neighbour(self.circuit).cost
            v3 = generate_neighbour(self.circuit).cost
            return (v1+v2+v3)/3
        while True:
            self.circuit = deepcopy(self.original_circuit)
            best_solution = 999
            t = initial_t()
            counter = 0
            iteration_string = ""
            while t > 0.0001:
                counter += 1
                iteration_string = iteration_string + f". {counter}° iter cost = {self.circuit.cost:.{3}f}\n"
                #print(f". {counter}° iter cost = {self.circuit.cost:.{3}f}")
                for i in range(self.sa_max):
                    new_circuit = generate_neighbour(self.circuit)
                    new_solution = new_circuit.cost
                    current_solution = self.circuit.cost
                    delta = new_solution - current_solution
                    if delta < 0:
                        self.circuit = new_circuit
                        if new_solution < best_solution:
                            best_circuit = new_circuit
                            best_solution = best_circuit.cost
                    else:
                        if randint(0, 100) < np.exp(-delta/t)*100:
                            self.circuit = new_circuit
                    t = t*self.alpha
            self.circuit = best_circuit
            if self.circuit.is_circuit_valid():
                break
        print(iteration_string)
        print("Circuito de melhor custo: ")
        self.circuit.print_circuit()
        self.circuit.print_points_stats()
        print(f"Custo da melhor solução = {best_solution}")
        self.plot_graph("./grafico/melhor.png")
        return best_solution
    
    def plot_graph(self, filename):
        fig, ax = plt.subplots()

        x_coords = []
        y_coords = []
        circuit = self.circuit
        
        for i in range(circuit.point_num):
            x_coords.append(circuit.points_list[i].x)
            y_coords.append(circuit.points_list[i].y)
        
        ax.scatter(x_coords, y_coords, color='blue', label='Points')

        for i in range(len(x_coords)):
            ax.text(x_coords[i], y_coords[i], str(i), fontsize=12, verticalalignment='bottom', horizontalalignment='right')
    
        
        connections = circuit.connections_list
        for conn in connections:
            p1 = conn.a_point
            p2 = conn.b_point
            ax.plot([p1.x, p2.x], [p1.y, p2.y], 'k-', linewidth=1)
        
        plt.xlabel('X')
        plt.ylabel('Y')
        plt.legend()
        plt.grid()
        plt.savefig(filename, dpi=300, bbox_inches='tight')
        plt.close()
