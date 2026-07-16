# try:

#     son = int(input("Son kiriting: "))
#     print(10 / son)

# # except: xatolik yuz berganda nima qilish kerakligi yoziladi
# except:
#     print("Xatolik yuz berdi!")


# # 2. try exceptni tekshirish uchun commentni oching
# try:
#     son = int(input("Son kiriting: "))
#     print(10 / son)

# except:
#     print("Xatolik yuz berdi!")


# # 3. finally ni ishlatish

# try:
#     son = int(input("Son: "))
#     print(10 / son)

# except:
#     print("Xato!")

# # finally esa har qanday holatda ishga tushadi,
# # xatolik bo‘lsa ham, bo‘lmasa ham.

# finally:
#     print("Dastur tugadi")




# finally:
#     print("Dastur tugadi")







# 1-mashq — Parol tekshirish

# Foydalanuvchi parol kiritsin.

# Agar:

# parol uzunligi 5 tadan kichik bo‘lsa → xato chiqsin
# bo‘sh bo‘lsa → xato chiqsin
# 2-mashq — Yosh tekshirish

# Foydalanuvchi yosh kiritsin.

# Agar:

# son bo‘lmasa → xato
# yosh manfiy bo‘lsa → xato
# aks holda → “Kirish mumkin”
# 3-mashq — Index xatosi

# List ichidan index orqali element chiqarish.

# Agar mavjud bo‘lmagan index kiritsa:
# IndexError ushlansin.

# Misol:

# mevalar = ["olma", "anor", "uzum"]
# O‘rta darajadagi mashqlar
# 4-mashq — Mini kalkulyator

# Foydalanuvchi:

# 2 ta son
# amal (+ - * /)

# kiritsin.

# Xatolar:

# harf kiritsa
# 0 ga bo‘lsa
# noto‘g‘ri amal kiritsa
# 5-mashq — Bank kartasi

# Kartadagi pul: 100000

# Foydalanuvchi qancha yechmoqchi ekanini kiritsin.

# Agar:

# balans yetmasa → xato
# manfiy son kiritsa → xato
# harf kiritsa → xato
# 6-mashq — Login tizimi

# To‘g‘ri login: admin

# To‘g‘ri parol: 12345

# Agar noto‘g‘ri kiritsa:
# xato chiqarilsin.

# 3 marta noto‘g‘ri kiritsa:
# “Akkaunt bloklandi”

# Qiyinroq mashqlar
# 7-mashq — Fayl ochish

# Foydalanuvchi fayl nomini kiritsin.

# Agar fayl topilmasa:
# FileNotFoundError

# 8-mashq — Baholar o‘rtachasi

# Foydalanuvchi baholar kiritsin.

# Agar:

# harf yozsa
# noto‘g‘ri format yozsa

# xato ushlansin.

# 9-mashq — Telefon raqam tekshirish

# Telefon raqam:

# faqat son bo‘lishi kerak
# 9 yoki 12 ta raqam bo‘lishi kerak

# Aks holda xato chiqsin.

# Juda qiziqarli challenge
# 10-mashq — PIN kod

# PIN kod: 2026

# Foydalanuvchi PIN kiritsin.

# Agar:

# noto‘g‘ri bo‘lsa → xato
# 3 marta noto‘g‘ri kiritsa → karta bloklansin
# to‘g‘ri kiritsa → “Xush kelibsiz”


# 1-mashq

try:
    parol = input("Parol kiriting: ")

    if len(parol) < 5:
        raise ValueError("Parol 5 tadan kichik bo‘lishi mumkin emas!")

    if parol == "":
        raise ValueError("Parol bo‘sh bo‘lishi mumkin emas!")

    print("Parol qabul qilindi!")
except ValueError as e:
    print(f"Xato: {e}")

print("\n---\n")

# 2-mashq