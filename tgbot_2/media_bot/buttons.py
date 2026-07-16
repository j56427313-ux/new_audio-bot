# buttons.py
# ---------------------------------------------------------------------------
# Botda ishlatiladigan barcha inline tugmalar (keyboard) shu yerda yig'ilgan.
# ---------------------------------------------------------------------------

from telegram import InlineKeyboardButton, InlineKeyboardMarkup


def download_choice_keyboard() -> InlineKeyboardMarkup:
    """Link yuborilgach chiqadigan 'Video / Musiqa' tanlov tugmalari."""
    return InlineKeyboardMarkup(
        [
            [
                InlineKeyboardButton("🎥 Video", callback_data="dl_video"),
                InlineKeyboardButton("🎵 Musiqa (mp3)", callback_data="dl_audio"),
            ]
        ]
    )