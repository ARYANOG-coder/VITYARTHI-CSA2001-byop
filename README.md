# 📚 Study Planner & Progress Tracker

A command-line application built in Python that helps students log study sessions, set weekly subject goals, and visualize their progress — all without needing an internet connection or a database.

---

## What It Does

- **Log study sessions** — record the subject, duration, and optional notes
- **View today's sessions** — instantly see how much you've studied today
- **Set weekly goals** — define target hours per subject for the week
- **Weekly text summary** — see progress bars comparing actual vs. goal hours, plus your study streak
- **Weekly chart** — a colourful grouped bar chart (matplotlib) comparing studied hours vs. goals
- **Study streak** — tracks how many consecutive days you've studied

---

## Project Structure

```
study-planner/
├── main.py            # Entry point; main menu loop
├── tracker.py         # Log sessions, view today's activity
├── goals.py           # Set and retrieve weekly goals
├── reports.py         # Text summary and matplotlib chart
├── utils.py           # Shared helpers: CSV I/O, colours, input validation
├── data/
│   ├── sessions.csv   # Auto-created; stores all logged sessions
│   └── goals.csv      # Auto-created; stores subject goals
├── requirements.txt   # Python dependencies
└── README.md
```

---

## Requirements

- Python 3.8 or higher
- pip (Python package manager)

---

## Setup & Installation

### 1. Clone the repository

```bash
git clone https://github.com/YOUR_USERNAME/study-planner.git
cd study-planner
```

### 2. (Recommended) Create a virtual environment

```bash
python -m venv venv

# On Windows:
venv\Scripts\activate

# On macOS/Linux:
source venv/bin/activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

---

## How to Run

```bash
python main.py
```

You will see the main menu:

```
╔═══════════════════════════════════════════╗
║        STUDY PLANNER & TRACKER  📚        ║
║     Track sessions · Set goals · Grow     ║
╚═══════════════════════════════════════════╝

MAIN MENU
─────────────────────────────────────
1  Log a study session
2  View today's sessions
3  Set a weekly subject goal
4  View all goals
5  Weekly summary (text)
6  Weekly summary (chart)
7  Exit
─────────────────────────────────────
```

---

## Usage Examples

### Logging a session

```
Enter your choice: 1

LOG A STUDY SESSION
─────────────────────────────
Subject name: Mathematics
Hours studied (e.g. 1.5): 2
Notes (optional): Completed Chapter 5 exercises

✔  Logged 2.0h of Mathematics on 2025-08-15.
```

### Setting a weekly goal

```
Enter your choice: 3

SET A WEEKLY GOAL
─────────────────────────────
Subject name: Mathematics
Target hours per week for Mathematics: 10

✔  Goal set: Mathematics → 10.0h/week.
```

### Viewing the weekly summary

```
WEEKLY SUMMARY
Week of 2025-08-11 to 2025-08-17
────────────────────────────────────────────────
● Mathematics         6.5h / 10.0h goal
  [█████████████░░░░░░░] 65%
● Physics             3.0h / 5.0h goal
  [████████████░░░░░░░░] 60%
────────────────────────────────────────────────
Total this week: 9.5h
Study streak: 4 day(s) in a row
```

---

## Data Storage

All data is stored locally in plain CSV files inside the `data/` folder. These files are created automatically on first run — no setup needed. You can open them in any spreadsheet application to inspect or edit your data.

| File | Contents |
|------|----------|
| `data/sessions.csv` | date, subject, hours, notes |
| `data/goals.csv` | subject, weekly_hours |

---

## Python Concepts Used

| Concept | Where |
|---------|-------|
| File I/O with `csv` module | `utils.py` |
| Functions & modular design | All modules |
| `datetime` module | Date filtering, streak calculation |
| `collections.defaultdict` | Aggregating hours per subject |
| Input validation with loops | `utils.py` |
| Data visualization | `reports.py` (matplotlib) |
| ANSI escape codes | `utils.py` (coloured CLI output) |

---

## Author

**[Your Name]**  
VIT — Python Programming Course  
BYOP Capstone Project
