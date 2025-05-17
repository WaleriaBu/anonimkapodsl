import asyncio
from aiogram import Bot, Dispatcher, types
from aiogram.enums import ParseMode
from aiogram.client.default import DefaultBotProperties
from aiogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.filters import CommandStart
from aiogram.fsm.storage.memory import MemoryStorage

API_TOKEN = '7909844613:AAEoh317Q8ah89Bii-WydIiaL0ecMMzCx-0'
CHANNEL_ID = '@Podsluhaprimkvn'
COOLDOWN = 30

last_message_time = {}

bot = Bot(token=API_TOKEN, default=DefaultBotProperties(parse_mode=ParseMode.HTML))
dp = Dispatcher(storage=MemoryStorage())

@dp.message(CommandStart())
async def start(message: Message):
    await message.answer("Привет, крысиный собрат! Пиши свой писк или кидай фото/видео — и я передам в нору.")

@dp.message()
async def anon_forward(message: Message):
    user_id = message.from_user.id
    now = asyncio.get_event_loop().time()

    if user_id in last_message_time and now - last_message_time[user_id] < COOLDOWN:
        await message.answer("СПАМИТЬ ЗАПРЕЩЕНО! БАН 30 СЕК.")
        return

    last_message_time[user_id] = now

    if message.text:
        text = message.text.strip()
        banned_words = ['http', 'реклама', 'подпишись']
        if any(word in text.lower() for word in banned_words) or len(text) < 10:
            await message.answer("Что за хуйню ты мне шлешь??")
            return
        await bot.send_message(CHANNEL_ID, f"Крысиный писк:\n{text}")
        await message.answer("Отправлено!")

    elif message.photo:
        caption = message.caption or ""
        await bot.send_photo(CHANNEL_ID, message.photo[-1].file_id, caption=f"🐀 Анонимное фото:\n{caption}")
        await message.answer("Спасибо за мем.")

    elif message.video:
        caption = message.caption or ""
        await bot.send_video(CHANNEL_ID, message.video.file_id, caption=f"🐀 Анонимное видео:\n{caption}")
        await message.answer("Видеопруф зафиксирован.")

    else:
        await message.answer("Пока что я принимаю только текст, фото и видео. А говно которое ты прислал, я не пон.")

async def monthly_reminder():
    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="НАПИСАТЬ СЛУХ", url="https://t.me/Anoanoano1Bot")]
    ])
    await bot.send_message(CHANNEL_ID, "📢 Хочешь рассказать что-то анонимно?", reply_markup=keyboard)

    while True:
        await asyncio.sleep(30 * 24 * 60 * 60)
        await bot.send_message(CHANNEL_ID, "📢 Хочешь рассказать что-то анонимно?", reply_markup=keyboard)

async def main():
    asyncio.create_task(monthly_reminder())
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
