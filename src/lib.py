#import random
from random import randint
import numpy as np

class circuit_point:
    def __init__(self, id, x, y):
        self.id = id
        self.x = x
        self.y = y
        self.connection_num = 0
    def add_connection(self):
        self.connection_num += 1
    def sub_connection(self):
        self.connection_num -= 1

class circuit_connection:
    def __init__(self, o_point, d_point):
        self.a_point = o_point
        self.b_point = d_point

class circuit:
    def __init__(self, num_points, num_connect, max_conn, x_positions, y_positions):
        self.max_connection = max_conn
        self.num_connections = num_connect
        # CHECAGEM SE O NUMERO DE PONTOS INFORMADO != NUMERO DE PONTOS PASSADOS
        if num_points != len(x_positions) or num_points != len(y_positions):
            print("Número de pontos indicado é diferente do número de coordenadas passadas. A operação seguirá apenas levando em consideração o número de coordenadas!")
        self.num_points = len(x_positions)
        # INICIALIZACAO DE PONTOS A SEREM CONECTADOS
        self.points_list = []
        index = 0
        for i in range(self.num_points):
            self.points_list.append(circuit_point(i, x_positions[i], y_positions[i]))
            index += 1
        # INICIALIZACAO DE CONECCOES ATRIBUIDAS ENTRE PONTOS ALEATORIAMENTE
        self.connections_list = [] # Armazena os pontos que ainda nao foram conectados pelo menos uma vez
        while True:
            for i in range(num_connect): # Gera uma solucao inicial
                while True:
                    a_index = randint(0, self.num_points-1)
                    b_index = randint(0, self.num_points-1)
                    if b_index != a_index and self.points_list[a_index].connection_num < max_conn and self.points_list[b_index].connection_num < max_conn:
                        break
                self.connections_list.append(circuit_connection(self.points_list[a_index], self.points_list[b_index]))
                self.points_list[a_index].add_connection()
                self.points_list[b_index].add_connection()

            valid_solution = True # Checa se a solucao inicial e valida levando em consideracao que todos os pontos devem estar conectados
            for connection in self.connections_list:
                if connection.a_point.connection_num == 0 or connection.b_point.connection_num == 0:
                    valid_solution = False
            if valid_solution:
                break

    def cost_calc(self):
        distance = 0
        for edge in self.connections_list:
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

    def print_circuit(self):
        for i, connection in enumerate(self.connections_list):
            print(f"Aresta {i}-> {connection.a_point.id}--{connection.b_point.id}")