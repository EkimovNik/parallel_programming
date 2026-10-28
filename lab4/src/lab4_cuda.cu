
#include <iostream>
#include <fstream>
#include <vector>
#include <cstdlib>
#include <cuda_runtime.h>

using Matrix = std::vector<std::vector<float>>;

template<int TILE>
__global__ void matrixMulTiled(const float* A, const float* B, float* C, int N) {
    __shared__ float As[TILE][TILE];
    __shared__ float Bs[TILE][TILE];

    int bx = blockIdx.x, by = blockIdx.y;
    int tx = threadIdx.x, ty = threadIdx.y;
    int row = by * TILE + ty;
    int col = bx * TILE + tx;
    float sum = 0.0f;

    for (int m = 0; m < (N + TILE - 1) / TILE; ++m) {
        if (row < N && (m * TILE + tx) < N) As[ty][tx] = A[row * N + m * TILE + tx];
        else As[ty][tx] = 0.0f;

        if ((m * TILE + ty) < N && col < N) Bs[ty][tx] = B[(m * TILE + ty) * N + col];
        else Bs[ty][tx] = 0.0f;

        __syncthreads();
        for (int k = 0; k < TILE; ++k) sum += As[ty][k] * Bs[k][tx];
        __syncthreads();
    }
    if (row < N && col < N) C[row * N + col] = sum;
}

Matrix readMatrix(const std::string& filename, int& n) {
    std::ifstream fin(filename);
    if (!fin) { std::cerr << "Cannot open " << filename << "\n"; std::exit(1); }
    fin >> n;
    Matrix m(n, std::vector<float>(n));
    for (int i = 0; i < n; ++i)
        for (int j = 0; j < n; ++j) fin >> m[i][j];
    return m;
}

void writeMatrix(const std::string& filename, const Matrix& m) {
    std::ofstream fout(filename);
    int n = (int)m.size();
    fout.precision(9);
    fout << n << "\n";
    for (int i = 0; i < n; ++i)
        for (int j = 0; j < n; ++j)
            fout << m[i][j] << (j + 1 < n ? ' ' : '\n');
}

int main(int argc, char** argv) {
    if (argc < 6) { std::cerr << "Usage: A.txt B.txt C.txt info.txt <blockSize>\n"; return 1; }

    int n; Matrix A = readMatrix(argv[1], n);
    Matrix B = readMatrix(argv[2], n);
    if ((int)B.size() != n) { std::cerr << "Size mismatch\n"; return 2; }

    int blockSize = std::atoi(argv[5]);
    if (blockSize != 8 && blockSize != 16 && blockSize != 32) {
        std::cerr << "blockSize must be 8, 16 or 32\n"; return 3;
    }

    size_t bytes = (size_t)n * n * sizeof(float);
    float* d_A, * d_B, * d_C;
    cudaError_t err;

    err = cudaMalloc(&d_A, bytes); if (err != cudaSuccess) { std::cerr << "cudaMalloc A failed: " << cudaGetErrorString(err) << "\n"; return 4; }
    err = cudaMalloc(&d_B, bytes); if (err != cudaSuccess) { std::cerr << "cudaMalloc B failed: " << cudaGetErrorString(err) << "\n"; return 5; }
    err = cudaMalloc(&d_C, bytes); if (err != cudaSuccess) { std::cerr << "cudaMalloc C failed: " << cudaGetErrorString(err) << "\n"; return 6; }

    std::vector<float> h_A(n * n), h_B(n * n);
    for (int i = 0; i < n; ++i)
        for (int j = 0; j < n; ++j) { h_A[i * n + j] = A[i][j]; h_B[i * n + j] = B[i][j]; }

    cudaMemcpy(d_A, h_A.data(), bytes, cudaMemcpyHostToDevice);
    cudaMemcpy(d_B, h_B.data(), bytes, cudaMemcpyHostToDevice);

    dim3 block(blockSize, blockSize);
    dim3 grid((n + blockSize - 1) / blockSize, (n + blockSize - 1) / blockSize);

    cudaEvent_t start, stop;
    cudaEventCreate(&start); cudaEventCreate(&stop);
    cudaEventRecord(start);

    if (blockSize == 8)       matrixMulTiled<8> << <grid, block >> > (d_A, d_B, d_C, n);
    else if (blockSize == 16) matrixMulTiled<16> << <grid, block >> > (d_A, d_B, d_C, n);
    else                      matrixMulTiled<32> << <grid, block >> > (d_A, d_B, d_C, n);

    err = cudaGetLastError();
    if (err != cudaSuccess) {
        std::cerr << "CUDA kernel launch error: " << cudaGetErrorString(err) << "\n";
        return 7;
    }

    cudaEventRecord(stop); cudaEventSynchronize(stop);
    float ms = 0; cudaEventElapsedTime(&ms, start, stop);

    std::vector<float> h_C(n * n);
    cudaMemcpy(h_C.data(), d_C, bytes, cudaMemcpyDeviceToHost);

    Matrix C(n, std::vector<float>(n));
    for (int i = 0; i < n; ++i)
        for (int j = 0; j < n; ++j) C[i][j] = h_C[i * n + j];
    writeMatrix(argv[3], C);

    double sec = ms / 1000.0;
    double ops = 2.0 * n * n * n;
    double gflops = (ops / sec) / 1e9;

    std::ofstream fout(argv[4]);
    fout.precision(9);
    fout << "n=" << n << "\n";
    fout << "block=" << blockSize << "x" << blockSize << "\n";
    fout << "grid=" << grid.x << "x" << grid.y << "\n";
    fout << "time_sec=" << sec << "\n";
    fout << "GFLOPS=" << gflops << "\n";

    std::cout << "n=" << n << " block=" << blockSize << "x" << blockSize
        << " time=" << sec << "s GFLOPS=" << gflops << "\n";

    cudaFree(d_A); cudaFree(d_B); cudaFree(d_C);
    return 0;
}