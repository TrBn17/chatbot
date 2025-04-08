# from openai import OpenAI
# from app.config import Config

# client = OpenAI(api_key=Config.OPENAI_API_KEY)

# def classify_query(input):
#     query = input.get("query", "")
#     system_prompt = """
#     Bạn là một bộ phân loại truy vấn người dùng. Phân loại câu hỏi vào một trong các nhóm sau:

#     - "requirement": nếu câu hỏi liên quan đến điều kiện, yêu cầu, thủ tục hoặc hồ sơ cần thiết cho các dịch vụ của công ty FOXAI (ví dụ: cần những gì để apply, quy trình tuyển dụng, v.v.).
#     - "faq": nếu câu hỏi nằm trong các câu hỏi thường gặp như thông tin dịch vụ, thời gian phản hồi, địa chỉ liên hệ, v.v.
#     - "chitchat": nếu là câu xã giao, chào hỏi, không mang tính nghiệp vụ.
#     - "unknown": nếu không xác định được hoặc nội dung lạ.

#     Chỉ trả về duy nhất một trong 4 nhãn: requirement, faq, chitchat, unknown.
#     """

#     try:
#         res = client.chat.completions.create(
#             model="gpt-4o",
#             messages=[
#                 {"role": "system", "content": system_prompt},
#                 {"role": "user", "content": query}
#             ],
#             temperature=0
#         )
#         label = res.choices[0].message.content.strip().lower()
#         label = label.strip().lower()

#         if label not in ["requirement", "faq", "chitchat", "unknown"]:
#             print("⚠️ Unexpected label from GPT:", label)
#             label = "unknown"

#     except Exception as e:
#         print("❌ GPT error:", e)
#         label = "unknown"

#     return {**input, "type": label}



# # if __name__ == "__main__":
# #     test_inputs = [
# #         "xin chào bạn ơi",
# #         "giờ làm việc công ty là khi nào",
# #         "cần chuẩn bị những gì để ứng tuyển vào FOXAI",
# #         "FOXAI có đang tuyển dụng không?",
# #         "thời tiết hôm nay thế nào?"
# #     ]

# #     for query in test_inputs:
# #         result = classify_query({"query": query})
# #         print(f"🔍 Query: {query}")
# #         print(f"📌 Classified as: {result['type']}")
# #         print("----")