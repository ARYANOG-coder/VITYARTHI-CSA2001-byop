"""
reports.py — Weekly text summary and matplotlib bar chart.
"""

from collections import defaultdict
from utils import (colored, bold, progress_bar,
                   read_csv, SESSIONS_FILE, SESSIONS_HEADERS,
                   current_week_dates)
from goals import get_goals_dict


# ── Shared data builder ──────────────────────────────────────────────────────

def _build_weekly_data():
    """
    Return (totals, goals) where:
      totals = {subject: hours_this_week}
      goals  = {subject: weekly_target}
    All subjects from both sessions and goals are included.
    """
    week_dates = set(current_week_dates())
    sessions   = read_csv(SESSIONS_FILE, SESSIONS_HEADERS)
    goals      = get_goals_dict()

    totals = defaultdict(float)
    for s in sessions:
        if s["date"] in week_dates:
            totals[s["subject"]] += float(s["hours"])

    # Ensure subjects with goals but no sessions still appear
    for subject in goals:
        if subject not in totals:
            totals[subject] = 0.0

    return dict(totals), goals


# ── Text summary ─────────────────────────────────────────────────────────────

def weekly_summary():
    """Print a text-based weekly summary with progress bars."""
    from datetime import datetime
    week = current_week_dates()
    print(f"\n  {bold('WEEKLY SUMMARY')}")
    print(f"  Week of {week[0]} to {week[-1]}")
    print("  " + "─" * 48)

    totals, goals = _build_weekly_data()

    if not totals:
        print(colored("  No sessions logged this week yet.", "yellow"))
        return

    grand_total = 0.0
    for subject in sorted(totals):
        hrs    = totals[subject]
        target = goals.get(subject, 0)
        grand_total += hrs

        bar = progress_bar(hrs, target) if target > 0 else colored("[no goal set]", "white")
        goal_str = f"/ {target:.1f}h goal" if target > 0 else ""
        print(f"  {colored('●', 'purple')} {subject:<18} {colored(f'{hrs:.1f}h', 'cyan')} {goal_str}")
        print(f"    {bar}")

    print("  " + "─" * 48)
    print(f"  {bold('Total this week:')} {colored(f'{grand_total:.1f}h', 'green')}")

    # Streak
    streak = _compute_streak()
    streak_color = "green" if streak >= 3 else ("yellow" if streak >= 1 else "red")
    print(f"  {bold('Study streak:')} {colored(f'{streak} day(s) in a row', streak_color)}")


# ── Streak calculator ────────────────────────────────────────────────────────

def _compute_streak() -> int:
    """Count consecutive days (ending today) where at least one session was logged."""
    from datetime import datetime, timedelta

    sessions  = read_csv(SESSIONS_FILE, SESSIONS_HEADERS)
    study_days = {s["date"] for s in sessions}

    streak = 0
    day    = datetime.now().date()
    while True:
        day_str = day.strftime("%Y-%m-%d")
        if day_str in study_days:
            streak += 1
            day -= timedelta(days=1)
        else:
            break
    return streak


# ── Matplotlib chart ─────────────────────────────────────────────────────────

def plot_weekly_chart():
    """Generate and display a grouped bar chart of actual vs. goal hours."""
    try:
        import matplotlib.pyplot as plt
        import matplotlib.patches as mpatches
        import numpy as np
    except ImportError:
        print(colored("\n  matplotlib or numpy not installed.", "red"))
        print(colored("  Run:  pip install matplotlib numpy", "yellow"))
        return

    totals, goals = _build_weekly_data()

    if not totals:
        print(colored("\n  No data to chart this week.", "yellow"))
        return

    subjects = sorted(totals.keys())
    actual   = [totals[s] for s in subjects]
    target   = [goals.get(s, 0) for s in subjects]

    x     = np.arange(len(subjects))
    width = 0.35

    fig, ax = plt.subplots(figsize=(10, 6))
    fig.patch.set_facecolor("#1a1a2e")
    ax.set_facecolor("#16213e")

    bars_actual = ax.bar(x - width / 2, actual, width,
                         label="Hours studied", color="#4cc9f0", zorder=3)
    bars_goal   = ax.bar(x + width / 2, target, width,
                         label="Weekly goal",   color="#f72585", alpha=0.7, zorder=3)

    # Value labels on bars
    for bar in bars_actual:
        h = bar.get_height()
        if h > 0:
            ax.annotate(f"{h:.1f}h",
                        xy=(bar.get_x() + bar.get_width() / 2, h),
                        xytext=(0, 4), textcoords="offset points",
                        ha="center", va="bottom", color="white", fontsize=9)

    for bar in bars_goal:
        h = bar.get_height()
        if h > 0:
            ax.annotate(f"{h:.1f}h",
                        xy=(bar.get_x() + bar.get_width() / 2, h),
                        xytext=(0, 4), textcoords="offset points",
                        ha="center", va="bottom", color="white", fontsize=9)

    # Styling
    from datetime import datetime
    week = current_week_dates()
    ax.set_title(f"Weekly Study Progress  ({week[0]} – {week[-1]})",
                 color="white", fontsize=14, pad=16)
    ax.set_xlabel("Subject", color="white", fontsize=11)
    ax.set_ylabel("Hours", color="white", fontsize=11)
    ax.set_xticks(x)
    ax.set_xticklabels(subjects, color="white", fontsize=10)
    ax.tick_params(axis="y", colors="white")
    ax.spines[:].set_color("#444466")
    ax.yaxis.grid(True, color="#333355", linestyle="--", alpha=0.7, zorder=0)
    ax.set_axisbelow(True)
    ax.legend(facecolor="#1a1a2e", edgecolor="#444466", labelcolor="white")

    plt.tight_layout()
    plt.show()
    print(colored("\n  Chart displayed. Close the chart window to continue.", "cyan"))
