import tkinter as tk
from tkinter import ttk


def launch_gui(people_list, days):
    root = tk.Tk()
    root.title("Common Free Times")

    tree = ttk.Treeview(root, columns=days, show="headings")
    for day in days:
        tree.heading(day, text=day)
        tree.column(day, width=120)

    # Fill the table with free times for each person
    for person in people_list:
        row = []
        for day in days:
            free_times = common_free_times(person, day)  # your function
            row.append(", ".join(free_times) if free_times else "Busy")
        tree.insert("", tk.END, values=row)

    tree.pack(expand=True, fill="both")
    root.mainloop()
