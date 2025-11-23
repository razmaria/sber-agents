#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Скрипт запуска Telegram-бота
"""
import sys
import os
import io

# Устанавливаем кодировку UTF-8 для вывода
if sys.platform == 'win32':
    try:
        sys.stdout.reconfigure(encoding='utf-8')
        sys.stderr.reconfigure(encoding='utf-8')
    except (AttributeError, ValueError):
        # Для старых версий Python
        sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
        sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8', errors='replace')

# Добавляем src в путь
project_root = os.path.dirname(os.path.abspath(__file__))
src_path = os.path.join(project_root, 'src')
sys.path.insert(0, src_path)

if __name__ == "__main__":
    print("=" * 50)
    print("Запуск Telegram-бота")
    print("=" * 50)
    print(f"Рабочая директория: {project_root}")
    print(f"Python путь: {sys.executable}")
    print(f"Python версия: {sys.version}")
    print("=" * 50)
    
    # Проверяем зависимости
    try:
        import aiogram
        print(f"[OK] aiogram установлен: {aiogram.__version__}")
    except ImportError as e:
        print(f"[ERROR] aiogram не установлен: {e}")
        print("Установите зависимости: py -3 -m pip install aiogram openai python-dotenv")
        sys.exit(1)
    
    try:
        import openai
        print(f"[OK] openai установлен")
    except ImportError as e:
        print(f"[ERROR] openai не установлен: {e}")
        sys.exit(1)
    
    try:
        import dotenv
        print(f"[OK] python-dotenv установлен")
    except ImportError as e:
        print(f"[ERROR] python-dotenv не установлен: {e}")
        sys.exit(1)
    
    # Проверяем .env
    env_path = os.path.join(project_root, '.env')
    if not os.path.exists(env_path):
        print(f"[ERROR] Файл .env не найден: {env_path}")
        sys.exit(1)
    else:
        print(f"[OK] Файл .env найден")
    
    print("=" * 50)
    print("Импорт модулей бота...")
    
    try:
        from config import TELEGRAM_BOT_TOKEN, OPENROUTER_API_KEY
        if TELEGRAM_BOT_TOKEN:
            print(f"[OK] TELEGRAM_BOT_TOKEN загружен (длина: {len(TELEGRAM_BOT_TOKEN)})")
        else:
            print("[ERROR] TELEGRAM_BOT_TOKEN не найден в .env")
            sys.exit(1)
        
        if OPENROUTER_API_KEY:
            print(f"[OK] OPENROUTER_API_KEY загружен")
        else:
            print("[ERROR] OPENROUTER_API_KEY не найден в .env")
            sys.exit(1)
    except Exception as e:
        print(f"[ERROR] Ошибка при загрузке конфигурации: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
    
    print("=" * 50)
    print("Запуск бота...")
    print("Нажмите Ctrl+C для остановки")
    print("=" * 50)
    
    try:
        from bot import main
        import asyncio
        asyncio.run(main())
    except KeyboardInterrupt:
        print("\n" + "=" * 50)
        print("Бот остановлен пользователем")
        print("=" * 50)
    except Exception as e:
        print("\n" + "=" * 50)
        print(f"ОШИБКА при запуске бота:")
        print("=" * 50)
        print(f"{type(e).__name__}: {e}")
        print("=" * 50)
        import traceback
        traceback.print_exc()
        sys.exit(1)

