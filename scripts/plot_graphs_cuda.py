#!/usr/bin/env python3
import os
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
ROOT       = os.path.dirname(SCRIPT_DIR)
LAB4       = os.path.join(ROOT, "lab4")
OUTPUT     = os.path.join(LAB4, "output")
TABLE      = os.path.join(OUTPUT, "experiments_cuda.txt")

GRAPH_TIME   = os.path.join(LAB4, "cuda_time_vs_size.png")
GRAPH_GFLOPS = os.path.join(LAB4, "cuda_gflops_vs_block.png")

data = {}
with open(TABLE, encoding="utf-8") as f:
    next(f)
    for line in f:
        p = line.split()
        if len(p) < 5: continue
        n, bs, t, g = int(p[0]), int(p[1]), float(p[2]), float(p[3])
        data[(n, bs)] = (t, g)

sizes  = sorted({k[0] for k in data})
blocks = sorted({k[1] for k in data})

# График 1: Время от размера
plt.figure(figsize=(9, 6))
for bs in blocks:
    xs = [n for n in sizes if (n, bs) in data]
    ys = [data[(n, bs)][0] for n in xs]
    plt.plot(xs, ys, marker='o', linewidth=2, label=f"Block {bs}x{bs}")
plt.xlabel("Размер матрицы N"); plt.ylabel("Время, с")
plt.title("CUDA: время умножения от размера матрицы")
plt.grid(True, linestyle='--', alpha=0.7); plt.legend()
plt.tight_layout(); plt.savefig(GRAPH_TIME, dpi=150); plt.close()
print(f"[OK] {GRAPH_TIME}")

# График 2: GFLOPS от размера блока
plt.figure(figsize=(9, 6))
for n in sizes:
    xs = [bs for bs in blocks if (n, bs) in data]
    ys = [data[(n, bs)][1] for bs in xs]
    plt.plot(xs, ys, marker='s', linewidth=2, label=f"N={n}")
plt.xlabel("Размер блока (потоков на сторону)"); plt.ylabel("GFLOPS")
plt.title("CUDA: производительность при разных конфигурациях блоков")
plt.grid(True, linestyle='--', alpha=0.7); plt.legend()
plt.tight_layout(); plt.savefig(GRAPH_GFLOPS, dpi=150); plt.close()
print(f"[OK] {GRAPH_GFLOPS}")