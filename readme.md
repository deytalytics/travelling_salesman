# Parallel Ant Colony Optimization (ACO) for the Traveling Salesman Problem

Welcome! This project solves the classic **Traveling Salesman Problem (TSP)** using a smart hybrid approach: **Ant Colony Optimization (ACO)** combined with **2-Opt local search**, accelerated by **multiprocessing** (using all your CPU cores at once).

---

## What Does This Program Do?
1. **Asks You for Scale:** When you run the script, it asks how many cities you want to visit.
2. **Generates a Map:** It randomly scatters that many cities across a 1000x1000 grid.
3. **Simulates Digital Ants:** A colony of virtual ants explores different routes simultaneously across your computer's CPU cores. 
4. **Learns and Improves:** Ants leave "pheromones" on successful paths. Shorter paths get heavier pheromone trails, attracting more ants over successive iterations.
5. **Polishes the Paths:** Every ant cleans up its route using a 2-opt "rubber-band" uncrossing algorithm to get rid of unnecessary loops.
6. **Plots the Results:** Once finished, it pops up a clean Matplotlib graph showing your cities, the starting hub, and the final optimized travel route.

---

## Requirements

To run this script, you will need **Python 3** and the **Matplotlib** library for plotting graphs. 

You can install Matplotlib via your terminal or command prompt:
```bash
pip install matplotlib
```

---

## How to Run It

1. Save the Python script (e.g., as `tsp_solver.py`).
2. Open your terminal or command prompt in that folder.
3. Run the command:
   ```bash
   python tsp_solver.py
   ```
4. When prompted, type the number of cities you want to test (for example: `50`, `100`, or `250`) and press Enter.
5. Watch the iteration progress in your terminal, and view the final visual map when the window pops up!