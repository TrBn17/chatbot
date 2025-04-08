import os
import chromadb
from openai import OpenAI
from app.config import Config
from lvbankgraph.nodes.normalize_query import normalize_query  # ✅ Gọi hàm normalize có sẵn

# ✅ Khởi tạo client
client = OpenAI(api_key=Config.OPENAI_API_KEY)
chroma_client = chromadb.HttpClient(host=Config.CHROMA_HOST, port=Config.CHROMA_PORT)
collection = chroma_client.get_or_create_collection(name="faq-lv-bank")

def search_faq(input):
    # ✅ Normalize câu hỏi bằng logic custom của đại ca
    normalized_input = normalize_query(input)
    query = normalized_input["query"]

    # ✅ Tạo embedding
    try:
        embed = client.embeddings.create(
            input=query,
            model="text-embedding-3-large"
        ).data[0].embedding
    except Exception as e:
        print("❌ GPT embedding error:", e)
        return {**input, "answer": "Không thể xử lý truy vấn lúc này."}

    # ✅ Truy vấn Chroma
    try:
        results = collection.query(
            query_embeddings=[embed],
            n_results=3
        )
    except Exception as e:
        print("❌ ChromaDB error:", e)
        return {**input, "answer": "Lỗi khi truy vấn dữ liệu."}

    # ✅ Lấy kết quả
    docs = results.get("documents", [[]])[0]
    metadatas = results.get("metadatas", [[]])[0]

    if not docs:
        return input  # Không tìm thấy gì → để call_ark xử lý tiếp

    # ✅ Format context cho đẹp
    context = "\n".join([
        f"{i+1}. {metadatas[i].get('answer', docs[i])}"
        for i in range(len(docs))
    ])

    return {**input, "context": context, "source": "faq"}
