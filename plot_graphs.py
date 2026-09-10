import matplotlib.pyplot as plt
import numpy as np

sizes = [500, 1000, 1500, 2000, 2500]
threads = [1, 2, 4, 8, 16, 20]

data = {
    500:  [0.0822, 0.0474, 0.0281, 0.0220, 0.0215, 0.0223],
    1000: [0.6149, 0.3303, 0.1691, 0.1418, 0.0934, 0.0851],
    1500: [2.3561, 1.2862, 0.7493, 0.4681, 0.2620, 0.2476],
    2000: [6.2398, 3.6045, 1.9153, 1.1266, 0.6853, 0.6491],
    2500: [12.8155, 7.1140, 3.9024, 2.2984, 1.4342, 1.4751],
}

fig, axes = plt.subplots(1, 2, figsize=(16, 6))

# ГРАФИК 1: Время выполнения
for size in sizes:
    axes[0].plot(threads, data[size], 'o-', label=f'{size}x{size}')

axes[0].set_xlabel('Число потоков')
axes[0].set_ylabel('Время (сек)')
axes[0].set_title('Время выполнения от числа потоков')
axes[0].set_yscale('log')
axes[0].legend()
axes[0].grid(True, alpha=0.3)

# ГРАФИК 2: Ускорение
for size in sizes:
    times = data[size]
    speedup = [times[0] / t for t in times]
    axes[1].plot(threads, speedup, 'o-', label=f'{size}x{size}')

# Идеальное ускорение
axes[1].plot(threads, threads, 'k--', alpha=0.5, label='Идеальное')

axes[1].set_xlabel('Число потоков')
axes[1].set_ylabel('Ускорение (раз)')
axes[1].set_title('Ускорение OpenMP')
axes[1].legend()
axes[1].grid(True, alpha=0.3)

plt.tight_layout()
plt.savefig('lab1_openmp/output/graphs.png', dpi=150)
plt.show()

print("Графики сохранены в lab1_openmp/output/graphs.png")