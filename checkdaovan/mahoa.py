import nltk
from nltk.tokenize import word_tokenize
from sklearn.feature_extraction.text import CountVectorizer
import pandas as pd

# Đảm bảo bạn đã tải các tài nguyên cần thiết
nltk.download('punkt')

# Hàm mã hóa chuỗi bằng cách tokenize và chuyển đổi thành vector
def encode_texts(texts):
    # Phân tách (tokenize) chuỗi
    tokenized_texts = [word_tokenize(text.lower()) for text in texts]
    
    # Chuyển đổi các chuỗi token thành vector sử dụng CountVectorizer
    vectorizer = CountVectorizer(tokenizer=lambda x: x, lowercase=False)
    vectors = vectorizer.fit_transform([' '.join(tokens) for tokens in tokenized_texts])
    
    return vectors.toarray(), vectorizer.get_feature_names_out()

# Ví dụ sử dụng
text1 = "tao ngu"
text2 = "tao khon"

encoded_vectors, feature_names = encode_texts([text1, text2])

# Tạo DataFrame từ kết quả
df = pd.DataFrame(encoded_vectors, columns=feature_names)

# Lưu DataFrame vào file CSV
df.to_csv('encoded_texts.csv', index=False)

print("Kết quả đã được lưu vào file 'encoded_texts.csv'.")
