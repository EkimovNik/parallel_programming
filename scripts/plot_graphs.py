# Построение графика зависимости времени умножения матриц от размера N.
import os
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

OUTPUT = os.path.join("..", "lab1", "output")
TABLE = os.path.join(OUTPUT, "experiments.txt")
GRAPH = os.path.join(OUTPUT, "graph.png")

# Чтение таблицы
sizes, times = [], []
with open(TABLE, encoding="utf-8") as f:
    next(f) 
    for line in f:
        parts = line.split()
        sizes.append(int(parts[0]))
        times.append(float(parts[2]))

# Построение графика
plt.figure(figsize=(9, 6))
plt.plot(sizes, times, marker='o', linewidth=2, color='#0066cc')
plt.xlabel("Размер матрицы N", fontsize=12)
plt.ylabel("Время выполнения, сек", fontsize=12)
plt.title("Зависимость времени умножения матриц от N", fontsize=13)
plt.grid(True, linestyle='--', alpha=0.7)
plt.tight_layout()
plt.savefig(GRAPH, dpi=150)
print(f"[OK] График сохранён: {GRAPH}")