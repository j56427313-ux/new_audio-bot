# (nested) Ichma-ich funksiyalar:

# parol tekshirish
# balans ko'rish
# pul yechish
# pul to'ldirish
#data = [
 #   {'karta': 1234567812345678, 'parol': 1111, 'balans':100000},
#    {'karta': 1234567812345679, 'parol': 1112, 'balans':200000},
#    {'karta': 1234567812345680, 'parol': 1113, 'balans':5000000},
#]

#def bankomat(karta_nomer, karta_parol):
#    def parol_tekshirish():
#        for i in data:
#            if karta_nomer == i['karta'] and karta_parol == i['parol']:
#                return True
#            else:
#                return f"Karta yoki parol xato!"

#def chek_balans():
#    user = parol_tekshirish()
#    return f"Hsobingizda{user['balans']}so'm bor!"

#if operation == 1:
#    print(chek_balans())


#user_karta =1234567812345678
#user_parol = 1111
#print("1 Balansi ko'rish")
#print("2 Pul yechish")
#print("3 Pul to'ldirish")
         
         
         


















# 1.Ichma-ich funksiyadan foydalangan holda, xabar chiqaradigan funksiya yozing. 


# lambda - 1 qatorli funksiya, nomsiz funksiya

# lambda parametr: natija

result = lambda x: x ** 2
print(result(10))

# 2.Lambda funksiyasi yordamida uchburchak yuzasini hisoblash formulasini yozing. 
yuzi = lambda a, h: f'Uchburchakning yuzi: {a * h / 2}'

print(yuzi(10, 5))

juft_toq = lambda son: "JUFT" if son % 2 == 0 else "TOQ"

def juft_toq(son):
     if son % 2 == 0:
         return "JUFT"
     else:
        return "TOQ"
print(juft_toq(77))


# 3.Lambda va filter() yordamida ro‘yxatdagi manfiy sonlarni olib tashlang. 
my_list = [-1, -2, 1, 2, 3, 4, 5, -5, -4, -3]
# result = filter(lambda x: x > 0, my_list)
result = lambda l: [x for x in l if x > 0]
print(result(my_list))

#
# 4.Lambda va map() yordamida harflarni katta harfga o‘tkazadigan funksiya yozing. 
   
mevalar = ['olma', 'anor', 'banan', 'shaftoli']


katta_mevalar = list(map(lambda meva: meva.upper(), mevalar))

print(katta_mevalar)


# 5.Lambda va sorted() yordamida ism uzunligi bo‘yicha ro‘yxatni tartiblang.

ismlar = ['Ali', 'Abdurahmon', 'Hasan', 'Olimjon', 'Vali']

tartiblangan_ismlar = sorted(ismlar, key=lambda ism: len(ism))

print(tartiblangan_ismlar)



ismlar = ['Ali', 'Abdurahmon', 'Hasan', 'Olimjon', 'Vali', 'Nodira']

tartiblangan = sorted(ismlar, key=lambda ism: len(ism), reverse=True)

print(tartiblangan)