import numpy as np
import sys
import os

size = int(sys.argv[1]) if len(sys.argv) > 1 else 200

os.makedirs("lab1_openmp/src/input", exist_ok=True)

A = np.random.rand(size, size)
B = np.random.rand(size, size)

np.savetxt("lab1_openmp/src/input/matrix_a.txt", A, fmt="%.6f", header=str(size), comments='')
np.savetxt("lab1_openmp/src/input/matrix_b.txt", B, fmt="%.6f", header=str(size), comments='')

print(f"Матрицы {size}x{size} созданы!")