# DDL Reminder 📚

A command-line tool to track assignment deadlines with SQLite database storage.
Never miss a submission again!

## Features
- ✅ Add assignments with course name and precise deadline (to the minute)
- 📋 View all / unfinished / completed tasks separately
- 🔥 Highlights urgent tasks (due within 24 hours)
- ⚠️ Shows overdue tasks
- ✔️ Mark tasks as done
- 🗑️ Delete tasks
- 📊 Year stats: completion rate & breakdown by course

## How to Use
1. Make sure Python 3 is installed
2. Run the program:
   python main.py
3. Choose from the menu:
   - 1: Show all tasks
   - 2: Show unfinished only
   - 3: Show completed only
   - 4: Add a new task
   - 5: Mark task as done
   - 6: Delete task
   - 7: Year stats
   - 8: Exit

## Tech Stack
- Python 3
- SQLite3 (built-in, no installation needed)
- datetime module

## Data Storage
All tasks are saved in a local `tasks.db` SQLite database file.
Data persists across sessions and accumulates all year.