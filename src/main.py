import lib
import simulated_annealing as sa

x = [12.1, 14.7, 9, 4.3, 1.2]
y = [15, 10, 2.4, 2.1, 0.8]

circuito = lib.circuit(5, 8, 4, x, y)
circuito.print_circuit()

teste = sa.sim_annealing(circuito)
print(teste.cost_calc())
novo = teste.gen_neighbour()
novo.print_circuit()