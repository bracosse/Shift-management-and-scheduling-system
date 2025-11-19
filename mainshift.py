import tkinter as tk
from tkinter import messagebox
from shift_scheduler import assign_shifts_for_roles_gui, export_shifts_to_excel  # Make sure both functions are available

def generate_shifts():
    month_input = month_entry.get()
    result = assign_shifts_for_roles_gui(month_input)
    result_label.config(text=result)

def export_to_excel():
    month_input = month_entry.get()
    try:
        year, month = map(int, month_input.split("-"))
        export_shifts_to_excel(year, month)
        messagebox.showinfo("Success", f"Shifts exported for {month_input}")
    except FileNotFoundError:
        messagebox.showerror("Not Found", f"No generated shifts found for {month_input}. Please generate them first.")
    except Exception as e:
        messagebox.showerror("Error", f"An error occurred: {e}")

root = tk.Tk()
root.title("Monthly Shift Generator")
root.geometry(f"{350}x{350}+{int((root.winfo_screenwidth() - 350) / 2)}+{int((root.winfo_screenheight() - 350) / 2)}")

tk.Label(root, text="Enter Month (YYYY-MM):").pack(pady=5)
month_entry = tk.Entry(root)
month_entry.pack(pady=5)

generate_btn = tk.Button(root, text="Generate Shifts", command=generate_shifts)
generate_btn.pack(pady=10)

export_btn = tk.Button(root, text="Export to Excel", command=export_to_excel)
export_btn.pack(pady=10)

result_label = tk.Label(root, text="", wraplength=300, justify="left", fg="green")
result_label.pack(pady=10)

root.mainloop()
