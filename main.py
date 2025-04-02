import tkinter as tk
from tkinter import messagebox, ttk
import json


class App(tk.Frame):
    def __init__(self, master, data):
        super().__init__(master)
        self.pack(padx=10, pady=10)
        print(data)
        self.todos = data if isinstance(data, list) else []
        print(self.todos)

        # 入力フレーム
        input_frame = tk.Frame(self)
        input_frame.pack(fill="x", pady=5)

        # 日付入力
        self.date_label = tk.Label(input_frame, text="日付:")
        self.date_label.grid(row=0, column=0, sticky="w", pady=2)
        self.date_entry = tk.Entry(input_frame, width=30)
        self.date_entry.grid(row=0, column=1, pady=2)

        # タイトル入力
        self.title_label = tk.Label(input_frame, text="タイトル:")
        self.title_label.grid(row=1, column=0, sticky="w", pady=2)
        self.title_entry = tk.Entry(input_frame, width=30)
        self.title_entry.grid(row=1, column=1, pady=2)

        # 本文入力
        self.body_label = tk.Label(input_frame, text="本文:")
        self.body_label.grid(row=2, column=0, sticky="w", pady=2)
        self.body_entry = tk.Entry(input_frame, width=30)
        self.body_entry.grid(row=2, column=1, pady=2)

        # ボタンフレーム
        button_frame = tk.Frame(self)
        button_frame.pack(pady=5)

        # 追加ボタン
        self.add_button = tk.Button(button_frame, text="追加", command=self.add_todo)
        self.add_button.pack(side="left", padx=5)

        # 削除ボタン
        self.delete_button = tk.Button(
            button_frame, text="削除", command=self.delete_todo
        )
        self.delete_button.pack(side="left", padx=5)

        # TODOリスト
        list_frame = tk.Frame(self)
        list_frame.pack(fill="both", expand=True, pady=5)

        self.tree = ttk.Treeview(
            list_frame, columns=("日付", "タイトル", "本文"), show="headings"
        )
        self.tree.heading("日付", text="日付")
        self.tree.heading("タイトル", text="タイトル")
        self.tree.heading("本文", text="本文")
        self.tree.column("日付", width=100)
        self.tree.column("タイトル", width=150)
        self.tree.column("本文", width=250)
        self.tree.pack(fill="both", expand=True)

        # Treeviewを初期化
        self.populate_treeview()

    def populate_treeview(self):
        # Treeviewをクリア
        for item in self.tree.get_children():
            self.tree.delete(item)
        # self.todosからTreeviewにデータを挿入
        for todo in self.todos:
            self.tree.insert("", "end", values=(todo["date"], todo["title"], todo["text"]))

    def add_todo(self):
        date = self.date_entry.get()
        title = self.title_entry.get()
        body = self.body_entry.get()

        if date and title:
            self.tree.insert("", "end", values=(date, title, body))
            self.todos.append({"date": date, "title": title, "text": body})
            self.clear_entries()
        else:
            messagebox.showerror("エラー", "日付とタイトルは必須です")
        print(self.todos)
        self.save_data()

    def delete_todo(self):
        selected_item = self.tree.selection()
        if selected_item:
            # 選択されたアイテムのインデックスを取得
            index = self.tree.index(selected_item)
            # self.todos からも削除
            del self.todos[index]
            # Treeview からアイテムを削除
            self.tree.delete(selected_item)
        else:
            messagebox.showinfo("情報", "削除するアイテムを選択してください")
        print(self.todos)
        self.save_data()

    def save_data(self):
        with open("./data", "w", encoding="utf-8") as f:
            json.dump(self.todos, f, ensure_ascii=False, indent=2)

    def clear_entries(self):
        self.date_entry.delete(0, tk.END)
        self.title_entry.delete(0, tk.END)
        self.body_entry.delete(0, tk.END)


try:
    with open("./data", "r", encoding="utf-8") as f:
        data = f.read()
        if data == "":
            data = []
            print("reset")
        else:
            data = json.loads(data)  # JSONデータをリストに変換
except (FileNotFoundError, json.JSONDecodeError):
    data = []
    print("reset")

root = tk.Tk()
root.title("TODOアプリ")
root.geometry("500x400")
myapp = App(root, data)
myapp.mainloop()
