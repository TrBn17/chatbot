from typing import TypedDict, Optional, List, Union

class Message(TypedDict):
    role: str
    content: str

class GraphState(TypedDict):
    query: str
    user_id: str
    answer: Optional[str]
    source: Optional[str]
    ark_failed: Optional[bool]
    gpt_failed: Optional[bool]
    context: Optional[str]  # ⬅️ Nếu dùng vector search để cung cấp thêm dữ liệu
    chat_history: Optional[List[Message]]  # ✅ Lưu lịch sử hội thoại
    memory: Optional[object]               # ✅ Để lưu lại sau khi trả lời
