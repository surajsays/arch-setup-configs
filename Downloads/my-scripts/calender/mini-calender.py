#!/usr/bin/env python3
import tkinter as tk
from datetime import date
import calendar
import json
from pathlib import Path

# --- Config ---
DATA_FILE = Path.home() / "Downloads/my-scripts/calender/data.json"
CELL_SIZE = 3
ROWS, COLS = 5, 7
WINDOW_BG = "#222222"
BTN_FG = "white"

# --- Load data ---
if DATA_FILE.exists():
    with open(DATA_FILE, "r") as f:
        data = json.load(f)
else:
    data = {}

def save():
    DATA_FILE.parent.mkdir(parents=True, exist_ok=True)
    with open(DATA_FILE, "w") as f:
        json.dump(data, f)

# --- Tk setup ---
root = tk.Tk()
root.overrideredirect(True)
root.attributes('-topmost', True)
root.attributes('-alpha', 0.9)
root.configure(bg=WINDOW_BG)
root.geometry("+1500+40")

today = date.today()
current_year = today.year
current_month = today.month

# --- Dragging logic ---
def start_move(event):
    root.x = event.x
    root.y = event.y

def on_move(event):
    deltax = event.x - root.x
    deltay = event.y - root.y
    x = root.winfo_x() + deltax
    y = root.winfo_y() + deltay
    root.geometry(f"+{x}+{y}")

root.bind("<Button-1>", start_move)
root.bind("<B1-Motion>", on_move)

# --- Month header ---
header_var = tk.StringVar()
header_label = tk.Label(root, textvariable=header_var, bg=WINDOW_BG, fg="white", font=("Arial", 10, "bold"))
header_label.grid(row=0, column=0, columnspan=COLS)
def update_header():
    header_var.set(f"{calendar.month_name[current_month]} {current_year}")
update_header()

# --- Month control buttons below header ---
button_frame = tk.Frame(root, bg=WINDOW_BG)
button_frame.grid(row=1, column=0, columnspan=COLS, pady=(2,5))

def prev_month():
    global current_month, current_year
    current_month -= 1
    if current_month < 1:
        current_month = 12
        current_year -= 1
    update_calendar()
    update_header()

def next_month():
    global current_month, current_year
    current_month += 1
    if current_month > 12:
        current_month = 1
        current_year += 1
    update_calendar()
    update_header()

def close_window():
    root.destroy()

# Minimal buttons with just text, no background square
btn_prev = tk.Button(button_frame, text="<", command=prev_month, bg=WINDOW_BG, fg=BTN_FG,
                     bd=0, relief="flat", font=("Arial", 10, "bold"))
btn_prev.pack(side="left", padx=3)

btn_next = tk.Button(button_frame, text=">", command=next_month, bg=WINDOW_BG, fg=BTN_FG,
                     bd=0, relief="flat", font=("Arial", 10, "bold"))
btn_next.pack(side="left", padx=3)

btn_close = tk.Button(button_frame, text="✕", command=close_window, bg=WINDOW_BG, fg=BTN_FG,
                      bd=0, relief="flat", font=("Arial", 10, "bold"))
btn_close.pack(side="left", padx=3)

# --- Calendar grid ---
grid_frame = tk.Frame(root, bg=WINDOW_BG)
grid_frame.grid(row=2, column=0, columnspan=COLS)

def toggle_today(event, color):
    day_str = f"{today.year}-{today.month:02d}-{today.day:02d}"
    data[day_str] = color
    save()
    update_calendar()

def update_calendar():
    for widget in grid_frame.winfo_children():
        widget.destroy()

    month_days = calendar.monthrange(current_year, current_month)[1]
    day_counter = 1

    for i in range(ROWS):
        for j in range(COLS):
            if day_counter <= month_days:
                day_str = f"{current_year}-{current_month:02d}-{day_counter:02d}"
                color = data.get(day_str, "#555555")  # neutral default

                border = 1
                if day_counter == today.day and current_month == today.month and current_year == today.year:
                    border = 2

                b = tk.Label(grid_frame, text=str(day_counter), width=CELL_SIZE, height=1,
                             bg=color, fg="white", relief="solid", bd=border)
                b.grid(row=i, column=j, padx=1, pady=1)

                # Only today clickable
                if day_counter == today.day and current_month == today.month and current_year == today.year:
                    b.bind("<Button-1>", lambda e, c="green": toggle_today(e, c))
                    b.bind("<Button-3>", lambda e, c="red": toggle_today(e, c))
            day_counter += 1

update_calendar()
root.mainloop()
