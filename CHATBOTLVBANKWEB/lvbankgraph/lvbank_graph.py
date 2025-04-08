from langgraph.graph import StateGraph, END
from lvbankgraph.state import GraphState
from lvbankgraph.nodes import *
from lvbankgraph.nodes.search_faq import search_faq
from lvbankgraph.nodes.normalize_query import normalize_query
from lvbankgraph.nodes.call_ark import call_ark
from lvbankgraph.nodes.fallbackgpt import fall_back_gpt
from lvbankgraph.nodes.send_response import send_response
from lvbankgraph.nodes.load_chat_history import load_chat_history
from lvbankgraph.nodes.save_chat_history import save_to_memory 

# ✅ Import logic điều kiện
from lvbankgraph.edges import should_call_ark, should_fallback_to_gpt

def build_graph():
    builder = StateGraph(GraphState)

    # ✅ Các node chính
    builder.add_node("load_chat_history", load_chat_history)
    builder.add_node("normalize_query", normalize_query)
    builder.add_node("search_faq", search_faq)
    builder.add_node("call_ark", call_ark)
    builder.add_node("fall_back_gpt", fall_back_gpt)
    builder.add_node("send_response", send_response)
    builder.add_node("save_to_memory", save_to_memory)
    builder.set_finish_point("save_to_memory")

    # ✅ Entry point: Load lịch sử đầu tiên
    builder.set_entry_point("load_chat_history")

    # ✅ Flow
    builder.add_edge("load_chat_history", "normalize_query")
    builder.add_edge("normalize_query", "search_faq")

    # ✅ Nếu có answer → trả lời luôn, ngược lại → gọi ARK
    builder.add_conditional_edges("search_faq", should_call_ark, {
        "default": "send_response",
        "call_llm": "call_ark"
    })

    # ✅ Nếu ARK lỗi → fallback GPT
    builder.add_conditional_edges("call_ark", should_fallback_to_gpt, {
        "default": "send_response",
        "ark_failed": "fall_back_gpt"
    })

    builder.add_edge("fall_back_gpt", "send_response")

    # ✅ Sau khi gửi response thì lưu lại lịch sử
    builder.add_edge("send_response", "save_to_memory")

    # ✅ Kết thúc sau khi lưu lịch sử
    builder.set_finish_point("save_to_memory")

    return builder.compile()
