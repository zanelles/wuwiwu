import os
from aiogram import Bot, Dispatcher, types
from aiogram.filters import Command
from aiogram.fsm.storage.memory import MemoryStorage
from dotenv import load_dotenv
import openai
from collections import defaultdict

load_dotenv()

API_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
openai.api_key = os.getenv("OPENROUTER_API_KEY")

# Убедитесь, что вы используете правильную базовую URL для OpenRouter
openai.api_base = "https://openrouter.ai/api/v1"

async def get_llm_response(user_id, message_text):
    response = await openai.ChatCompletion.acreate(
        model="deepseek/deepseek-r1-0528-qwen3-8b:free",
        messages=[
            {"role": "user", "content": message_text}
        ]
    )
    # Возвращаем текст ответа от модели
    return response.choices[0].message['content']

bot = Bot(token=API_TOKEN)
storage = MemoryStorage()
dp = Dispatcher(storage=storage)

@dp.message(Command("start", "reset"))
async def send_welcome_and_reset(message: types.Message):
    user_id = message.from_user.id
    await message.reply("Привет! Я ваш бот. История диалога была сброшена. Как я могу помочь вам сегодня?")

@dp.message(Command("help"))
async def send_help(message: types.Message):
    await message.reply("Справка: просто отправьте мне сообщение, и я постараюсь ответить!")

@dp.message()
async def handle_message(message: types.Message):
    user_id = message.from_user.id
    # Получение ответа от модели
    response = await get_llm_response(user_id, message.text)
    # Отправка ответа пользователю
    await message.answer(response)


if __name__ == '__main__':
    dp.run_polling(bot)
