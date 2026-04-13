from qiskit import QuantumCircuit, QuantumRegister, ClassicalRegister

class QuantumGameBackend:
    def __init__(self):
        self.grid_reg = QuantumRegister(9, name="grid")
        # Increased limit from 9 to 50 to allow longer games.
        self.move_reg = QuantumRegister(50, name="move")
        self.cl_reg = ClassicalRegister(9, name="measure")
        self.circuit = QuantumCircuit(self.grid_reg, self.move_reg, self.cl_reg)

    def make_spooky_move(self, move_index: int, s1: int, s2: int):
        self.circuit.h(self.move_reg[move_index])
        self.circuit.cx(self.move_reg[move_index], self.grid_reg[s1])
        self.circuit.x(self.move_reg[move_index])
        self.circuit.cx(self.move_reg[move_index], self.grid_reg[s2])
