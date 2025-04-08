from app.config import Config
import httpx

def call_ark(input):
    query = input.get("query", "")
    user_id = input.get("user_id", "anonymous")
    context = input.get("context")
    history = input.get("chat_history", [])

    headers = {
        "Authorization": f"Bearer {Config.ARK_API_KEY}",
        "Content-Type": "application/json"
    }

    # ✅ System message luôn đứng đầu
    system_prompts = [
        {"role": "system", "content": "ທ່ານແມ່ນຜູ້ຊ່ວຍສ່ວນຕົວອັນສະຫຼາດ ຂອງທະນາຄານ Lao Viet Bank. ໜ້າທີ່ຂອງທ່ານແມ່ນໃຫ້ຂໍ້ມູນທີ່ຖືກຕ້ອງ ແລະທັນເວລາ."},
        {"role": "system", "content": "ຖ້າຄຳຖາມເກັ່ງກ່ຽວກັບອັດຕາແລກປ່ຽນ, ໃຫ້ແນະນຳໃຫ້ໃຊ້ຊື່ສະກຸນເງິນທີ່ຖືກຕ້ອງ (USD, LAK, VND)."},
        {"role": "system", "content": "ໃນການຕອບກັບ, ໃຫ້ໃຊ້ຂໍ້ມູນຈາກພາຍໃນແລະບໍ່ເສີມເຕີມຂໍ້ມູນອື່ນ."}
    ]

    # ✅ Context nội bộ nếu có
    if context:
        system_prompts.append({
            "role": "system",
            "content": f"📚 Dữ liệu nội bộ (vector search):\n{context}"
        })

    # ✅ Final message history gồm system + hội thoại cũ + query mới
    messages = system_prompts + history + [
        {"role": "user", "content": query}
    ]
    payload = {
        "model": "ep-20250226190052-v82z2",
        "stream": False,
        "messages": messages,
        "user_id": user_id,
        "temperature": 0.3,
        "top_p": 0.9,
        "max_tokens": 1440
    }

    ark_url = "https://ark.ap-southeast.bytepluses.com/api/v3/chat/completions"

    try:
        response = httpx.post(ark_url, json=payload, headers=headers, timeout=20)
        response.raise_for_status()
        result = response.json()

        answer = result.get("choices", [{}])[0].get("message", {}).get("content")
        if answer:
            input["answer"] = answer.strip()
            input["source"] = "ark"
        else:
            print("❌ ARK trả về không có answer")
            input["ark_failed"] = True

    except Exception as e:
        print("❌ ARK error:", e)
        input["ark_failed"] = True

    return input
