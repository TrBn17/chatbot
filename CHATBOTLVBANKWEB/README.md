# 🏦 Chatbot LVBank Web – Hướng dẫn Triển khai Backend

Hệ thống Chatbot LVBank là giải pháp AI hỗ trợ tư vấn khách hàng, xây dựng bằng Python, tích hợp mô hình GPT (OpenAI hoặc Deepseek), LangChain, LangGraph, Flask API và vector search với ChromaDB.

---

## 🚀 Tính năng chính

- ✅ Tự động trả lời câu hỏi bằng GPT (FAQ hoặc Deepseek Agent)
- 🔍 Tìm kiếm thông tin theo vector từ dữ liệu đã index vào ChromaDB
- 🧠 Ghi nhớ hội thoại 10 câu gần nhất theo từng user
- 📝 Lưu lịch sử dạng JSON theo ngày/tháng/năm
- 🧩 API Flask dễ tích hợp vào frontend (VueJS, React,...)
- 🔐 Dễ dàng triển khai nội bộ (on-premise)

---

## 🧱 Kiến trúc hệ thống

```text
User <--> Frontend (Web / Chat UI)
                |
                V
        Flask Backend (app/)
                |
      LangGraph Pipeline (lvbankgraph/)
      /         |         \
 Normalize   Search FAQ   Deepseek
                |            \
               Answer      Fallback GPT
```

---

## 📁 Cấu trúc thư mục

```text
CHATBOTLVBANKWEB/
├── app/                       # Flask backend
│   ├── chat_routes.py        # Route phân luồng xử lý chat
│   ├── chromadb_routes.py    # Route thao tác vector DB
│   ├── controller.py         # (optional, không cần nếu dùng routes)
│   ├── config.py             # Biến môi trường
├── lvbankgraph/
│   ├── nodes/                # Danh sách các node LangGraph
│   ├── memory/               # Lưu và load lịch sử JSON
│   ├── lvbank_graph.py       # Build toàn bộ pipeline
│   ├── state.py              # Khai báo GraphState
├── chat_history/             # Lưu lịch sử hội thoại theo ngày
├── .env                      # Key môi trường
├── run.py                    # Khởi chạy Flask app
├── requirements.txt          # Bộ thư viện
├── README.md
```

---

## 🛠 Cài đặt

```bash
# Bước 1: Clone project
$ git clone https://github.com/tenban/CHATBOTLVBANKWEB
$ cd CHATBOTLVBANKWEB

# Bước 2: Tạo môi trường
$ python -m venv venv
$ source venv/bin/activate (hoặc .\venv\Scripts\activate)

# Bước 3: Cài dependencies
$ pip install -r requirements.txt
```

---

## 🔐 Cấu hình .env

Tạo file `.env`:

```env
OPENAI_API_KEY=sk-...
CHROMA_HOST=localhost
CHROMA_PORT=8000
```

---

## 🧪 Chạy test nội bộ (CLI)

```bash
python testbot.py
```

Gõ câu hỏi như:

```
Bạn: Giờ làm việc của ngân hàng?
```

---

## 🌐 Khởi chạy Flask server

```bash
python run.py
```

Server chạy ở `http://localhost:5001`

---

## 🔌 API Endpoints

### 1. Gửi câu hỏi:

```
POST /api/chat/chat
```

```json
{
  "query": "Giờ làm việc là gì?",
  "user_id": "test_user"
}
```

Kết quả:

```json
{
  "html": "<div class='bot-reply'>...</div>",
  "source": "ARK"
}
```

### 2. Lấy lịch sử:

```
GET /api/chat/history/<user_id>
```

### 3. Xoá lịch sử:

```
DELETE /api/chat/clear_history/<user_id>
```

### 4. Lấy tất cả vector:

```
GET /api/chromadb/
```

### 5. Thêm vector mới:

```
POST /api/chromadb/add
```

```json
{
  "documents": ["..."],
  "metadatas": [{ "answer": "..." }],
  "ids": ["id_abc"]
}
```

### 6. Xoá vector:

```
DELETE /api/chromadb/delete
```

```json
{ "ids": ["id_abc"] }
```

### 7. Cập nhật vector:

```
PUT /api/chromadb/update
```

```json
{
  "id": "id_abc",
  "document": "...",
  "metadata": { "answer": "..." }
}
```

---

## 🤖 Mô hình sử dụng

Hệ thống hỗ trợ:

- `gpt-4o`, `gpt-4`, `gpt-3.5-turbo`
- Hoặc mô hình nội bộ qua Skylark, ARK API (qua `call_ark.py`)

Lịch sử hội thoại được lưu trong `chat_history/<user_id>/<yyyy-mm-dd>.json`

---

## 📌 Ghi chú

- Lịch sử hội thoại tự động tạo nếu chưa tồn tại.
- Mỗi người dùng có thể lưu tối đa 10 tin nhắn gần nhất.
- Tất cả lịch sử lưu dạng JSON, dễ truy xuất + backup.
- Frontend có thể gọi API trực tiếp và render `html` từ `send_response`.

---

## 🤝 Liên hệ kỹ thuật

Nếu bạn cần hỗ trợ hoặc tích hợp chatbot vào sản phẩm khác:

- Đội AI của **FOXAI** sẽ hỗ trợ trực tiếp
- Hoặc liên hệ qua Zalo/Telegram đã cung cấp trong tài liệu nội bộ

---

> Made by FOXAI – Your trusted partner.
