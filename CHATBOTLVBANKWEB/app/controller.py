# # app/controller.py
# from lvbankgraph.lvbank_graph import build_graph

# graph = build_graph()

# def handle_user_message(text, sender_id):
#     try:
#         state = {
#             "query": text,
#             "user_id": sender_id
#         }

#         result = graph.invoke(state)
#         answer = result.get("answer", "🤖 Xin lỗi, mình chưa hiểu rõ câu hỏi của bạn.")
#         return answer

#     except Exception as e:
#         print("❌ Error in controller:", e)
#         return "🤖 Xin lỗi, có lỗi xảy ra trong quá trình xử lý."
