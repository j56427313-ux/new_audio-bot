# try:
#     prin(sonlar[1])
# except Exception as xatolik:
#     print(f"Shunaqa xatolik bo'ladi: {xatolik}")


# TypeError
# IndexError
# ZeroDivisionError
# ValueError
# KeyError
# SyntaxError
# IndentationError
# NameError


# fayl = open(fayl_manzili, rejim)
# fayl....

# fayl = open('modul4/dars11/nimadir.txt', 'a')
# fayl.write("Nimadir ma'lumot\n") 


students = [
    {'ism': "Muhammadrizo", "familiya": "Ilhomov", "coin": 5000},
    {'ism': "Shaxzod", "familiya": "Jalilov", "coin": 3000},
    {'ism': "Ahmadjon", "familiya": "Sultonov", "coin": 2000},
]


# for student in students:
#     with open('modul4/dars11/students_info.txt', 'a') as file:
#         file.write(f"{students.index(student)+1}. O'quvchining ismi: {student['ism']}, Familiyasi: {student['familiya']}, Coin: {student['coin']};\n")
        
ind = 0  
try:  
    while len(students) > 0:
        with open('modul4/dars11/students_info.txt', 'a') as file:
            file.write(f"{ind+1}. O'quvchining ismi: {students[ind]['ism']}, Familiyasi: {students[ind]['familiya']}, Coin: {students[ind]['coin']};\n")
        students.remove(students[ind])
        ind += 1
except Exception as xato:
    print(f"Qandaydir xatolik: {xato}")