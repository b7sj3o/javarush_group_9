import asyncio
import os

from aiogram import Bot, Dispatcher
from aiogram.filters import Command, CommandStart
from aiogram.types import Message

from dotenv import load_dotenv

from storage import load_users, save_user

load_dotenv()

dp = Dispatcher()


@dp.message(CommandStart())
async def start(message: Message) -> None:
    visits = save_user(message.from_user.id, message.from_user.full_name)
    print(f"/start від (тест) {message.from_user.full_name}, візит №{visits}", flush=True)
    await message.answer(f"Привіт! Це твій візит №{visits}")


@dp.message(Command("stats"))
async def stats(message: Message) -> None:
    await message.answer(f"Усього користувачів: {len(load_users())}")


async def main() -> None:
    print("Бот запущено", flush=True)
    await dp.start_polling(Bot(os.getenv("BOT_TOKEN")))


if __name__ == "__main__":
    asyncio.run(main())
