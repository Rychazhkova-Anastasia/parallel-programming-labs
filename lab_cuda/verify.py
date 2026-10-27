import numpy as np
import sys

def verify():
    try:
        cuda_result = np.loadtxt('output/result.txt')
        ref_result = np.loadtxt('output/reference_result.txt')
    except Exception as e:
        print(f"Ошибка при чтении файлов: {e}")
        sys.exit(1)

    max_error = np.max(np.abs(cuda_result - ref_result))
    print(f"Максимальная ошибка: {max_error:.6f}")
    
    if max_error < 1e-3:
        print("ВЕРИФИКАЦИЯ ПРОЙДЕНА! Результаты совпадают.")
    else:
        print("ОШИБКА! Результаты не совпадают.")
        sys.exit(1)

if __name__ == "__main__":
    verify()
