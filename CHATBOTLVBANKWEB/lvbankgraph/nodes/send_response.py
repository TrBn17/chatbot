import markdown  # pip install markdown

def send_response(input):
    answer = input.get("answer")
    source = input.get("source", "N/A")

    # Nếu không có answer từ LLM, phản hồi lỗi (vì LLM phải chịu trách nhiệm chính)
    if not answer:
        answer = "🤖 Xin lỗi, hiện tại tôi không thể phản hồi được câu hỏi này."

    # ✅ Convert sang HTML nếu cần render
    try:
        html_answer = markdown.markdown(answer, extensions=["extra"])
    except:
        html_answer = f"<p>{answer}</p>"

    full_html = f"""
        <div class='bot-reply'>
            {html_answer}
            <div class='source'>📌 Source: <strong>{source.upper()}</strong></div>
        </div>
    """

    print("📤 Final Response:\n", full_html)

    return {
        "response": full_html,
        "answer": answer,
        "source": source
    }
