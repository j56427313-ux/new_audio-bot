"""
🎙️ TEXT -> VOICE (edge-tts) va 🎧 VOICE -> TEXT (whisper) uchun yordamchi funksiyalar.

O'RNATISH:
    pip install edge-tts openai-whisper

MUHIM: openai-whisper ishlashi uchun kompyuterda FFMPEG o'rnatilgan va PATH'ga
qo'shilgan bo'lishi shart, aks holda audio fayllarni o'qiy olmaydi.
    - Windows: https://www.gyan.dev/ffmpeg/builds/ dan yuklab, PATH'ga qo'shing
    - yoki:    choco install ffmpeg   (agar chocolatey o'rnatilgan bo'lsa)
"""

import asyncio
import glob
import os
import shutil
import edge_tts
import whisper

# O'zbek tilida so'zlovchi ovoz. Boshqa ovozlar: edge-tts --list-voices orqali ko'rish mumkin.
OVOZ_AYOL = "uz-UZ-MadinaNeural"
OVOZ_ERKAK = "uz-UZ-SardorNeural"

# Whisper modeli birinchi ishlatilganda yuklanadi va xotirada saqlanadi
# (tiny / base / small / medium / large) - katta model aniqroq, lekin sekinroq.
_WHISPER_MODEL_NOMI = "base"
_whisper_model = None


def _ffmpegni_topish_va_pathga_qoshish() -> bool:
    """ffmpeg PATH'da bormi tekshiradi. Topilmasa, Windows'dagi eng ko'p
    uchraydigan o'rnatish joylaridan qidirib, topsa shu jarayon uchun
    PATH'ga vaqtincha qo'shib qo'yadi (terminalni qayta ochish shart bo'lmaydi)."""
    if shutil.which("ffmpeg"):
        return True

    nomzod_papkalar = [
        r"C:\ffmpeg\bin",
        r"C:\Program Files\ffmpeg\bin",
        r"C:\Program Files (x86)\ffmpeg\bin",
    ]
    # winget "ffmpeg" o'rnatganda odatda shu yerga qo'yadi:
    nomzod_papkalar += glob.glob(
        os.path.expandvars(r"%LOCALAPPDATA%\Microsoft\WinGet\Packages\Gyan.FFmpeg*\**\bin"),
        recursive=True,
    )

    for papka in nomzod_papkalar:
        if os.path.isfile(os.path.join(papka, "ffmpeg.exe")):
            os.environ["PATH"] = papka + os.pathsep + os.environ.get("PATH", "")
            return True

    return False


async def matnni_ovozga_aylantir(matn: str, fayl_path: str, ovoz: str = OVOZ_AYOL) -> None:
    """Berilgan matnni edge-tts orqali ovozli faylga (mp3) aylantiradi."""
    communicate = edge_tts.Communicate(text=matn, voice=ovoz)
    await communicate.save(fayl_path)


def _whisper_modelni_olish():
    global _whisper_model
    if _whisper_model is None:
        _whisper_model = whisper.load_model(_WHISPER_MODEL_NOMI)
    return _whisper_model


def _whisper_transkripsiya(fayl_path: str) -> str:
    # Whisper audio faylni o'qish uchun ichkarida ffmpeg dasturini chaqiradi.
    # Agar ffmpeg PATH'da bo'lmasa, "WinError 2 / [Errno 2] No such file" kabi
    # tushunarsiz xato chiqadi - shuni oldindan tekshirib, aniq xabar beramiz.
    if not _ffmpegni_topish_va_pathga_qoshish():
        raise RuntimeError(
            "FFMPEG topilmadi. Ovozni matnga aylantirish (STT) ishlashi uchun "
            "ffmpeg o'rnatilgan va PATH'ga qo'shilgan bo'lishi shart.\n"
            "Windows: 'winget install ffmpeg' yoki 'choco install ffmpeg' buyrug'ini "
            "bajarib, KOMPYUTERNI QAYTA ISHGA TUSHIRING, so'ng qayta urinib ko'ring."
        )

    model = _whisper_modelni_olish()
    # Til avtomatik aniqlansa, qisqa audio'larda ko'pincha xato tilga
    # o'xshatib (masalan turkcha/qozoqcha alifbo bilan) yozib beradi.
    # Shuning uchun tilni majburan o'zbekcha qilib beramiz.
    natija = model.transcribe(
        fayl_path,
        language="uz",
        # Juda qisqa/sifatsiz audio'da model oldingi bo'lakka "asoslanib"
        # tasodifiy matn o'ylab topishi (hallucination) kamayadi:
        condition_on_previous_text=False,
    )

    # Whisper ba'zan tovush deyarli yo'q yoki juda qisqa audio'da ham
    # o'zidan tasodifiy so'z "o'ylab topadi" (masalan "GStations").
    # Har bir bo'lakning ishonch darajasini tekshirib, ishonchsizlarini tashlab yuboramiz.
    ishonchli_boleklar = []
    for bolak in natija.get("segments", []):
        agar_ovoz_yoq_ehtimoli = bolak.get("no_speech_prob", 0.0)
        ishonch_darajasi = bolak.get("avg_logprob", 0.0)
        if agar_ovoz_yoq_ehtimoli > 0.6 or ishonch_darajasi < -1.0:
            continue
        ishonchli_boleklar.append(bolak.get("text", "").strip())

    return " ".join(ishonchli_boleklar).strip()


async def ovozni_matnga_aylantir(fayl_path: str) -> str:
    """Audio faylni (ogg/mp3/wav...) whisper orqali matnga aylantiradi.
    Whisper bloklovchi (sync) kutubxona bo'lgani uchun alohida thread'da ishga tushiriladi."""
    return await asyncio.to_thread(_whisper_transkripsiya, fayl_path)