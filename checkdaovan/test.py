import tokenize
from io import BytesIO
import ast
import difflib

def verbatim_cloning_similarity_ratio(code1,code2):
        similary_ratio = difflib.SequenceMatcher(None,code1,code2).ratio()
        return similary_ratio
    
def tokenize_code(code):
    tokens = []
    g = tokenize.tokenize(BytesIO(code.encode('utf-8')).readline)
    for toknum,tokval, _,_,_ in g:
        if toknum != tokenize.ENCODING:
            tokens.append((toknum,tokval))
    return tokens

def renaming_identifier_cloning(code1,code2):
    tokens1 = tokenize_code(code1)
    tokens2 = tokenize_code(code2)
    return tokens1 == tokens2

def compare_nodes(node1,node2):
    if type(node1) != type(node2):
        return False
    if isinstance(node1,ast.AST):
        for field in node1._fields:
            if not compare_nodes(getattr(node1,field),getattr(node2,field)):
                return False
        return True
    elif isinstance(node1,list):
        return all(compare_nodes(n1,n2) for n1,n2 in zip (node1,node2))
    else:
        return node1 == node2
    
def control_flow_restructuring_cloning(code1,code2):
    tree1 = ast.parse(code1)
    tree2 = ast.parse(code2)
    return compare_nodes(tree1,tree2)

def compare_code(code1,code2):
    results = {
         "Verbatim Cloning Similarity Ratio": verbatim_cloning_similarity_ratio(code1, code2),
        "Renaming Identifier Cloning": renaming_identifier_cloning(code1, code2),
        "Control Flow Restructuring Cloning": control_flow_restructuring_cloning(code1, code2)
    }
    return results

code1 = "def add(a, b):\n    return a + b\n"
code2 = "def add(x, y):\n    return x + y\n"
code3 = "def add(a, b):\n    result = a + b\n    return result\n"

print("Comparing code1 and code2:")
results1 = compare_code(code1, code2)
for key, value in results1.items():
    print(f"{key}: {value}")

print("\nComparing code1 and code3:")
results2 = compare_code(code1, code3)
for key, value in results2.items():
    print(f"{key}: {value}")