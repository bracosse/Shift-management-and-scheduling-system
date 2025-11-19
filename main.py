import sys
import subprocess
import tkinter as tk


def launch_script(script_name):
    # Hide the launcher window
    root.withdraw()
    # Call the external script, blocking until it exits
    subprocess.call([sys.executable, script_name])
    # When the called script exits, show launcher again
    root.deiconify()

def exit_app():
    root.quit()  # This will close the main Tkinter window and exit the application

# Create main launcher window
title = "Launcher"
root = tk.Tk()
root.title(title)
root.geometry("550x350")
root.geometry(f"{550}x{550}+{int((root.winfo_screenwidth() - 550) / 2)}+{int((root.winfo_screenheight() - 550) / 2)}")
# Create a welcome label
welcome_label = tk.Label(root, text="Welcome to the BETA version of the shift shceduler System", font=("Arial", 14))
welcome_label.pack(pady=10)

# Create buttons for each module
frame = tk.Frame(root, padx=20, pady=20)
frame.pack(expand=True)

btn_emp = tk.Button(frame, text="Employee Manager", width=20,
                    command=lambda: launch_script("mainemp.py"))
btn_emp.pack(pady=5)

btn_shift = tk.Button(frame, text="Shift Scheduler", width=20,
                      command=lambda: launch_script("mainshift.py"))
btn_shift.pack(pady=5)

btn_holiday = tk.Button(frame, text="Holiday Manager", width=20,
                        command=lambda: launch_script("mainholiday.py"))
btn_holiday.pack(pady=5)

btn_exception = tk.Button(frame, text="Exception Manager", width=20,
                        command=lambda: launch_script("mainexception.py"))
btn_exception.pack(pady=5)

btn_exit = tk.Button(root, text="Exit", width=20, command=exit_app)
btn_exit.pack(pady=5)

if __name__ == "__main__":
    root.mainloop()
