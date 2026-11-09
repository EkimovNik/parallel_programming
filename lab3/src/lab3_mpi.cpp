
#include <mpi.h>          
#include <cstdlib>
#include <iostream>
#include <fstream>
#include <vector>

typedef std::vector<std::vector<double> > Matrix;

Matrix readMatrix(const char* filename, int& n) {
    std::ifstream fin(filename);
    if (!fin) { std::cerr << "Cannot open " << filename << "\n"; std::exit(1); }
    fin >> n;
    Matrix m(n, std::vector<double>(n));
    for (int i = 0; i < n; ++i)
        for (int j = 0; j < n; ++j) fin >> m[i][j];
    return m;
}

void writeMatrix(const char* filename, const Matrix& m) {
    std::ofstream fout(filename);
    int n = (int)m.size();
    fout.precision(17);
    fout << n << "\n";
    for (int i = 0; i < n; ++i)
        for (int j = 0; j < n; ++j)
            fout << m[i][j] << (j + 1 < n ? ' ' : '\n');
}

int main(int argc, char** argv) {
    MPI_Init(&argc, &argv);
    int rank, size;
    MPI_Comm_rank(MPI_COMM_WORLD, &rank);
    MPI_Comm_size(MPI_COMM_WORLD, &size);

    int n = 0;
    Matrix A, B, C;
    double start_time = 0, end_time = 0;

    if (rank == 0) {
        A = readMatrix(argv[1], n);
        B = readMatrix(argv[2], n);
        C.resize(n, std::vector<double>(n, 0.0));
        start_time = MPI_Wtime();
    }

    MPI_Bcast(&n, 1, MPI_INT, 0, MPI_COMM_WORLD);

    std::vector<double> flatB(n * n);
    if (rank == 0) {
        for (int i = 0; i < n; ++i)
            for (int j = 0; j < n; ++j) flatB[i * n + j] = B[i][j];
    }
    MPI_Bcast(&flatB[0], n * n, MPI_DOUBLE, 0, MPI_COMM_WORLD);

    int rows_per_proc = n / size;
    int remainder = n % size;
    int local_rows = rows_per_proc + (rank < remainder ? 1 : 0);

    std::vector<double> localA(local_rows * n);
    std::vector<int> sendcounts(size), displs(size);
    int offset = 0;
    for (int i = 0; i < size; ++i) {
        int r = rows_per_proc + (i < remainder ? 1 : 0);
        sendcounts[i] = r * n;
        displs[i] = offset;
        offset += r * n;
    }

    std::vector<double> flatA;
    double* ptrA = 0;
    if (rank == 0) {
        flatA.resize(n * n);
        for (int i = 0; i < n; ++i)
            for (int j = 0; j < n; ++j) flatA[i * n + j] = A[i][j];
        ptrA = &flatA[0];
    }
    MPI_Scatterv(ptrA, &sendcounts[0], &displs[0],
                 MPI_DOUBLE, &localA[0], local_rows * n, MPI_DOUBLE, 0, MPI_COMM_WORLD);

    std::vector<double> localC(local_rows * n, 0.0);
    for (int i = 0; i < local_rows; ++i) {
        for (int k = 0; k < n; ++k) {
            double a = localA[i * n + k];
            for (int j = 0; j < n; ++j)
                localC[i * n + j] += a * flatB[k * n + j];
        }
    }

    std::vector<double> flatC;
    double* ptrC = 0;
    if (rank == 0) {
        flatC.resize(n * n);
        ptrC = &flatC[0];
    }
    MPI_Gatherv(&localC[0], local_rows * n, MPI_DOUBLE,
                ptrC, &sendcounts[0], &displs[0],
                MPI_DOUBLE, 0, MPI_COMM_WORLD);

    if (rank == 0) {
        end_time = MPI_Wtime();
        for (int i = 0; i < n; ++i)
            for (int j = 0; j < n; ++j) C[i][j] = flatC[i * n + j];
        writeMatrix(argv[3], C);
        std::cout << "n = " << n << "\n";
        std::cout << "procs = " << size << "\n";
        std::cout << "time = " << (end_time - start_time) << " s\n";
    }

    MPI_Finalize();
    return 0;
}