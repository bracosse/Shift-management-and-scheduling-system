# import tkinter as tk
# from tkinter import ttk, messagebox
# import employee_manager as em
# from employee_manager import modify_employee_data

# class EmployeeManagerApp:
#     def __init__(self, root):
#         self.root = root
#         self.root.title("Employee Manager")
#         self.root.geometry("900x600")
        
#         self.setup_widgets()
#         self.refresh_employee_list()

#     def setup_widgets(self):
#         # Frame for employee list
#         self.tree = ttk.Treeview(self.root, columns=("ID", "Name", "Role", "Start Date", "End Date", "Nationality"), show="headings")
#         for col in self.tree["columns"]:
#             self.tree.heading(col, text=col)
#             self.tree.column(col, width=120)
#         self.tree.pack(pady=10, fill=tk.BOTH, expand=True)
        
#         # Buttons
#         btn_frame = tk.Frame(self.root)
#         btn_frame.pack(pady=10)

#         tk.Button(btn_frame, text="Add Employee", command=self.add_employee_popup).grid(row=0, column=0, padx=5)
#         tk.Button(btn_frame, text="Modify Employee", command=self.modify_employee_popup).grid(row=0, column=1, padx=5)
#         tk.Button(btn_frame, text="Delete Employee", command=self.delete_employee).grid(row=0, column=2, padx=5)

#     def refresh_employee_list(self):
#         for row in self.tree.get_children():
#             self.tree.delete(row)
#         for emp in em.get_employees():
#             self.tree.insert("", "end", values=emp)

#     def add_employee_popup(self):
#         self.employee_form_popup("Add Employee")

#     def modify_employee_popup(self):
#         selected = self.tree.focus()
#         if not selected:
#             messagebox.showwarning("No selection", "Select an employee to modify.")
#             return
#         values = self.tree.item(selected, "values")
#         self.employee_form_popup("Modify Employee", values)

#     def employee_form_popup(self, title, values=None):
#         popup = tk.Toplevel(self.root)
#         popup.title(title)
#         popup.geometry("400x400")

#         fields = ["Name", "RoleID", "StartDate (YYYY-MM-DD)", "EndDate (YYYY-MM-DD or blank)", "Nationality"]
#         entries = []

#         for i, label in enumerate(fields):
#             tk.Label(popup, text=label).pack()
#             entry = tk.Entry(popup)
#             entry.pack()
#             if values:
#                 if label == "EndDate (YYYY-MM-DD or blank)":
#                     entry.insert(0, values[4] if values[4] != "None" else "")
#                 else:
#                     entry.insert(0, values[fields.index(label) + 1])
#             entries.append(entry)

#         def submit():
#             data = [e.get().strip() for e in entries]
#             if not data[0] or not data[1] or not data[2]:
#                 messagebox.showerror("Missing Data", "Please fill out all required fields.")
#                 return

#             if title == "Add Employee":
#                 em.add_employee(*data)
#                 messagebox.showinfo("Success", "Employee added.")
#             else:
#                 employee_id = int(values[0])  # Get Employee ID from selected employee
#                 em.modify_employee_data(employee_id, *data)  # Pass employee ID along with other data for modification
#                 messagebox.showinfo("Success", "Employee modified.")
#             popup.destroy()
#             self.refresh_employee_list()

#         tk.Button(popup, text="Submit", command=submit).pack(pady=10)


#     def delete_employee(self):
#         selected = self.tree.focus()
#         if not selected:
#             messagebox.showwarning("No selection", "Select an employee to delete.")
#             return
#         values = self.tree.item(selected, "values")
#         confirm = messagebox.askyesno("Confirm", f"Delete employee {values[1]}?")
#         if confirm:
#             employee_id = int(values[0])  # Get the employee ID
#             em.delete_employee(employee_id)  # Pass employee ID to delete function
#             self.refresh_employee_list()

#     def reset_table(self):
#         confirm = messagebox.askyesno("Confirm Reset", "This will delete all employee data. Continue?")
#         if confirm:
#             em.reset_employee_table()
#             self.refresh_employee_list()

#     def show_holiday_balance(self):
#         balances = em.calculate_holiday_balance()
#         msg = "\n".join([f"{name}: {days:.1f} days" for name, days in balances])
#         messagebox.showinfo("Holiday Balances", msg)

# if __name__ == "__main__":
#     root = tk.Tk()
#     app = EmployeeManagerApp(root)
#     root.mainloop()


import tkinter as tk
from tkinter import ttk, messagebox
from datetime import datetime
from employee_manager import (
    add_employee,
    modify_employee_data,
    delete_employee,
    get_employees,
    reset_employees_table,
    calculate_all_holiday_balances,
)

def add_employee_gui():
    try:
        name = entry_name.get()
        role_id = int(entry_role_id.get())
        start_date = entry_start_date.get()
        end_date = entry_end_date.get()
        nationality = entry_nationality.get()
        add_employee(name, role_id, start_date, end_date, nationality)
        messagebox.showinfo("Success", f"Employee {name} added.")
    except Exception as e:
        messagebox.showerror("Error", str(e))

def delete_employee_gui():
    try:
        employee_id = int(entry_employee_id.get())
        delete_employee(employee_id)
        messagebox.showinfo("Success", f"Employee {employee_id} deleted.")
    except Exception as e:
        messagebox.showerror("Error", str(e))

def modify_employee_gui():
    try:
        employee_id = int(entry_employee_id.get())
        name = entry_name.get()
        role_id = int(entry_role_id.get())
        start_date = entry_start_date.get()
        end_date = entry_end_date.get()
        nationality = entry_nationality.get()
        modify_employee_data(employee_id, name, role_id, start_date, end_date, nationality)
        messagebox.showinfo("Success", f"Employee {employee_id} modified.")
    except Exception as e:
        messagebox.showerror("Error", str(e))

def show_employees_gui():
    employees = get_employees()
    output_text.delete(1.0, tk.END)
    if employees:
        output_text.insert(tk.END, f"{'ID':<5}{'Name':<20}{'Role':<15}{'Start Date':<12}{'End Date':<12}{'Nationality':<12}\n")
        output_text.insert(tk.END, "-" * 75 + "\n")
        for emp in employees:
            output_text.insert(tk.END, f"{emp[0]:<5}{emp[1]:<20}{emp[2]:<15}{emp[3]:<12}{emp[4]:<12}{emp[5]:<12}\n")
    else:
        output_text.insert(tk.END, "No employees found.\n")

# def reset_table_gui():
#     reset_employees_table()
#     messagebox.showinfo("Success", "All employees deleted and ID counter reset.")

def calculate_holidays_gui():
    calculate_all_holiday_balances()
    messagebox.showinfo("Success", "Holiday balances updated.")

# Tkinter GUI layout
root = tk.Tk()
root.title("Employee Management System")
# root.geometry(f"{550}x{750}+{int((root.winfo_screenwidth() - 750) / 2)}+{int((root.winfo_screenheight() - 750) / 2)}")
tk.Label(root, text="Employee ID (for modify/delete):").grid(row=0, column=0)
entry_employee_id = tk.Entry(root)
entry_employee_id.grid(row=0, column=1)

tk.Label(root, text="Name:").grid(row=1, column=0)
entry_name = tk.Entry(root)
entry_name.grid(row=1, column=1)

tk.Label(root, text="Role ID:").grid(row=2, column=0)
entry_role_id = tk.Entry(root)
entry_role_id.grid(row=2, column=1)

tk.Label(root, text="Start Date (YYYY-MM-DD):").grid(row=3, column=0)
entry_start_date = tk.Entry(root)
entry_start_date.grid(row=3, column=1)

tk.Label(root, text="End Date (YYYY-MM-DD):").grid(row=4, column=0)
entry_end_date = tk.Entry(root)
entry_end_date.grid(row=4, column=1)

tk.Label(root, text="Nationality:").grid(row=5, column=0)
entry_nationality = tk.Entry(root)
entry_nationality.grid(row=5, column=1)

tk.Button(root, text="Add Employee", command=add_employee_gui).grid(row=6, column=0)
tk.Button(root, text="Modify Employee", command=modify_employee_gui).grid(row=6, column=1)
tk.Button(root, text="Delete Employee", command=delete_employee_gui).grid(row=7, column=0)
tk.Button(root, text="Show Employees", command=show_employees_gui).grid(row=7, column=1)
tk.Button(root, text="Refresh Holidays", command=calculate_holidays_gui).grid(row=8, column=1)

output_text = tk.Text(root, height=15, width=100)
output_text.grid(row=9, column=0, columnspan=2)

root.mainloop()
