# main.py
"""
Maktab Telegram Boti - Asosiy ishga tushirish fayli

Ishga tushirish uchun:
    1. .env.example faylini nusxalab, nomini ".env" ga o'zgartiring
    2. .env faylida API_TOKEN va ADMIN_ID ni to'g'ri kiriting
    3. Terminalda quyidagi buyruqni bajaring:
        pip install -r requirements.txt
    4. Botni ishga tushiring:
        python main.py
"""

import asyncio
import logging

from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode

import config
import database as db
from handlers import router


async def main():
    # Loglarni sozlaymiz - konsolda botning ishlashini kuzatish uchun foydali
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s - %(levelname)s - %(message)s",
    )
    logger = logging.getLogger(__name__)

    # Ma'lumotlar bazasini ishga tushirish (jadval mavjud bo'lmasa yaratadi)
    await db.init_db()
    logger.info("✅ Ma'lumotlar bazasi tayyor.")

    # Bot obyektini yaratamiz. Barcha xabarlar avtomatik HTML formatida yuboriladi
    bot = Bot(
        token=config.API_TOKEN,
        default=DefaultBotProperties(parse_mode=ParseMode.HTML),
    )

    # Dispatcher - kiruvchi xabarlarni handlerlarga yo'naltiruvchi asosiy obyekt
    dp = Dispatcher()

    # handlers.py dagi barcha buyruq/tugma handlerlarini ulaymiz
    dp.include_router(router)

    # Eski (keraksiz) update'larni tashlab, botni polling rejimida ishga tushiramiz
    await bot.delete_webhook(drop_pending_updates=True)

    logger.info("🚀 Bot muvaffaqiyatli ishga tushdi!")
    await dp.start_polling(bot)


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("🛑 Bot to'xtatildi.")
