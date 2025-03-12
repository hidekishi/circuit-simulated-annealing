import numpy as np
from random import randint

class point:
    def __init__(self, id, x, y):
        self.x = x
        self.y = y
        self.id = id
        self.connection_num = 0 
        self.connected_points = []
    def add_connection(self):
        self.connection_num += 1
    def sub_connection(self):
        self.connection_num -= 1

class connection:
    def __init__(self, a_point, b_point):
        a_point.add_connection()
        b_point.add_connection()
        a_point.connected_points.append(b_point)
        b_point.connected_points.append(a_point)
        self.a_point = a_point
        self.b_point = b_point
        self.cost = self.cost_calc()
    def cost_calc(self):
        a_x = self.a_point.x
        a_y = self.a_point.y
        b_x = self.b_point.x
        b_y = self.b_point.y
        return np.sqrt(np.power(a_x-b_x, 2)+np.power(a_y-b_y, 2))
    def switch(self, c_point, d_point):
        self.a_point.sub_connection()
        self.b_point.sub_connection()
        self.a_point.connected_points.remove(self.b_point)
        self.b_point.connected_points.remove(self.a_point)
        c_point.add_connection()
        d_point.add_connection()
        c_point.connected_points.append(d_point)
        d_point.connected_points.append(c_point)
        self.a_point = c_point
        self.b_point = d_point
        self.cost = self.cost_calc()
class circuit:
    def __init__(self, x_list, y_list, point_num, connection_num, max_connection_per_point):
        self.points_list = []
        self.connections_list = []
        self.point_num = point_num
        self.connection_num = connection_num
        self.max_connection_per_point = max_connection_per_point
        # INICIALIZA PONTOS COM COORDENADAS ENTRADAS
        for i in range(point_num):
            self.points_list.append(point(i, x_list[i], y_list[i]))
        # INICIALIZA CONEXOES ALEATORIAS
        while(True):
            for p in self.points_list:
                p.connection_num = 0
            self.connections_list = []
            for i in range(connection_num):
                # GARANTE QUE OS DOIS PONTOS SELECIONADOS SERAO DIFERENTES
                while(True):
                    a_index = randint(0, point_num-1)
                    b_index = randint(0, point_num-1)
                    if a_index != b_index:
                        if self.points_list[a_index].connection_num < max_connection_per_point and self.points_list[b_index].connection_num < max_connection_per_point:
                            break
                self.connections_list.append(connection(self.points_list[a_index], self.points_list[b_index]))
            if self.is_circuit_valid():
                break
        self.cost_calc()
        # IMPRIME AS CONEXOES DO CIRCUITO INICIAL PRONTO
        #print("Circuito inicial gerado: ")
        #self.print_circuit()
        #self.print_points_stats()
        #print(f"Custo inicial da solução = {self.cost}")
    # FUNCAO PARA PRINTAR AS CONEXOES DO CIRCUITO
    def print_circuit(self):
        for i, c in enumerate(self.connections_list):
            print(f"{i} -> {c.a_point.id} --- {c.b_point.id}; Custo = {c.cost}")
    # FUNCAO PARA PRINTAR O NUMERO DE CONEXOES DE CADA PONTO
    def print_points_stats(self):
        for p in self.points_list:
            print(f"{p.id} --> {p.connection_num} conexões; Pontos conectados = ", end='')
            for po in p.connected_points:
                print(f"{po.id}", end=' ')
            print()
    # FUNCAO PARA CALCULO DE CUSTO DO CIRCUITO
    def cost_calc(self):
        cost = 0
        for c in self.connections_list:
            cost += c.cost
        self.cost = cost
    # CHECA VALIDADE DO CIRCUITO
    def is_circuit_valid(self):
        # CHECA SE O NUMERO DE CONEXOES DO CIRCUITO BATE COM O NUMERO REQUERIDO
        if len(self.connections_list) < self.connection_num:
            print("ERRO: Número de conexões insuficientes na lista!")
            return False
        # CHECA SE TODOS OS PONTOS POSSUEM PELO MENOS UMA CONEXAO
        while(True):
            for p in self.points_list:
                if p.connection_num == 0:
                    print("ERRO: Circuito possui ponto(s) desconectado(s)")
                    return False
            break
        return True
# CHECA CONECTIVIDADE DO GRAFO
def is_circuit_connected(circuit):
    points = circuit.points_list
