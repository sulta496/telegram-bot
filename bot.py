import asyncio
import re
from aiogram import Bot, Dispatcher, F, types
from aiogram.filters import Command
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton, MessageEntity

# استبدل هذا السطر بالتوكن الخاص بك من BotFather
TOKEN = "ضع_التوكن_هنا"

bot = Bot(token=TOKEN)
dp = Dispatcher()

EMOJIS_MAP = {
    # ضع هنا رقم الكود ومعرف الإيموجي الخاص به (Custom Emoji ID)
    # مثال: "1": "1234567890123456789"
}

@dp.message(Command("start"))
async def start_command(message: types.Message):
    text = (
        "قائمة الإيموجيات الجاهزة 🤍\n\n"
        "الطريقة ⬇\n\n"
        "1 ➔ اضغط على اي زر من الازرار في القائمة.\n"
        "2 ➔ انسخ الكود المختصر (مثل {1}) والصقه في أي رسالة.\n"
        "3 ➔ أرسل الرسالة وسيظهر لك المنشور بالإيموجيهات."
    )
    
    keyboard = InlineKeyboardMarkup(inline_markup=[
        [
            InlineKeyboardButton(text="👑 {1}", callback_data="emoji_1"),
            InlineKeyboardButton(text="⚙️ {2}", callback_data="emoji_2")
        ],
        [
            InlineKeyboardButton(text="📌 التالي", callback_data="next_page")
        ]
    ])
    
    await message.answer(text, reply_markup=keyboard)

@dp.message(F.text)
async def text_parser(message: types.Message):
    user_text = message.text
    
    pattern = r"\{(\d+)\}"
    matches = re.findall(pattern, user_text)
    
    if not matches:
        return
    
    entities = []
    processed_text = user_text
    
    for match in matches:
        key = match
        if key in EMOJIS_MAP:
            emoji_id = EMOJIS_MAP[key]
            target_str = f"{{{key}}}"
            idx = processed_text.find(target_str)
            
            if idx != -1:
                entities.append(
                    MessageEntity(
                        type="custom_emoji",
                        offset=idx,
                        length=len(target_str),
                        custom_emoji_id=emoji_id
                    )
                )

    if entities:
        await message.answer(text=processed_text, entities=entities)
    else:
        await message.answer("هذا الرقم غير مسجل في القائمة.")

async def main():
    print("البوت يعمل الآن...")
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
