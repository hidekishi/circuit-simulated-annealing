import lib
import simulated_annealing as sa

x = [12.1, 5, 20, 60, 95, 1, 30, 14.7, 9, 4.3, 1.2]
y = [15, 1, 90, 5, 123, 4, 98, 10, 2.4, 2.1, 0.8]

circuito = lib.circuit(5, 14, 4, x, y)
circuito.print_circuit()

teste = sa.sim_annealing(circuito)
teste.solution()