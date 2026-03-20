# ObfusQate (Qibo)

A collection of quantum circuit transformations and obfuscation techniques implemented using **Qibo**.

This project explores how quantum operations can be modified, hidden, or restructured while preserving their functionality.

---

## 🚀 Features

* Superposition-based transformations
* Entanglement-based obfuscation
* Cloaked and delayed quantum gates
* Composite and inverse gate constructions
* Superposition shrouding techniques
* Support for standard QASM circuits (Grover, QFT, Shor, etc.)

---

## 📦 Requirements

* Python 3.x
* qibo==0.2.21

---

## ⚙️ Installation

```bash
git clone <your-repo-link>
cd ObfusQate_Qibo
pip install -r requirements.txt
```

---

## ▶️ Usage

Run any module directly:

```bash
python superpositionOP_Qibo.py
```

or

```bash
python entangledOP_Qibo.py
```

Each script demonstrates a different obfuscation/transformation technique applied to quantum circuits.

---

## 📁 Project Structure

```
ObfusQate_Qibo/
│
├── superpositionOP_Qibo.py
├── entangledOP_Qibo.py
├── simpleEntanglementOP_Qibo.py
├── superpositionShroudOP_Qibo.py
├── cloakedGates_Qibo.py
├── delayedGates_Qibo.py
├── inverseGates_Qibo.py
├── compositeGates_Qibo.py
│
├── QASM Circuits/
│   ├── Grover(101).qasm
│   ├── QFT.qasm
│   ├── Shor.qasm
│   ├── Simon.qasm
│   ├── VQE.qasm
│   └── ...
│
└── requirements.txt
```

---

## 🧠 How It Works

The project applies different strategies to modify quantum circuits:

* **Superposition Obfuscation**: Embeds operations within superposed states
* **Entanglement Obfuscation**: Uses entangled qubits to mask logic
* **Gate Cloaking**: Hides operations through equivalent transformations
* **Delayed Gates**: Rearranges execution order without changing outcome
* **Inverse/Composite Gates**: Reconstructs circuits using mathematically equivalent forms

All transformations aim to preserve correctness while altering structure.

---

## 🧪 Example Circuits

Includes standard quantum algorithms:

* Grover's Search
* Quantum Fourier Transform (QFT)
* Shor’s Algorithm
* Simon’s Algorithm
* Deutsch-Jozsa (Balanced & Constant)
* Variational Quantum Eigensolver (VQE)

---

## ⚠️ Notes

* Built using Qibo simulator (no real hardware required)
* Uses Python built-in modules (sys, time, random, ast)
* Designed for experimentation, not production deployment

---

## 🛠️ Future Improvements

* Benchmark performance impact of obfuscation
* Add visualization of transformed circuits
* Support for more quantum frameworks (Qiskit, Cirq)
* Automate transformation pipelines

---

## 📜 License

MIT License
