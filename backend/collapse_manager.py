from qiskit import transpile
from qiskit_aer import QasmSimulator

class GraphState:
    def __init__(self):
        self.adj = {i: [] for i in range(9)}
    def add_edge(self, u, v, move_id):
        if v not in self.adj[u]:
            self.adj[u].append((v, move_id))
            self.adj[v].append((u, move_id))
    def remove_edge(self, u, v):
        
        self.adj[u] = [item for item in self.adj[u] if item[0] != v]
        self.adj[v] = [item for item in self.adj[v] if item[0] != u]
    def detect_cycle(self):
        visited = set()
        parent = {}
        def get_cycle_path(start, end):
            path = [start]
            curr = start
            while curr != end:
                curr = parent[curr]
                path.append(curr)
            return path
        for i in range(9):
            if i not in visited:
                stack = [(i, None)]
                while stack:
                    curr, p = stack.pop()
                    if curr not in visited:
                        visited.add(curr)
                        parent[curr] = p
                        for neighbor, m_id in self.adj[curr]:
                            if neighbor == p: continue
                            if neighbor in visited: return get_cycle_path(curr, neighbor)
                            stack.append((neighbor, curr))
        return None

def trigger_collapse(backend, cycle_nodes):
    for node in cycle_nodes:
        backend.circuit.measure(backend.grid_reg[node], backend.cl_reg[node])
    simulator = QasmSimulator()
    transpiled_circuit = transpile(backend.circuit, simulator)
    job = simulator.run(transpiled_circuit, shots=1)
    result = job.result()
    counts = result.get_counts()
    bitstring = list(counts.keys())[0]
    results_map = {}
    reversed_bits = bitstring[::-1]
    for node in cycle_nodes:
        results_map[node] = int(reversed_bits[node])
    return results_map
