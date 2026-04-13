# ⚛️ Quantum Tic-Tac-Toe

![Demo](demo.gif)

[![React](https://img.shields.io/badge/React-20232A?style=for-the-badge&logo=react&logoColor=61DAFB)](https://reactjs.org/)
[![Next.js](https://img.shields.io/badge/Next.js-000000?style=for-the-badge&logo=next.js&logoColor=white)](https://nextjs.org/)
[![Python](https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white)](https://www.python.org/)
[![Qiskit](https://img.shields.io/badge/Qiskit-6929C4?style=for-the-badge&logo=qiskit&logoColor=white)](https://qiskit.org/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg?style=for-the-badge)](https://opensource.org/licenses/MIT)

## Important Mentality

Forget everything you know about Tic-Tac-Toe. This isn't just a game of X’s and O’s; it’s a high-stakes battle of **probabilities, superposition, and entanglement**. In this version, players don’t just claim a square—they exist in two places at once. Reality only takes shape when the universe is forced to choose, collapsing the quantum web into a definitive victory or a chaotic draw. Built with **IBM’s Qiskit**.

## 🧠 The "Why"

Quantum mechanics is often dismissed as a series of abstract equations in a textbook. I built this just to understand how the concepts of superposition, entanglement and quantum measurement can be modelled in the web. By mapping quantum states to a familiar 3x3 grid, players can *feel* the Spooky Action at a Distance™ and understand how measurement fundamentally alters the state of a system. Shout out to GDG OAU quantum computing community, that gave me this challenge.

---

## 🛠️ How it Works (The Physics & Logic)

This project models complex quantum phenomena using Python and the IBM Qiskit SDK. Here is the technical breakdown of how the physics is translated into code.

### 1. Superposition
In quantum mechanics, **Superposition** is the phenomenon where a particle can exist in multiple states simultaneously until it is observed. In this game, every move is a "Spooky Move" that spans two squares.

We model this by assigning a **Move Qubit** to every turn. We use a **Hadamard Gate** (`h`) to put this move into a state of 0 and 1 at the same time, and then link it to the grid squares using **Controlled-NOT (CNOT)** gates.

**From `q_backend.py`:**
```python
def make_spooky_move(self, move_index: int, s1: int, s2: int):
    # Step 1: Create superposition on the move qubit
    self.circuit.h(self.move_reg[move_index])
    
    # Step 2: Entangle the move qubit with Square 1
    self.circuit.cx(self.move_reg[move_index], self.grid_reg[s1])
    
    # Step 3: Flip the move qubit and entangle with Square 2
    # This creates the "Either Square 1 OR Square 2" logic
    self.circuit.x(self.move_reg[move_index])
    self.circuit.cx(self.move_reg[move_index], self.grid_reg[s2])
```

### 2. Entanglement
**Entanglement** occurs when qubits become linked such that the state of one instantly depends on the state of another, regardless of distance. In the context of this game, entanglement happens when different moves share the same square.

If move $A$ is in squares $(1, 2)$ and move $B$ is in squares $(2, 3)$, they are now entangled through square $2$. If square $2$ eventually collapses to move $A$, move $B$ is "pushed" into square $3$.

We use an undirected graph to track these links. Every move is an edge, and every square is a node. 

### 3. Measurement & State Collapse
In quantum computing, **Measurement** is the act of observing a qubit, which forces it to "collapse" into a classical state ($0$ or $1$). In our project, measurement is only triggered when the entanglement graph detects a **cycle**—a closed loop of moves that "locks" the board.

#### How the Graph Algorithm Works:
We use a **Depth-First Search (DFS)** algorithm inside `collapse_manager.py` to constantly monitor the board. When the DFS finds a path that returns to a starting node, it signals that a "Loop of Entanglement" has formed, and the universe must now choose a reality.

#### Triggering the Collapse:
Once a cycle is detected, we tell the Qiskit engine to measure the specific qubits involved in that cycle.

**From `collapse_manager.py`:**
```python
def trigger_collapse(backend, cycle_nodes):
    # Apply measurement to only the qubits involved in the cycle
    for node in cycle_nodes:
        backend.circuit.measure(backend.grid_reg[node], backend.cl_reg[node])
    
    # Run the simulation on the QasmSimulator
    simulator = QasmSimulator()
    job = simulator.run(transpile(backend.circuit, simulator), shots=1)
    result = job.result().get_counts()
    
    # Convert the quantum bitstring into classical grid positions
    # (Extracts which square became 'X' or 'O')
```

---

## 🎮 How to Play (Strategy Guide)

Quantum Tic-Tac-Toe is a game of management, not just positioning. To win, you must master the "Chain."

### Basic Rules
1. **Choose Two Squares**: On your turn, click any two empty or partially occupied squares. Your mark will appear in both in a "spooky" (faded) state.
2. **Form a Cycle**: You win by getting three of your collapsed marks in a row. However, marks only collapse when a cycle is formed.
3. **The Collapse**: When a cycle forms, the last player to move gets to "choose" the collapse orientation in some variants, but in this version, the **Quantum Simulator** determines the outcome based on probability.

### Tips to Win
- **The "Parasite" Strategy**: Don't just try to build your own lines. Entangle your moves with your opponent's "hot" squares. By doing this, you force them into a collapse where they might lose their position.
- **Aggressive Cycling**: If you have two marks near each other, try to close a cycle as fast as possible. The sooner you force a measurement, the sooner your marks become "real" and block your opponent.
- **The Corner Trap**: In classical Tic-Tac-Toe, corners are strong. In Quantum, corners are even stronger because they are easier to link into multiple potential cycles.
- **Don't Flee Entanglement**: Beginners often try to play in empty squares to "stay safe." Expert players embrace entanglement; the person who controls the largest "web" usually controls the final collapse.

---

## 🤖 The "Fierce" AI (PvE Mode)

Highlighting the `bot_player.py`: The AI doesn't use simple Minimax. It analyzes the **Entanglement Graph** to aggressively hijack your superposition web. It looks for the most connected nodes and poisons them with its own marks, ensuring that when the board collapses, it has the highest probability of coming out on top.

## ⚡ Getting Started

### Prerequisites
- Python 3.10+
- Node.js 18+

### 1. Setup Backend
```bash
cd backend
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
uvicorn api:app --reload --port 8000
```

### 2. Setup Frontend
```bash
cd frontend
npm install
npm run dev
```

---
Built with ⚛️ for the **GDG OAU Quantum Community**.
