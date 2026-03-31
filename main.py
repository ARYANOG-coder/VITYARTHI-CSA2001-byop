"""
Study Planner & Progress Tracker
A CLI tool to log study sessions, set goals, and visualize progress.
"""

from utils import clear_screen, print_banner, print_menu, colored
from tracker import log_session, view_today
from goals import set_goal, view_goals
from reports import weekly_summary, plot_weekly_chart


def main():
    print_banner()

    while True:
        print_menu()
        choice = input(colored("  Enter your choice (1-7): ", "cyan")).strip()

        if choice == "1":
            log_session()
        elif choice == "2":
            view_today()
        elif choice == "3":
            set_goal()
        elif choice == "4":
            view_goals()
        elif choice == "5":
            weekly_summary()
        elif choice == "6":
            plot_weekly_chart()
        elif choice == "7":
            print(colored("\n  Goodbye! Keep studying consistently. 📚\n", "green"))
            break
        else:
            print(colored("\n  Invalid choice. Please enter 1–7.\n", "red"))

        input(colored("\n  Press Enter to return to menu...", "yellow"))
        clear_screen()


if __name__ == "__main__":
    main()
