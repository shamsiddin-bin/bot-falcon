# 🏫 Maktab Telegram Boti

Aiogram v3 va SQLite (aiosqlite) asosida yozilgan maktab uchun Telegram bot.

## 📁 Fayllar tuzilishi

```
school_bot/
├── .env.example      # Muhit o'zgaruvchilari namunasi (nusxalab .env qiling)
├── config.py         # Sozlamalar: .env dan token/admin, maktab ma'lumotlari
├── database.py       # SQLite bilan ishlash (aiosqlite, to'liq async)
├── keyboards.py       # Inline va Reply klaviaturalar
├── handlers.py       # /start, /help, /about, /contacts va callback handlerlar
├── main.py           # Botni ishga tushiruvchi asosiy fayl
└── requirements.txt  # Kerakli kutubxonalar
```

## ⚙️ O'rnatish

1. **Kutubxonalarni o'rnating:**
   ```bash
   pip install -r requirements.txt
   ```

2. **`.env` faylini yarating:**
   `.env.example` faylidan nusxa oling va nomini `.env` ga o'zgartiring:
   ```bash
   cp .env.example .env
   ```
   Keyin `.env` faylini oching va quyidagilarni to'ldiring:
   - `API_TOKEN` — [@BotFather](https://t.me/BotFather) orqali olingan token
   - `ADMIN_ID` — sizning Telegram ID raqamingiz ([@userinfobot](https://t.me/userinfobot) orqali bilib olishingiz mumkin)

3. **`config.py` faylida maktab ma'lumotlarini o'zgartiring:**
   - `WEBAPP_URL` — maktab veb-sayti manzili (https bilan boshlanishi shart)
   - `INSTAGRAM_URL`, `TELEGRAM_CHANNEL_URL` — ijtimoiy tarmoq linklari
   - `SCHOOL_ADDRESS`, `SCHOOL_PHONE_1/2`, `SCHOOL_EMAIL` — aloqa ma'lumotlari
   - `ABOUT_TEXT` — maktab haqida matn

4. **Botni ishga tushiring:**
   ```bash
   python main.py
   ```

## 🔄 Foydalanuvchi jarayoni

1. Foydalanuvchi `/start` bosadi → ismi va IDsi bazaga saqlanadi
2. Bot undan telefon raqamini so'raydi (maxsus tugma orqali)
3. Raqam ulashilgach, "👨‍👩‍👧‍👦 Ota-ona" yoki "🎓 O'quvchi" tanlanadi
4. Shundan so'ng to'liq Inline menyu ochiladi:
   - 🏫 Maktab Web App
   - 📸 Instagram / 📢 Telegram Kanal
   - ℹ️ Biz haqimizda / 📞 Aloqa
   - ⚙️ Admin Panel (faqat ADMIN_ID uchun)

## ⚙️ Admin Panel imkoniyatlari

- Jami foydalanuvchilar soni
- Telefon raqamini ulashganlar soni
- Ota-onalar va o'quvchilar soni alohida
- So'nggi 5 ta ro'yxatdan o'tgan foydalanuvchi (ism, ID, username, telefon, rol)

## 🔒 Xavfsizlik eslatmalari

- `.env` faylini **hech qachon** GitHub yoki ochiq joyga yuklamang
- Telefon raqami faqat foydalanuvchining o'zi yuborgan holatdagina qabul qilinadi
- Admin Panelga faqat `.env` dagi `ADMIN_ID` ga mos foydalanuvchi kira oladi
