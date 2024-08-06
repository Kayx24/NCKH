import tokenize
from io import BytesIO
import ast
from collections import defaultdict

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

def verbatim_cloning_similarity_ratio(code1, code2):
    tokens1 = tokenize_code(code1)
    tokens2 = tokenize_code(code2)
    return jaccard_similarity(tokens1, tokens2)

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

def sorted_neighborhood_comparison(blocks, window_size=3):
    combined_results = []
    for block in blocks:
        block.sort(key=lambda x: x[0])
        num_blocks = len(block)
        for i in range(num_blocks):
            for j in range(i + 1, min(i + window_size, num_blocks)):
                code1, code2 = block[i][1], block[j][1]
                tokens1 = tokenize_code(code1)
                tokens2 = tokenize_code(code2)
                jaccard_score = jaccard_similarity(tokens1, tokens2)
                combined_results.append(jaccard_score)
    return combined_results

def renaming_identifier_cloning_jaccard(code_list, window_size=3):
    blocks = defaultdict(list)
    for code in code_list:
        tokens = tuple(tokenize_code(code))
        blocks[tokens].append((tokens, code))
    
    code_blocks = list(blocks.values())
    results = []
    for block in code_blocks:
        results.extend(sorted_neighborhood_comparison([block], window_size))
    return results

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
    tree1 = ast.parse(code1)
    tree2 = ast.parse(code2)
    return compare_nodes_detailed(tree1, tree2)

def combined_similarity_score_detailed(code1, code2):
    tokens1 = tokenize_code(code1)
    tokens2 = tokenize_code(code2)
    verbatim_score = 1.0 if kmp_search(tokens1, tokens2) else verbatim_cloning_similarity_ratio(code1, code2)
    renaming_scores = renaming_identifier_cloning_jaccard([code1, code2])
    renaming_score = sum(renaming_scores) / len(renaming_scores) if renaming_scores else 0
    control_flow_score = 1.0 if control_flow_restructuring_cloning_detailed(code1, code2) else 0.0

    combined_score = (verbatim_score * 0.5 + renaming_score * 0.3 + control_flow_score * 0.2)
    return combined_score * 100

def read_code_from_file(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        return file.read()

file1 = "D:/HOCTAP/NCKH/checkdaovan/code1.py"
file2 = "D:/HOCTAP/NCKH/checkdaovan/code2.py"

code1 = read_code_from_file(file1)
code2 = read_code_from_file(file2)

print("Comparing code1 and code2:")
combined_score1 = combined_similarity_score_detailed(code1, code2)
print(f"Combined Similarity Score: {combined_score1:.2f}%")

renaming_scores = renaming_identifier_cloning_jaccard([code1, code2])
print("\nJaccard Similarity Scores between code1 and code2:",verbatim_cloning_similarity_ratio(code1, code2)*100 )

for score in renaming_scores:
    print(f"{score:.2f}")
