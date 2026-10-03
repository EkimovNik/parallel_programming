# Лабораторные работы по параллельному программированию

**Автор:** Екимов Никита  
**Группа:** 6214  
**Курс:** Параллельное программирование

---
## Список работ

-  [Лаба №1 — Умножение матриц (последовательная версия)](lab1/README.md)

---
## Структура репозитория

```
parallel_programming/
├── lab1/
│   ├── src/lab1.cpp
│   ├── input/
│   ├── output/
│   └── README.md
├── scripts/
│   ├── generate_matrix.py
│   ├── verify.py
│   ├── experiments.py
│   └── plot_graphs.py
└── README.md
```
---

## Как запускать скрипты

Все скрипты запускаются из папки `scripts/`:

```cmd
cd scripts
py -3.12 experiments.py
py -3.12 plot_graphs.py