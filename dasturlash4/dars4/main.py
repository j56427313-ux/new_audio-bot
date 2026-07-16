 While loop + break va continue operatorlari
 loop - tsikl (takrorlash operatori)
 for loop & while loop

 for loop - qachonki sikl nechi marta ishlashi oldindan ma'lum bo'lsa

 while loop - oldindan nechi marta ishlashi noma'lum bo'lsa

import random

son = random.randint(1, 10)

while True: # cheksiz sikl
    user_son = int(input("Son toping: "))
    if user_son == son:
        print("TABRIKLAYMAN SON TOPILDI!!!")
#       break
    print("Topolmadingiz yana urinib ko'ring!")
    


    user_son = int(input("Nechigacha hisoblash kerak: "))
    summa = 0
    i = 1       
    while i <= user_son:
    summa += i
    i += 1
    
#print("Yig'indi:", summa)


 while shart: agar shart True bo'lsa while loop ishlaydi
     kod blok








# 1.1 dan 100 gacha bo‘lgan sonlarni chiqarish, lekin 50 ga yetganda siklni to‘xtatish (break). 
i = 1

# 2.Foydalanuvchidan faqat musbat sonlar kiritishini so‘rab, agar u manfiy son kiritsa, siklni to‘xtatish (break). 

# 3.1 dan 20 gacha bo‘lgan toq sonlarni chiqarish (continue). 

# 4.Foydalanuvchidan har safar son so‘rab, faqat juft sonlarni chiqarish (continue). 

# 5.Tasodifiy sonlar kiritib borish, agar foydalanuvchi "stop" yozsa, siklni to‘xtatish (break).#