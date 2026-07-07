# config.py
"""
Ushbu fayl botning barcha sozlamalarini bir joyda saqlaydi:
- .env fayldan maxfiy ma'lumotlarni (API_TOKEN, ADMIN_ID) yuklaydi
- Maktabga oid ochiq ma'lumotlarni (linklar, manzil, telefon) saqlaydi

Diqqat: API_TOKEN va ADMIN_ID hech qachon kod ichida to'g'ridan-to'g'ri
yozilmaydi - xavfsizlik uchun ular .env faylidan o'qiladi.
"""

import os
from dotenv import load_dotenv

# .env faylini yuklaymiz
load_dotenv()

# --- MAXFIY MA'LUMOTLAR (.env faylidan) ---
API_TOKEN: str = os.getenv("API_TOKEN")
ADMIN_ID: int = int(os.getenv("ADMIN_ID", "0"))

# Agar .env sozlanmagan bo'lsa - dasturchiga xato beramiz
if not API_TOKEN:
    raise ValueError(
        "❌ API_TOKEN topilmadi! Iltimos, .env faylini yarating va "
        "unga API_TOKEN=... qatorini qo'shing."
    )

if ADMIN_ID == 0:
    raise ValueError(
        "❌ ADMIN_ID topilmadi! Iltimos, .env faylida ADMIN_ID=... "
        "qatorini to'g'ri kiriting."
    )

# --- MAKTAB HAQIDA OCHIQ MA'LUMOTLAR ---
# Bu joylardagi qiymatlarni o'zingizning maktabingiz ma'lumotlariga
# moslab o'zgartiring.

SCHOOL_NAME = "🏫 20-son Maktab"

# Maktab veb-sayti (Telegram Web App sifatida ochiladi, https bo'lishi shart)
WEBAPP_URL = "https://example-maktab.uz"

# Ijtimoiy tarmoqlar
INSTAGRAM_URL = "https://instagram.com/maktab_example"
TELEGRAM_CHANNEL_URL = "https://t.me/maktab_example_channel"

# Aloqa ma'lumotlari
SCHOOL_ADDRESS = "Toshkent shahri, Chilonzor tumani, 25-uy"
SCHOOL_PHONE_1 = "+998 71 123 45 67"
SCHOOL_PHONE_2 = "+998 90 123 45 67"
SCHOOL_EMAIL = "info@maktab-example.uz"

# Maktab haqida qisqacha matn (/about buyrug'i uchun)
ABOUT_TEXT = (
    f"🏫 <b>{SCHOOL_NAME}</b>\n\n"
    "📚 Bizning maktab 1985-yildan buyon zamonaviy ta'lim xizmatlarini "
    "yosh avlodga yetkazib kelmoqda.\n\n"
    "✅ Zamonaviy o'quv xonalari\n"
    "✅ Malakali va tajribali o'qituvchilar\n"
    "✅ Chet tillari chuqurlashtirilgan sinflar\n"
    "✅ Sport va ijodiy to'garaklar\n"
    "✅ Raqamli ta'lim texnologiyalari\n\n"
    "🎯 <i>Bizning maqsadimiz - har bir o'quvchida bilim, "
    "ahloq va zamonaviy ko'nikmalarni uyg'unlikda rivojlantirish!</i>"
)

# Baza faylining nomi
DATABASE_NAME = "school_bot.db"
