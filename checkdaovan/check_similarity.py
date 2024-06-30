import ast
from collections import Counter

# Đoạn mã 1
code1 = """
def is_prime(n):
    if n <= 1:
        return False
    elif n == 2:
        return True
    else:
        for i in range(2, n):
            if n % i == 0:
                return False
        return True
"""

# Đoạn mã 2
code2 = """
def check_prime(number):
    if number < 2:
        return False
    for divisor in range(2, number):
        if number % divisor == 0:
            return False
    return True
"""

# Hàm để trích xuất đặc trưng từ AST
def extract_features(tree):
    features = []
    for node in ast.walk(tree):
        if isinstance(node, ast.FunctionDef):
            features.append(('FunctionDef', node.name))
        elif isinstance(node, ast.For):
            features.append('For')
        elif isinstance(node, ast.If):
            features.append('If')
        elif isinstance(node, ast.Compare):
            features.append('Compare')
        elif isinstance(node, ast.Return):
            features.append('Return')
        # Có thể thêm nhiều loại node khác nếu cần thiết
    return features

# Phân tích mã nguồn thành AST và trích xuất đặc trưng
tree1 = ast.parse(code1)
tree2 = ast.parse(code2)

features1 = extract_features(tree1)
features2 = extract_features(tree2)

print("Features from code1:", features1)
print("Features from code2:", features2)

# Đếm tần suất xuất hiện của các đặc trưng
counter1 = Counter(features1)
counter2 = Counter(features2)

# Tính toán độ tương tự (Jaccard Similarity)
def jaccard_similarity(counter1, counter2):
    intersection = sum((counter1 & counter2).values())
    union = sum((counter1 | counter2).values())
    return intersection / union

similarity = jaccard_similarity(counter1, counter2)
print(f"Jaccard Similarity: {similarity:.2%}")
