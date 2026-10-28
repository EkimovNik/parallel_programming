#!/usr/bin/env python3
# Серия экспериментов для ЛР5 (Stanford CS149, Program 1)
# Запускает mandelbrot.exe с разным числом потоков, собирает ускорение
# и сохраняет результаты в lab5/experiments_cs149.txt

import os
import sys
import subprocess
import re
import matplotlib.pyplot as plt


SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
ROOT       = os.path.dirname(SCRIPT_DIR)
LAB5_DIR   = os.path.join(ROOT, "lab5", "prog1_mandelbrot_threads")


EXE = os.path.join(LAB5_DIR, "mandelbrot.exe")
if not os.path.exists(EXE):
    EXE = os.path.join(LAB5_DIR, "mandelbrot")

OUTPUT_TXT = os.path.join(ROOT, "lab5", "experiments_cs149.txt")
OUTPUT_PNG = os.path.join(ROOT, "lab5", "speedup_view1.png")

THREADS = [1, 2, 4, 8, 16]


env = os.environ.copy()
msys_bin = "C:\\msys64\\ucrt64\\bin"
if os.path.exists(msys_bin):
    env["PATH"] = msys_bin + ";" + env.get("PATH", "")

def run_mandelbrot(threads, view=1):
    print(f"  Running {threads} threads (view {view})...", end=" ", flush=True)
    cmd = [EXE, "-t", str(threads), "--view", str(view)]
    
   
    res = subprocess.run(cmd, capture_output=True, text=True, env=env)
    

    match = re.search(r"\(([\d.]+)x speedup from", res.stdout)
    if match:
        speedup = float(match.group(1))
        print(f"Speedup: {speedup:.2f}x")
        return speedup
    else:
        print(f"Error: Could not parse speedup.")
        print(f"Output: {res.stdout[:100]}...")
        print(f"Error output: {res.stderr[:100]}...")
        return None

results_view1 = []
results_view2 = []

print("=== View 1 ===")
for t in THREADS:
    sp = run_mandelbrot(t, view=1)
    if sp: results_view1.append((t, sp))

print("\n=== View 2 (8 threads) ===")
sp2 = run_mandelbrot(8, view=2)
if sp2: results_view2.append((8, sp2))


with open(OUTPUT_TXT, "w", encoding="utf-8") as f:
    f.write("N_Threads | Speedup(View 1) | Speedup(View 2)\n")
    f.write("----------|-----------------|----------------\n")
    for t, sp in results_view1:
        sp2_val = f"{sp2:.2f}" if (t == 8 and sp2) else "-"
        f.write(f"{t:9} | {sp:15.2f} | {sp2_val:>14}\n")

print(f"\n[OK] Таблица сохранена: {OUTPUT_TXT}")


if results_view1:
    threads_list = [r[0] for r in results_view1]
    speedups_list = [r[1] for r in results_view1]

    plt.figure(figsize=(8, 5))
    plt.plot(threads_list, speedups_list, marker='o', linewidth=2, label='Реальное ускорение (View 1)')
    plt.plot(threads_list, threads_list, linestyle='--', color='gray', label='Идеальное (y=x)')
    plt.title('Ускорение генерации фрактала Мандельброта (View 1)')
    plt.xlabel('Количество потоков')
    plt.ylabel('Ускорение')
    plt.grid(True, linestyle=':', alpha=0.7)
    plt.xticks(threads_list)
    plt.legend()
    plt.savefig(OUTPUT_PNG, dpi=150, bbox_inches='tight')
    print(f"[OK] График сохранен: {OUTPUT_PNG}")