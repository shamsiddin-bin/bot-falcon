# handlers.py
"""
Ushbu fayl foydalanuvchi yuboradigan barcha buyruqlar (/start, /help va h.k.)
va tugma bosilishlariga (callback) javob beruvchi funksiyalarni o'z ichiga oladi.

Foydalanuvchi jarayoni (flow):
1. /start bosiladi -> foydalanuvchi bazaga saqlanadi
2. Darhol asosiy Inline menyu ko'rsatiladi (Web App tugmasi shu yerda,
   birinchi qatorda chiqadi) - telefon yoki rol so'ralmaydi
"""

from aiogram import Router, F, Bot
from aiogram.filters import CommandStart, Command
from aiogram.types import Message, CallbackQuery

import config
import database as db
import keyboards as kb

# Router - barcha handlerlarni guruhlab, main.py ichida bitta joyda ulash uchun
router = Router()


def is_admin(user_id: int) -> bool:
    """Foydalanuvchi admin ekanligini tekshiradi (.env dagi ADMIN_ID bilan solishtirib)."""
    return user_id == config.ADMIN_ID


# ==================== /start BUYRUG'I ====================

@router.message(CommandStart())
async def cmd_start(message: Message):
    """
    /start buyrug'i bosilganda ishga tushadi.
    Foydalanuvchini bazaga saqlaydi va darhol asosiy menyuni
    (Web App tugmasi bilan birga) ko'rsatadi.
    """
    user = message.from_user

    # Foydalanuvchini bazaga saqlaymiz (yoki mavjud bo'lsa yangilaymiz)
    await db.add_user(
        user_id=user.id,
        username=user.username or "—",
        full_name=user.full_name,
    )

    welcome_text = (
        f"👋 Assalomu alaykum, <b>{user.full_name}</b>!\n\n"
        f"{config.SCHOOL_NAME} rasmiy botiga xush kelibsiz! 🎉\n\n"
        "👇 Quyidagi menyudan kerakli bo'limni tanlang:"
    )

    await message.answer(
        welcome_text, reply_markup=kb.main_menu_keyboard(is_admin=is_admin(user.id))
    )


# ==================== /help BUYRUG'I ====================

HELP_TEXT = (
    "🆘 <b>Yordam bo'limi</b>\n\n"
    "Ushbu bot orqali siz quyidagi imkoniyatlardan foydalanishingiz mumkin:\n\n"
    "🔹 /start - Botni ishga tushirish va asosiy menyuni ochish\n"
    "🔹 /help - Ushbu yordam matnini ko'rish\n"
    "🔹 /about - Maktabimiz haqida ma'lumot olish\n"
    "🔹 /contacts - Maktab manzili va telefon raqamlarini ko'rish\n\n"
    "📋 Asosiy menyudagi tugmalar orqali:\n"
    "🏫 <b>Maktab Web App</b> - Maktab veb-saytini bot ichida ochadi\n"
    "📸 <b>Instagram</b> - Rasmiy Instagram sahifamiz\n"
    "📢 <b>Telegram Kanal</b> - Rasmiy Telegram kanalimiz\n"
    "ℹ️ <b>Biz haqimizda</b> - Maktab tarixi va yutuqlari\n"
    "📞 <b>Aloqa</b> - Manzil va telefon raqamlar\n\n"
    "❓ Savollaringiz bo'lsa, 📞 Aloqa bo'limi orqali biz bilan bog'laning!"
)


@router.message(Command("help"))
async def cmd_help(message: Message):
    await message.answer(HELP_TEXT, reply_markup=kb.back_to_menu_keyboard())


# ==================== /about BUYRUG'I ====================

@router.message(Command("about"))
async def cmd_about(message: Message):
    await message.answer(config.ABOUT_TEXT, reply_markup=kb.back_to_menu_keyboard())


@router.callback_query(F.data == "about")
async def callback_about(callback: CallbackQuery):
    await callback.message.edit_text(
        config.ABOUT_TEXT, reply_markup=kb.back_to_menu_keyboard()
    )
    await callback.answer()


# ==================== /contacts BUYRUG'I ====================

def build_contacts_text() -> str:
    return (
        "📞 <b>Biz bilan bog'lanish</b>\n\n"
        f"🏫 <b>{config.SCHOOL_NAME}</b>\n\n"
        f"📍 <b>Manzil:</b> {config.SCHOOL_ADDRESS}\n"
        f"☎️ <b>Telefon 1:</b> {config.SCHOOL_PHONE_1}\n"
        f"☎️ <b>Telefon 2:</b> {config.SCHOOL_PHONE_2}\n"
        f"📧 <b>Email:</b> {config.SCHOOL_EMAIL}\n\n"
        "🕘 <b>Ish vaqti:</b> Dushanba - Shanba, 08:00 - 17:00\n\n"
        "😊 Har qanday savol yoki taklif bo'yicha murojaat qilishingiz mumkin!"
    )


@router.message(Command("contacts"))
async def cmd_contacts(message: Message):
    await message.answer(build_contacts_text(), reply_markup=kb.back_to_menu_keyboard())


@router.callback_query(F.data == "contacts")
async def callback_contacts(callback: CallbackQuery):
    await callback.message.edit_text(
        build_contacts_text(), reply_markup=kb.back_to_menu_keyboard()
    )
    await callback.answer()


# ==================== ASOSIY MENYUGA QAYTISH ====================

@router.callback_query(F.data == "back_to_menu")
async def callback_back_to_menu(callback: CallbackQuery):
    await callback.message.edit_text(
        "📋 <b>Asosiy menyu</b>\n\n👇 Quyidagi menyudan kerakli bo'limni tanlang:",
        reply_markup=kb.main_menu_keyboard(is_admin=is_admin(callback.from_user.id)),
    )
    await callback.answer()


# ==================== ADMIN PANEL ====================

@router.callback_query(F.data == "admin_panel")
async def callback_admin_panel(callback: CallbackQuery):
    """
    Faqat ADMIN_ID ga mos foydalanuvchi uchun ishlaydi.
    Bazadagi umumiy statistikani (jami foydalanuvchilar soni) ko'rsatadi.
    """
    user_id = callback.from_user.id

    # Xavfsizlik: admin bo'lmagan foydalanuvchi hech qachon bu ma'lumotni ko'rmasligi kerak
    if not is_admin(user_id):
        await callback.answer("⛔ Sizda ushbu bo'limga ruxsat yo'q!", show_alert=True)
        return

    stats = await db.get_stats()
    recent_users = await db.get_recent_users(limit=5)

    text = (
        "⚙️ <b>ADMIN PANEL</b>\n\n"
        "📊 <b>Umumiy statistika:</b>\n"
        f"👥 Jami foydalanuvchilar: <b>{stats['total']}</b>\n\n"
        "🕐 <b>So'nggi 5 ta ro'yxatdan o'tgan foydalanuvchi:</b>\n"
    )

    if recent_users:
        for i, u in enumerate(recent_users, start=1):
            username = f"@{u['username']}" if u["username"] and u["username"] != "—" else "username yo'q"
            text += (
                f"\n{i}. <b>{u['full_name']}</b>\n"
                f"    🆔 <code>{u['user_id']}</code> | {username}\n"
            )
    else:
        text += "\n<i>Hozircha foydalanuvchilar mavjud emas.</i>"

    await callback.message.edit_text(text, reply_markup=kb.back_to_menu_keyboard())
    await callback.answer()


# ==================== NOMA'LUM XABARLARGA JAVOB ====================

@router.message()
async def handle_unknown_message(message: Message):
    """Foydalanuvchi tushunarsiz/mavjud bo'lmagan buyruq yuborsa ishga tushadi."""
    await message.answer(
        "🤔 Kechirasiz, bu buyruqni tushunmadim.\n\n"
        "Iltimos, /help buyrug'ini yuborib, mavjud buyruqlar bilan tanishing 🙏"
    )
