# app/chromadb_routes.py
from flask import Blueprint, request, jsonify
import chromadb
from app.config import Config
chromadb_bp = Blueprint("chromadb", __name__)
chroma_client = chromadb.HttpClient(host="160.30.252.28", port="8000")
COLLECTION_NAME = "faq-lv-bank"

def get_collection():
    return chroma_client.get_or_create_collection(name=COLLECTION_NAME)

# ✅ Get all vectors
@chromadb_bp.route("/", methods=["GET"])
def get_all():
    collection = get_collection()
    data = collection.get()
    return jsonify(data)

# ✅ Add new vector
@chromadb_bp.route("/add", methods=["POST"])
def add_vector():
    data = request.get_json()
    documents = data.get("documents", [])
    metadatas = data.get("metadatas", [{} for _ in documents])
    ids = data.get("ids", [f"doc-{i}" for i in range(len(documents))])

    try:
        collection = get_collection()
        collection.add(documents=documents, metadatas=metadatas, ids=ids)
        return jsonify({"message": "Thêm vector thành công", "count": len(documents)})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# ✅ Delete vector by id
@chromadb_bp.route("/delete", methods=["DELETE"])
def delete_vector():
    data = request.get_json()
    ids = data.get("ids", [])
    try:
        collection = get_collection()
        collection.delete(ids=ids)
        return jsonify({"message": f"Đã xoá {len(ids)} vector"})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# ✅ Update vector metadata (no native update → emulate by delete+add)
@chromadb_bp.route("/update", methods=["PUT"])
def update_vector():
    data = request.get_json()
    id = data.get("id")
    new_doc = data.get("document")
    new_metadata = data.get("metadata")

    if not id:
        return jsonify({"error": "Thiếu ID để cập nhật"}), 400

    try:
        collection = get_collection()
        # Delete old
        collection.delete(ids=[id])
        # Add new
        collection.add(ids=[id], documents=[new_doc], metadatas=[new_metadata])
        return jsonify({"message": "Đã cập nhật vector"})
    except Exception as e:
        return jsonify({"error": str(e)}), 500
