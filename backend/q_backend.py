from typing import List, Optional
from qiskit import QuantumCircuit, QuantumRegister, ClassicalRegister

class QuantumGameBackend:
    """Handles the quantum circuit logic for Quantum Tic-Tac-Toe.

    This class manages the initialization of quantum and classical registers
    and provides methods to apply quantum gates representing player moves.

    Attributes:
        grid_reg (QuantumRegister): 9 qubits representing the game squares.
        move_reg (QuantumRegister): 10 qubits for tracking move superposition.
        cl_reg (ClassicalRegister): 9 classical bits for square measurement.
        move_cl_reg (ClassicalRegister): 10 classical bits for move resolution.
        circuit (QuantumCircuit): The primary circuit used for the game state.
    """

    def __init__(self) -> None:
        """Initializes the quantum registers and the circuit."""
        self.grid_reg = QuantumRegister(9, name="grid")
        # Limited to 10 moves to maintain simulator stability (keeping total qubits < 30).
        self.move_reg = QuantumRegister(10, name="move")
        self.cl_reg = ClassicalRegister(9, name="measure")
        self.move_cl_reg = ClassicalRegister(10, name="move_measure")
        self.circuit = QuantumCircuit(self.grid_reg, self.move_reg, self.cl_reg, self.move_cl_reg)

    def make_spooky_move(self, move_index: int, s1: int, s2: int) -> None:
        """Applies a quantum move entangling two squares.

        Args:
            move_index (int): The unique index of the current move.
            s1 (int): The index of the first target square (0-8).
            s2 (int): The index of the second target square (0-8).
        """
        # Put the move qubit in superposition
        self.circuit.h(self.move_reg[move_index])
        
        # Entangle with first square
        self.circuit.cx(self.move_reg[move_index], self.grid_reg[s1])
        
        # Flip move qubit to handle the second square choice
        self.circuit.x(self.move_reg[move_index])
        
        # Entangle with second square
        self.circuit.cx(self.move_reg[move_index], self.grid_reg[s2])
