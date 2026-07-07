# keyboards.py
"""
Ushbu fayl botda ishlatiladigan barcha klaviaturalarni (tugmalarni)
bir joyda saqlaydi. Bu kodni toza va boshqarish uchun qulay qiladi.
"""

from aiogram.types import (
    InlineKeyboardMarkup,
    InlineKeyboardButton,
    WebAppInfo,
)

import config


def main_menu_keyboard(is_admin: bool = False) -> InlineKeyboardMarkup:
    """
    Botning asosiy Inline menyusi.
    Agar foydalanuvchi admin bo'lsa, qo'shimcha "⚙️ Admin Panel" tugmasi chiqadi.
    """
    buttons = [
        [
            InlineKeyboardButton(
                text="🏫 Maktab Web App",
                web_app=WebAppInfo(url=config.WEBAPP_URL),
            )
        ],
        [
            InlineKeyboardButton(text="📸 Instagram", url=config.INSTAGRAM_URL),
            InlineKeyboardButton(text="📢 Telegram Kanal", url=config.TELEGRAM_CHANNEL_URL),
        ],
        [
            InlineKeyboardButton(text="ℹ️ Biz haqimizda", callback_data="about"),
            InlineKeyboardButton(text="📞 Aloqa", callback_data="contacts"),
        ],
    ]

    if is_admin:
        buttons.append(
            [InlineKeyboardButton(text="⚙️ Admin Panel", callback_data="admin_panel")]
        )

    return InlineKeyboardMarkup(inline_keyboard=buttons)


def back_to_menu_keyboard() -> InlineKeyboardMarkup:
    """Ortga - asosiy menyuga qaytish tugmasi."""
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text="◀️ Asosiy menyu", callback_data="back_to_menu")]
        ]
    )

