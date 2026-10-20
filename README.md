# Лабораторные работы по параллельному программированию

**Автор:** Екимов Никита  
**Группа:** 6214  
**Курс:** Параллельное программирование

---
## Список работ

- [Лаба №1 — Умножение матриц (последовательная версия)](lab1/README.md)
- [Лаба №2 — Умножение матриц (OpenMP)](lab2/README.md)

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
├── scripts/
│   ├── generate_matrix.py
│   ├── verify.py
│   ├── experiments.py
│   ├── plot_graphs.py
│   ├── experiments_omp.py    
│   └── plot_graphs_omp.py     
└── README.md
```
---

## Как запускать скрипты

Все скрипты запускаются из папки `scripts/` (для ЛР1):

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