#include <iostream>
#include <fstream>
#include <vector>
#include <chrono>
#include <string>
#include <filesystem>
#include <iomanip>

#ifdef _WIN32
   #include <windows.h>
#endif


namespace fs = std::filesystem;

// ---------- Чтение квадр. матрицы из файла ----------
std::vector<std::vector<double>> readMatrix(const std::string& filename, int& size) {
    std::ifstream infile(filename);
    if (!infile.is_open()) {
        std::cerr << "Ошибка: не удалось открыть файл " << filename << std::endl;
        exit(1);
    }
    infile >> size;
    std::vector<std::vector<double>> matrix(size, std::vector<double>(size));
    for (int i = 0; i < size; ++i)
        for (int j = 0; j < size; ++j)
            infile >> matrix[i][j];
    infile.close();
    return matrix;
}

// ---------- Запись матрицы в файл ----------
void writeMatrix(const std::string& filename, const std::vector<std::vector<double>>& matrix) {
    std::ofstream outfile(filename);
    if (!outfile.is_open()) {
        std::cerr << "Ошибка: не удалось создать файл " << filename << std::endl;
        exit(1);
    }
    int size = matrix.size();
    outfile << size << "\n";
    for (int i = 0; i < size; ++i) {
        for (int j = 0; j < size; ++j)
            outfile << std::setprecision(15) << matrix[i][j] << " ";
        outfile << "\n";
    }
    outfile.close();
}

int main(int argc, char* argv[]) {
#ifdef _WIN32
    SetConsoleOutputCP(65001);
#endif
 
    if (argc != 5) {
        std::cerr << "Использование: " << argv[0]
                  << " <файл_A> <файл_B> <выходной_результат> <выходной_info>\n";
        return 1;
    }

    std::string fileA = argv[1];
    std::string fileB = argv[2];
    std::string fileOutC = argv[3];
    std::string fileInfo = argv[4];

    // Создание папки output, если её нет
    fs::path outPath = fs::path(fileOutC).parent_path();
    if (!outPath.empty() && !fs::exists(outPath)) {
        fs::create_directories(outPath);
    }

    int sizeA, sizeB;
    std::vector<std::vector<double>> A = readMatrix(fileA, sizeA);
    std::vector<std::vector<double>> B = readMatrix(fileB, sizeB);

    if (sizeA != sizeB) {
        std::cerr << "Ошибка: размеры матриц не совпадают\n";
        return 1;
    }

    int N = sizeA;
    std::vector<std::vector<double>> C(N, std::vector<double>(N, 0.0));

    // Замер времени
    auto start = std::chrono::high_resolution_clock::now();

    for (int i = 0; i < N; ++i) {
        for (int k = 0; k < N; ++k) {
            double a_ik = A[i][k];
            for (int j = 0; j < N; ++j) {
                C[i][j] += a_ik * B[k][j];
            }
        }
    }

    auto end = std::chrono::high_resolution_clock::now();
    std::chrono::duration<double> duration = end - start;

    // Запись результата
    writeMatrix(fileOutC, C);

    // Запись info-файла
    std::ofstream info(fileInfo);
    if (!info.is_open()) {
        std::cerr << "Ошибка: не удалось создать файл " << fileInfo << std::endl;
        return 1;
    }
    long long volume = (long long)N * N;
    info << "size=" << N << "\n";
    info << "volume=" << volume << "\n";
    info << "time_sec=" << duration.count() << "\n";
    info.close();

    std::cout << "=====================================\n";
    std::cout << "Размер матрицы (N x N): " << N << " x " << N << "\n";
    std::cout << "Объем задачи (N*N): " << volume << " элементов\n";
    std::cout << "Время выполнения: " << duration.count() << " секунд\n";
    std::cout << "Результат: " << fileOutC << "\n";
    std::cout << "Информация: " << fileInfo << "\n";
    std::cout << "=====================================\n";

    return 0;
}