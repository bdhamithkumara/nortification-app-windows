import tkinter as tk
from datetime import datetime, timedelta
import os, json, pytz, sys, webbrowser
from PIL import Image, ImageTk  # pip install pillow

APP_VERSION = "1.0.0"
APP_AUTHOR = "bdhamithkumara"

GITHUB_URL = "https://github.com/bdhamithkumara"
LINKEDIN_URL = "https://www.linkedin.com/in/bdhamithkumara/"

WORK_HOURS = 8
NOTIFICATION_INTERVAL_HOURS = 1

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
        try:
            with open(STATE_FILE, 'r') as f:
                return json.load(f)
        except (json.JSONDecodeError, IOError):
            return {}
    return {}

def save_state(state):
    with open(STATE_FILE, 'w') as f:
        json.dump(state, f)

def mark_dismissed():
    state = load_state()
    today = datetime.now().strftime("%Y-%m-%d")
    
    # Store dismissal for the basic periodic reminder
    state['last_dismissed'] = today
    
    # Store work start time if not already set for today
    if state.get('work_date') != today:
        state['work_date'] = today
        state['start_time'] = datetime.now().isoformat()
        state['last_notified_hour'] = 0
    
    save_state(state)
    root.withdraw()

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
root.geometry(f"400x300+{screen_width - 420}+20")

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
work_status_lbl = tk.Label(root, text="", font=("Arial", 12, "italic"), fg="blue")
work_status_lbl.pack(pady=5)

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
    
    # Update work progress
    state = load_state()
    today = now.strftime("%Y-%m-%d")
    if state.get('work_date') == today and 'start_time' in state:
        start_time = datetime.fromisoformat(state['start_time'])
        elapsed = now - start_time
        remaining = timedelta(hours=WORK_HOURS) - elapsed
        
        if remaining.total_seconds() > 0:
            hours, remainder = divmod(int(remaining.total_seconds()), 3600)
            minutes, _ = divmod(remainder, 60)
            work_status_lbl.config(text=f"Work remaining: {hours}h {minutes}m")
            
            # Check for hourly notification
            elapsed_hours = int(elapsed.total_seconds() // 3600)
            if elapsed_hours > state.get('last_notified_hour', 0):
                state['last_notified_hour'] = elapsed_hours
                save_state(state)
                reminder_lbl.config(text=f"Progress: {hours} hours remaining!")
                root.deiconify()
                root.attributes("-topmost", True)
        else:
            work_status_lbl.config(text="Work shift completed!", fg="green")
            if state.get('done_notified') != today:
                state['done_notified'] = today
                save_state(state)
                reminder_lbl.config(text="Shift completed! Great job!")
                root.deiconify()
                root.attributes("-topmost", True)
    
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
root.deiconify() # Ensure visible on manual launch
root.mainloop()
