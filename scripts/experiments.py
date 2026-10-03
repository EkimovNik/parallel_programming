# Серия экспериментов: прогоняем lab1.exe для разных N и собираем время в таблицу.
import os
import sys
import subprocess
import time

# Размеры матриц 
SIZES = [200, 400, 800, 1200, 1600, 2000]

# Пути относительно папки scripts
LAB_DIR = os.path.join("..", "lab1")
EXE = os.path.join(LAB_DIR, "lab1.exe")
INPUT = os.path.join(LAB_DIR, "input")
OUTPUT = os.path.join(LAB_DIR, "output")
GEN = "generate_matrix.py"

os.makedirs(INPUT, exist_ok=True)
os.makedirs(OUTPUT, exist_ok=True)

results = []

for N in SIZES:
    print(f"\n=== N = {N} ===")

    fileA = os.path.join(INPUT, "matrix_a.txt")
    fileB = os.path.join(INPUT, "matrix_b.txt")
    fileC = os.path.join(OUTPUT, "result.txt")
    fileInfo = os.path.join(OUTPUT, "info.txt")

    # Генерация матриц через Python
    print(f"Генерация матриц {N}x{N}...")
    subprocess.run(
        [sys.executable, GEN, str(N), fileA, fileB],
        check=True
    )

    # Запуск программы на С++
    print(f"Запуск {EXE}...")
    t0 = time.time()
    subprocess.run([EXE, fileA, fileB, fileC, fileInfo], check=True)
    wall = time.time() - t0

    # Чтение time_sec из info-файла
    time_sec = None
    with open(fileInfo, encoding="utf-8") as f:
        for line in f:
            if line.startswith("time_sec="):
                time_sec = float(line.strip().split("=")[1])

    results.append((N, N*N, time_sec, wall))
    print(f"N={N}, time={time_sec:.4f} сек (wall={wall:.4f})")

# Запись файла в файл
table_path = os.path.join(OUTPUT, "experiments.txt")
with open(table_path, "w", encoding="utf-8") as f:
    f.write(f"{'N':>6} {'N^2':>12} {'time_sec':>14} {'wall_sec':>14}\n")
    for N, vol, t, w in results:
        f.write(f"{N:>6} {vol:>12} {t:>14.6f} {w:>14.6f}\n")

print(f"\n[OK] Таблица сохранена: {table_path}")