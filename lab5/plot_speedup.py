import matplotlib.pyplot as plt
import os


threads = [1, 2, 4, 8, 16]
speedups = [0.99, 2.05, 4.00, 7.97, 8.97]


ideal = threads

plt.figure(figsize=(8, 5))
plt.plot(threads, speedups, marker='o', linewidth=2, markersize=8, label='Реальное ускорение (View 1)')
plt.plot(threads, ideal, linestyle='--', color='gray', label='Идеальное ускорение (y=x)')

plt.title('Ускорение генерации фрактала Мандельброта (View 1)', fontsize=14)
plt.xlabel('Количество потоков', fontsize=12)
plt.ylabel('Ускорение (Speedup)', fontsize=12)
plt.grid(True, linestyle=':', alpha=0.7)
plt.xticks(threads)
plt.yticks(range(0, 11, 2))
plt.legend()


output_path = os.path.join(os.path.dirname(__file__), 'speedup_view1.png')
plt.savefig(output_path, dpi=150, bbox_inches='tight')
print(f"[OK] График сохранен: {output_path}")