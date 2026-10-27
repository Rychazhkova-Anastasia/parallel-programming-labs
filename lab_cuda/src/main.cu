#include <iostream>
#include <fstream>
#include <vector>
#include <chrono>
#include <cuda_runtime.h>

#define TILE_SIZE 32

__global__ void matrixMulKernel(float* d_A, float* d_B, float* d_C, int N) {
    __shared__ float shared_A[TILE_SIZE][TILE_SIZE];
    __shared__ float shared_B[TILE_SIZE][TILE_SIZE];

    int row = blockIdx.y * TILE_SIZE + threadIdx.y;
    int col = blockIdx.x * TILE_SIZE + threadIdx.x;
    float sum = 0.0f;

    for (int t = 0; t < (N + TILE_SIZE - 1) / TILE_SIZE; ++t) {
        if (row < N && (t * TILE_SIZE + threadIdx.x) < N)
            shared_A[threadIdx.y][threadIdx.x] = d_A[row * N + t * TILE_SIZE + threadIdx.x];
        else
            shared_A[threadIdx.y][threadIdx.x] = 0.0f;

        if ((t * TILE_SIZE + threadIdx.y) < N && col < N)
            shared_B[threadIdx.y][threadIdx.x] = d_B[(t * TILE_SIZE + threadIdx.y) * N + col];
        else
            shared_B[threadIdx.y][threadIdx.x] = 0.0f;

        __syncthreads();

        for (int k = 0; k < TILE_SIZE; ++k)
            sum += shared_A[threadIdx.y][k] * shared_B[k][threadIdx.x];

        __syncthreads();
    }

    if (row < N && col < N)
        d_C[row * N + col] = sum;
}


std::vector<float> readMatrix(const std::string& filename, int& N) {
    std::ifstream infile(filename);
    if (!infile.is_open()) {
        std::cerr << "Ошибка: не удалось открыть файл " << filename << std::endl;
        exit(1);
    }
    infile >> N; 
    std::vector<float> matrix(N * N);
    for (int i = 0; i < N * N; ++i) {
        infile >> matrix[i];
    }
    return matrix;
}

int main() {
    int N;
    std::vector<float> h_A = readMatrix("../input/matrix_a.txt", N);
    std::vector<float> h_B = readMatrix("../input/matrix_b.txt", N);
    std::vector<float> h_C(N * N, 0.0f);
    
    std::cout << "Размер матриц из файлов: " << N << "x" << N << std::endl;
    size_t bytes = N * N * sizeof(float);

    float *d_A, *d_B, *d_C;
    cudaMalloc(&d_A, bytes);
    cudaMalloc(&d_B, bytes);
    cudaMalloc(&d_C, bytes);

    cudaMemcpy(d_A, h_A.data(), bytes, cudaMemcpyHostToDevice);
    cudaMemcpy(d_B, h_B.data(), bytes, cudaMemcpyHostToDevice);

    dim3 dimBlock(TILE_SIZE, TILE_SIZE);
    dim3 dimGrid((N + TILE_SIZE - 1) / TILE_SIZE, (N + TILE_SIZE - 1) / TILE_SIZE);

    cudaEvent_t start, stop;
    cudaEventCreate(&start);
    cudaEventCreate(&stop);

    cudaEventRecord(start);
    matrixMulKernel<<<dimGrid, dimBlock>>>(d_A, d_B, d_C, N);
    cudaEventRecord(stop);
    cudaEventSynchronize(stop);

    float milliseconds = 0;
    cudaEventElapsedTime(&milliseconds, start, stop);

    cudaMemcpy(h_C.data(), d_C, bytes, cudaMemcpyDeviceToHost);

    std::ofstream out_result("../output/result.txt");
    for (int i = 0; i < N; ++i) {
        for (int j = 0; j < N; ++j) {
            out_result << h_C[i * N + j] << " ";
        }
        out_result << "\n";
    }
    out_result.close();


    std::ofstream out_info("../output/info.txt");
    out_info << "Matrix size: " << N << "x" << N << "\n";
    out_info << "CUDA Kernel Time: " << milliseconds << " ms\n";
    out_info << "Tile Size: " << TILE_SIZE << "x" << TILE_SIZE << "\n";
    out_info.close();

    std::cout << "Время на GPU: " << milliseconds << " ms" << std::endl;
    std::cout << "Результаты сохранены в result.txt и info.txt" << std::endl;

    cudaFree(d_A);
    cudaFree(d_B);
    cudaFree(d_C);

    return 0;
}
