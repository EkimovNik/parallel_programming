import os
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
ROOT       = os.path.dirname(SCRIPT_DIR)
LAB2       = os.path.join(ROOT, "lab2")
OUTPUT     = os.path.join(LAB2, "output")
TABLE      = os.path.join(OUTPUT, "experiments_omp.txt")

GRAPH_SPEEDUP = os.path.join(LAB2, "speedup.png")
GRAPH_EFF     = os.path.join(LAB2, "efficiency.png")
GRAPH_TIME    = os.path.join(LAB2, "time_vs_size.png")

# ---------- чтение таблицы ----------
# Формат: N threads time_sec speedup eff GFLOPS
data = {}
with open(TABLE, encoding="utf-8") as f:
    next(f)
    for line in f:
        parts = line.split()
        if len(parts) < 6:
            continue
        n  = int(parts[0])
        t  = int(parts[1])
        ts = float(parts[2])
        sp = float(parts[3])
        ef = float(parts[4])
        gf = float(parts[5])
        data[(n, t)] = (ts, sp, ef, gf)

sizes   = sorted({k[0] for k in data})
threads = sorted({k[1] for k in data})

# ---------- 1) Ускорение S(p) для разных N ----------
plt.figure(figsize=(9, 6))
for n in sizes:
    xs = [t for t in threads if (n, t) in data]
    ys = [data[(n, t)][1] for t in xs]
    plt.plot(xs, ys, marker='o', linewidth=2, label=f"N={n}")
plt.plot(threads, threads, 'k--', linewidth=1, alpha=0.6, label="идеал")
plt.xlabel("Число потоков p", fontsize=12)
plt.ylabel("Ускорение S(p)", fontsize=12)
plt.title("Ускорение OpenMP-перемножения от числа потоков", fontsize=13)
plt.grid(True, linestyle='--', alpha=0.7)
plt.legend(fontsize=10)
plt.tight_layout()
plt.savefig(GRAPH_SPEEDUP, dpi=150)
plt.close()
print(f"[OK] {GRAPH_SPEEDUP}")

# ---------- 2) Эффективность E(p) ----------
plt.figure(figsize=(9, 6))
for n in sizes:
    xs = [t for t in threads if (n, t) in data]
    ys = [data[(n, t)][2] for t in xs]
    plt.plot(xs, ys, marker='s', linewidth=2, label=f"N={n}")
plt.axhline(1.0, color='k', linestyle='--', linewidth=1, alpha=0.6, label="идеал")
plt.xlabel("Число потоков p", fontsize=12)
plt.ylabel("Эффективность E(p) = S(p)/p", fontsize=12)
plt.title("Эффективность OpenMP-перемножения", fontsize=13)
plt.grid(True, linestyle='--', alpha=0.7)
plt.legend(fontsize=10)
plt.tight_layout()
plt.savefig(GRAPH_EFF, dpi=150)
plt.close()
print(f"[OK] {GRAPH_EFF}")

# ---------- 3) Время от размера N для разных p ----------
plt.figure(figsize=(9, 6))
for t in threads:
    xs = [n for n in sizes if (n, t) in data]
    ys = [data[(n, t)][0] for n in xs]
    plt.plot(xs, ys, marker='o', linewidth=2, label=f"p={t}")
plt.xlabel("Размер матрицы N", fontsize=12)
plt.ylabel("Время выполнения, сек", fontsize=12)
plt.title("Зависимость времени умножения от N (разное число потоков)", fontsize=13)
plt.grid(True, linestyle='--', alpha=0.7)
plt.legend(fontsize=10)
plt.tight_layout()
plt.savefig(GRAPH_TIME, dpi=150)
plt.close()
print(f"[OK] {GRAPH_TIME}")