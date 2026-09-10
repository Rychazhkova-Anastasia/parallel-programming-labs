import subprocess
import os
import re

sizes = [500, 1000, 1500, 2000, 2500]
threads = [1, 2, 4, 8, 16, 20]

print()
print("=" * 75)
print("ЭКСПЕРИМЕНТЫ: OpenMP умножение матриц")
print("=" * 75)
print()
print(f"{'Размер':<8} | {'Потоки':<7} | {'Время (сек)':<12} | {'Ускорение':<10} | {'Эффективность':<12}")
print("-" * 75)

results = []

for size in sizes:
    subprocess.run(["python", "generate_matrix.py", str(size)], capture_output=True)
    
    baseline = None
    
    for t in threads:
        env = os.environ.copy()
        env["OMP_NUM_THREADS"] = str(t)
        
        result = subprocess.run(
            ["main.exe"],
            cwd=r"lab1_openmp\src",
            shell=True,
            capture_output=True,
            text=True,
            env=env
        )
        
        match = re.search(r"time: ([\d.]+) sec", result.stdout)
        elapsed = float(match.group(1)) if match else 0
        
        if t == 1:
            baseline = elapsed
        
        speedup = baseline / elapsed if elapsed > 0 else 0
        efficiency = (speedup / t * 100) if t > 0 else 0
        
        print(f"{size:<8} | {t:<7} | {elapsed:<12.4f} | {speedup:<10.2f} | {efficiency:<12.1f}%")
        results.append([size, t, elapsed, speedup, efficiency])
    
    print("-" * 75)

os.makedirs("lab1_openmp/output", exist_ok=True)
with open("lab1_openmp/output/experiments.txt", "w", encoding="utf-8") as f:
    f.write("Размер | Потоки | Время (сек) | Ускорение | Эффективность\n")
    f.write("-" * 60 + "\n")
    for r in results:
        f.write(f"{r[0]} | {r[1]} | {r[2]:.4f} | {r[3]:.2f} | {r[4]:.1f}%\n")

print()
print("Результаты сохранены в lab1_openmp/output/experiments.txt")