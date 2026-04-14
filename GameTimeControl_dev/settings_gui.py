import psutil
import tkinter as tk
from tkinter import messagebox
from tkinter import ttk
import os
import sys
import os

if getattr(sys, 'frozen', False):
    BASE_DIR = os.path.dirname(sys.executable)
else:
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))

DATA_FOLDER = os.path.join(BASE_DIR, "data")

if not os.path.exists(DATA_FOLDER):
    os.makedirs(DATA_FOLDER)

APPS_FILE = os.path.join(DATA_FOLDER, "monitored_apps.txt")
SETTINGS_FILE = os.path.join(DATA_FOLDER, "settings.txt")
IGNORE_FILE = os.path.join(DATA_FOLDER, "ignore.txt")
SERVICES_FILE = os.path.join(DATA_FOLDER, "List_of_services.txt")

def load_ignore_list():
    if not os.path.exists(IGNORE_FILE):
        return []
    with open(IGNORE_FILE, "r") as f:
        return [line.strip() for line in f.readlines()]

def get_apps():
    apps = set()
    for p in psutil.process_iter(['name']):
        try:
            name = p.info['name']
            if name.endswith(".exe"):
                apps.add(name)
        except:
            pass

    ignore_list = load_ignore_list()
    filtered_apps = [a for a in apps if a.lower() not in ignore_list]

    with open(SERVICES_FILE, "w") as f:
        for app in sorted(filtered_apps):
            f.write(app + "\n")

    return sorted(filtered_apps)

def save_settings():
    selected_apps = []
    for i in range(len(app_vars)):
        if app_vars[i].get():
            selected_apps.append(app_list[i])

    time_limit = time_entry.get()

    with open(APPS_FILE, "w") as f:
        for a in selected_apps:
            f.write(a + "\n")

    with open(SETTINGS_FILE, "w") as f:
        f.write("TIME_LIMIT=" + time_limit)

    messagebox.showinfo("Saved", "Settings saved successfully")

root = tk.Tk()
root.title("Chrono GTC Settings")
root.geometry("400x500")

tk.Label(root,text="Select games to monitor",font=("Segoe UI", 11)).pack(pady=5)

list_container = tk.Frame(root)
list_container.pack(fill="both", expand=True)

canvas = tk.Canvas(list_container)
scrollbar = tk.Scrollbar(list_container, orient="vertical", command=canvas.yview)

scrollable_frame = tk.Frame(canvas)
scrollable_frame.bind("<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("all")))

canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
canvas.configure(yscrollcommand=scrollbar.set)

canvas.pack(side="left", fill="both", expand=True)
scrollbar.pack(side="right", fill="y")

def _on_mousewheel(event):
    canvas.yview_scroll(int(-1*(event.delta/120)), "units")

canvas.bind_all("<MouseWheel>", _on_mousewheel)

app_list = get_apps()
app_vars = []

for app in app_list:
    var = tk.BooleanVar()
    chk = ttk.Checkbutton(scrollable_frame, text=app, variable=var, takefocus=0)
    chk.pack(anchor="w", padx=10)
    app_vars.append(var)

tk.Label(root,text="Allowed Play Time (Minutes)",font=("Segoe UI", 10)).pack(pady=5)

time_entry = tk.Entry(root)
time_entry.insert(0,"60")
time_entry.pack()

ttk.Button(root,text="Save",command=save_settings).pack(pady=10)

root.mainloop()