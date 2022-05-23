from extend_graph import *

# num: the size of the matrix
# graph.run_XOR3(): search for the circuit with 2/3-input XOR gates
# graph.run_XOR3_XOR4(): search for the circuit with 2/3/4-input XOR gates

# for each circuit, we have three lines: area/depth/No.

num = 32

graph = ExtendGraph(num)  # size

# graph.run_XOR3()
graph.run_XOR3_XOR4()
