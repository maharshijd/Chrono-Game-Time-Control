import psutil
import time
import os
from tkinter import Tk,messagebox

DATA_FOLDER = "../data"
APPS_FILE = os.path.join(DATA_FOLDER,"monitored_apps.txt")
SETTINGS_FILE = os.path.join(DATA_FOLDER,"settings.txt")
WARNING_10 = 10*60
WARNING_5 = 5*60

def load_monitored_apps():
    if not os.path.exists(APPS_FILE):
        return []
    with open(APPS_FILE,"r") as f:
        return [line.strip.lower() for line in f.readlines()]

def load_time_limit():
    if not os.path.exists(SETTINGS_FILE):
        return 60*60
    with open(SETTINGS_FILE,"r") as f:
        line = f.read().strip()
        try:
            minutes = int(line.split("=")[1])
            return minutes*60
        except:
            return 60*60
        
def get_running_apps():
    running = []
    for p in psutil.process_iter(['name']):
        try:
            running.append(p.info['name'].lower())
        except:
            pass
    return running

def close_game(process_name):
    os.system(f'taskkill /f /im "{process_name}"')

def show_popup(message):
    root = Tk()
    root.withdraw()
    messagebox.showwarning("Chrono GTC",message)
    root.destroy()

monitored_apps = load_monitored_apps()
remaining_time = load_time_limit()

warn10_done = False
warn5_done = False

print("Chrono GTC running.....")
while True:
    running_apps = get_running_apps()
    game_running = None
    for app in monitored_apps:
        if app in running_apps:
            game_running = app
            break
    if game_running:
        time.sleep(1)
        remaining_time -=1
        if remaining_time <= WARNING_10 and not warn10_done:
            show_popup("10 minutes left to play")
            warn10_done = True
        if remaining_time <= WARNING_5 and not warn5_done:
            show_popup("5 minutes left to play")
            warn5_done = True 
        if remaining_time <= 0:
            close_game(game_running)
            show_popup("Time Limit Reached. Game Closed.")
            break
    else:
        time.sleep(2)
