import tkinter as tk
from tkinter import messagebox, simpledialog
import json
import random
import os

FILENAME = 'tasks.json'
DEFAULT_TASKS = [
    {"text": "Прочитать статью", "type": "учёба"},
    {"text": "Сделать зарядку", "type": "спорт"},
    {"text": "Написать отчёт", "type": "работа"},
]

def load_tasks():
    if os.path.exists(FILENAME):
        with open(FILENAME, 'r', encoding='utf-8') as f:
            return json.load(f)
    return DEFAULT_TASKS.copy()

def save_tasks(tasks):
    with open(FILENAME, 'w', encoding='utf-8') as f:
        json.dump(tasks, f, ensure_ascii=False, indent=2)

def generate_task():
    if not tasks:
        messagebox.showinfo("Инфо", "Список задач пуст. Добавьте задачи!")
        return
    task = random.choice(tasks)
    history_listbox.insert(tk.END, f"{task['text']} [{task['type']}]")
    save_tasks(tasks)  # Сохраняем на случай добавления новых задач

def add_task():
    text = simpledialog.askstring("Новая задача", "Введите текст задачи:")
    if not text or text.strip() == "":
        messagebox.showerror("Ошибка", "Задача не может быть пустой!")
        return
    task_type = type_var.get()
    tasks.append({"text": text, "type": task_type})
    save_tasks(tasks)
    update_task_list()

def filter_tasks():
    selected_type = type_var.get()
    update_task_list(selected_type)

def update_task_list(filter_type=None):
    task_listbox.delete(0, tk.END)
    for task in tasks:
        if not filter_type or task["type"] == filter_type:
            task_listbox.insert(tk.END, f"{task['text']} [{task['type']}]")

# --- Основное окно ---
root = tk.Tk()
root.title("Random Task Generator")
root.geometry("500x600")

tasks = load_tasks()

# Фильтр по типу задачи
type_var = tk.StringVar(value="все")
filter_frame = tk.Frame(root)
filter_frame.pack(pady=5)
tk.Label(filter_frame, text="Фильтр по типу:").pack(side=tk.LEFT)
tk.OptionMenu(filter_frame, type_var, "все", "учёба", "спорт", "работа", command=lambda x: filter_tasks()).pack(side=tk.LEFT)

# Список задач
task_listbox = tk.Listbox(root, width=60, height=10)
task_listbox.pack(pady=10)
update_task_list()

# Кнопки управления задачами
btn_frame = tk.Frame(root)
btn_frame.pack(pady=5)
tk.Button(btn_frame, text="Сгенерировать задачу", command=generate_task).pack(side=tk.LEFT, padx=5)
tk.Button(btn_frame, text="Добавить задачу", command=add_task).pack(side=tk.LEFT, padx=5)

# История сгенерированных задач
history_label = tk.Label(root, text="История сгенерированных задач:")
history_label.pack()
history_listbox = tk.Listbox(root, width=60, height=10)
history_listbox.pack(pady=10)

root.mainloop()
