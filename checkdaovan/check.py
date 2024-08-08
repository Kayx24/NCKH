import tokenize
from io import BytesIO
import ast
import os

# Gia thuat jaccard vs bien doi token
#------------------------------------------------------------------------------------------------#
def jaccard_similarity(set1, set2):
    intersection = len(set1 & set2)
    union = len(set1 | set2)
    return intersection / union if union != 0 else 0

def tokenize_code(code):
    tokens = set()
    g = tokenize.tokenize(BytesIO(code.encode('utf-8')).readline)
    for toknum, tokval, _, _, _ in g:
        if toknum not in {tokenize.ENCODING, tokenize.NEWLINE, tokenize.INDENT, tokenize.DEDENT}:
            tokens.add((toknum, tokval))
    return tokens
#------------------------------------------------------------------------------------------------#

def normalize_tokens(tokens):
    normalized_tokens = set()
    for toknum, tokval in tokens:
        if toknum == tokenize.NAME:
            normalized_tokens.add((toknum, 'identifier'))
        else:
            normalized_tokens.add((toknum, tokval))
    return normalized_tokens

def verbatim_cloning_similarity_ratio(code1, code2):
    tokens1 = tokenize_code(code1)
    tokens2 = tokenize_code(code2)
    return jaccard_similarity(tokens1, tokens2)

# Thuật toán so khớp chuỗi Knuth–Morris–Pratt (KMP)
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

def renaming_identifier_cloning_similarity_ratio(code1, code2):
    tokens1 = tokenize_code(code1)
    tokens2 = tokenize_code(code2)
    norm_tokens1 = normalize_tokens(tokens1)
    norm_tokens2 = normalize_tokens(tokens2)
    return jaccard_similarity(norm_tokens1, norm_tokens2)

def compare_nodes_detailed(node1, node2):
    if type(node1) != type(node2):
        return False
    if isinstance(node1, ast.AST):
        return all(compare_nodes_detailed(getattr(node1, field, None), getattr(node2, field, None))
                   for field in node1._fields)
    elif isinstance(node1, list):
        return len(node1) == len(node2) and all(compare_nodes_detailed(n1, n2) for n1, n2 in zip(node1, node2))
    else:
        return node1 == node2

def control_flow_restructuring_cloning_detailed(code1, code2):
    try:
        tree1 = ast.parse(code1)
        tree2 = ast.parse(code2)
        return compare_nodes_detailed(tree1, tree2)
    except SyntaxError:
        return False

def combined_similarity_score_detailed(code1, code2):
    tokens1 = tokenize_code(code1)
    tokens2 = tokenize_code(code2)
    verbatim_score = 1.0 if kmp_search(tokens1, tokens2) else verbatim_cloning_similarity_ratio(code1, code2)
    renaming_score = renaming_identifier_cloning_similarity_ratio(code1, code2)
    control_flow_score = 1.0 if control_flow_restructuring_cloning_detailed(code1, code2) else 0.0

    return {
        'verbatim': verbatim_score * 100,
        'renaming': renaming_score * 100,
        'restructuring': control_flow_score * 100
    }

def read_code_from_file(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        return file.read()

def print_similarity_scores(file1, file2):
    code1 = read_code_from_file(file1)
    code2 = read_code_from_file(file2)
    
    scores = combined_similarity_score_detailed(code1, code2)
    
    print(f"Sao chép nguyên văn: {scores['verbatim']:.2f}%")
    print(f"Sao chép với đổi tên định danh: {scores['renaming']:.2f}%")
    print(f"Sao chép với tái cấu trúc luồng điều khiển: {scores['restructuring']:.2f}%")

# Example usage
directory_path = "D:/HOCTAP/NCKH/checkdaovan/test"
files = [os.path.join(directory_path, f) for f in os.listdir(directory_path) if os.path.isfile(os.path.join(directory_path, f))]

for i in range(len(files)):
    for j in range(i + 1, len(files)):
        print(f"\nComparing {files[i]} and {files[j]}:")
        print_similarity_scores(files[i], files[j])
