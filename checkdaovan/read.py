import difflib
import re

def detect_language(file_path):
    if file_path.endswith('.py'):
        return 'python'
    elif file_path.endswith('.java'):
        return 'java'
    elif file_path.endswith('.c') or file_path.endswith('.cpp') or file_path.endswith('.h'):
        return 'c'
    else:
        return 'unknown'

def read_file(file_path, language):
    try:
        with open(file_path, 'r',encoding='utf-8') as file:
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

# Xác định ngôn ngữ của từng tệp
file1_path = r'D:\HOCTAP\NCKH\checkdaovan\data1.py'
file2_path = r'D:\HOCTAP\NCKH\checkdaovan\data2.py'

file1_language = detect_language(file1_path)
file2_language = detect_language(file2_path)

if file1_language == 'unknown' or file2_language == 'unknown':
    print("Unsupported file type for comparison.")
else:
    file1_content = read_file(file1_path, file1_language)
    file2_content = read_file(file2_path, file2_language)

    if file1_content is not None and file2_content is not None:
        sequence_matcher = difflib.SequenceMatcher(None, file1_content, file2_content)
        similarity_ratio = sequence_matcher.ratio()

        similarity_percentage = similarity_ratio * 100
        print(f'Mức độ trùng lặp: {similarity_percentage:.2f}%')
    else:
        print("Comparison could not be performed due to missing file content.")
