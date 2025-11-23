"""
LLM клиент для работы с OpenRouter API
"""
import asyncio
import httpx
from config import OPENROUTER_API_KEY, OPENROUTER_MODEL, OPENROUTER_BASE_URL


# Системный промпт для роли "Финансовый гид"
SYSTEM_PROMPT = """Ты — Финансовый гид, ИИ-ассистент, который помогает клиентам банка:
- Решать повседневные финансовые задачи
- Получать персональные рекомендации
- Получать мгновенный доступ к информации о продуктах и услугах

Отвечай дружелюбно, профессионально и полезно. Если не знаешь точного ответа, признай это и предложи обратиться к специалисту банка."""


def _make_llm_request(user_message: str, conversation_history: list = None) -> str:
    """
    Синхронная функция для отправки запроса в LLM через OpenRouter API.
    Использует прямые HTTP запросы для точного контроля заголовков.
    """
    # Проверяем, что API ключ загружен
    if not OPENROUTER_API_KEY:
        raise Exception("OPENROUTER_API_KEY не установлен в конфигурации")

    # Формируем список сообщений
    messages = [
        {"role": "system", "content": SYSTEM_PROMPT}
    ]
    
    # Добавляем историю диалога, если она есть
    if conversation_history:
        messages.extend(conversation_history)
    
    # Добавляем текущее сообщение пользователя
    messages.append({"role": "user", "content": user_message})
    
    # Формируем URL для запроса
    url = f"{OPENROUTER_BASE_URL}/chat/completions"
    
    # Подготавливаем заголовки (OpenRouter требует правильный формат)
    headers = {
        "Authorization": f"Bearer {OPENROUTER_API_KEY}",
        "Content-Type": "application/json",
        "Referer": "https://github.com/sber-agents/03-aidd",  # Для отслеживания использования
        "X-Title": "Telegram Financial Assistant Bot",  # Название приложения
    }
    
    # Подготавливаем тело запроса
    payload = {
        "model": OPENROUTER_MODEL,
        "messages": messages,
    }
    
    # Отправляем запрос в LLM
    try:
        with httpx.Client(timeout=60.0) as client:
            response = client.post(url, headers=headers, json=payload)
            response.raise_for_status()  # Вызовет исключение для статусов 4xx/5xx
            
            result = response.json()
            
            # Извлекаем и возвращаем текст ответа
            if "choices" in result and len(result["choices"]) > 0:
                return result["choices"][0]["message"]["content"]
            else:
                raise Exception(f"Неожиданный формат ответа от API: {result}")
                
    except httpx.HTTPStatusError as e:
        # Обработка HTTP ошибок (401, 403, 500 и т.д.)
        error_detail = "Неизвестная ошибка"
        try:
            error_detail = e.response.json()
        except:
            error_detail = e.response.text
            
        if e.response.status_code == 401:
            raise Exception(
                f"Ошибка авторизации OpenRouter API (401). "
                f"Проверьте, что API ключ правильный и активен. "
                f"Детали: {error_detail}"
            )
        else:
            raise Exception(
                f"Ошибка при запросе к OpenRouter API: {e.response.status_code}. "
                f"Детали: {error_detail}"
            )
    except Exception as e:
        raise Exception(f"Ошибка при запросе к OpenRouter API: {str(e)}")


async def get_llm_response(user_message: str, conversation_history: list = None) -> str:
    """
    Асинхронная функция для отправки запроса в LLM через OpenRouter API.
    """
    # Запускаем синхронный запрос в отдельном потоке
    return await asyncio.to_thread(_make_llm_request, user_message, conversation_history)
