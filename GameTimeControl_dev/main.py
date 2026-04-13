import psutil
import time
import os
import tkinter as tk
from tkinter import messagebox


BASE_DIR = os.path.dirname(os.path.abspath(__file__))
PARENT_DIR = os.path.dirname(BASE_DIR)
DATA_FOLDER = os.path.join(PARENT_DIR, "data")

if not os.path.exists(DATA_FOLDER):
    os.makedirs(DATA_FOLDER)

APPS_FILE = os.path.join(DATA_FOLDER, "monitored_apps.txt")
SETTINGS_FILE = os.path.join(DATA_FOLDER, "settings.txt")
WARNING_10 = 55
WARNING_5 = 20

def load_monitored_apps():
    if not os.path.exists(APPS_FILE):
        return []
    with open(APPS_FILE, "r") as f:
        return [line.strip().lower() for line in f.readlines()]

def load_time_limit():
    if not os.path.exists(SETTINGS_FILE):
        return 60 * 60
    with open(SETTINGS_FILE, "r") as f:
        line = f.read().strip()
        try:
            minutes = int(line.split("=")[1])
            return minutes * 60
        except:
            return 60 * 60

def get_running_apps():
    running = []
    for p in psutil.process_iter(['name']):
        try:
            running.append(p.info['name'].lower())
        except:
            pass
    return running

def close_game(process_name):
    if not process_name.endswith('.exe'):
        process_name = process_name + '.exe'
    os.system(f'taskkill /f /im "{process_name}"')

def show_popup(message):
    popup = tk.Tk()
    popup.title("Chrono GTC - Warning")
    popup.geometry("350x155")
    popup.configure(bg='#f0f0f0')
    
    popup.attributes('-topmost', True)
    popup.lift()
    popup.focus_force()
    
    popup.eval('tk::PlaceWindow . center')
    
    tk.Label(popup, text="⏰", font=("Segoe UI", 24), bg='#f0f0f0').pack(pady=5)
    tk.Label(popup, text=message, font=("Segoe UI", 11, "bold"), bg='#f0f0f0').pack()
    
    tk.Button(popup, text="OK", command=popup.destroy, width=10, 
              bg='#4CAF50', fg='white', font=("Segoe UI", 10)).pack(pady=10)
    
    popup.after(10000, popup.destroy)
    
    popup.mainloop()

monitored_apps = load_monitored_apps()
remaining_time = load_time_limit()

warn10_done = False
warn5_done = False

print("Chrono GTC running.....")
print(f"Monitoring: {monitored_apps}")
print(f"Time limit: {remaining_time // 60} minutes")

# Accurate timing using monotonic clock
last_check = time.monotonic()
game_active = False

while True:
    running_apps = get_running_apps()
    game_running = None
    
    for app in monitored_apps:
        if app in running_apps:
            game_running = app
            break
    
    now = time.monotonic()
    
    if game_running:
        if not game_active:
            # Game just started
            last_check = now
            game_active = True
        
        elapsed = now - last_check
        if elapsed >= 1.0:
            remaining_time -= elapsed
            last_check = now
            
            print(f"Time remaining: {int(remaining_time // 60)}:{int(remaining_time % 60):02d}")
            
            if remaining_time <= WARNING_10 and not warn10_done:
                show_popup("10 minutes remaining!")
                warn10_done = True
            elif remaining_time <= WARNING_5 and not warn5_done:
                show_popup("5 minutes remaining!")
                warn5_done = True
            
            if remaining_time <= 0:
                close_game(game_running)
                show_popup("Time limit reached! Game closed.")
                break
    else:
        game_active = False
        time.sleep(2)