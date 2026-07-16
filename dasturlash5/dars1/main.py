# 1.Book nomli sinf yaratib, unga muallif, 
# nom va narx atributlarini berish. 
class Book:  # class yaratilishi
    def __init__(self, nom, muallif, narx, sharx) -> None:  # konstruktor
        self.nom = nom  # atributlar -> xususiyat
        self.muallif = muallif
        self.narx = narx
        self.sharx = sharx
        
    def info(self):  # classning metodi
        return f'Kitobning nomi: {self.nom}\n © Muallif: {self.muallif}\n💰 Narx: {self.narx} !'
        
    def skidka_narx(self, foiz):
        return f"Yangi narx: {self.narx - self.narx // 100 * foiz}"
  
# obyekt yaratilishi:
b1 = Book("Tom Soyerning sarguzashtlari", "Mark Tven", 66000, "Asaxiy Books loyihasida jahon adabiyoti durdonasi - “Tom Soyerning sarguzashtlari” kitobi premyerasi!")


# print(b1.info()) # metodni chaqirish
print(b1.skidka_narx(50))

print(b1.narx)  # atributni chaqirish





# 2.Person nomli sinf yaratib, ism va yosh 
# xususiyatlarini aniqlash. 
class Person:
    def __init__(self, ism, familya, yosh):
        self.ism     = ism
        self.familya = familya
        self.yosh    = yosh

    def tanishuv(self):
        print(f"Salom! Mening ismim {self.ism},"
              f"Familyam {self.familya}, Yoshim {self.yosh}.")


p1 = Person("Javlonbek", "Abdujalolov", 13)
p2 = Person("Jahongirbek", "Abdujalolov", 16)

print(p1.ism)          
print(p1.yosh)         
p1.tanishuv()
p2.tanishuv()

# 3.Rectangle nomli sinf yaratib, uzunlik va 
# kenglik asosida maydonni hisoblash metodini yozish.
class Rectangle:
    def __init__(self, uzunlik, kenglik):
        self.uzunlik = uzunlik
        self.kenglik = kenglik

    def maydon(self):
        return self.uzunlik * self.kenglik

    def perimetr(self):
        return 2 * (self.uzunlik + self.kenglik)


r1 = Rectangle(3, 7)
r2 = Rectangle(8, 11)

print(f"Maydon: {r1.maydon()}")    
print(f"Perimetr: {r1.perimetr()}")  
print(f"Maydon: {r2.maydon()}")    
print(f"Perimetr: {r2.perimetr()}")  
