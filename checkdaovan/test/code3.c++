#include <iostream>

// Hàm đệ quy để tính tổng từ 1 đến n
int sum(int n) {
    if (n == 1) {
        return 1; // Điều kiện dừng: Nếu n = 1, trả về 1
    } else {
        return n + sum(n - 1); // Gọi đệ quy sum(n-1) và cộng với n
    }
}

int main() {
    int n;
    std::cout << "Nhập một số nguyên dương n: ";
    std::cin >> n;

    if (n <= 0) {
        std::cout << "Vui lòng nhập một số nguyên dương lớn hơn 0." << std::endl;
    } else {
        int result = sum(n); // Gọi hàm đệ quy để tính tổng
        std::cout << "Tổng của các số từ 1 đến " << n << " là: " << result << std::endl;
    }

    return 0;
}
