import logging

from aiogram import BaseMiddleware
from aiogram.types import TelegramObject, Message, CallbackQuery
from aiogram.client.session.middlewares.base import BaseRequestMiddleware
from aiogram.methods import SendMessage, EditMessageText
from typing import Callable, Dict, Any, Awaitable

from obuna import obunani_tekshir, obuna_klaviaturasi, OBUNA_MATNI

ADMIN_ID = 7467403246

# Adminga yuborilgan log-xabar ID'sini foydalanuvchi ID'siga bog'laydi.
# Shu orqali admin log-xabarga "Reply" qilib, to'g'ridan-to'g'ri
# o'sha foydalanuvchiga javob yozishi mumkin bo'ladi.
admin_reply_map: Dict[int, int] = {}


class SubscriptionMiddleware(BaseMiddleware):
    """
    Adminidan boshqa har bir foydalanuvchini majburiy kanallarga obuna
    bo'lganligini tekshiradi. Obuna bo'lmagan bo'lsa, botning boshqa
    handlerlariga umuman yo'l bermaydi va obuna klaviaturasini ko'rsatadi.
    """

    async def __call__(
        self,
        handler: Callable[[TelegramObject, Dict[str, Any]], Awaitable[Any]],
        event: TelegramObject,
        data: Dict[str, Any],
    ) -> Any:
        user = event.from_user

        # Admin uchun majburiy obuna talab qilinmaydi
        if not user or user.id == ADMIN_ID:
            return await handler(event, data)

        # "✅ Obunani tekshirish" tugmasi hali obuna bo'lmagan holatda ham
        # bosila olishi kerak, shuning uchun uni to'sib qo'ymaymiz
        if isinstance(event, CallbackQuery) and event.data == "check_subscription":
            return await handler(event, data)

        obuna_bolmagan = await obunani_tekshir(event.bot, user.id)

        if obuna_bolmagan:
            kb = obuna_klaviaturasi(obuna_bolmagan)
            if isinstance(event, Message):
                await event.answer(OBUNA_MATNI, reply_markup=kb, parse_mode="HTML")
            elif isinstance(event, CallbackQuery):
                await event.answer(
                    "❌ Botdan foydalanish uchun avval kanallarga obuna bo'ling!",
                    show_alert=True,
                )
                await event.message.answer(OBUNA_MATNI, reply_markup=kb, parse_mode="HTML")
            return  # handler chaqirilmaydi

        return await handler(event, data)


class IncomingLogMiddleware(BaseMiddleware):
    """Foydalanuvchi botga yozgan har bir xabarni adminga jo'natadi."""

    async def __call__(
        self,
        handler: Callable[[TelegramObject, Dict[str, Any]], Awaitable[Any]],
        event: TelegramObject,
        data: Dict[str, Any],
    ) -> Any:
        user = event.from_user

        # Adminning o'z xabarlarini qayta o'ziga jo'natmaymiz
        if user and user.id != ADMIN_ID:
            try:
                username_qismi = f" (@{user.username})" if user.username else ""

                if isinstance(event, Message):
                    matn = event.text or event.caption or f"[{event.content_type}]"
                    log_msg = await event.bot.send_message(
                        ADMIN_ID,
                        f"👤 <b>{user.full_name}</b>{username_qismi} (id: <code>{user.id}</code>) yozdi:\n{matn}",
                        parse_mode="HTML",
                    )
                    admin_reply_map[log_msg.message_id] = user.id
                elif isinstance(event, CallbackQuery):
                    log_msg = await event.bot.send_message(
                        ADMIN_ID,
                        f"👤 <b>{user.full_name}</b>{username_qismi} (id: <code>{user.id}</code>) "
                        f"tugma bosdi: <code>{event.data}</code>",
                        parse_mode="HTML",
                    )
                    admin_reply_map[log_msg.message_id] = user.id
            except Exception:
                logging.exception("Adminga kiruvchi xabarni yuborishda xatolik")

        return await handler(event, data)


class OutgoingLogMiddleware(BaseRequestMiddleware):
    """Bot yuborgan har bir javobni (matnli xabar/tahrir) adminga jo'natadi."""

    def __init__(self):
        super().__init__()
        # chat_id -> tayyor ko'rinishdagi nom (@username yoki to'liq ism)
        # Har safar get_chat chaqirmaslik uchun keshlab qo'yamiz.
        self._chat_nom_keshi: Dict[int, str] = {}

    async def _foydalanuvchi_nomini_ol(self, bot, chat_id) -> str:
        """chat_id bo'yicha @username (bo'lmasa to'liq ism, u ham bo'lmasa ID) qaytaradi."""
        if chat_id in self._chat_nom_keshi:
            return self._chat_nom_keshi[chat_id]

        nom = f"id: <code>{chat_id}</code>"
        try:
            chat = await bot.get_chat(chat_id)
            if chat.username:
                nom = f"id: <code>{chat_id}</code>, @{chat.username}"
            elif getattr(chat, "full_name", None):
                nom = f"id: <code>{chat_id}</code>, {chat.full_name}"
        except Exception:
            logging.exception(f"{chat_id} uchun foydalanuvchi ma'lumotini olishda xatolik")

        self._chat_nom_keshi[chat_id] = nom
        return nom

    async def __call__(self, make_request, bot, method):
        result = await make_request(bot, method)

        try:
            chat_id = getattr(method, "chat_id", None)
            text = getattr(method, "text", None)

            # Adminga yuborilayotgan (yoki chat_id bo'lmagan) xabarlarni qayta log qilmaymiz
            if (
                isinstance(method, (SendMessage, EditMessageText))
                and text
                and chat_id is not None
                and str(chat_id) != str(ADMIN_ID)
            ):
                foydalanuvchi = await self._foydalanuvchi_nomini_ol(bot, chat_id)
                await bot.send_message(
                    ADMIN_ID,
                    f"🤖 Bot javobi ({foydalanuvchi}):\n{text}",
                    parse_mode="HTML",
                )
        except Exception:
            logging.exception("Adminga chiquvchi xabarni yuborishda xatolik")

        return result