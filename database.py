# database.py
"""
Ushbu fayl SQLite ma'lumotlar bazasi bilan bog'liq barcha funksiyalarni
o'z ichiga oladi. Aiogram v3 to'liq asinxron (async) ishlagani uchun,
biz ham "aiosqlite" kutubxonasidan foydalanamiz - bu botni sekinlatmaydi.

Jadval tuzilishi (users):
    user_id        - Telegramdagi noyob foydalanuvchi ID raqami (Primary Key)
    username       - Telegram username (@mavjud bo'lmasa NULL)
    full_name      - Foydalanuvchining to'liq ismi (Telegramdagi ism-familiya)
    registered_at  - Ro'yxatdan o'tgan sana va vaqt
"""

import aiosqlite
from datetime import datetime
from config import DATABASE_NAME


async def init_db() -> None:
    """Bot ishga tushganda chaqiriladi - jadvalni yaratadi (agar mavjud bo'lmasa)."""
    async with aiosqlite.connect(DATABASE_NAME) as db:
        await db.execute(
            """
            CREATE TABLE IF NOT EXISTS users (
                user_id INTEGER PRIMARY KEY,
                username TEXT,
                full_name TEXT,
                registered_at TEXT
            )
            """
        )
        await db.commit()


async def add_user(user_id: int, username: str, full_name: str) -> None:
    """
    Yangi foydalanuvchini bazaga qo'shadi.
    Agar foydalanuvchi allaqachon mavjud bo'lsa - username va ismini
    yangilaydi (masalan, foydalanuvchi ismini o'zgartirgan bo'lishi mumkin).
    """
    async with aiosqlite.connect(DATABASE_NAME) as db:
        await db.execute(
            """
            INSERT INTO users (user_id, username, full_name, registered_at)
            VALUES (?, ?, ?, ?)
            ON CONFLICT(user_id) DO UPDATE SET
                username = excluded.username,
                full_name = excluded.full_name
            """,
            (user_id, username, full_name, datetime.now().strftime("%Y-%m-%d %H:%M:%S")),
        )
        await db.commit()


async def get_user(user_id: int):
    """Bitta foydalanuvchi haqida to'liq ma'lumotni qaytaradi (yoki None)."""
    async with aiosqlite.connect(DATABASE_NAME) as db:
        db.row_factory = aiosqlite.Row
        async with db.execute(
            "SELECT * FROM users WHERE user_id = ?", (user_id,)
        ) as cursor:
            row = await cursor.fetchone()
            return dict(row) if row else None


async def get_total_users() -> int:
    """Bazadagi jami foydalanuvchilar sonini qaytaradi."""
    async with aiosqlite.connect(DATABASE_NAME) as db:
        async with db.execute("SELECT COUNT(*) FROM users") as cursor:
            result = await cursor.fetchone()
            return result[0] if result else 0


async def get_stats() -> dict:
    """Admin panel uchun to'liq statistikani hisoblab qaytaradi: jami foydalanuvchilar soni."""
    async with aiosqlite.connect(DATABASE_NAME) as db:
        stats = {}

        async with db.execute("SELECT COUNT(*) FROM users") as cur:
            stats["total"] = (await cur.fetchone())[0]

        return stats


async def get_recent_users(limit: int = 10) -> list:
    """
    Admin panelda ko'rsatish uchun so'nggi ro'yxatdan o'tgan
    foydalanuvchilar ro'yxatini qaytaradi.
    """
    async with aiosqlite.connect(DATABASE_NAME) as db:
        db.row_factory = aiosqlite.Row
        async with db.execute(
            "SELECT * FROM users ORDER BY registered_at DESC LIMIT ?", (limit,)
        ) as cursor:
            rows = await cursor.fetchall()
            return [dict(row) for row in rows]
