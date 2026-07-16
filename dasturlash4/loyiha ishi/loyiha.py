# List metodlari
#listga berilgan indexga yangi index qoshadi
#Mavjud xususiyatlarni qayta yozmasdan, ularni o'zlashtirish va ustiga yangilarini qo'shish.

# List metodlari
# append - list oxiriga yangi element qo'shadi
# insert -listga berilgan indexga yangi index qoshadi 
# extend - Mavjud xususiyatlarni qayta yozmasdan, ularni o'zlashtirish va ustiga yangilarini qo'shish.
# remove -Ro'yxatdan ko'rsatilgan qiymatni o'chiradi. 
# pop - Ro'yxatdan ko'rsatilgan qiymatni o'chiradi.
# clear - indexdagi barcha narsani ochiradi
# max - Ro'yxatdagi eng katta qiymatni topadi.
# min - Ro'yxatdagi eng kichik qiymatni topadi.
# len - Ro'yxatning uzunligini (elementlar sonini) aniqlaydi.
# copy - Ro'yxatdan nusxa oladi.
# sort - Elementlarni tartiblaydi (o'sish tartibida).
# reverse - Ro'yxatni teskarisiga ag'daradi.
# index - Elementning tartib raqamini (indeksini) topadi.
# count - Element ro'yxatda necha marta qatnashganini hisoblaydi.

#sonlar = [10, 80, 30, 25, 77, 10]
#print(sonlar)

# qo'shish uchun: append(), insert, extend()
#sonlar.append(100) 
#print(sonlar)

#sonlar.insert(3, 99)
#print(sonlar)

#ismlar = ["Ulug'bek", "Zafar"]
#ismlar.extend(sonlar) # type:ignore
#print(ismlar)


# o'chirish uchun: remove(), pop(), clear()
#ismlar.remove("Zafar")
#print(ismlar)

#ismlar.pop(-1)
#print(ismlar)

#ismlar.clear()
#print(ismlar)


# sort(), reverse(), copy(), count(), index()
#sonlar.

# 1.  listiga "uzum" ni bilan va "anor" ni 1-indexga bilan qo‘shib natijani chiqaring.
mevalar = ["olma", "shoptoli"]
mevalar.append("uzum") 
mevalar.insert(1, "anor")  
print(mevalar) 
# 2. listlarini birlashtirib natijani hammasini yig'indisini chiqaring.
a = [10, 20, 30]
b = [40, 50]
c = a + b           
natija = sum(c)      
print(natija) 
# 3. listidan 15 ni va oxirgi elementni o‘chirib natijani chiqaring.
sonlar = [5, 10, 15, 20, 25] 
sonlar.remove(15)     
sonlar.pop()           
print(sonlar) 
# 4. listini tartiblab, so‘ng teskari tartibda natijani chiqaring.
raqamlar = [12, 4, 9, 1, 7]
raqamlar.sort()       
raqamlar.reverse()    
print(raqamlar)
# 5. listida 2 lar sonini, birinchi 2 indeksini va uzunligini aniqlang.
nums = [2, 4, 2, 6, 2, 8]
sanoq = nums.count(2)    #
indeks = nums.index(2) 
uzunlik = len(nums)    

print(sanoq)
print(indeks)
print(uzunlik)