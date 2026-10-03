"""
Генератор двух квадратных матриц со случайными числами.
"""
import sys
import random
import os


def generate_matrix(filename, size):
    """
    Создание файла с квадратной матрицей size x size.
    Формат файла: первая строка — размер N, далее N строк по N чисел.
    """
    os.makedirs(os.path.dirname(filename) or ".", exist_ok=True)

    with open(filename, 'w') as f:
        f.write(f"{size}\n")
        for _ in range(size):
            row = [f"{random.uniform(-10.0, 10.0):.15g}" for _ in range(size)]
            f.write(" ".join(row) + "\n")


if __name__ == "__main__":
    if len(sys.argv) != 4:
        print("Использование: py -3.12 generate_matrix.py <размер> <файл_A> <файл_B>")
        sys.exit(1)

    size = int(sys.argv[1])
    fileA = sys.argv[2]
    fileB = sys.argv[3]

    generate_matrix(fileA, size)
    generate_matrix(fileB, size)

    print(f"[OK] Матрицы {size}x{size} созданы: {fileA}, {fileB}")