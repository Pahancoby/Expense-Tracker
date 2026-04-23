import tkinter as tk
from tkinter import ttk, messagebox
import json
from datetime import datetime
import os

FILE = "expenses.json"

class App:
    def __init__(self, root):
        self.root = root
        self.root.title("Expense Tracker")
        self.data = []

        frame = tk.Frame(root)
        frame.pack(pady=10)

        tk.Label(frame, text="Сумма").grid(row=0, column=0)
        tk.Label(frame, text="Категория").grid(row=1, column=0)
        tk.Label(frame, text="Дата (YYYY-MM-DD)").grid(row=2, column=0)

        self.amount = tk.Entry(frame)
        self.category = tk.Entry(frame)
        self.date = tk.Entry(frame)

        self.amount.grid(row=0, column=1)
        self.category.grid(row=1, column=1)
        self.date.grid(row=2, column=1)

        tk.Button(frame, text="Добавить расход", command=self.add).grid(row=3, columnspan=2)

        self.tree = ttk.Treeview(root, columns=("Amount","Category","Date"), show="headings")
        for col in ("Amount","Category","Date"):
            self.tree.heading(col, text=col)
        self.tree.pack()

        tk.Button(root, text="Сохранить", command=self.save).pack()
        tk.Button(root, text="Загрузить", command=self.load).pack()

        self.load()

    def add(self):
        try:
            amount = float(self.amount.get())
            if amount <= 0:
                raise ValueError
        except:
            messagebox.showerror("Ошибка","Сумма должна быть положительной")
            return

        try:
            datetime.strptime(self.date.get(), "%Y-%m-%d")
        except:
            messagebox.showerror("Ошибка","Дата в формате YYYY-MM-DD")
            return

        item = {"amount":amount,"category":self.category.get(),"date":self.date.get()}
        self.data.append(item)
        self.update()

    def update(self):
        self.tree.delete(*self.tree.get_children())
        for i in self.data:
            self.tree.insert("",tk.END,values=(i["amount"],i["category"],i["date"]))

    def save(self):
        with open(FILE,"w",encoding="utf-8") as f:
            json.dump(self.data,f,indent=4,ensure_ascii=False)

    def load(self):
        if os.path.exists(FILE):
            with open(FILE,"r",encoding="utf-8") as f:
                self.data=json.load(f)
                self.update()

root=tk.Tk()
app=App(root)
root.mainloop()