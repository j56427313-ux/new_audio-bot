# states.py
# ---------------------------------------------------------------------------
# Bot ishlayotgan vaqtda vaqtinchalik saqlanadigan ma'lumotlar (RAM'da).
# Bot qayta ishga tushirilsa, bu ma'lumotlar tozalanadi — bu oddiy holat
# uchun yetarli, katta loyihada bu o'rniga baza (SQLite) ishlatiladi.
# ---------------------------------------------------------------------------

# forward qilingan xabar_id (admin chatida) -> shu xabarni yozgan foydalanuvchi ID
# Admin forward qilingan xabarga Reply qilganda, qaysi userga javob
# yuborish kerakligini shu lug'at orqali topamiz.
forward_map: dict[int, int] = {}

# har bir foydalanuvchi (chat_id) uchun oxirgi yuborgan link
# "Video" yoki "Musiqa" tugmasi bosilganda shu linkni yuklaymiz.
pending_links: dict[int, str] = {}


def save_forward(forwarded_msg_id: int, user_id: int) -> None:
    """Adminga forward qilingan xabar bilan foydalanuvchini bog'lash."""
    forward_map[forwarded_msg_id] = user_id


def get_user_by_forward(forwarded_msg_id: int) -> int | None:
    """Admin qaysi xabarga Reply qilganini bilib, foydalanuvchi ID'sini topish."""
    return forward_map.get(forwarded_msg_id)


def save_pending_link(chat_id: int, url: str) -> None:
    """Foydalanuvchi yuborgan linkni vaqtincha saqlash (tugma bosilishini kutib)."""
    pending_links[chat_id] = url


def get_pending_link(chat_id: int) -> str | None:
    return pending_links.get(chat_id)


def clear_pending_link(chat_id: int) -> None:
    pending_links.pop(chat_id, None)