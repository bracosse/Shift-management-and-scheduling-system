import sqlite3
from datetime import datetime
from dateutil.relativedelta import relativedelta
from employee_manager import calculate_all_holiday_balances
from shift_scheduler import update_shifts_for_holiday

# Define role-based holiday accumulation rates (per month)
ROLE_RATES = {
    1: 1.0,  # HR
    2: 1.0,  # Agent
    3: 1.0,  # Manager
    4: 1.0,  # Team Leader
}
def recalculate_holiday_balance_for_employee(employee_id):
    try:
        # Get the total available holidays for the employee
        available_holidays = get_available_holidays(employee_id)
        print(f"✅ Holiday balance recalculated. Remaining balance: {available_holidays:.1f} days.")

    except Exception as e:
        print(f"❌ Error while recalculating holiday balance: {e}")
# Function to calculate the number of days between two dates (inclusive)
def calculate_days(start, end):
    start_date = datetime.strptime(start, "%Y-%m-%d")
    end_date = datetime.strptime(end, "%Y-%m-%d")
    return (end_date - start_date).days + 1

# Function to submit a holiday request
def add_holiday_request():
    try:
        employee_id = int(input("\nEnter Employee ID to request holiday: "))
        holiday_start_date = input("Enter holiday start date (YYYY-MM-DD): ")
        holiday_end_date = input("Enter holiday end date (YYYY-MM-DD): ")

        # Validate start date at least 1 month in advance
        start_date = datetime.strptime(holiday_start_date, "%Y-%m-%d")
        current_date = datetime.today()
        if start_date < current_date + relativedelta(months=1):
            print("❌ Holiday request must be made at least 1 month in advance.")
            return

        # Check available balance
        available = get_available_holidays(employee_id)
        requested_days = calculate_days(holiday_start_date, holiday_end_date)

        if requested_days > available:
            print(f"❌ Not enough holiday balance. You have {available:.1f} days left.")
            return

        # Save holiday request to database
        conn = sqlite3.connect('company_schedule.db')
        cursor = conn.cursor()
        cursor.execute('''
            INSERT INTO Holidays (EmployeeID, HolidayStartDate, HolidayEndDate, Type, Status)
            VALUES (?, ?, ?, ?, ?)
        ''', (employee_id, holiday_start_date, holiday_end_date, "Annual Leave", "Pending"))
        conn.commit()
        conn.close()
        print(f"✅ Holiday request for {requested_days} days submitted. Remaining balance: {available - requested_days:.1f} days\n")
        
    except ValueError:
        print("❌ Invalid input. Please enter a valid Employee ID and dates.")
    except Exception as e:
        print(f"❌ Error: {e}")

def calculate_holiday_balance():
    try:
        employee_id = int(input("\nEnter Employee ID to check holiday balance: "))
        conn = sqlite3.connect('company_schedule.db')
        cursor = conn.cursor()
        cursor.execute('''
            SELECT e.Name, r.RoleName, e.StartDate, e.EndDate, e.RoleID
            FROM Employees e
            JOIN Roles r ON e.RoleID = r.RoleID
            WHERE e.EmployeeID = ?
        ''', (employee_id,))
        row = cursor.fetchone()
        conn.close()
        calculate_all_holiday_balances()
        if not row:
            print("Employee not found.")
            return

        name, role_name, start_str, end_str, role_id = row
        start_date = datetime.strptime(start_str, "%Y-%m-%d")

        # Restrict the end date to the current year
        current_year_end = datetime(datetime.today().year, 12, 31)
        end_date = datetime.strptime(end_str, "%Y-%m-%d") if end_str else current_year_end

        # Ensure the end date is within the current year
        if end_date > current_year_end:
            end_date = current_year_end

        # Calculate months worked during the current year
        delta = relativedelta(end_date, start_date)
        months = delta.years * 12 + delta.months
        if end_date.day >= start_date.day:
            months += 1

        balance = months * ROLE_RATES.get(role_id, 0)
        available = get_available_holidays(employee_id)
        print(f"\n🧾 Holiday Balance for {name} ({role_name}):")
        print(f"• Contract Period in this year: {start_date.date()} to {end_date.date()}")
        print(f" Working months: {months}")
        print(f"•🧾 Holiday Balance: {available:.1f} days remaining\n")
    except ValueError:
        print("❌ Invalid input. Please enter a numeric Employee ID.")
    except Exception as e:
        print(f"❌ Error: {e}")
        
# Function to check available holiday balance
def get_available_holidays(employee_id):
    conn = sqlite3.connect('company_schedule.db')
    cursor = conn.cursor()

    cursor.execute('''
        SELECT e.Name, r.RoleName, e.StartDate, e.EndDate, e.RoleID
        FROM Employees e
        JOIN Roles r ON e.RoleID = r.RoleID
        WHERE e.EmployeeID = ?
    ''', (employee_id,))
    row = cursor.fetchone()

    if not row:
        conn.close()
        raise ValueError("Employee not found.")

    name, role_name, start_str, end_str, role_id = row
    start_date = datetime.strptime(start_str, "%Y-%m-%d")

    # Current year limits
    year = datetime.today().year
    year_start = datetime(year, 1, 1)
    year_end = datetime(year, 12, 31)

    # Trim contract to fit this year
    if start_date < year_start:
        start_date = year_start
    end_date = datetime.strptime(end_str, "%Y-%m-%d") if end_str else year_end
    if end_date > year_end:
        end_date = year_end

    # Compute number of working months in current year
    delta = relativedelta(end_date, start_date)
    months = delta.years * 12 + delta.months
    if end_date.day >= start_date.day:
        months += 1

    # Calculate entitled holidays
    entitled = months * ROLE_RATES.get(role_id, 0)

    # Fetch requested days in the current year
    cursor.execute('''
        SELECT HolidayStartDate, HolidayEndDate FROM Holidays
        WHERE EmployeeID = ? AND
              strftime('%Y', HolidayStartDate) = ? AND
              strftime('%Y', HolidayEndDate) = ? AND Status IN ('Approved', 'Pending')
    ''', (employee_id, str(year), str(year)))
    holidays = cursor.fetchall()
    conn.close()

    used = sum(calculate_days(start, end) for start, end in holidays)
    return entitled - used
# def add_holidays_back_to_balance(employee_id, days_to_add):
#     try:
#         # Assuming holidays are calculated on the fly, we can log the restoration
#         print(f"✅ {days_to_add} holiday days restored to Employee ID {employee_id}.")
#         # If you track remaining days explicitly in a table, update that here.
#     except Exception as e:
#         print(f"❌ Error restoring holiday days: {e}")

# Function to approve or reject a holiday request
def update_holiday_status():
    try:
        holiday_id = int(input("\nEnter the Holiday ID to update: "))
        status_input = input("Enter new status (1 for Approved, 2 for Pending, 3 for Rejected): ").strip()

        status_map = {"1": "Approved", "2": "Pending", "3": "Rejected"}
        status = status_map.get(status_input)

        if not status:
            print("❌ Invalid status. Please enter 1 for Approved, 2 for Pending, or 3 for Rejected.")
            return

        conn = sqlite3.connect('company_schedule.db')
        cursor = conn.cursor()

        # Get current holiday data
        cursor.execute('''
            SELECT EmployeeID, Status, HolidayStartDate, HolidayEndDate 
            FROM Holidays WHERE HolidayID = ?
        ''', (holiday_id,))
        result = cursor.fetchone()

        if not result:
            print("❌ Holiday ID not found.")
            return

        employee_id, current_status, start_date, end_date = result

        if current_status == "Approved" and status == "Rejected":
            print("❌ Approved holidays cannot be rejected.")
            return

        # Update holiday status
        cursor.execute('''
            UPDATE Holidays
            SET Status = ?
            WHERE HolidayID = ?
        ''', (status, holiday_id))

        conn.commit()
        calculate_all_holiday_balances()
        # If the status is rejected, calculate the days and add them back to balance
        if status == "Rejected":
            days_to_add = (datetime.strptime(end_date, "%Y-%m-%d") - datetime.strptime(start_date, "%Y-%m-%d")).days + 1
            #recalculate_holiday_balance_for_employee(employee_id)
            #add_holidays_back_to_balance(employee_id, days_to_add, cursor)
        conn.close()
        print(f"✅ Holiday request status updated to {status}.")
        update_shifts_for_holiday(employee_id, start_date, end_date)
    except ValueError:
        print("❌ Invalid input. Please enter a valid Holiday ID.")
    except Exception as e:
        print(f"❌ Error: {e}")

def add_holidays_back_to_balance(employee_id, days_to_add, cursor):
    try:
        # Update the HolidayBalance in the Employees table
        cursor.execute('''
            UPDATE Employees
            SET HolidayBalance = HolidayBalance + ?
            WHERE EmployeeID = ?
        ''', (days_to_add, employee_id))

        cursor.connection.commit()
        print(f"✅ {days_to_add} holiday days added back to Employee ID {employee_id}'s balance.")
    except Exception as e:
        print(f"❌ Error restoring holiday days: {e}")



# Function to view holiday requests per employee
def view_holidays_by_employee():
    try:
        employee_id = int(input("\nEnter Employee ID to view holidays: "))
        
        conn = sqlite3.connect('company_schedule.db')
        cursor = conn.cursor()

        cursor.execute('''
            SELECT HolidayID, HolidayStartDate, HolidayEndDate, Type, Status
            FROM Holidays
            WHERE EmployeeID = ?
        ''', (employee_id,))
        holidays = cursor.fetchall()
        conn.close()

        if holidays:
            print("\nHoliday Requests for Employee ID:", employee_id)
            for holiday in holidays:
                print(f"Holiday ID: {holiday[0]} | Start: {holiday[1]} | End: {holiday[2]} | Type: {holiday[3]} | Status: {holiday[4]}")
        else:
            print("❌ No holiday requests found for this employee.")
    
    except ValueError:
        print("❌ Invalid input. Please enter a valid Employee ID.")
    except Exception as e:
        print(f"❌ Error: {e}")
def delete_holiday():
    try:
        holiday_id = int(input("\nEnter the Holiday ID to delete: "))

        conn = sqlite3.connect('company_schedule.db')
        cursor = conn.cursor()

        # Check if the holiday status is 'Approved'
        cursor.execute('''
            SELECT EmployeeID, Status FROM Holidays WHERE HolidayID = ?
        ''', (holiday_id,))
        result = cursor.fetchone()

        if not result:
            print("❌ Holiday ID not found.")
            return

        employee_id, status = result
        if status == "Approved":
            print("❌ Approved holidays cannot be deleted.")
            return

        # If the holiday is not approved, proceed to delete
        cursor.execute('''
            DELETE FROM Holidays WHERE HolidayID = ?
        ''', (holiday_id,))

        conn.commit()
        conn.close()

        # Recalculate the holiday balance for the employee after deletion
        recalculate_holiday_balance_for_employee(employee_id)

        print(f"✅ Holiday request with ID {holiday_id} has been deleted.")
    
    except ValueError:
        print("❌ Invalid input. Please enter a valid Holiday ID.")
    except Exception as e:
        print(f"❌ Error: {e}")

# Menu
def main():
    while True:
        print("\n===== HOLIDAY MANAGEMENT MENU =====")
        print("1. Submit Holiday Request")
        print("2. Check Holiday Balance")
        print("3. View Holidays by Employee")
        print("4. Update Holiday Status (Approve/Reject)")
        print("5. Delete Holiday Request")
        print("6. Exit")
        choice = input("Select an option: ")

        if choice == "1":
            add_holiday_request()
        elif choice == "2":
            calculate_holiday_balance()
        elif choice == "3":
            view_holidays_by_employee()
        elif choice == "4":
            update_holiday_status()
        elif choice == "5":
            delete_holiday()
        elif choice == "6":
            print("Goodbye!")
            break
        else:
            print("Invalid option. Please select 1, 2, 3, 4, or 5.")

if __name__ == "__main__":
    main()
