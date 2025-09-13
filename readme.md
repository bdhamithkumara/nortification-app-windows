
# ⏰ Daily Reminder App

A lightweight Python/Tkinter-based reminder app that pops up a daily message with current local time and Australian time (Sydney).  
It also shows app info and links to your GitHub and LinkedIn.

---

## ✨ Features

- Shows **daily reminder message** (editable in Settings)
- Displays **local time** and **Australia (Sydney)** time in AM/PM format
- **App info** (version, author) inside Settings
- **GitHub & LinkedIn** buttons to open your profiles
- Stays **on top** of other windows when displayed
- Works as a **portable EXE** - no installation needed

---

## 📝 How to Install & Run  

1. **Download the EXE**  
   Get `DailyReminder.exe` from the [Releases](./releases) section.

2. **(Optional) Create a Desktop Shortcut**  
   - Right-click on `DailyReminder.exe` → *Send to* → *Desktop (create shortcut)*.

3. **Add to Windows Startup (so it runs when the PC starts):**

   - Press **Win + R**, type `shell:startup`, and press **Enter**.  
     This opens your personal Startup folder.
   - Copy either `DailyReminder.exe` **or its shortcut** into this folder.  
     (Right-click → Copy, then right-click inside the Startup folder → Paste.)

   ✅ Windows will automatically launch DailyReminder every time you log in.

4. **First Run**  
   - Double-click `DailyReminder.exe` (or the desktop shortcut).  
   - The reminder window should appear.  
   - Click “OK” to hide it; it keeps running in the background.  
   - Use “Settings” to change the reminder text or open your GitHub/LinkedIn.

---

## 📌 Notes for Users  

- **Hidden after OK -** The app stays running in the background so it can pop up again after sleep/unlock or the next day.  
- **Exit completely -** Use Task Manager (or add a tray icon in a future version) to exit the program.  
- **Auto-update reminder -** Open *Settings* to change the daily message.

---

## ⚙️ Build from Source (Optional)

If you want to build the EXE yourself,

```bash
pip install pyinstaller pillow pytz
pyinstaller --onefile --windowed --icon=stopwatch.ico daily_reminder.py

```

## 🖥 How to Make Daily Reminder Start with Windows

There are **two ways** to have the app start automatically:

### ✅ Method 1 — Using Windows Startup Folder (Recommended)

1. Make sure `DailyReminder.exe` is somewhere permanent (for example `C:\Program Files\DailyReminder\DailyReminder.exe`).
2. Press **Win + R** on your keyboard.
3. Type `shell:startup` and press **Enter**.  
   This opens your personal Startup folder.
4. In the window that opens, **copy your EXE or its shortcut**:
   - Right-click your `DailyReminder.exe` → *Copy*
   - Right-click inside the Startup folder → *Paste*
5. Done! Windows will now launch the app automatically whenever you sign in.

### 🟣 Method 2 — Using PowerShell (One-liner)

Open **PowerShell** and run (change path as needed):

```
$source = "C:\Path\To\DailyReminder.exe"
$startup = [Environment]::GetFolderPath('Startup')
Copy-Item $source -Destination $startup
Write-Host "DailyReminder added to startup!"
```

