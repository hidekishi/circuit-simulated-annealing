from circuit import point, connection, circuit
from sim_annealing import simulated_annealing

with open("input.txt", "r") as file:
    lines = file.readlines()

point_num = int(lines[0])
connection_num = int(lines[1])
max_conn = int(lines[2])
x = [float(x) for x in lines[3].split()]
y = [float(x) for x in lines[4].split()]

circuito = circuit(x, y, point_num, connection_num, max_conn)
teste = simulated_annealing(circuito)
print(teste.best_solution)