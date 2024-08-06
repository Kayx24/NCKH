# arithmetic_operations_v1.py

def add(a, b, c, d):
    return a + b + c + d

def subtract(a, b, c, d):
    return a - b - c - d

def multiply(a, b, c, d):
    return a * b * c * d

def divide(a, b, c, d):
    if b == 0 or c == 0 or d == 0:
        raise ValueError("Cannot divide by zero.")
    return a / b / c / d

def main():
    a, b, c, d = 8, 4, 2, 1
    print(f"Addition: {add(a, b, c, d)}")
    print(f"Subtraction: {subtract(a, b, c, d)}")
    print(f"Multiplication: {multiply(a, b, c, d)}")
    print(f"Division: {divide(a, b, c, d)}")

if __name__ == "__main__":
    main()
