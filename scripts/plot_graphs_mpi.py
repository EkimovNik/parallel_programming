#!/usr/bin/env python3
import os
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
ROOT       = os.path.dirname(SCRIPT_DIR)
LAB3       = os.path.join(ROOT, "lab3")
TABLE      = os.path.join(LAB3, "output", "results.txt")

GRAPH_TIME   = os.path.join(LAB3, "mpi_time_vs_size.png")
GRAPH_SPEEDUP = os.path.join(LAB3, "mpi_speedup_vs_procs.png")

data = {}
with open(TABLE, encoding="utf-8") as f:
    next(f)
    next(f) 
    for line in f:
        p = line.split()
        if len(p) < 3: continue
        n = int(p[0])
        procs = int(p[1])
        time = float(p[2])
        data[(n, procs)] = time

sizes = sorted({k[0] for k in data})
procs = sorted({k[1] for k in data})

# График 1: Время от размера N
plt.figure(figsize=(9, 6))
for p_val in procs:
    xs = [n for n in sizes if (n, p_val) in data]
    ys = [data[(n, p_val)] for n in xs]
    plt.plot(xs, ys, marker='o', linewidth=2, label=f"{p_val} процессов")
plt.xlabel("Размер матрицы N"); plt.ylabel("Время, с")
plt.title("MPI: Время умножения от размера матрицы")
plt.grid(True, linestyle='--', alpha=0.7); plt.legend()
plt.tight_layout(); plt.savefig(GRAPH_TIME, dpi=150); plt.close()
print(f"[OK] {GRAPH_TIME}")

# График 2: Ускорение от числа процессов
plt.figure(figsize=(9, 6))
for n in sizes:
    if (n, 1) not in data: continue
    base = data[(n, 1)]
    xs = [p for p in procs if (n, p) in data]
    ys = [base / data[(n, p)] for p in xs]
    plt.plot(xs, ys, marker='s', linewidth=2, label=f"N={n}")
plt.plot(procs, procs, 'k--', linewidth=1, alpha=0.6, label="идеал")
plt.xlabel("Число процессов"); plt.ylabel("Ускорение S(p)")
plt.title("MPI: Ускорение от числа процессов")
plt.grid(True, linestyle='--', alpha=0.7); plt.legend()
plt.tight_layout(); plt.savefig(GRAPH_SPEEDUP, dpi=150); plt.close()
print(f"[OK] {GRAPH_SPEEDUP}")