#include <iostream>

double add(double a, double b) {
    return a + b;
}

double subtract(double a, double b) {
    return a - b;
}

double multiply(double a, double b) {
    return a * b;
}

double divide(double a, double b) {
    if (b != 0) {
        return a / b;
    } else {
        std::cerr << "Division by zero is not allowed." << std::endl;
        return 0;
    }
}

int main() {
    double num1, num2;
    std::cout << "Enter two numbers: ";
    std::cin >> num1 >> num2;

    std::cout << "Addition: " << add(num1, num2) << std::endl;
    std::cout << "Subtraction: " << subtract(num1, num2) << std::endl;
    std::cout << "Multiplication: " << multiply(num1, num2) << std::endl;
    std::cout << "Division: " << divide(num1, num2) << std::endl;

    return 0;
}
