from openai import OpenAI
from app.config import Config

client = OpenAI(api_key=Config.OPENAI_API_KEY)

def fall_back_gpt(input):
    query = input.get("query", "")
    user_id = input.get("user_id", "anonymous")
    context = input.get("context")

    # ✅ System message chuẩn
    messages = [
        {"role": "system", "content": "ທ່ານແມ່ນຜູ້ຊ່ວຍສ່ວນຕົວອັນສະຫຼາດ ຂອງທະນາຄານ Lao Viet Bank. ໜ້າທີ່ຂອງທ່ານແມ່ນໃຫ້ຂໍ້ມູນທີ່ຖືກຕ້ອງ ແລະທັນເວລາກ່ຽວກັບການເງິນ ອັດຕາແລກປ່ຽນ ແລະຄະນະຜູ້ນຳ."},
        {"role": "system", "content": "ຖ້າຄຳຖາມເກັ່ງກ່ຽວກັບອັດຕາແລກປ່ຽນ, ໃຫ້ແນະນຳໃຫ້ໃຊ້ຊື່ສະກຸນເງິນທີ່ຖືກຕ້ອງ (ເຊັ່ນ USD, LAK, VND). ຖ້າເປັນຄຳຖາມກ່ຽວກັບຄະນະຜູ້ນຳ ໃຫ້ໃຊ້ຂໍ້ມູນລ່າສຸດທີ່ມີ."},
        {"role": "system", "content": "ໃນການຕອບກັບ, ໃຫ້ໃຊ້ຂໍ້ມູນຈາກພາຍໃນໄດ້ຢ່າງມີຂອບເຂດ ແລະບໍ່ເສີມເຕີມເລື່ອງທີ່ບໍ່ຢູ່ໃນບັນທຶກ."}
    ]

    if context:
        messages.append({
            "role": "system",
            "content": f"📚 ຂໍ້ມູນຈາກ vector search:\n{context}"
        })

    messages.append({
        "role": "user",
        "content": query
    })

    try:
        res = client.chat.completions.create(
            model="gpt-4o",
            messages=messages,
            temperature=0.3,
            max_tokens=1440
        )
        answer = res.choices[0].message.content.strip()
        input["answer"] = answer
        input["source"] = "gpt"
    except Exception as e:
        print("❌ GPT fallback error:", e)
        input["gpt_failed"] = True

    return input
