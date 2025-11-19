import tkinter as tk
from tkinter import messagebox
from Exceptions_manager import report_sick_leave_gui, day_on_demand_gui  # These wrappers will call your existing logic

def submit_sick_leave():
    employee_id = entry_employee_id_sick.get()
    date_str = entry_date_sick.get()
    result = report_sick_leave_gui(employee_id, date_str)
    messagebox.showinfo("Result", result)

def submit_day_on_demand():
    employee_id = entry_employee_id_dod.get()
    date_str = entry_date_dod.get()
    result = day_on_demand_gui(employee_id, date_str)
    messagebox.showinfo("Result", result)

root = tk.Tk()
root.title("Exception System")
root.geometry("300x350")
root.geometry(f"{350}x{350}+{int((root.winfo_screenwidth() - 350) / 2)}+{int((root.winfo_screenheight() - 350) / 2)}")
# Sick Leave Frame
frame_sick = tk.LabelFrame(root, text="Report Sick Leave", padx=10, pady=10)
frame_sick.pack(padx=10, pady=10, fill="x")

tk.Label(frame_sick, text="Employee ID:").pack()
entry_employee_id_sick = tk.Entry(frame_sick)
entry_employee_id_sick.pack()

tk.Label(frame_sick, text="Date (YYYY-MM-DD):").pack()
entry_date_sick = tk.Entry(frame_sick)
entry_date_sick.pack()

tk.Button(frame_sick, text="Submit Sick Leave", command=submit_sick_leave).pack(pady=5)

# Day on Demand Frame
frame_dod = tk.LabelFrame(root, text="Request Day on Demand", padx=10, pady=10)
frame_dod.pack(padx=10, pady=10, fill="x")

tk.Label(frame_dod, text="Employee ID:").pack()
entry_employee_id_dod = tk.Entry(frame_dod)
entry_employee_id_dod.pack()

tk.Label(frame_dod, text="Date (YYYY-MM-DD):").pack()
entry_date_dod = tk.Entry(frame_dod)
entry_date_dod.pack()

tk.Button(frame_dod, text="Submit Day on Demand", command=submit_day_on_demand).pack(pady=5)

root.mainloop()
