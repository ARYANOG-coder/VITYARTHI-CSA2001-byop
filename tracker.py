"""
tracker.py — Log study sessions and view today's activity.
"""

from utils import (colored, bold, SESSIONS_FILE, SESSIONS_HEADERS,
                   read_csv, append_csv, today_str,
                   get_float_input, get_nonempty_input)


def log_session():
    """Prompt the user for session details and save to sessions.csv."""
    print("\n  " + bold("LOG A STUDY SESSION"))
    print("  ─────────────────────────────")

    subject = get_nonempty_input(colored("  Subject name: ", "cyan")).title()
    hours   = get_float_input(colored("  Hours studied (e.g. 1.5): ", "cyan"), 0.1, 24.0)
    notes   = input(colored("  Notes (optional): ", "cyan")).strip()

    row = {
        "date":    today_str(),
        "subject": subject,
        "hours":   hours,
        "notes":   notes,
    }
    append_csv(SESSIONS_FILE, SESSIONS_HEADERS, row)

    msg = "  OK  Logged " + str(hours) + "h of " + subject + " on " + today_str() + "."
    print(colored(msg, "green"))


def view_today():
    """Display all sessions logged today."""
    date = today_str()
    print("\n  " + bold("TODAY'S SESSIONS  (" + date + ")"))
    print("  ─────────────────────────────────────")

    sessions = read_csv(SESSIONS_FILE, SESSIONS_HEADERS)
    today_sessions = [s for s in sessions if s["date"] == date]

    if not today_sessions:
        print(colored("  No sessions logged today. Start studying!", "yellow"))
        return

    total = 0.0
    for s in today_sessions:
        hrs = float(s["hours"])
        total += hrs
        hrs_str  = colored(str(round(hrs, 1)) + "h", "cyan")
        note_str = colored("  -- " + s["notes"], "white") if s["notes"] else ""
        subj     = s["subject"]
        print("  " + colored("*", "purple") + " " + subj.ljust(20) + " " + hrs_str + note_str)

    print("  " + "─" * 36)
    print("  " + bold("Total today:") + " " + colored(str(round(total, 1)) + "h", "green"))


def get_all_sessions():
    """Return all sessions as a list of dicts."""
    return read_csv(SESSIONS_FILE, SESSIONS_HEADERS)
