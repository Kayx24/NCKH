def brute_force_algorithm(numbers):
    # Tìm số lớn nhất bằng thuật toán vét cạn
    max_number = numbers[0]
    for number in numbers[1:]:
        if number > max_number:
            max_number = number
    return max_number

if __name__ == "__main__":
    numbers = [10, 5, 8, 20, 2]
    result = brute_force_algorithm(numbers)
    print(f"Brute force algorithm result: {result}")
