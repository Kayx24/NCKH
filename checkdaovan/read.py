from flask import Flask, request, render_template
from werkzeug.utils import secure_filename
import os
import difflib
import re

app = Flask(__name__)
UPLOAD_FOLDER = '/path/to/uploads'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

def detect_language(file_path):
    if file_path.endswith('.cpp') or file_path.endswith('.c') or file_path.endswith('.h'):
        return 'c++'
    else:
        return 'unknown'

def read_file(file_path):
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            content = file.read()
            keywords = r'\b(int|float|if|for|while|else|return|include|define|try|catch|finally|class|break|continue|static|assert|throw|this|private|protected|public|void|volatile|unsigned|signed|struct|union|typedef|default|char|short|long|double|switch|case|do|goto|const|sizeof|namespace|using|bool|template|friend|inline|virtual|explicit|typename|extern|register|auto|static_cast|dynamic_cast|const_cast|reinterpret_cast|typeid|mutable|nullptr|enum)\b'
            cleaned_content = re.sub(keywords, '', content)
            return cleaned_content
    except FileNotFoundError:
        print(f"Error: {file_path} not found.")
        return None

@app.route('/')
def index():
    return render_template('upload.html')

@app.route('/compare', methods=['POST'])
def compare_files():
    uploaded_files = request.files.getlist('file[]')
    file_contents = []
    file_languages = []

    for file in uploaded_files:
        if file:
            filename = secure_filename(file.filename)
            file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            file.save(file_path)

            language = detect_language(file_path)
            if language == 'unknown':
                print(f"Unsupported file type: {filename}")
            else:
                file_languages.append(language)
                content = read_file(file_path)
                if content:
                    file_contents.append(content)
                else:
                    print(f"Error reading content from file: {filename}")

    if len(file_contents) < 2:
        return "Comparison requires at least two valid files."

    sequence_matcher = difflib.SequenceMatcher(None, file_contents[0], file_contents[1])
    similarity_ratio = sequence_matcher.ratio()
    similarity_percentage = similarity_ratio * 100

    return f'Mức độ trùng lặp giữa hai tệp: {similarity_percentage:.2f}%'

if __name__ == '__main__':
    app.run(debug=True)
