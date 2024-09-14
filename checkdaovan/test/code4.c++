#include <iostream>

// Hàm tính tổng các số từ 1 đến n sử dụng vòng lặp
int sumLoop(int n) {
    int sum = 0;
    for (int i = 1; i <= n; ++i) {
        sum += i;
    }
    return sum;
}

int main() {
    int n;
    std::cout << "Nhập một số nguyên dương n: ";
    std::cin >> n;

    if (n < 1) {
        std::cout << "Vui lòng nhập một số nguyên dương." << std::endl;
        return 1;
    }

    int total = sumLoop(n);
    std::cout << "Tổng các số từ 1 đến " << n << " là: " << total << std::endl;
    return 0;
}
