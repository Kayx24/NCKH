#include <iostream>

// Hàm tính tổng các số từ 1 đến n sử dụng đệ quy
int sumRecursive(int n) {
    if (n <= 0) return 0;
    return n + sumRecursive(n - 1);
}

int main() {
    int n;
    std::cout << "Nhập một số nguyên dương n: ";
    std::cin >> n;

    if (n < 1) {
        std::cout << "Vui lòng nhập một số nguyên dương." << std::endl;
        return 1;
    }

    int total = sumRecursive(n);
    std::cout << "Tổng các số từ 1 đến " << n << " là: " << total << std::endl;
    return 0;
}
