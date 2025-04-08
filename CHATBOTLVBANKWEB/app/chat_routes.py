from flask import Blueprint, request, jsonify
from lvbankgraph.lvbank_graph import build_graph
import os
import json
from datetime import datetime
import traceback

user_bp = Blueprint("chat", __name__)
graph = build_graph()

# ✅ Route chat chính
@user_bp.route("/chat", methods=["POST"])
def chat():
    try:
        data = request.get_json()
        query = data.get("query", "")
        user_id = data.get("user_id", "anonymous")

        if not query:
            return jsonify({"error": "Thiếu câu hỏi"}), 400

        # ✅ Gọi LangGraph xử lý
        result = graph.invoke({
            "query": query,
            "user_id": user_id
        })

        # ✅ Trả về dữ liệu an toàn (không access key không tồn tại)
        return jsonify({
            "html": result.get("answer"),  # Nếu là HTML từ send_response
            "source": result.get("source", "N/A"),
            "context": result.get("context", None)
        })

    except Exception:
        print("❌ Error in /chat route:", traceback.format_exc())
        return jsonify({"error": "Internal Server Error"}), 500

# ✅ Lấy lịch sử hội thoại
@user_bp.route("/history/<user_id>", methods=["GET"])
def get_history(user_id):
    today = datetime.now().strftime("%Y-%m-%d")
    path = f"chat_history/{user_id}/{today}.json"

    if not os.path.exists(path):
        return jsonify({"history": []})

    try:
        with open(path, "r", encoding="utf-8") as f:
            messages = json.load(f)
            return jsonify({"history": messages})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# ✅ Xoá lịch sử user
@user_bp.route("/clear_history/<user_id>", methods=["DELETE"])
def clear_history(user_id):
    user_dir = f"chat_history/{user_id}"
    try:
        if os.path.exists(user_dir):
            for file in os.listdir(user_dir):
                os.remove(os.path.join(user_dir, file))
            return jsonify({"message": "Đã xoá toàn bộ lịch sử."})
        else:
            return jsonify({"message": "Không có lịch sử để xoá."})
    except Exception as e:
        return jsonify({"error": str(e)}), 500
