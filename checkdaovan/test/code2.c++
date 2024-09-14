#include <iostream>

double calculate(char operation, double a, double b) {
    switch(operation) {
        case '+':
            return a + b;
        case '-':
            return a - b;
        case '*':
            return a * b;
        case '/':
            if (b != 0) {
                return a / b;
            } else {
                std::cerr << "Division by zero is not allowed." << std::endl;
                return 0;
            }
        default:
            std::cerr << "Invalid operation." << std::endl;
            return 0;
    }
}

int main() {
    double num1, num2;
    char operation;
    
    std::cout << "Enter two numbers: ";
    std::cin >> num1 >> num2;

    std::cout << "Enter an operation (+, -, *, /): ";
    std::cin >> operation;

    double result = calculate(operation, num1, num2);
    std::cout << "Result: " << result << std::endl;

    return 0;
}
