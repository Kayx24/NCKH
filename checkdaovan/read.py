import difflib
import re

def read_file(file_path, language):
    try:
        with open(file_path, 'r') as file:
            content = file.read()
            # Tùy theo ngôn ngữ lập trình, loại bỏ các từ khóa tương ứng
            if language == 'python':
                keywords = r'\b(int|float|if|for|while|else|elif|return|import|from|as|try|except|finally|with|def|class|break|continue|pass|assert|lambda|yield|global|nonlocal|del|raise|in|is|not|or|and)\b'
            elif language == 'java':
                keywords = r'\b(int|float|if|for|while|else|else if|return|import|package|try|catch|finally|synchronized|with|class|break|continue|static|assert|lambda|new|throw|throws|this|super|extends|implements|instanceof|interface|enum|private|protected|public|void|volatile|transient|abstract|final|native|strictfp|default|boolean|char|byte|short|long|double|switch|case|do|goto|const|assert|catch|instanceof)\b'
            elif language == 'c':
                keywords = r'\b(int|float|if|for|while|else|return|include|define|try|catch|finally|class|break|continue|static|assert|throw|this|private|protected|public|void|volatile|unsigned|signed|struct|union|typedef|default|char|short|long|double|switch|case|do|goto|const|sizeof|namespace|using|bool|template|friend|inline|virtual|explicit|typename|extern|register|auto|static_cast|dynamic_cast|const_cast|reinterpret_cast|typeid|mutable|nullptr|enum)\b'
            else:
                print(f"Unsupported language: {language}")
                return None

            cleaned_content = re.sub(keywords, '', content)
            return cleaned_content
    except FileNotFoundError:
        print(f"Error: {file_path} not found.")
        return None

# Đọc file với ngôn ngữ Python
file1_content = read_file('D:\HOCTAP\Python\checkdaovan\data1.py', 'python')
file2_content = read_file('D:\HOCTAP\Python\checkdaovan\data2.py', 'python')

if file1_content is not None and file2_content is not None:
    sequence_matcher = difflib.SequenceMatcher(None, file1_content, file2_content)
    similarity_ratio = sequence_matcher.ratio()

    similarity_percentage = similarity_ratio * 100
    print(f'Mức độ trùng lặp: {similarity_percentage:.2f}%')
else:
    print("Comparison could not be performed due to missing file content.")
