import os
import chromadb
import pandas as pd
from tqdm import tqdm
from openai import OpenAI

# Import config từ app
from app.config import Config

# ✅ Khởi tạo OpenAI client
client = OpenAI(api_key=Config.OPENAI_API_KEY)

# ✅ Khởi tạo ChromaDB client
chroma_client = chromadb.HttpClient(
    host=Config.CHROMA_HOST,
    port=Config.CHROMA_PORT
)

# ✅ Truy cập hoặc tạo collection
collection = chroma_client.get_or_create_collection(name="foxai_v2")

# ✅ Đọc dữ liệu từ file CSV
df = pd.read_csv("FOX-AI_CHATBOT_RESPONSE.csv")

# ✅ Hàm tạo embedding
def get_embedding(text):
    response = client.embeddings.create(
        input=text,
        model="text-embedding-3-large"
    )
    return response.data[0].embedding

# ✅ Nhúng từng dòng dữ liệu
for index, row in tqdm(df.iterrows(), total=len(df)):
    prompt_text = row["question"]
    completion_text = row["answer"]
    embedding = get_embedding(prompt_text)

    collection.add(
        ids=[str(index)],
        embeddings=[embedding],
        documents=completion_text,
        metadatas=[{
            "question": prompt_text,
            "answer": completion_text
        }]
    )

print("✅ Dữ liệu đã được nhúng và lưu vào ChromaDB!")
