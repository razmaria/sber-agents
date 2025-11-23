from aiogram import Router
from aiogram.types import Message

router = Router()


@router.message()
async def handle_message(message: Message):
    # Пока просто отвечаем фиксированным текстом
    await message.answer(
        "Привет! Я финансовый гид. Пока что я только учусь, но скоро смогу помочь вам с финансовыми вопросами."
    )


