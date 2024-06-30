def greedy_algorithm(numbers):
    # Sắp xếp mảng theo thứ tự giảm dần
    numbers.sort(reverse=True)
    # Chọn số lớn nhất
    max_number = numbers[0]
    return max_number

if __name__ == "__main__":
    numbers = [10, 5, 8, 20, 2]
    result = greedy_algorithm(numbers)
    print(f"Greedy algorithm result: {result}")
