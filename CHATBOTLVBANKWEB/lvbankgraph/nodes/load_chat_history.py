from lvbankgraph.memory.json_file_memory import JSONFileMemory

def load_chat_history(input: dict) -> dict:
    user_id = input.get("user_id", "anonymous")
    memory = JSONFileMemory(user_id=user_id, k=5)

    input["memory"] = memory

    full_data = memory.load_memory_variables({})
    full_history = full_data.get("chat_history", [])

    # ✅ Lấy đúng 5 cặp gần nhất (user + assistant)
    history_for_llm = full_history[-10:]  # giữ nguyên cả câu hỏi + trả lời

    input["chat_history"] = history_for_llm

    print(f"📚 Loaded {len(history_for_llm)} messages (5 turns) for LLM")

    return input
