# lvbankgraph/nodes/save_chat_history.py

def save_to_memory(input: dict) -> dict:
    memory = input.get("memory")
    query = input.get("query", "")
    answer = input.get("answer", "")

    if not memory:
        print("⚠️ Không có memory trong input → không lưu được")
        return input

    try:
        memory.save_context({"input": query}, {"output": answer})
    except Exception as e:
        print(f"❌ Lỗi khi lưu history: {e}")

    return input
