import tkinter as tk
from tkinter import messagebox, ttk

class OquvMarkazApp:
    def __init__(self, root):
        self.root = root
        self.root.title("O'quv Markazi - Boshqaruv Paneli")
        self.root.geometry("700x750")
        self.root.configure(bg="#f0fdf4")  # Juda och yashil fon

        # Ranglar palitrasi
        self.color_primary = "#2e7d32"  # To'q sabsirang
        self.color_bg = "#ffffff"       # Oq
        self.color_accent = "#c8e6c9"   # Och sabsirang
        self.color_red = "#ef5350"      # Qizil (yo'qlar uchun)
        self.color_green = "#66bb6a"    # Yashil (borlar uchun)

        # O'quvchilar ro'yxati (15 ta)
        self.students = [
            {"id": i, "name": f"O'quvchi {i+1}", "coins": 0, "status": None}
            for i in range(15)
        ]

        self.setup_ui()

    def setup_ui(self):
        # Sarlavha
        header = tk.Frame(self.root, bg=self.color_primary, pady=15)
        header.pack(fill="x")
        
        lbl_title = tk.Label(header, text="O'QUV MARKAZI DAVOMAT VA COIN TIZIMI", 
                             fg="white", bg=self.color_primary, 
                             font=("Segoe UI", 16, "bold"))
        lbl_title.pack()

        # Asosiy konteyner (Scrollbar bilan)
        main_frame = tk.Frame(self.root, bg="#f0fdf4")
        main_frame.pack(fill="both", expand=True, padx=20, pady=10)

        # Sarlavhalar paneli
        cols_frame = tk.Frame(main_frame, bg="#f0fdf4")
        cols_frame.pack(fill="x", pady=5)
        
        tk.Label(cols_frame, text="Ism sharifi", width=20, anchor="w", bg="#f0fdf4", font=("Arial", 10, "bold")).pack(side="left")
        tk.Label(cols_frame, text="Davomat", width=15, bg="#f0fdf4", font=("Arial", 10, "bold")).pack(side="left")
        tk.Label(cols_frame, text="Coin qo'shish", width=15, bg="#f0fdf4", font=("Arial", 10, "bold")).pack(side="left")
        tk.Label(cols_frame, text="Jami Coin", width=10, bg="#f0fdf4", font=("Arial", 10, "bold")).pack(side="left")

        # O'quvchilar qatorlari
        for student in self.students:
            self.create_student_row(main_frame, student)

    def create_student_row(self, parent, student):
        row = tk.Frame(parent, bg=self.color_bg, pady=5, padx=10, 
                       highlightbackground=self.color_accent, highlightthickness=1)
        row.pack(fill="x", pady=2)

        # Ism
        lbl_name = tk.Label(row, text=student["name"], width=20, anchor="w", 
                            bg=self.color_bg, font=("Arial", 10))
        lbl_name.pack(side="left")

        # Davomat tugmalari (Bor/Yo'q)
        btn_attendance = tk.Button(row, text="Kelmadi", width=10, 
                                   bg="#eeeeee", relief="flat",
                                   command=lambda s=student, b=None: self.toggle_attendance(s, b))
        # Bizga tugmaning o'zi kerak bo'lgani uchun uni konfiguratsiya qilamiz
        btn_attendance.config(command=lambda s=student, b=btn_attendance: self.toggle_attendance(s, b))
        btn_attendance.pack(side="left", padx=10)

        # Coin kiritish joyi
        coin_entry = tk.Entry(row, width=8, justify="center")
        coin_entry.pack(side="left", padx=5)
        coin_entry.insert(0, "0")

        # Coin qo'shish tugmasi
        btn_add = tk.Button(row, text="+", bg=self.color_accent, width=3, 
                            relief="flat", cursor="hand2",
                            command=lambda s=student, e=coin_entry: self.add_coins(s, e))
        btn_add.pack(side="left")

        # Jami Coin ko'rsatkichi
        student["coin_label"] = tk.Label(row, text="0", width=8, 
                                         fg=self.color_primary, bg=self.color_bg, 
                                         font=("Arial", 10, "bold"))
        student["coin_label"].pack(side="left", padx=10)

    def toggle_attendance(self, student, button):
        if student["status"] != "bor":
            student["status"] = "bor"
            button.config(text="BOR", bg=self.color_green, fg="white")
        else:
            student["status"] = "yoq"
            button.config(text="YO'Q", bg=self.color_red, fg="white")

    def add_coins(self, student, entry):
        try:
            val = int(entry.get())
            if val < 0: raise ValueError
            
            student["coins"] += val
            student["coin_label"].config(text=str(student["coins"]))
            entry.delete(0, tk.END)
            entry.insert(0, "0")
        except ValueError:
            messagebox.showerror("Xato", "Iltimos, coin uchun musbat son kiriting!")

if __name__ == "__main__":
    root = tk.Tk()
    app = OquvMarkazApp(root)
    root.mainloop()