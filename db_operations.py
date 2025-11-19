# import sqlite3

# # Function to add a role
# def add_role(role_name):
#     conn = sqlite3.connect('company_schedule.db')
#     cursor = conn.cursor()
#     cursor.execute("INSERT INTO Roles (RoleName) VALUES (?)", (role_name,))
#     conn.commit()
#     conn.close()

# # Function to get all roles
# def get_roles():
#     conn = sqlite3.connect('company_schedule.db')
#     cursor = conn.cursor()
#     cursor.execute("SELECT * FROM Roles")
#     roles = cursor.fetchall()
#     conn.close()
#     return roles

# # Function to get all employees (with Role Names)
# def get_employees():
#     conn = sqlite3.connect('company_schedule.db')
#     cursor = conn.cursor()
    
#     # Fetch all employees with their role names
#     cursor.execute('''
#     SELECT Employees.EmployeeID, Employees.Name, Roles.RoleName, Employees.StartDate, Employees.EndDate, Employees.Nationality
#     FROM Employees
#     JOIN Roles ON Employees.RoleID = Roles.RoleID
#     ''')
#     employees = cursor.fetchall()
    
#     conn.close()
    
#     return employees


