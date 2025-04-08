# lvbankgraph/memory/json_file_memory.py
import os
import json
from datetime import datetime

HISTORY_DIR = "chat_history"

class JSONFileMemory:
    def __init__(self, user_id: str, k: int = 5):
        self.user_id = user_id
        self.k = k
        self.today = datetime.now().strftime("%Y-%m-%d")

        self.user_dir = os.path.join(HISTORY_DIR, user_id)
        os.makedirs(self.user_dir, exist_ok=True)

        self.save_path = os.path.join(self.user_dir, f"{self.today}.json")
        self.chat_history = self._load_history()

    def _load_history(self):
        if os.path.exists(self.save_path):
            try:
                with open(self.save_path, "r", encoding="utf-8") as f:
                    data = json.load(f)
                    if isinstance(data, list):
                        return data[-(self.k * 2):]
            except Exception as e:
                print(f"⚠️ Lỗi đọc file history: {e}")
        return []

    def load_memory_variables(self, _):
        return {"chat_history": self.chat_history}

    def save_context(self, inputs, outputs):
        user_msg = {"role": "user", "content": inputs.get("input", "")}
        bot_msg = {"role": "assistant", "content": outputs.get("output", "")}

        self.chat_history.append(user_msg)
        self.chat_history.append(bot_msg)

        self.chat_history = self.chat_history[-(self.k * 2):]

        try:
            with open(self.save_path, "w", encoding="utf-8") as f:
                json.dump(self.chat_history, f, ensure_ascii=False, indent=2)
        except Exception as e:
            print(f"❌ Lỗi lưu file history: {e}")
