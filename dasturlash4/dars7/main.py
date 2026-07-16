# Funstions: *args , **kwargs
# *args - argumentlar, funksiyaga istalgancha parametr berishni bildiradi
# tuple ko'rinishida beriladi

#def summa(*sonlar): # sonlar: tuple
 #   result = 0
 #   for i in sonlar:
 #       result += i
#   return f"Sonlar yig'indisi: {result}"

#print(summa(10, 20, 15, 25, 35))
#print(sum([10, 20, 15, 25, 35]))


# **kwargs - keyword-argumentlar, funksiyaga istalgancha parametr berishni bildiradi
# dict ko'rinishida beriladi

#def get_info(**data): # info: dict
#    result = "Foydalanuvchi ma'lumotlari:\n"
#    for k,v in data.items():
#        result += f"{k} - {v};\n"
#    return result

#print(get_info(ism="Axmadjon", yosh=16, coin=1500, xotini="Mubina"))


# 1.Berilgan sonlarning ko‘paytmasini hisoblaydigan *args funksiyasini yozing. 
def kopaytma(*sonlar):
    result = 1
    for son in sonlar:
        result *= son
    return result

print(kopaytma(2, 4, 5))
# 2.Foydalanuvchi haqidagi ma’lumotlarni (ism, yosh, kasb) qabul qiladigan **kwargs funksiyasini yozing. 
def get_info(**data): # info: dict
    result = "Foydalanuvchi ma'lumotlari:\n"
    for k,v in data.items():
        result += f"{k} - {v};\n"
    return result
# 3.Matnlarni *args orqali qabul qilib, ularning uzunligini hisoblovchi funksiya yozing. 
def matn_uzunligi(*args):
    for matn in args:
        print(f"'{matn}' uzunligi: {len(matn)}")

matn_uzunligi("Salom", "Python", "Dasturlash")  

# 4.*args orqali istalgan sonlarni qabul qilib, faqat musbatlarini ajratib oluvchi funksiya yozing. 

# 5.*args va **kwargs ni birgalikda ishlatib, foydalanuvchi haqida to‘liq ma’lumot qaytaruvchi

