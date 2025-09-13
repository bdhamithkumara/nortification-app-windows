import tkinter as tk
from datetime import datetime
import os, json, pytz, sys, webbrowser
from PIL import Image, ImageTk  # pip install pillow

APP_VERSION = "1.0.0"
APP_AUTHOR = "bdhamithkumara"

GITHUB_URL = "https://github.com/bdhamithkumara"
LINKEDIN_URL = "https://www.linkedin.com/in/bdhamithkumara/"

STATE_FILE = os.path.expanduser("~/.daily_reminder.json")
CONFIG_FILE = os.path.expanduser("~/.daily_reminder_config.json")

def resource_path(relative_path):
    try:
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")
    return os.path.join(base_path, relative_path)

# persistence
def load_state():
    if os.path.exists(STATE_FILE):
        with open(STATE_FILE, 'r') as f:
            return json.load(f)
    return {}

def save_state(state):
    with open(STATE_FILE, 'w') as f:
        json.dump(state, f)

def mark_dismissed():
    state = {'last_dismissed': datetime.now().strftime("%Y-%m-%d")}
    save_state(state)
    root.withdraw()  # hide instead of destroy

def load_config():
    if os.path.exists(CONFIG_FILE):
        with open(CONFIG_FILE, 'r') as f:
            return json.load(f)
    return {"reminder_message": "Don’t forget to do your tasks!"}

# Settings window
def open_settings():
    settings_win = tk.Toplevel(root)
    settings_win.title("Settings / About")
    settings_win.geometry("300x300")
    settings_win.resizable(False, False)

    tk.Label(settings_win, text=f"App Version: {APP_VERSION}", font=("Arial", 11)).pack(pady=5)
    tk.Label(settings_win, text=f"Author: {APP_AUTHOR}", font=("Arial", 11)).pack(pady=5)

    def open_github(): webbrowser.open(GITHUB_URL)
    def open_linkedin(): webbrowser.open(LINKEDIN_URL)

    tk.Button(settings_win, text="GitHub", command=open_github, fg="white", bg="#24292e").pack(pady=3, fill='x', padx=20)
    tk.Button(settings_win, text="LinkedIn", command=open_linkedin, fg="white", bg="#0e76a8").pack(pady=3, fill='x', padx=20)

    tk.Label(settings_win, text="Reminder message:").pack(pady=(10, 0))
    reminder_entry = tk.Entry(settings_win, width=30)
    reminder_entry.pack(pady=5)

    cfg = load_config()
    reminder_entry.insert(0, cfg.get("reminder_message"))

    def save_settings():
        new_cfg = {"reminder_message": reminder_entry.get()}
        with open(CONFIG_FILE, 'w') as f:
            json.dump(new_cfg, f)
        settings_win.destroy()

    tk.Button(settings_win, text="Save", command=save_settings).pack(pady=10)

# GUI
root = tk.Tk()
root.title("Daily Reminder")
root.attributes("-topmost", True)

icon_path = resource_path("stopwatch.ico")
try:
    root.iconbitmap(icon_path)
except Exception as e:
    print("Could not load icon:", e)

screen_width = root.winfo_screenwidth()
root.geometry(f"400x250+{screen_width - 420}+20")

config = load_config()

logo_path = resource_path("stopwatch.png")
if os.path.exists(logo_path):
    img = Image.open(logo_path).resize((48, 48))
    photo = ImageTk.PhotoImage(img)
    logo_label = tk.Label(root, image=photo)
    logo_label.image = photo
    logo_label.pack(pady=5)

reminder_lbl = tk.Label(root, text=config.get("reminder_message"), font=("Arial", 14, "bold"))
reminder_lbl.pack(pady=5)

local_time_lbl = tk.Label(root, text="", font=("Arial", 12))
local_time_lbl.pack()
aus_time_lbl = tk.Label(root, text="", font=("Arial", 12))
aus_time_lbl.pack()

frame = tk.Frame(root)
frame.pack(pady=10)
tk.Button(frame, text="OK", command=mark_dismissed).grid(row=0, column=0, padx=5)
tk.Button(frame, text="Settings", command=open_settings).grid(row=0, column=1, padx=5)

def update_time():
    now = datetime.now()
    local_time_lbl.config(text=now.strftime("Local: %Y-%m-%d %I:%M:%S %p"))
    aus_tz = pytz.timezone("Australia/Sydney")
    aus_time = datetime.now(aus_tz)
    aus_time_lbl.config(text=aus_time.strftime("Australia (Sydney): %Y-%m-%d %I:%M:%S %p"))
    root.after(1000, update_time)

# check every 30s if we should show again
def periodic_check():
    state = load_state()
    today = datetime.now().strftime("%Y-%m-%d")
    if state.get('last_dismissed') != today:
        root.deiconify()  # show window
    root.after(30000, periodic_check)

update_time()
periodic_check()
root.mainloop()
