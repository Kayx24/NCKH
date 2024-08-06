# arithmetic_operations_v2.py

class ArithmeticOperations:
    def __init__(self, a, b, c, d):
        self.a = a
        self.b = b
        self.c = c
        self.d = d

    def add(self):
        return self.a + self.b + self.c + self.d

    def subtract(self):
        return self.a - self.b - self.c - self.d

    def multiply(self):
        return self.a * self.b * self.c * self.d

    def divide(self):
        if self.b == 0 or self.c == 0 or self.d == 0:
            raise ValueError("Cannot divide by zero.")
        return self.a / self.b / self.c / self.d

def main():
    a, b, c, d = 8, 4, 2, 1
    operations = ArithmeticOperations(a, b, c, d)
    print(f"Addition: {operations.add()}")
    print(f"Subtraction: {operations.subtract()}")
    print(f"Multiplication: {operations.multiply()}")
    print(f"Division: {operations.divide()}")

if __name__ == "__main__":
    main()
