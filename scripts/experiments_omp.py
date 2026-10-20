import os
import sys
import subprocess

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
ROOT       = os.path.dirname(SCRIPT_DIR)

LAB2    = os.path.join(ROOT, "lab2")
EXE     = os.path.join(LAB2, "lab2_omp.exe")
INPUT   = os.path.join(LAB2, "input")
OUTPUT  = os.path.join(LAB2, "output")
LOGS    = os.path.join(LAB2, "logs")
GEN     = os.path.join(SCRIPT_DIR, "generate_matrix.py")
VERIFY  = os.path.join(SCRIPT_DIR, "verify.py")

SIZES     = [200, 400, 800, 1200, 1600, 2000]
THREADS   = [1, 2, 4, 8]
TOLERANCE = "1e-8"

os.makedirs(INPUT,  exist_ok=True)
os.makedirs(OUTPUT, exist_ok=True)
os.makedirs(LOGS,   exist_ok=True)

fileA = os.path.join(INPUT,  "matrix_a.txt")
fileB = os.path.join(INPUT,  "matrix_b.txt")
fileC = os.path.join(OUTPUT, "result.txt")

def gen(n):
    subprocess.run([sys.executable, GEN, str(n), fileA, fileB], check=True)

def run_bin(threads):
    env = os.environ.copy()
    env["OMP_NUM_THREADS"] = str(threads)
    info = os.path.join(OUTPUT, "info.txt")
    subprocess.run(
        [EXE, fileA, fileB, fileC, info],
        check=True, env=env, capture_output=True, text=True
    )
    # читаем info.txt
    d = {}
    with open(info, encoding="utf-8") as f:
        for line in f:
            if "=" in line:
                k, v = line.strip().split("=", 1)
                try:
                    d[k] = float(v)
                except ValueError:
                    pass
    return d

def parse_stdout(txt):
    d = {}
    for line in txt.splitlines():
        if "=" not in line:
            continue
        k, v = line.split("=", 1)
        k, v = k.strip(), v.strip()
        try:
            d[k] = float(v.rstrip("s").strip())
        except ValueError:
            pass
    return d

# ---------- 1) проверка корректности на n=200 ----------
print("=== Проверка корректности (n=200, threads=4) ===")
gen(200)
run_bin(4)
r = subprocess.run(
    [sys.executable, VERIFY, fileA, fileB, fileC, TOLERANCE],
    capture_output=True, text=True
)
print(r.stdout.strip())
if r.returncode != 0:
    print("Verification FAILED — серия не запущена.")
    sys.exit(1)

# ---------- 2) основная серия ----------
results = []

for n in SIZES:
    print(f"\n=== N = {n} ===")
    gen(n)
    for t in THREADS:
        print(f"  threads={t} ...", end=" ", flush=True)
        d = run_bin(t)

        n_val      = int(d.get("n", n))
        thr_val    = int(d.get("threads", t))
        time_val   = float(d.get("time_sec", 0.0))
        gflops_val = float(d.get("GFLOPS", 0.0))
        results.append((n_val, thr_val, time_val, gflops_val))
        print(f"time={time_val:.4f}s, GFLOPS={gflops_val:.2f}")

        # (опционально) сохранить info.txt как лог
        log_path = os.path.join(LOGS, f"n{n}_t{t}.log")
        with open(log_path, "w", encoding="utf-8") as f:
            f.write(f"n={n_val}\nthreads={thr_val}\ntime_sec={time_val}\nGFLOPS={gflops_val}\n")

# ---------- 3) сводная таблица ----------
base = {(n, 1): t for (n, th, t, _) in results if th == 1}

table_path = os.path.join(OUTPUT, "experiments_omp.txt")
with open(table_path, "w", encoding="utf-8") as f:
    f.write(f"{'N':>6} {'threads':>8} {'time_sec':>14} {'speedup':>10} "
            f"{'eff':>8} {'GFLOPS':>10}\n")
    for (n, t, time_val, gflops_val) in sorted(results):
        sp  = base[(n, 1)] / time_val if (n, 1) in base else 0.0
        eff = sp / t
        f.write(f"{n:>6} {t:>8} {time_val:>14.6f} {sp:>10.3f} "
                f"{eff:>8.3f} {gflops_val:>10.2f}\n")

print(f"\n[OK] Таблица сохранена: {table_path}")
print(f"[OK] Логи: {LOGS}")