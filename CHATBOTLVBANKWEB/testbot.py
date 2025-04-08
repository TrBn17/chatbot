# testbot.py

from lvbankgraph.lvbank_graph import build_graph
import traceback

# ✅ Khởi tạo graph
graph = build_graph()

print("🤖 Chatbot LVBank đã sẵn sàng. Gõ 'exit' để thoát.\n")

while True:
    try:
        query = input("🧑 Bạn: ").strip()
        if query.lower() in ["exit", "quit"]:
            print("👋 Tạm biệt!")
            break

        # ✅ Gửi query qua LangGraph
        result = graph.invoke({
            "query": query,
            "user_id": "debug_user"
        })
        if "chat_history" in result:
            print("\n📚 Lịch sử hội thoại:")
            for msg in result["chat_history"]:
                role = msg.get("role", "unknown")
                content = msg.get("content", "").strip()

                if role == "user":
                    print(f"🧑 {content}")
                elif role == "assistant":
                    print(f"🤖 {content}")
                else:
                    print(f"❓ {role}: {content}")


        # ✅ In kết quả
        print("\n📥 Query:", query)
        print("📌 Trả lời:", result.get("answer", "❌ Không có phản hồi."))
        print("🔍 Source:", result.get("source", "N/A"))
        print("------\n")

    except Exception as e:
        print("❌ Đã xảy ra lỗi:")
        print(traceback.format_exc())
        print("------\n")
