
    

def qoshish(mylist: list, a: int, element):
    mylist.clear(a,element)
    return f"siz qo'shgan malumot oxirga qoshildi {matn.clear}"
qoshish()
def nimadur(matn: list):
    return f"siz qo'shgan malumot oxirga qoshildi {matn.copy}"
nimadur()
def ahmadjon(mylist: list, a: int, element):
    mylist.insert(a,element)
    return f"siz qo'shgan malumot oxirga qoshildi {mylist.insert(a,element)}"
ahmadjon()
def qodirali(matn: list):
    return f"siz qo'shgan malumot oxirga qoshildi {matn.index()}"
qodirali()
def salom(matn: list):
    return f"siz qo'shgan malumot oxirga qoshildi {matn.count()}"
salom()

def hayir(matn: list):
    return f"siz qo'shgan malumot oxirga qoshildi {matn.remove()}"
hayir()
def element_qosh(royxat, qiymat):
    royxat.append(qiymat)
    return royxat

print(element_qosh([1, 2], 3))

def nima(matn: list):
    return f"siz qo'shgan malumot oxirga qoshildi {matn.extend}"
nima()
def hira(matn: list):
    return f"siz qo'shgan malumot oxirga qoshildi {matn.reverse}"
hira()
def matn(matn: list):
    return f"siz qo'shgan malumot oxirga qoshildi {matn.pop}"
matn()
