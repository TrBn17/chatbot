# ✅ Điều kiện sau khi search vector
def should_call_ark(state: dict) -> str:
    return "default" if state.get("answer") else "call_llm"

# ✅ Điều kiện sau khi gọi ARK
def should_fallback_to_gpt(state: dict) -> str:
    return "ark_failed" if state.get("ark_failed") else "default"

# ✅ Nếu cần xác định kết thúc sớm (ít dùng)
def should_end(state: dict) -> str:
    return "default" if state.get("answer") else "fallback"
