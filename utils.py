"""
utils.py — Shared helper functions for the Study Planner.
"""

import os
import csv
from datetime import datetime

# ── File paths ──────────────────────────────────────────────────────────────
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
SESSIONS_FILE = os.path.join(BASE_DIR, "data", "sessions.csv")
GOALS_FILE    = os.path.join(BASE_DIR, "data", "goals.csv")

SESSIONS_HEADERS = ["date", "subject", "hours", "notes"]
GOALS_HEADERS    = ["subject", "weekly_hours"]


# ── ANSI colour helper ───────────────────────────────────────────────────────
COLORS = {
    "red":    "\033[91m",
    "green":  "\033[92m",
    "yellow": "\033[93m",
    "blue":   "\033[94m",
    "purple": "\033[95m",
    "cyan":   "\033[96m",
    "white":  "\033[97m",
    "reset":  "\033[0m",
    "bold":   "\033[1m",
}

def colored(text, color="white"):
    return f"{COLORS.get(color, '')}{text}{COLORS['reset']}"

def bold(text):
    return f"{COLORS['bold']}{text}{COLORS['reset']}"


# ── CSV initialisation ───────────────────────────────────────────────────────
def ensure_csv(filepath, headers):
    """Create a CSV with headers if it doesn't already exist."""
    os.makedirs(os.path.dirname(filepath), exist_ok=True)
    if not os.path.exists(filepath):
        with open(filepath, "w", newline="") as f:
            writer = csv.DictWriter(f, fieldnames=headers)
            writer.writeheader()

def init_data_files():
    ensure_csv(SESSIONS_FILE, SESSIONS_HEADERS)
    ensure_csv(GOALS_FILE, GOALS_HEADERS)


# ── CSV read/write ───────────────────────────────────────────────────────────
def read_csv(filepath, headers):
    ensure_csv(filepath, headers)
    with open(filepath, "r", newline="") as f:
        reader = csv.DictReader(f)
        return list(reader)

def append_csv(filepath, headers, row: dict):
    ensure_csv(filepath, headers)
    with open(filepath, "a", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=headers)
        writer.writerow(row)

def write_csv(filepath, headers, rows: list):
    """Overwrite entire file (used for updating goals)."""
    with open(filepath, "w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=headers)
        writer.writeheader()
        writer.writerows(rows)


# ── Date helpers ─────────────────────────────────────────────────────────────
def today_str():
    return datetime.now().strftime("%Y-%m-%d")

def current_week_dates():
    """Return a list of YYYY-MM-DD strings for the current Mon–Sun week."""
    from datetime import timedelta
    today = datetime.now().date()
    monday = today - timedelta(days=today.weekday())
    return [(monday + timedelta(days=i)).strftime("%Y-%m-%d") for i in range(7)]


# ── UI helpers ───────────────────────────────────────────────────────────────
def clear_screen():
    os.system("cls" if os.name == "nt" else "clear")

def print_banner():
    clear_screen()
    banner = r"""
  ╔═══════════════════════════════════════════╗
  ║        STUDY PLANNER & TRACKER  📚        ║
  ║     Track sessions · Set goals · Grow     ║
  ╚═══════════════════════════════════════════╝
    """
    print(colored(banner, "cyan"))

def print_menu():
    menu = f"""
  {bold("MAIN MENU")}
  ─────────────────────────────────────
  {colored('1', 'yellow')}  Log a study session
  {colored('2', 'yellow')}  View today's sessions
  {colored('3', 'yellow')}  Set a weekly subject goal
  {colored('4', 'yellow')}  View all goals
  {colored('5', 'yellow')}  Weekly summary (text)
  {colored('6', 'yellow')}  Weekly summary (chart)
  {colored('7', 'yellow')}  Exit
  ─────────────────────────────────────
    """
    print(menu)

def progress_bar(current, target, width=20):
    """Return a coloured ASCII progress bar string."""
    if target <= 0:
        return "[" + "?" * width + "]"
    ratio = min(current / target, 1.0)
    filled = int(ratio * width)
    bar = "█" * filled + "░" * (width - filled)
    pct = int(ratio * 100)
    color = "green" if ratio >= 1.0 else ("yellow" if ratio >= 0.5 else "red")
    return colored(f"[{bar}] {pct}%", color)


# ── Input validation ─────────────────────────────────────────────────────────
def get_float_input(prompt, min_val=0.0, max_val=24.0):
    while True:
        try:
            val = float(input(prompt))
            if min_val <= val <= max_val:
                return val
            print(colored(f"  Please enter a value between {min_val} and {max_val}.", "red"))
        except ValueError:
            print(colored("  Invalid input. Please enter a number.", "red"))

def get_nonempty_input(prompt):
    while True:
        val = input(prompt).strip()
        if val:
            return val
        print(colored("  This field cannot be empty.", "red"))


# Initialise data files on import
init_data_files()
