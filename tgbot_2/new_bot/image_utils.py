"""
🖼️ RASM PROCESSING (OpenCV, Pillow), 🎭 YUZ FILTRI (mediapipe),
🧼 FON OLIB TASHLASH (rembg), 🔤 OCR (easyocr) uchun yordamchi funksiyalar.

O'RNATISH:
    pip install opencv-python Pillow mediapipe rembg easyocr numpy

ESLATMA: mediapipe, rembg va easyocr birinchi marta ishlatilganda o'z ichki
modellarini internetdan yuklab oladi (bir martalik, keyin keshda saqlanadi).
"""

import cv2
import numpy as np

# ====================== ⚫ OQ-QORA / 🌫 BLUR / ✏️ CARTOON ======================

def oq_qora_qilish(kirish_path: str, chiqish_path: str) -> None:
    rasm = cv2.imread(kirish_path)
    kulrang = cv2.cvtColor(rasm, cv2.COLOR_BGR2GRAY)
    cv2.imwrite(chiqish_path, kulrang)


def blur_qilish(kirish_path: str, chiqish_path: str) -> None:
    rasm = cv2.imread(kirish_path)
    xira = cv2.GaussianBlur(rasm, (25, 25), 0)
    cv2.imwrite(chiqish_path, xira)


def cartoon_effekt(kirish_path: str, chiqish_path: str) -> None:
    """OpenCV asosidagi yengil cartoon/anime uslubidagi effekt
    (chekkalarni ajratib, ranglarni tekislash orqali)."""
    rasm = cv2.imread(kirish_path)

    kulrang = cv2.cvtColor(rasm, cv2.COLOR_BGR2GRAY)
    kulrang = cv2.medianBlur(kulrang, 5)
    chekkalar = cv2.adaptiveThreshold(
        kulrang, 255, cv2.ADAPTIVE_THRESH_MEAN_C, cv2.THRESH_BINARY, blockSize=9, C=9
    )

    rangli = cv2.bilateralFilter(rasm, d=9, sigmaColor=250, sigmaSpace=250)
    cartoon = cv2.bitwise_and(rangli, rangli, mask=chekkalar)
    cv2.imwrite(chiqish_path, cartoon)


# ====================== 🧼 FON OLIB TASHLASH (rembg) ======================

def fon_ochirish(kirish_path: str, chiqish_path: str) -> None:
    try:
        from rembg import remove  # birinchi chaqirilganda yuklanadi (sekin import)
    except SystemExit as e:
        # rembg ichidagi onnxruntime topilmasa, u sys.exit(1) chaqiradi.
        # Buni oddiy xatoga aylantiramiz, aks holda butun bot to'xtab qoladi.
        raise RuntimeError(
            "rembg ishlashi uchun 'onnxruntime' kutubxonasi o'rnatilmagan. "
            "Terminalda: pip install onnxruntime"
        ) from e

    with open(kirish_path, "rb") as f:
        kirish_data = f.read()
    chiqish_data = remove(kirish_data)
    with open(chiqish_path, "wb") as f:
        f.write(chiqish_data)


# ====================== 🎭 YUZ MESH FILTRI (mediapipe) ======================

def yuz_mesh_filtri(kirish_path: str, chiqish_path: str) -> bool:
    """Rasmdagi yuz(lar)ni aniqlab, ustiga mesh (to'r) chizadi.
    Yuz topilmasa False qaytaradi."""
    import mediapipe as mp

    mp_face_mesh = mp.solutions.face_mesh
    mp_drawing = mp.solutions.drawing_utils
    mp_styles = mp.solutions.drawing_styles

    rasm = cv2.imread(kirish_path)
    rgb = cv2.cvtColor(rasm, cv2.COLOR_BGR2RGB)

    with mp_face_mesh.FaceMesh(
        static_image_mode=True, max_num_faces=5, refine_landmarks=True,
        min_detection_confidence=0.5,
    ) as face_mesh:
        natija = face_mesh.process(rgb)
        if not natija.multi_face_landmarks:
            return False

        for yuz_landmarks in natija.multi_face_landmarks:
            mp_drawing.draw_landmarks(
                image=rasm,
                landmark_list=yuz_landmarks,
                connections=mp_face_mesh.FACEMESH_TESSELATION,
                landmark_drawing_spec=None,
                connection_drawing_spec=mp_styles.get_default_face_mesh_tesselation_style(),
            )
            mp_drawing.draw_landmarks(
                image=rasm,
                landmark_list=yuz_landmarks,
                connections=mp_face_mesh.FACEMESH_CONTOURS,
                landmark_drawing_spec=None,
                connection_drawing_spec=mp_styles.get_default_face_mesh_contours_style(),
            )

    cv2.imwrite(chiqish_path, rasm)
    return True


# ====================== 🔤 OCR (easyocr) ======================

_ocr_reader = None


def _ocr_reader_olish():
    global _ocr_reader
    if _ocr_reader is None:
        import easyocr

        # lotin alifbosidagi o'zbekcha matn 'en' model bilan ham yaxshi o'qiladi
        _ocr_reader = easyocr.Reader(["en", "ru"], gpu=False)
    return _ocr_reader


def matnni_ochirish(kirish_path: str) -> str:
    reader = _ocr_reader_olish()
    natijalar = reader.readtext(kirish_path, detail=0)
    return "\n".join(natijalar)