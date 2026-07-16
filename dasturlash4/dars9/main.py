# 9. Standart modullar (math, random, datetime, os, sys)

# modul -> python fayl, ma'lum bir funksiyalardan iborat kutubxona

import math

# math.sqrt() -> sonning kv ildizini topadi

print(math.sqrt(9))

# 5! = 1*2*3*4*5 = 120
print(math.factorial(10))

print(math.ceil(9.1)) # tepaga
print(math.floor(9.9)) # pastga
print(round(9.5))

# print(math.pow(son, daraja))
print(math.pow(25, 0.5))


import random

print(random.randint(1, 10))

ismlar = ["Umar", "Jovlon", "Abdulbosit", "Mubina", "Madina", "Saida"]
print(random.choice(ismlar))
print(random.choices(ismlar, k=2))
random.shuffle(ismlar)
print(ismlar)


import datetime

print(datetime.datetime.now())
# ichida 5 ta funksiyani o'rganish
# soatni qayerdan oladi shuni topish



import calendar

# print(calendar.calendar(2026)) # ...

print(calendar.month(2009, 11))  # ...