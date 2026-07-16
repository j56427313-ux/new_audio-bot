# OOP - Obyektga yo'naltirilgan dasturlash

# class - shablon, obyektlar uchun umumiy template
# obyekt - shablon (class) dan olingan namuna

# vorislik - ota classdan ba'zi yoki barcha metod va 
            # xususiyatlarini me'ros qilib oladi
            
# User -> ism, familiya, login, parol, nomer

# Student, Teacher, Adminstrator, Manager

class User:
    def __init__(self, ism, familiya, login, parol, nomer) -> None:
        self.ism = ism  # atributlar -> xususiyatlar
        self.familiya = familiya
        self.__login = login
        self.__parol = parol
        self.nomer = nomer
        
    def info(self):  # metod
        return f"Ism: {self.ism}\nFamiliya: {self.familiya}\nNomer: {self.nomer}"

    def get_login(self):
        return f"LOGIN: {self.__login}"


class Student(User):  # inheritance - vorislik
    def __init__(self, ism, familiya, login, parol, nomer, coin, balans, reyting, guruh) -> None:
        super().__init__(ism, familiya, login, parol, nomer)
        self.coin = coin
        self.balans = balans
        self.reyting = reyting
        self.guruh = guruh
        
        
    def info(self):  # metod
        return f"Ism: {self.ism}\nFamiliya: {self.familiya}\n" \
               f"Coin: {self.coin}\nReyting: {self.reyting}\nGuruh: {self.guruh}"
               
# Polimorfizm - ota classning metodini nomini o'zgartirmasdan, 
             #  ishlashini o'zgartirishga aytiladi.

s1 = Student("Muhammadrizo", "Javohirov", 'javlon', 1234, 123456789, 123456, 1234567, 1, 123)
print(s1.info())
print(s1.get_login())
print(s1.__login)

class Teacher(User):  # inheritance - vorislik
    def __init__(self, ism, familiya, login, parol, nomer, fan, oylik) -> None:
        super().__init__(ism, familiya, login, parol, nomer)
        self.fan = fan
        self.oylik = oylik
        
    def info(self):  # metod
        return f"Ism: {self.ism}\nFamiliya: {self.familiya}\n" \
               f"Fan: {self.fan}\nOylik: {self.oylik}"
               
# Abstraksiya - metodni ichki ishlashini yashirish
# Inkapsulyatsiya - tashqi chaqirishdan himoyalash