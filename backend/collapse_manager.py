from typing import Dict, List, Optional, Tuple, Set
from qiskit import transpile
from qiskit_aer import QasmSimulator
from q_backend import QuantumGameBackend

class GraphState:
    """Manages the graph representation of quantum entanglement.

    This class tracks the relationships between squares on the grid and detects
    closed loops (cycles) that trigger quantum collapses.

    Attributes:
        adj (Dict[int, List[Tuple[int, int]]]): Adjacency list mapping square 
            indices to lists of (neighbor, move_id) tuples.
    """

    def __init__(self) -> None:
        """Initializes an empty graph for the 3x3 board."""
        self.adj: Dict[int, List[Tuple[int, int]]] = {i: [] for i in range(9)}

    def add_edge(self, u: int, v: int, move_id: int) -> None:
        """Adds a move edge between two squares in the graph.

        Args:
            u (int): Index of the first square.
            v (int): Index of the second square.
            move_id (int): Unique identifier for the move.
        """
        if v not in [edge[0] for edge in self.adj[u]]:
            self.adj[u].append((v, move_id))
            self.adj[v].append((u, move_id))

    def remove_edge(self, u: int, v: int) -> None:
        """Removes an edge between two squares.

        Args:
            u (int): Index of the first square.
            v (int): Index of the second square.
        """
        self.adj[u] = [item for item in self.adj[u] if item[0] != v]
        self.adj[v] = [item for item in self.adj[v] if item[0] != u]

    def detect_cycle(self) -> Optional[List[Tuple[int, int, int]]]:
        """Detects a cycle in the current graph state.

        Returns:
            Optional[List[Tuple[int, int, int]]]: A list of moves forming the cycle, 
            each as (u, v, move_id), or None if no cycle exists.
        """
        visited: Set[int] = set()
        parent: Dict[int, Tuple[Optional[int], Optional[int]]] = {} # node -> (parent, move_id)
        
        def get_cycle_info(start: int, end: int, last_move_id: int) -> List[Tuple[int, int, int]]:
            moves = [(start, end, last_move_id)]
            curr = start
            while curr != end:
                p, m_id = parent[curr]
                if p is None or m_id is None: break
                moves.append((p, curr, m_id))
                curr = p
            return moves

        for i in range(9):
            if i not in visited:
                stack: List[Tuple[int, Optional[int], Optional[int]]] = [(i, None, None)]
                while stack:
                    curr, p, m_id = stack.pop()
                    if curr not in visited:
                        visited.add(curr)
                        parent[curr] = (p, m_id)
                        for neighbor, edge_m_id in self.adj[curr]:
                            if neighbor == p: continue
                            if neighbor in visited: 
                                return get_cycle_info(curr, neighbor, edge_m_id)
                            stack.append((neighbor, curr, edge_m_id))
        return None

def trigger_collapse(backend: QuantumGameBackend, cycle_moves: List[Tuple[int, int, int]]) -> Dict[int, int]:
    """Resolves a quantum cycle into a classical state using a simulator.

    Args:
        backend (QuantumGameBackend): The quantum engine instance.
        cycle_moves (List[Tuple[int, int, int]]): The moves forming the cycle.

    Returns:
        Dict[int, int]: A mapping of move ID to the square it collapsed into.
    """
    if not cycle_moves:
        return {}

    # Pick a reality using a quantum superposition
    picker_id = cycle_moves[0][2]
    backend.circuit.h(backend.move_reg[picker_id])
    backend.circuit.measure(backend.move_reg[picker_id], backend.move_cl_reg[picker_id])
    
    simulator = QasmSimulator()
    transpiled = transpile(backend.circuit, simulator)
    job = simulator.run(transpiled, shots=1)
    result = job.result()
    bitstring = list(result.get_counts().keys())[0]
    
    # Parse the measured bit for the choice
    parts = bitstring.split()
    move_bits = parts[0] if len(parts) > 1 else bitstring
    choice = int(move_bits[::-1][picker_id])
    
    # Resolve the cycle based on the quantum choice
    resolution = {}
    for u, v, m_id in cycle_moves:
        resolution[m_id] = u if choice == 1 else v
        
    return resolution
