import os
from dotenv import load_dotenv

# ✅ Load biến môi trường NGAY khi file được import
load_dotenv()

class Config:
    OPENAI_API_KEY = os.getenv("OPENAI_API_KEY", "")
    ARK_API_KEY = os.getenv("ARK_API_KEY", "")
    CHROMA_HOST = os.getenv("CHROMA_HOST", "localhost")
    CHROMA_PORT = int(os.getenv("CHROMA_PORT", 8000))

def print_env():
    print("🔑 OPENAI_API_KEY:", Config.OPENAI_API_KEY[:10] + "..." if Config.OPENAI_API_KEY else "❌ Not set")
    print("🔑 ARK_API_KEY:", Config.ARK_API_KEY[:10] + "..." if Config.ARK_API_KEY else "❌ Not set")
    print("🌐 ChromaDB:", f"http://{Config.CHROMA_HOST}:{Config.CHROMA_PORT}")

# if __name__ == "__main__":
#     print("✅ OPENAI_KEY:", Config.OPENAI_API_KEY)
#     print("✅ ARK_KEY:", Config.ARK_API_KEY)
#     print("✅ CHROMA:", Config.CHROMA_HOST, Config.CHROMA_PORT)
