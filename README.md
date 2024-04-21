# QForest-Graviton-24

QForest Graviton 2.0 2024 - Team Quantum Harvesters

## Setup and installations

1. **Recommended:** create a Python virtual environment to avoid installing the required packages globally and prevent version conflicts

```powershell
python -m venv your-env
```

2. Activate the virtual environment

```powershell
path/to/your-env/Scripts/Activate.ps1
```

3. Install the required packages

```powershell
cd QForest-Graviton-24
python -m ensurepip --upgrade
python -m pip install -r requirements.txt
```

## Run the server

To run the Flask backend,

```powershell
cd QForest-Graviton-24
python VRP-explorations\server.py
```

To run the Vite app,

```powershell
cd final_frontend
npm run dev
```

## References

This project is based on the following publications and existing works:

[1] [Classical heuristical TSP solver for demonstration - VRP-explorations](https://github.com/AsishMandoi/VRP-explorations/tree/main)

[2] [Travelling Salesman Problem - Qiskit Tutorials](https://qiskit-community.github.io/qiskit-optimization/tutorials/06_examples_max_cut_and_tsp.html)

[3] [Ising model - Wikipedia](https://en.wikipedia.org/wiki/Ising_model)

[4] [arXiv:1805.10928v1 [quant-ph] ](https://github.com/Qiskit/qiskit-ibm-provider "https://arxiv.org/abs/1805.10928")

## Contributors

Team Quantum Harvesters, Gravition-2.0 2024

* [Samar Garg](https://github.com/Samsonnyyeet)
* [Vibhav Tiwari](https://github.com/vibhav950)
* [Shreevathsa GP](https://github.com/ShreevathsaGP)
* [Sai Tarun A](https://github.com/skullcrushr11)
