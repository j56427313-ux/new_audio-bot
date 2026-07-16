# fikrlashni talab qiladi va r, w, a rejimlarini yaxshi tushunganini tekshiradi.
# 1-mashq
# students.txt fayl yarating va ichiga 5 ta o‘quvchi ismini yozing.
# Keyin faylni qayta ochib ekranga chiqaring.
# Talab:
# w
# r
# open()

# 2-mashq
# data.txt fayliga quyidagi matn yozilgan:
# Python
# Java
# C++
# Go
# Dastur:
# faylni o‘qisin
# nechta qator borligini aniqlasin
# natijani chiqarsin
# Masalan:
# Qatorlar soni: 4

# 3-mashq
# users.txt fayliga ism yozing.
# Har safar dastur ishlaganda yangi ism eski yozuvni o‘chirmasdan qo‘shilsin.
# Masalan:
# Ali
# Vali
# Humoyun
# Talab:
# a rejimi ishlatilishi kerak

# 4-mashq
# numbers.txt fayliga 1 dan 100 gacha sonlarni yozing.
# Natija:
# 1
# 2
# 3
# 4
# ...
# 100
# Talab:
# w
# for
# \n

# 5-mashq (Qiyin)
# secret.txt faylida quyidagi matn bor:
# Python juda kuchli dasturlash tili
# Dastur:
# faylni o‘qisin
# nechta harf borligini aniqlasin
# nechta so‘z borligini aniqlasin
# Natija misoli:
# So'zlar soni: 5
# Harflar soni: 33
# Talab:
# read()
# split()
# len()








# 1-mashq: students.txt faylini yaratish va o‘quvchi isimlarini yozish
students = ["Ali", "Vali", "Gulnora", "Rashid", "Diyor"]
with open("students.txt", "w", encoding="utf-8") as f:
    for student in students:
        f.write(student + "\n")

print("1-mashq: students.txt ichidagi matn:")
with open("students.txt", "r", encoding="utf-8") as f:
    print(f.read().strip())

print("\n---\n")

# 2-mashq: data.txt faylini o‘qish va qatorlar sonini hisoblash
sample_data = ["Python", "Java", "C++", "Go"]
with open("data.txt", "w", encoding="utf-8") as f:
    for item in sample_data:
        f.write(item + "\n")

with open("data.txt", "r", encoding="utf-8") as f:
    lines = f.readlines()
print("2-mashq: Qatorlar soni:", len(lines))
print("data.txt ichidagi qatorlar:")
for line in lines:
    print(line.strip())

print("\n---\n")

# 3-mashq: users.txt fayliga ism qo‘shish (append rejimida)
name_to_add = input("3-mashq: Istalgan ism kiriting: ").strip()
if name_to_add:
    with open("users.txt", "a", encoding="utf-8") as f:
        f.write(name_to_add + "\n")

print("users.txt ichidagi hozirgi ism:")
with open("users.txt", "r", encoding="utf-8") as f:
    print(f.read().strip())

print("\n---\n")

# 4-mashq: numbers.txt fayliga 1 dan 100 gacha sonlarni yozish
with open("numbers.txt", "w", encoding="utf-8") as f:
    for number in range(1, 101):
        f.write(str(number) + "\n")
print("4-mashq: numbers.txt fayliga 1 dan 100 gacha sonlar yozildi.")

print("\n---\n")

# 5-mashq: secret.txt faylini o‘qish va harflar hamda so‘zlar sonini hisoblash
secret_text = "Python juda kuchli dasturlash tili"
try:
    with open("secret.txt", "r", encoding="utf-8") as f:
        text = f.read().strip()
except FileNotFoundError:
    with open("secret.txt", "w", encoding="utf-8") as f:
        f.write(secret_text)
    text = secret_text

words = text.split()
letters = sum(1 for ch in text if ch.isalpha())
print("5-mashq: secret.txt ichidagi matn:")
print(text)
print("So'zlar soni:", len(words))
print("Harflar soni:", letters)
