More Inputs Makes Difference: Implementations of Linear Layers Using Gates with More Than Two Inputs.


'Implementations' contains all the implementations in two libraries.


We require Python3.


'CONSTANT' contains the cost of each gate. We provide two libraries.

Then, write the circuit in 'seq.txt' (s-XOR) or 'myseq.txt' (g-XOR).

If we use 'seq.txt', we just add 'self.ReadFromXiang()' in function 'run_XOR3_XOR4()' and 'run_XOR3()' in 'extend_graph.py' to transform the s-XOR circuit into g-XOR circuit.

Then, modify the number in 'main.py' representing the size of the matrix.

Finally, run 'main.py'.





In the result, we can obtain the circuit areas with 2/3-input xor gates and 2/3/4-input xor gates.

We provide an example with AES.
Run 'main.py' directly, and we can obtain the circuit with 243 GE.
