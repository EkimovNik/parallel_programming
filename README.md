# Лабораторные работы по параллельному программированию

**Автор:** Екимов Никита  
**Группа:** 6214  
**Курс:** Параллельное программирование

---
## Список работ

- [Лаба №1 — Умножение матриц (последовательная версия)](lab1/README.md)
- [Лаба №2 — Умножение матриц (OpenMP)](lab2/README.md)
- [Лаба №3 — Умножение матриц (MPI)](lab3/README.md) *(в процессе)*
- [Лаба №4 — Умножение матриц (CUDA)](lab4/README.md) *(в процессе)*
- [Лаба №5 — Stanford CS149 Asst1 (Program 1)](lab5/README.md)

---
## Структура репозитория

```
parallel_programming/
├── lab1/
│   ├── src/lab1.cpp
│   ├── input/
│   ├── output/
│   └── README.md
├── lab2/
│   ├── src/lab2_omp.cpp
│   ├── input/
│   ├── output/
│   ├── speedup.png
│   ├── efficiency.png
│   ├── time_vs_size.png
│   └── README.md
├── lab3/                         <-- (ЛР3, в процессе)
│   └── README.md
├── lab4/                         <-- (ЛР4, в процессе)
│   └── README.md
├── lab5/
│   ├── common/
│   │   ├── CycleTimer.h
│   │   ├── ppm.cpp
│   │   └── tasksys.cpp
│   ├── prog1_mandelbrot_threads/
│   │   ├── main.cpp
│   │   ├── mandelbrotSerial.cpp
│   │   ├── mandelbrotThread.cpp
│   │   └── Makefile
│   ├── experiments_cs149.txt
│   ├── speedup_view1.png
│   └── README.md
├── scripts/
│   ├── generate_matrix.py
│   ├── verify.py
│   ├── experiments.py
│   ├── plot_graphs.py
│   ├── experiments_omp.py
│   ├── plot_graphs_omp.py
│   └── experiments_cs149.py
├── .gitignore
└── README.md
```

---
## Как запускать скрипты

Для ЛР1 скрипты запускаются из папки `scripts/`:

```cmd
cd scripts
py -3.12 experiments.py
py -3.12 plot_graphs.py
```

Для ЛР2 скрипты запускаются из корня репозитория:

```cmd
py -3.12 scripts\experiments_omp.py
py -3.12 scripts\plot_graphs_omp.py
```

Для ЛР5 скрипт автотестирования запускается из корня репозитория (требует собранного `mandelbrot.exe` в `lab5/prog1_mandelbrot_threads/`):

```cmd
py -3.12 scripts\experiments_cs149.py
```