import psutil
import tkinter as tk
from tkinter import messagebox
import os

DATA_FOLDER = "data"
if not os.path.exists(DATA_FOLDER):
    os.makedirs(DATA_FOLDER)
APPS_FILE = os.path.join(DATA_FOLDER,"monitored_apps.txt")
SETTINGS_FILE = os.path.join(DATA_FOLDER,"settings.txt")
def get_apps():
    apps = set()
    for p in psutil.process_iter(['name']):
        try:
            name = p.info['name']
            if name.endswith(".exe"):
                apps.add(name)
        except:
            pass
    ignore = ["explorer.exe","cmd.exe","SearchApp.exe","python.exe"]
    return sorted([a for a in apps if a not in ignore])
def save_settings():
    selected_apps = []
    for i in range(len(app_vars)):
        if app_vars[i].get():
            selected_apps.append(app_list[i])
    time_limit = time_entry.get()
    with open(APPS_FILE,"w") as f:
        for a in selected_apps:
            f.write(app + "\n")
    with open(SETTINGS_FILE,"w") as f:
        f.write("TIME_LIMIT="+time_limit)
    messagebox.showinfo("Saved","Settings saved successfully")

root = tk.Tk()
root.title("ChronoGTC Settings")
root.geometry("350x500")
tk.Label(root,text="Select games to monitor").pack()
app_list = get_apps()
app_vars = []

# frame = tk.Frame(root)
# frame.pack()
# for app in app_list:
#     var = tk.BooleanVar()
#     chk = tk.Checkbutton(frame,text=app,variable=var)
#     chk.pack(anchor="w")

#     app_vars.append(var)

canvas = tk.Canvas(root)
scrollbar = tk.Scrollbar(root,orient="vertical",command=canvas.yview)
scrollable_frame = tk.Frame(canvas)
scrollable_frame.bind("<Configure>",lambda e: canvas.configure(scrollregion=canvas.bbox("all")))





tk.Label(root,text="\nAllowed Play Time (Minutes)").pack()
time_entry = tk.Entry(root)
time_entry.insert(0,"60")
time_entry.pack()
tk.Button(root,text="Save",command=save_settings).pack(pady=10)
root.mainloop()