# 1.Dictionary yaratish va unga 5 ta element qo‘shish. 
student = {
    'ism': "Javlonbek",
    'familya': "Abdujalolov",
    'yosh': 20,
    'kurs': "Informatika",
    'Oquv markazi': "mars IT"}
print(student)

# 2.Foydalanuvchidan kalit kiritishini so‘rab, tepadagi dictdan
# shu kalitga tegishli qiymatni ekranga chiqarish (get()). 
kalit = input("Kalitni kiriting: ")
print(f"siz soragan qiymat: {student.get(kalit)}")


# 3.Dictionary dan Foydalanuvchidan kalit kiritishini so‘rab elementni o‘chirish (pop()).
print(student.pop('yosh'))
print(student)
# 4.Dictionary ning barcha kalit va qiymatlarini alohida chiqarish (keys(), values()). 

# 5.Dictionary ustida for sikli yordamida barcha elementlarni ekranga chiqarish.