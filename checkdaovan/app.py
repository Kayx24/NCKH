import ast
import tokenize
from io import BytesIO
from functools import lru_cache
from flask import Flask, request, jsonify
import pandas as pd
import os

app = Flask(__name__)

# Hàm tính tỷ lệ tương đồng Jaccard
def jaccard_similarity(set1, set2):
    intersection = len(set1 & set2)
    union = len(set1 | set2)
    return intersection / union if union != 0 else 0

# Hàm phân tích mã nguồn thành token
def tokenize_code(code):
    tokens = set()
    try:
        g = tokenize.tokenize(BytesIO(code.encode('utf-8')).readline)
        for toknum, tokval, _, _, _ in g:
            if toknum not in {tokenize.ENCODING, tokenize.NEWLINE, tokenize.INDENT, tokenize.DEDENT}:
                tokens.add((toknum, tokval))
    except Exception as e:
        print(f"Lỗi khi phân tích mã nguồn thành token: {e}")
    return tokens

# Chuẩn hóa token
def normalize_tokens(tokens):
    normalized_tokens = set()
    for toknum, tokval in tokens:
        if toknum == tokenize.NAME:
            normalized_tokens.add((toknum, 'identifier'))
        else:
            normalized_tokens.add((toknum, tokval))
    return normalized_tokens

# Tỷ lệ sao chép nguyên văn
def verbatim_cloning_similarity_ratio(code1, code2):
    tokens1 = tokenize_code(code1)
    tokens2 = tokenize_code(code2)
    return jaccard_similarity(tokens1, tokens2)

# Tìm kiếm chuỗi bằng thuật toán KMP
def kmp_search(text_tokens, pattern_tokens):
    def compute_lps(pattern):
        lps = [0] * len(pattern)
        length = 0
        i = 1
        while i < len(pattern):
            if pattern[i] == pattern[length]:
                length += 1
                lps[i] = length
                i += 1
            else:
                if length != 0:
                    length = lps[length - 1]
                else:
                    lps[i] = 0
                    i += 1
        return lps

    text = list(text_tokens)
    pattern = list(pattern_tokens)
    lps = compute_lps(pattern)
    i = j = 0
    while i < len(text):
        if pattern[j] == text[i]:
            i += 1
            j += 1
        if j == len(pattern):
            return True
        elif i < len(text) and pattern[j] != text[i]:
            if j != 0:
                j = lps[j - 1]
            else:
                i += 1
    return False

# Tỷ lệ sao chép với đổi tên định danh
def renaming_identifier_cloning_similarity_ratio(code1, code2):
    tokens1 = tokenize_code(code1)
    tokens2 = tokenize_code(code2)
    norm_tokens1 = normalize_tokens(tokens1)
    norm_tokens2 = normalize_tokens(tokens2)
    return jaccard_similarity(norm_tokens1, norm_tokens2)

# So sánh các node AST với caching
@lru_cache(maxsize=None)
def compare_ast_nodes_cached(node1, node2):
    if isinstance(node1, ast.AST) and isinstance(node2, ast.AST):
        if type(node1) != type(node2):
            return False, 0
        
        matching_nodes = 0
        total_nodes = 0
        
        for field in node1._fields:
            child1 = getattr(node1, field, None)
            child2 = getattr(node2, field, None)
            
            if isinstance(child1, list) and isinstance(child2, list):
                if len(child1) != len(child2):
                    return False, 0
                list_matches = [
                    compare_ast_nodes_cached(c1, c2)[1]
                    for c1, c2 in zip(child1, child2)
                ]
                matching_nodes += sum(list_matches)
                total_nodes += len(child1)
            else:
                is_match, similarity = compare_ast_nodes_cached(child1, child2)
                if is_match:
                    matching_nodes += 1
                total_nodes += 1
        
        return matching_nodes == total_nodes, matching_nodes / total_nodes if total_nodes > 0 else 1.0
    else:
        return node1 == node2, 1.0 if node1 == node2 else 0.0

# Tỷ lệ sao chép với tái cấu trúc luồng điều khiển
def control_flow_restructuring_cloning_detailed(code1, code2):
    try:
        tree1 = ast.parse(code1)
        tree2 = ast.parse(code2)
        _, similarity = compare_ast_nodes_cached(tree1, tree2)
        return similarity * 100
    except SyntaxError as e:
        print(f"Lỗi cú pháp: {e}")
        return 0.0

# Tính toán tỷ lệ tương đồng tổng hợp
def combined_similarity_score_detailed(code1, code2):
    tokens1 = tokenize_code(code1)
    tokens2 = tokenize_code(code2)
    verbatim_score = 1.0 if kmp_search(tokens1, tokens2) else verbatim_cloning_similarity_ratio(code1, code2)
    renaming_score = renaming_identifier_cloning_similarity_ratio(code1, code2)
    control_flow_score = control_flow_restructuring_cloning_detailed(code1, code2)

    return {
        'verbatim': verbatim_score * 100,
        'renaming': renaming_score * 100,
        'restructuring': control_flow_score
    }

# Đọc mã nguồn từ file
def read_code_from_file(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        return file.read()

# Tính toán ma trận tương đồng cho các file đã tải lên
def calculate_similarity_matrix(files):
    num_files = len(files)
    similarity_matrix = pd.DataFrame(index=files, columns=files)

    for i in range(num_files):
        for j in range(i + 1, num_files):
            file1 = files[i]
            file2 = files[j]
            code1 = read_code_from_file(file1)
            code2 = read_code_from_file(file2)

            if not code1 or not code2:
                print(f"Lỗi: Không thể đọc mã nguồn từ file {file1} hoặc {file2}.")
                continue

            scores = combined_similarity_score_detailed(code1, code2)

            similarity_matrix.at[file1, file2] = f"{scores['verbatim']:.2f},{scores['renaming']:.2f},{scores['restructuring']:.2f}"
            similarity_matrix.at[file2, file1] = similarity_matrix.at[file1, file2]

    return similarity_matrix

# Điểm cuối API để xử lý việc tải lên file và trả về ma trận tương đồng
@app.route('/upload', methods=['POST'])
def upload_files():
    files = request.files.getlist('files')
    if not files:
        return jsonify({'error': 'Không có file nào được tải lên'}), 400

    # Lưu các file vào thư mục tạm thời
    file_paths = []
    temp_dir = 'temp_uploads'
    os.makedirs(temp_dir, exist_ok=True)
    
    for file in files:
        file_path = os.path.join(temp_dir, file.filename)
        file.save(file_path)
        file_paths.append(file_path)
    
    # Tính toán ma trận tương đồng
    similarity_matrix = calculate_similarity_matrix(file_paths)

    # Chuẩn bị kết quả dưới dạng định dạng JSON
    matrix_data = []
    for i, file1 in enumerate(file_paths):
        row = []
        for j, file2 in enumerate(file_paths):
            if file1 != file2:
                verbatim, renaming, restructuring = map(float, similarity_matrix.at[file1, file2].split(','))
                row.append({
                    'verbatim': verbatim,
                    'renaming': renaming,
                    'restructuring': restructuring
                })
            else:
                row.append(None)
        matrix_data.append(row)

    # Trả về kết quả dưới dạng JSON
    return jsonify({'matrix': matrix_data})

if __name__ == '__main__':
    app.run(debug=True)
