import re

def normalize_query(input):
    query = input.get("query", "")

    # 1. Lowercase toàn bộ (an toàn cho cả English và phần lớn Unicode Lao)
    normalized = query.lower()

    # 2. Bỏ dấu câu (giữ nguyên ký tự Lào vì regex \w vẫn hỗ trợ Unicode)
    normalized = re.sub(r"[^\w\sກ-ຮະ-ເົ-ໄ]", "", normalized)

    # 3. Chuẩn hóa alias (English & Lao nếu có)
    replacements = {
        "lao viet bank": "lvb",
        "ທະນາຄານ ລາວ ໄວດ": "lvb",  # Lao Viet Bank tiếng Lào
        "lao-viet": "lvb",
        "lvbank": "lvb",
    }
    for k, v in replacements.items():
        normalized = normalized.replace(k, v)

    # 4. Loại bỏ từ dư thừa thông dụng (greeting, polite phrases)
    stopwords = [
        # English
        "please", "could you", "i want to ask", "may i know", "can you tell me",
        # Lao (các cụm chào hỏi / xã giao)
        "ຂໍຖາມ", "ຂໍຂໍ້ມູນ", "ຂໍໃຫ້ຊ່ວຍ", "ສະບາຍດີ",
    ]
    for sw in stopwords:
        normalized = normalized.replace(sw, "")

    # 5. Làm gọn dấu cách
    normalized = re.sub(r"\s+", " ", normalized).strip()

    return {**input, "query": normalized}

# if __name__ == "__main__":
#     test_inputs = [
#     "Can you tell me the interest rates of Lao Viet Bank?",
#     "ຂໍຖາມ ກ່ຽວກັບ ການກູ້ຢືມ ທະນາຄານ ລາວ ໄວດ",
#     "Please, what is LVB's exchange rate today?",
#     "ສະບາຍດີ ຂ້ອຍຢາກຮູ້ອັດຕາແລກປ່ຽນ",
# ]
#     for query in test_inputs:
#         results = normalize_query({"query":query})
#         print(f"Raw:{query}")
#         print(f"{results['query']}")
#         print("_____")