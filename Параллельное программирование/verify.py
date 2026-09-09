import numpy as np

def load_matrix(filename):
    with open(filename, 'r') as filename:
        n = int(filename.readline())
        matrix = []
        for i in range(n):
            row = list(map(float, filename.readline().split()))
            matrix.append(row)
    return np.array(matrix)

print("------ВЕРИФИКАЦИЯ---")

try:
    A = load_matrix("lab1/input/matrix_a.txt")
    B = load_matrix("lab1/input/matrix_b.txt")
    my_result = load_matrix("lab1/output/result.txt")
    
    correct_result = np.matmul(A, B)
    
    max_error = np.max(np.abs(correct_result - my_result))
    print(f"Максимальная ошибка: {max_error:.10f}")
    
    if max_error < 1e-6:
        print("ВЕРИФИКАЦИЯ ПРОЙДЕНА!")
		
    else:
        print("ВЕРИФИКАЦИЯ НЕ ПРОЙДЕНА!")
        print(f"Ошибка слишком большая: {max_error:.10f}")
        
#------------------------
    print("\n--- Матрица A ---")
    print(A)
    print("\n--- Матрица B ---")
    print(B)
    print("\n--- Результат (NumPy) ---")
    print(correct_result)
    print("\n--- Результат (ваша программа) ---")
    print(my_result)
        
except FileNotFoundError as e:
    print(f" Ошибка: файл не найден!")
    print(f"  {e}")
  
except Exception as e:
    print(f" Ошибка: {e}")