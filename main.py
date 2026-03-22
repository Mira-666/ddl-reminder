import sqlite3
import os
from datetime import datetime

DB_FILE = "tasks.db"

def init_db():
    """create table if not exists"""
    conn = sqlite3.connect(DB_FILE)
    c = conn.cursor()
    #自增字段
    c.execute("""
        CREATE TABLE IF NOT EXISTS tasks(
              id        INTEGER  PRIMARY KEY AUTOINCREMENT,
              course    TEXT     NOT NULL,
              title     TEXT     NOT NULL,
              ddl       TEXT     NOT NULL,
              done      INTEGER  NOT NULL DEFAULT 0,
              created   TEXT     NOT NULL
              )
              
    """)
    conn.commit()
    conn.close()

def get_conn():
    return sqlite3.connect(DB_FILE)
    
def get_time_left(ddl_str):
    """calculate time remaining,returns a display string"""
    ddl = datetime.strptime(ddl_str,"%Y-%m-%d %H:%M")
    now = datetime.now()
    diff = ddl - now

    if diff.total_seconds() < 0:
        return None,"⚠️ OVERDUE!"
    
    total_seconds = int(diff.total_seconds())
    days = total_seconds // 86400
    hours = (total_seconds % 86400) // 3600
    minutes = (total_seconds % 3600)//60

    if days == 0 and hours < 24:
        return total_seconds, f"{hours}h {minutes}m left ← URGENT!"
    elif days <= 3:
        return total_seconds, f"{days}d {hours}h {minutes}m left"
    else:
        return total_seconds, f"{days}d {hours}h {minutes}m left"
    
def show_tasks(filter_done=None):
    """
    filter_done:None = show all
                0    = unfinished only
                1    = done only
    """

    conn = get_conn()
    c = conn.cursor()

    if filter_done is None:
        c.execute("Select id, course, title, ddl, done, created FROM tasks ORDER BY ddl ASC")
    else:
        c.execute("SELECT id,course,title,ddl,done,creater FROM tasks WHERE done=? ORDER BY ddl ASC", (filter_done,))

    rows = c.fetchall()
    conn.close()

    if not rows:
        print("\n📫 no tasks now")
        return
    
    print("\n📋 your tasks:")
    print("-" * 65)

    for row in rows:
        id_, course,title,ddl,done,created = row
        status = "✅" if done else "❌"

        if done:
            time_display = "completed"
        else:
            _, time_display = get_time_left(ddl)
        print(f"[{id_}] {status}[{course}] {title}")
        print(f"      DDL:{ddl}  |  {time_display}")
        print(f"      added: {created}")
    print("-" * 65)

def add_task():
    print("\n➕ add new task")
    course = input("课程名称：")
    title = input("作业名称：")

    while True:
        ddl = input("截止日期(YYYY-MM-DD HH:MM): ")
        try:
            datetime.strptime(ddl,"%Y-%m-%d %H:%M")
            break
        except ValueError:
            print("❌ invalid format, use YYYY-MM-DD HH:MM")

    created = datetime.now().strftime("%Y-%m-%d %H:%M")
    
    conn = get_conn()
    c = conn.cursor()
    c.execute(
        "INSERT INTO tasks (course, title, ddl, done, created) VALUES (?, ?, ?, 0, ?)",
         (course, title, ddl, created)
    )
    conn.commit()
    conn.close()
    print("✅ task added")

def mark_done():
    show_tasks(filter_done=0)
    try:
        id_ = int(input("\nenter task ID to mark as done:"))
        conn = get_conn()
        c = conn.cursor()
        c.execute("UPDATE tasks SET done=1 WHERE id=?", (id_,))
        if c.rowcount == 0:
            print("❌ task ID not found")
        else:
            conn.commit()
            print("✅ task marked as done")
            conn.close()
    
    except ValueError:
        print("❌ please enter a number")

def delete_task():
    show_tasks()
    try:
        id_ = int(input("\nenter task ID to delete:"))
        conn = get_conn()
        c = conn.cursor()
        c.execute("SELECT title FROM tasks WHERE id=?", (id_,))
        row = c.fetchone()
        if not row:
            print("❌ task ID not found")
        else:
            c.execute("DELETE FROM tasks WHERE id=?", (id_,))
            conn.commit()
            print(f" deleted: {row[0]}")
        conn.close()
    except ValueError:
        print("❌ please enter a number")

def show_stats():
    conn = get_conn()
    c = conn.cursor()
    c.execute("SELECT COUNT(*) FROM tasks")
    total = c.fetchone()[0]

    c.execute("SELECT COUNT(*) FROM tasks WHERE done=1")
    done = c.fetchone()[0]

    now_str = datetime.now().strftime("%Y-%m-%d %H:%M")
    c.execute("SELECT COUNT(*) FROM tasks WHERE done=0 AND ddl < ?", (now_str,))
    overdue = c.fetchone()[0]

    c.execute("""
        SELECT course,
              COUNT(*) as total,
              SUM(done) as finished
        FROM tasks
        GROUP BY course
        ORDER BY total DESC
    """)
    by_course = c.fetchall()
    conn.close()

    print("\n📊 your stats:")
    print("-" * 40)
    print(f"  total tasks     : {total}")
    print(f"  completed       : {done}")
    print(f"  unfinished      : {total - done}")
    print(f"  overdue         : {overdue}")
    if total > 0:
        rate = round(done / total * 100)
        print(f"  completion     : {rate}%")
    print("\n  by course:")
    for course, t, f in by_course:
        f = f or 0
        print(f"    {course:<20}  {f}/{t}  done")
    print("-" * 40)


def main():
    init_db()

    while True:
        print("\n========== DDL Reminder ==========")
        print("1. Show all tasks")
        print("2. Show unfinished only")
        print("3. Show completed only")
        print("4. Add task")
        print("5. Mark task as done")
        print("6. Delete task")
        print("7. Year stats")
        print("8. Exit")

        choice = input("\nenter your choice: ")

        if choice == "1": show_tasks()
        elif choice == "2": show_tasks(filter_done = 0)
        elif choice == "3": show_tasks(filter_done = 1)
        elif choice == "4": add_task()
        elif choice == "5": mark_done()
        elif choice == "6": delete_task()
        elif choice == "7": show_stats()
        elif choice == "8":
            print("👋 goodbye!")
            break
        else:
            print("❌ invalid choice")

main()
