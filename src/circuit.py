import numpy as np
from random import randint
from copy import deepcopy
import os

# CLASSE DO PONTO
class points:
    def __init__(self, x, y, id):
        self.id = id
        self.x = x
        self.y = y
        self.num_connection = 0

    def add_connection(self):
        self.num_connection += 1
    
    def sub_connection(self):
        self.num_connection -= 1

# CLASSE DA CONEXAO ENTRE DOIS PONTOS
class connection:
    def __init__(self, a_point, b_point):
        self.a = deepcopy(a_point)
        self.b = deepcopy(b_point)
        self.cost = self.cost_calc()

    def cost_calc(self):
        return np.sqrt((self.a.x - self.b.x)**2 + (self.a.y - self.b.y)**2)
    
    def switch(self, a, b):
        self.a.sub_connection()
        self.b.sub_connection()
        self.a = deepcopy(a)
        self.b = deepcopy(b)
        self.a.add_connection()
        self.b.add_connection()
        self.cost = self.cost_calc()

class circuit:
    def __init__(self, x_list, y_list, point_num, connection_num, max_connection_per_point):
        self.point_list = []
        self.point_num = point_num
        self.connection_list = []
        self.connection_num = connection_num
        self.max_connection_per_point = max_connection_per_point

        os.system("cls")
        print(f"Gerando o circuito inicial com {self.point_num} pontos e {self.connection_num} conexões... ")

        # cria lista de pontos com as coordenadas fornecidas
        for i in range(self.point_num):
            self.point_list.append(points(x_list[i], y_list[i], i))
        
        # cria lista de conexoes com pontos aleatorios
        while True:
            valid_circuit = True
            #print(f"numero de conexoes {connection_num}")
            for i in range(connection_num):
                while True:
                    a_index = randint(0, self.point_num-1)
                    b_index = randint(0, self.point_num-1)
                    if a_index != b_index and self.point_list[a_index].num_connection < self.max_connection_per_point and self.point_list[b_index].num_connection < self.max_connection_per_point:
                        break
                a_point = self.point_list[a_index]
                b_point = self.point_list[b_index]
                #print(a_point.id, b_point.id)
                self.connection_list.append(connection(a_point, b_point))
                a_point.add_connection()
                b_point.add_connection()
            for point in self.point_list:
                if point.num_connection == 0:
                    valid_circuit = False
                    break
            if valid_circuit:
                break

        self.cost = self.cost_calc()
    
    def cost_calc(self):
        sum = 0
        for connection in self.connection_list:
            sum += connection.cost
        return sum
    
    def print(self):
        for i, connection in enumerate(self.connection_list):
            print(f"{i}-> {connection.a.id} <---> {connection.b.id} = {connection.cost:.{3}f}")
        print(f"Custo = {self.cost:.{3}f}")