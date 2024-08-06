import tokenize
from io import BytesIO

code = "def add(a, b):\n    return a + b\n"
code_bytes = code.encode('utf-8')
buffer = BytesIO(code_bytes)
readline = buffer.readline

# In ra các token
for token in tokenize.tokenize(readline):
    print(token)
