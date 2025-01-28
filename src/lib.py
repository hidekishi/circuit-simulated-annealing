#import random
from random import randint

class circuit_point:
    def __init__(self, id, x, y):
        self.id = id
        self.x = x
        self.y = y
        self.connection_num = 0
    def add_connection(self):
        self.connection_num += 1

class circuit_connection:
    def __init__(self, o_point, d_point):
        self.origin_point = o_point
        self.destin_point = d_point

class circuit:
    def __init__(self, num_points, num_connect, max_conn, x_positions, y_positions):
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
        non_assigned_points = list(range(0, self.num_points))
        for i in range(num_connect):
            while True:
                a_index = randint(0, self.num_points-1)
                b_index = randint(0, self.num_points-1)
                if b_index != a_index and self.points_list[a_index].connection_num < max_conn and self.points_list[b_index].connection_num < max_conn:
                    break
            if a_index in non_assigned_points:
                non_assigned_points.remove(a_index) # Remove o ponto conectado da lista de nao conectados
            if b_index in non_assigned_points:
                non_assigned_points.remove(b_index) # Remove o ponto conectado da lista de nao conectados
            self.connections_list.append(circuit_connection(self.points_list[a_index], self.points_list[b_index]))

    def print_circuit(self):
        for i, connection in enumerate(self.connections_list):
            print(f"Aresta {i}-> {connection.origin_point.id}--{connection.destin_point.id}")