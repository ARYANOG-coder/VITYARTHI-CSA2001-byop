"""
goals.py — Set and display weekly study goals per subject.
"""

from utils import (colored, bold, GOALS_FILE, GOALS_HEADERS,
                   read_csv, write_csv, get_float_input, get_nonempty_input)


def _load_goals() -> dict:
    """Return goals as {subject: weekly_hours} dict."""
    rows = read_csv(GOALS_FILE, GOALS_HEADERS)
    return {r["subject"]: float(r["weekly_hours"]) for r in rows}


def _save_goals(goals: dict):
    rows = [{"subject": s, "weekly_hours": h} for s, h in goals.items()]
    write_csv(GOALS_FILE, GOALS_HEADERS, rows)


def set_goal():
    """Add or update a weekly goal for a subject."""
    print(f"\n  {bold('SET A WEEKLY GOAL')}")
    print("  ─────────────────────────────")

    goals   = _load_goals()
    subject = get_nonempty_input(colored("  Subject name: ", "cyan")).title()

    if subject in goals:
        print(colored(f"  Current goal for {subject}: {goals[subject]:.1f}h/week", "yellow"))

    hours = get_float_input(
        colored(f"  Target hours per week for {subject}: ", "cyan"),
        min_val=0.5, max_val=168.0
    )

    goals[subject] = hours
    _save_goals(goals)

    print(colored(f"\n  ✔  Goal set: {subject} → {hours:.1f}h/week.", "green"))


def view_goals():
    """Display all goals in a formatted table."""
    print(f"\n  {bold('WEEKLY GOALS')}")
    print("  ─────────────────────────────")

    goals = _load_goals()

    if not goals:
        print(colored("  No goals set yet. Use option 3 to add one.", "yellow"))
        return

    for subject, hours in sorted(goals.items()):
        print(f"  {colored('►', 'purple')} {subject:<20} {colored(f'{hours:.1f}h / week', 'cyan')}")


def get_goals_dict() -> dict:
    """Public accessor used by reports.py."""
    return _load_goals()
