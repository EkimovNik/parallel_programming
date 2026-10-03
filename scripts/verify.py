# Верификация результата умножения матриц через NumPy.
import sys
import numpy as np


def read_matrix(filename):
    with open(filename, 'r') as f:
        size = int(f.readline().strip())
        matrix = np.loadtxt(f, dtype=float)

    if matrix.shape != (size, size):
        raise ValueError(f"{filename}: ожидалось {size}x{size}, получено {matrix.shape}")
    return matrix


if __name__ == "__main__":
    if len(sys.argv) != 5:
        print("Использование: python verify.py <A> <B> <C> <допуск>")
        sys.exit(1)

    fileA = sys.argv[1]
    fileB = sys.argv[2]
    fileC_cpp = sys.argv[3]
    tolerance = float(sys.argv[4])

    A = read_matrix(fileA)
    B = read_matrix(fileB)
    C_cpp = read_matrix(fileC_cpp)

    C_numpy = np.dot(A, B)

    if np.allclose(C_cpp, C_numpy, atol=tolerance, rtol=0):
        max_diff = np.max(np.abs(C_cpp - C_numpy))
        print(f"[OK] ВЕРИФИКАЦИЯ ПРОЙДЕНА (макс. расхождение: {max_diff:.2e})")
        sys.exit(0)
    else:
        max_diff = np.max(np.abs(C_cpp - C_numpy))
        print(f"[FAIL] ОШИБКА: макс. расхождение = {max_diff}")
        sys.exit(2)