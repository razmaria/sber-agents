from aiogram import Router
from aiogram.types import Message
from aiogram.enums import ChatAction
from aiogram.filters import Command
from llm_client import get_llm_response

router = Router()


@router.message(Command("start"))
async def command_start_handler(message: Message) -> None:
    """
    Обработчик команды /start
    """
    await message.answer("Привет! Я финансовый гид. Я готов помочь вам с финансовыми вопросами.")


@router.message()
async def handle_message(message: Message):
    # Получаем текст сообщения от пользователя
    user_text = message.text or message.caption or ""
    
    if not user_text:
        await message.answer("Пожалуйста, отправьте текстовое сообщение.")
        return
    
    # Показываем индикатор набора текста
    await message.bot.send_chat_action(chat_id=message.chat.id, action=ChatAction.TYPING)
    
    # Получаем ответ от LLM (без истории диалога для этой итерации)
    try:
        llm_response = await get_llm_response(user_text)
        # Отправляем ответ пользователю
        await message.answer(llm_response)
    except Exception as e:
        # Временно обрабатываем ошибки простым сообщением
        # Более детальная обработка будет в итерации 5
        await message.answer(f"Произошла ошибка при обработке запроса: {str(e)}")


