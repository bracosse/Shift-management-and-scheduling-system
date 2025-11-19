import tkinter as tk
from tkinter import messagebox
from tkinter import simpledialog
import io
import sys
from holiday_manager import (
    add_holiday_request, calculate_holiday_balance, view_holidays_by_employee,
    update_holiday_status, delete_holiday
)

def submit_holiday_request_gui():
    try:
        employee_id = int(entry_employee_id.get())
        start_date = entry_start_date.get()
        end_date = entry_end_date.get()

        # Inject values into the backend via monkey patching input
        import builtins
        old_input = builtins.input
        inputs = iter([str(employee_id), start_date, end_date])
        builtins.input = lambda _: next(inputs)
        add_holiday_request()
        builtins.input = old_input
    except Exception as e:
        messagebox.showerror("Error", str(e))

def check_balance_gui():
    try:
        employee_id = simpledialog.askinteger("Holiday Balance", "Enter Employee ID:")
        if employee_id is None:
            return

        import builtins
        old_input = builtins.input
        builtins.input = lambda _: str(employee_id)

        old_stdout = sys.stdout
        sys.stdout = buffer = io.StringIO()

        calculate_holiday_balance()

        builtins.input = old_input
        sys.stdout = old_stdout

        result = buffer.getvalue()
        last_line = result.strip().split('\n')[-1] if result.strip() else "No output available."
        messagebox.showinfo("Holiday Balance", last_line)

    except Exception as e:
        messagebox.showerror("Error", str(e))


def view_holidays_gui():
    try:
        employee_id = simpledialog.askinteger("View Holidays", "Enter Employee ID:")
        if employee_id is None:
            return

        import builtins
        old_input = builtins.input
        builtins.input = lambda _: str(employee_id)

        old_stdout = sys.stdout
        sys.stdout = buffer = io.StringIO()

        view_holidays_by_employee()

        builtins.input = old_input
        sys.stdout = old_stdout

        result = buffer.getvalue()
        messagebox.showinfo("Holiday Requests", result)

    except Exception as e:
        messagebox.showerror("Error", str(e))
def update_holiday_gui():
    try:
        holiday_id = simpledialog.askinteger("Update Holiday", "Enter Holiday ID:")
        if holiday_id is None:
            return
        status = simpledialog.askstring("Status", "Enter status (1=Approved, 2=Pending, 3=Rejected):")
        if status not in ['1', '2', '3']:
            messagebox.showerror("Invalid Input", "Status must be 1, 2, or 3.")
            return

        import builtins
        old_input = builtins.input
        inputs = iter([str(holiday_id), status])
        builtins.input = lambda _: next(inputs)
        update_holiday_status()
        builtins.input = old_input
    except Exception as e:
        messagebox.showerror("Error", str(e))

def delete_holiday_gui():
    try:
        holiday_id = simpledialog.askinteger("Delete Holiday", "Enter Holiday ID:")
        if holiday_id is None:
            return
        import builtins
        old_input = builtins.input
        builtins.input = lambda _: str(holiday_id)
        delete_holiday()
        builtins.input = old_input
    except Exception as e:
        messagebox.showerror("Error", str(e))

# GUI Setup
root = tk.Tk()
root.title("Holiday System")
root.geometry("300x300")
root.geometry(f"{550}x{350}+{int((root.winfo_screenwidth() - 550) / 2)}+{int((root.winfo_screenheight() - 350) / 2)}")
tk.Label(root, text="Employee ID").pack()
entry_employee_id = tk.Entry(root)
entry_employee_id.pack()

tk.Label(root, text="Holiday Start Date (YYYY-MM-DD)").pack()
entry_start_date = tk.Entry(root)
entry_start_date.pack()

tk.Label(root, text="Holiday End Date (YYYY-MM-DD)").pack()
entry_end_date = tk.Entry(root)
entry_end_date.pack()

tk.Button(root, text="Submit Holiday Request", command=submit_holiday_request_gui).pack(pady=5)
tk.Button(root, text="Check Holiday Balance", command=check_balance_gui).pack(pady=5)
tk.Button(root, text="View Holidays", command=view_holidays_gui).pack(pady=5)
tk.Button(root, text="Update Holiday Status", command=update_holiday_gui).pack(pady=5)
tk.Button(root, text="Delete Holiday", command=delete_holiday_gui).pack(pady=5)
tk.Button(root, text="Exit", command=root.quit).pack(pady=10)

root.mainloop()
