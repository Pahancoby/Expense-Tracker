import tkinter as tk
from tkinter import ttk, messagebox
import json
import os

DATA_FILE = "movies.json"

class MovieLibrary:
    def __init__(self, root):
        self.root = root
        self.root.title("Movie Library")
        self.movies = []

        frame = tk.Frame(root)
        frame.pack(pady=10)

        tk.Label(frame, text="Название").grid(row=0, column=0)
        tk.Label(frame, text="Жанр").grid(row=1, column=0)
        tk.Label(frame, text="Год").grid(row=2, column=0)
        tk.Label(frame, text="Рейтинг").grid(row=3, column=0)

        self.title_entry = tk.Entry(frame)
        self.genre_entry = tk.Entry(frame)
        self.year_entry = tk.Entry(frame)
        self.rating_entry = tk.Entry(frame)

        self.title_entry.grid(row=0, column=1)
        self.genre_entry.grid(row=1, column=1)
        self.year_entry.grid(row=2, column=1)
        self.rating_entry.grid(row=3, column=1)

        tk.Button(frame, text="Добавить фильм", command=self.add_movie).grid(row=4, columnspan=2, pady=5)

        self.tree = ttk.Treeview(root, columns=("Title","Genre","Year","Rating"), show="headings")
        for col in ("Title","Genre","Year","Rating"):
            self.tree.heading(col, text=col)
        self.tree.pack(pady=10)

        self.load_data()

    def add_movie(self):
        title = self.title_entry.get()
        genre = self.genre_entry.get()
        year = self.year_entry.get()
        rating = self.rating_entry.get()

        if not year.isdigit():
            messagebox.showerror("Ошибка", "Год должен быть числом")
            return

        try:
            rating = float(rating)
            if not (0 <= rating <= 10):
                raise ValueError
        except:
            messagebox.showerror("Ошибка", "Рейтинг должен быть от 0 до 10")
            return

        movie = {"title": title, "genre": genre, "year": int(year), "rating": rating}
        self.movies.append(movie)
        self.update_table()

    def update_table(self):
        self.tree.delete(*self.tree.get_children())
        for m in self.movies:
            self.tree.insert("", tk.END, values=(m["title"], m["genre"], m["year"], m["rating"]))

    def save_data(self):
        with open(DATA_FILE, "w", encoding="utf-8") as f:
            json.dump(self.movies, f, ensure_ascii=False, indent=4)

    def load_data(self):
        if os.path.exists(DATA_FILE):
            with open(DATA_FILE, "r", encoding="utf-8") as f:
                self.movies = json.load(f)
                self.update_table()

if __name__ == "__main__":
    root = tk.Tk()
    app = MovieLibrary(root)
    root.mainloop()
