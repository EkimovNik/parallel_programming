#include <iostream>
#include <fstream>
#include <sstream>
#include <vector>
#include <string>
#include <chrono>
#include <cstdlib>
#include <cctype>
#include <omp.h>

using Matrix = std::vector<std::vector<double>>;

static bool isBlankOrComment(const std::string& s) {
    for (char c : s) {
        if (std::isspace((unsigned char)c)) continue;
        return c == '#';
    }
    return true;
}

static Matrix readMatrix(const std::string& filename, int& n) {
    std::ifstream fin(filename);
    if (!fin) { std::cerr << "Cannot open " << filename << "\n"; std::exit(1); }

    std::vector<std::string> lines;
    std::string line;
    while (std::getline(fin, line)) {
        if (isBlankOrComment(line)) continue;
        lines.push_back(line);
    }
    if (lines.empty()) { std::cerr << "Empty file " << filename << "\n"; std::exit(1); }

    std::istringstream header(lines[0]);
    int sz = 0;
    if (!(header >> sz) || sz <= 0) {
        std::cerr << "Bad header in " << filename << "\n"; std::exit(1);
    }
    double extra;
    if (header >> extra) {
        std::cerr << "Header must contain only size in " << filename << "\n"; std::exit(1);
    }
    n = sz;

    Matrix m(n, std::vector<double>(n, 0.0));
    int cnt = 0;
    for (size_t i = 1; i < lines.size(); ++i) {
        std::istringstream is(lines[i]);
        double x;
        while (is >> x) {
            if (cnt >= n * n) { std::cerr << "Too many values in " << filename << "\n"; std::exit(1); }
            m[cnt / n][cnt % n] = x;
            ++cnt;
        }
    }
    if (cnt != n * n) { std::cerr << "Not enough values in " << filename << "\n"; std::exit(1); }
    return m;
}

static void writeMatrix(const std::string& filename, const Matrix& m) {
    std::ofstream fout(filename);
    fout.precision(17);   // ← добавить: 17 значащих цифр для double
    int n = (int)m.size();
    fout << n << "\n";
    for (int i = 0; i < n; ++i)
        for (int j = 0; j < n; ++j)
            fout << m[i][j] << (j + 1 < n ? ' ' : '\n');
}
static Matrix multiply(const Matrix& A, const Matrix& B) {
    int n = (int)A.size();
    Matrix C(n, std::vector<double>(n, 0.0));

    #pragma omp parallel for schedule(static)
    for (int i = 0; i < n; ++i) {
        for (int k = 0; k < n; ++k) {
            double a = A[i][k];
            const double* Bk = B[k].data();
            double* Ci = C[i].data();
            for (int j = 0; j < n; ++j)
                Ci[j] += a * Bk[j];
        }
    }
    return C;
}

int main(int argc, char** argv) {
    if (argc < 5) {
        std::cerr << "Usage: " << argv[0] << " A.txt B.txt C.txt info.txt\n";
        return 1;
    }
    int nA = 0, nB = 0;
    Matrix A = readMatrix(argv[1], nA);
    Matrix B = readMatrix(argv[2], nB);
    if (nA != nB) { std::cerr << "Size mismatch: " << nA << " vs " << nB << "\n"; return 2; }
    int n = nA;

    int threads = omp_get_max_threads();

    auto t0 = std::chrono::high_resolution_clock::now();
    Matrix C = multiply(A, B);
    auto t1 = std::chrono::high_resolution_clock::now();

    writeMatrix(argv[3], C);

    double sec = std::chrono::duration<double>(t1 - t0).count();
    double ops = 2.0 * (double)n * n * n;
    double gflops = (ops / sec) / 1e9;

    // запись статистики в info.txt
    std::ofstream fout(argv[4]);
    fout.precision(17);
    fout << "n=" << n << "\n";
    fout << "threads=" << threads << "\n";
    fout << "time_sec=" << sec << "\n";
    fout << "GFLOPS=" << gflops << "\n";
    fout << "volume=" << (long long)n * n << "\n";
    fout << "ops=" << (long long)ops << "\n";

    // дублируем в консоль (для глаза)
    std::cout << "n = " << n << "\n";
    std::cout << "threads = " << threads << "\n";
    std::cout << "time = " << sec << " s\n";
    std::cout << "GFLOPS = " << gflops << "\n";
    return 0;
}