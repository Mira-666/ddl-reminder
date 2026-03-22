import json
import os
from datetime import datetime,date

DATA_FILE = "tasks.json" #save tasks in file

def load_tasks():
    """read tasks from file"""
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE,"r",encoding="utf-8") as f:
            return json.load(f)
    return []

def save_tasks(tasks):
    """save tasks to file"""
    with open(DATA_FILE,"w",encoding = "utf-8") as f:
        json.dump(tasks,f,ensure_ascii=False, indent = 2)

def show_tasks(tasks):
    """display all tasks"""
    if not tasks:
        print("\n📫 no tasks now")
        return
    
    print("\n📋 your tasks:")
    print("-" * 50)
    today = date.today()

    for i, task in enumerate(tasks):
        ddl = datetime.strptime(task["ddl"],"%Y-%m-%d").date()
        days_left = (ddl - today).days
        status = "✅" if task["done"] else "❌"
        if not task["done"]:
            if days_left < 0:
                urgent = " ⚠️ overdue"
            elif days_left <= 3:
                urgent = f" 🔥 only {days_left} days "
            else:
                urgent = f" {days_left} days"
        else:
            urgent = ""
        print(f"{i+1}.{status}[{task['course']}] {task['title']}")
        print(f"  DDL:{task['ddl']}{urgent}")
    print("-" * 50)

def add_task(tasks):
    """add new task"""
    print("\n➕ add new task")
    course = input("课程名称：")
    title = input("作业名称：")
    ddl = input("截止日期(YYYY-MM-DD)：")

    task = {
        "course": course,
        "title": title,
        "ddl": ddl,
        "done": False
    }
    tasks.append(task)
    save_tasks(tasks)
    print("✅ task added")

def mark_done(tasks):
    """mark task as done"""
    show_tasks(tasks)
    num = int(input("\n enter task number to mark as done: ")) - 1
    tasks[num]["done"] = True
    save_tasks(tasks)
    print("✅ task marked as done")

def main():
    tasks = load_tasks()

    while True:
        print("\n========== DDL Reminder ==========")
        print("1. Show Tasks")
        print("2. Add Task")
        print("3. Mark Task as Done")
        print("4. Exit")

        choice = input("\nenter your choice: ")

        if choice == "1":
            show_tasks(tasks)
        elif choice == "2":
            add_task(tasks)
        elif choice == "3":
            mark_done(tasks)
        elif choice == "4":
            print("👋 goodbye!")
            break
        else:
            print("❌ invalid choice, try again.")

main()
