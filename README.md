# Automate — Finite Automata Algorithms

> Academic project developed as part of my Formal Languages & Automata course at Sorbonne Université

A Python implementation of core finite automata algorithms, covering determinization (NFA → DFA), minimization, complementation, and language recognition. The project was an introduction to formal language theory and automata-based computation.

## 🛠️ Tech Stack

- **Core Technologies**: Python 3
- **Tools & Environment**: Makefile, Graphviz (optional — automata visualization)

## 📦 Installation & Setup

### Prerequisites

- Python 3.9+

### Instructions

```bash
# 1. Clone the repository
git clone https://github.com/Tinshea/Automate.git
cd Automate

# 2. Run
python main.py

# OR with Make
make run
```

## ⚙️ Implemented Algorithms

| Algorithm | Description |
|---|---|
| NFA → DFA (subset construction) | Converts a non-deterministic automaton to an equivalent deterministic one |
| DFA minimization (Hopcroft) | Reduces a DFA to its minimal equivalent form |
| Complementation | Builds the complement automaton recognizing the language's complement |
| Language recognition | Tests whether a word is accepted by a given automaton |
| Concatenation / Union | Operations on automata for language composition |

## 🗂️ Project Structure

```
Automate/
├── automate.py         # Automaton class (states, transitions, alphabet)
├── algorithms.py       # Determinization, minimization, operations
├── main.py             # Entry point and demo
└── tests/              # Test cases
```

## 👤 Author

**Malek Bouzarkouna** — Sorbonne Université

## 📄 License

No license specified.
