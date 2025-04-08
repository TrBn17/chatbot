from chromadb import HttpClient
from app.config import Config
from openai import OpenAI

# Kết nối ChromaDB
chroma_client = HttpClient(
    host=Config.CHROMA_HOST,
    port=Config.CHROMA_PORT
)

# Load collection đã tạo sẵn
collection = chroma_client.get_or_create_collection(name="foxai_v2")

# Hàm query vector từ câu hỏi
def query_vector_db(query: str, top_k: int = 3):
    # Tạo embedding cho câu query
    client = OpenAI(api_key=Config.OPENAI_API_KEY)
    embedding = client.embeddings.create(
        input=query,
        model="text-embedding-3-large"
    ).data[0].embedding

    # Truy vấn Chroma
    results = collection.query(
        query_embeddings=[embedding],
        n_results=top_k
    )

    return results  # Gồm documents, distances, metadatas
if __name__ == "__main__":
    query = "quy trình tuyển dụng của công ty là gì?"
    res = query_vector_db(query)
    
    print("📚 Top match:")
    for i, doc in enumerate(res['documents'][0]):
        print(f"{i+1}. {doc}")
