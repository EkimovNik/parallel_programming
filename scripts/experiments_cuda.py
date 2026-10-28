#!/usr/bin/env python3
import os, subprocess, sys

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
ROOT       = os.path.dirname(SCRIPT_DIR)
LAB4       = os.path.join(ROOT, "lab4")
EXE        = os.path.join(LAB4, "lab4_cuda.exe")
INPUT      = os.path.join(LAB4, "input")
OUTPUT     = os.path.join(LAB4, "output")
GEN        = os.path.join(SCRIPT_DIR, "generate_matrix.py")
VERIFY     = os.path.join(SCRIPT_DIR, "verify.py")

SIZES       = [200, 400, 800, 1200, 1600, 2000]
BLOCK_SIZES = [8, 16, 32]
TOLERANCE   = "0.1"

os.makedirs(INPUT,  exist_ok=True)
os.makedirs(OUTPUT, exist_ok=True)

fileA = os.path.join(INPUT,  "matrix_a.txt")
fileB = os.path.join(INPUT,  "matrix_b.txt")
fileC = os.path.join(OUTPUT, "result.txt")
fileInfo = os.path.join(OUTPUT, "info.txt")

results = []

print("=== CUDA Matrix Multiplication ===")
for n in SIZES:
    print(f"\n--- N = {n} ---")
    subprocess.run([sys.executable, GEN, str(n), fileA, fileB], check=True)
    
    for bs in BLOCK_SIZES:
        print(f"  Block {bs}x{bs} ...", end=" ", flush=True)
        
        res = subprocess.run([EXE, fileA, fileB, fileC, fileInfo, str(bs)], capture_output=True, text=True)
        if res.returncode != 0:
            print(f"ERROR: {res.stderr}")
            continue
            
       
        d = {}
        with open(fileInfo) as f:
            for line in f:
                if "=" in line:
                    k, v = line.strip().split("=", 1)
                    d[k] = v
        
        time_val = float(d.get("time_sec", 0))
        gflops_val = float(d.get("GFLOPS", 0))
        
      
        r = subprocess.run([sys.executable, VERIFY, fileA, fileB, fileC, TOLERANCE], capture_output=True, text=True)
        ok = (r.returncode == 0)
        
        print(f"time={time_val:.4f}s, GFLOPS={gflops_val:.2f}, verify={'OK' if ok else 'FAIL'}")
        results.append((n, bs, time_val, gflops_val, ok))


table_path = os.path.join(OUTPUT, "experiments_cuda.txt")
with open(table_path, "w") as f:
    f.write(f"{'N':>6} {'block':>6} {'time_sec':>14} {'GFLOPS':>10} {'verify':>8}\n")
    for (n, bs, t, g, ok) in results:
        f.write(f"{n:>6} {bs:>6} {t:>14.6f} {g:>10.2f} {'OK' if ok else 'FAIL':>8}\n")

print(f"\n[OK] Таблица сохранена: {table_path}")