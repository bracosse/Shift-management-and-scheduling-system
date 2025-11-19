import sqlite3

def setup_database():
    """Creates the database with all tables matching your schema"""
    conn = sqlite3.connect('company_schedule.db')
    cursor = conn.cursor()

    # Create Roles Table
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS Roles (
        RoleID INTEGER PRIMARY KEY,
        RoleName TEXT NOT NULL
    );
    ''')

    # Create Employees Table
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS Employees (
        EmployeeID INTEGER PRIMARY KEY AUTOINCREMENT,
        Name TEXT NOT NULL,
        RoleID INTEGER,
        StartDate TEXT NOT NULL,
        EndDate TEXT,
        Nationality TEXT,
        FOREIGN KEY (RoleID) REFERENCES Roles(RoleID)
    );
    ''')

    # Create Shifts Table
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS Shifts (
        ShiftID INTEGER PRIMARY KEY AUTOINCREMENT,
        EmployeeID INTEGER,
        Date TEXT NOT NULL,
        ShiftType TEXT NOT NULL,
        FOREIGN KEY (EmployeeID) REFERENCES Employees(EmployeeID)
    );
    ''')

    # Create Holidays Table
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS Holidays (
        HolidayID INTEGER PRIMARY KEY AUTOINCREMENT,
        EmployeeID INTEGER,
        HolidayStartDate TEXT NOT NULL,
        HolidayEndDate TEXT NOT NULL,
        Type TEXT NOT NULL,
        FOREIGN KEY (EmployeeID) REFERENCES Employees(EmployeeID)
    );
    ''')

    # Create Exceptions Table
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS Exceptions (
        ExceptionID INTEGER PRIMARY KEY AUTOINCREMENT,
        EmployeeID INTEGER,
        ExceptionDate TEXT NOT NULL,
        Type TEXT NOT NULL,
        FOREIGN KEY (EmployeeID) REFERENCES Employees(EmployeeID)
    );
    ''')

    # Add EmployeeName and Role columns to Shifts if they don't exist
    try:
        cursor.execute("ALTER TABLE Shifts ADD COLUMN EmployeeName TEXT;")
    except sqlite3.OperationalError:
        pass  # Column already exists

    try:
        cursor.execute("ALTER TABLE Shifts ADD COLUMN Role TEXT;")
    except sqlite3.OperationalError:
        pass  # Column already exists

    conn.commit()
    conn.close()
    print("Database tables created successfully with all required columns.")

if __name__ == "__main__":
    setup_database()

#ALTER TABLE Holidays ADD COLUMN Status TEXT DEFAULT 'Pending';
#ALTER TABLE Employees ADD COLUMN HolidayBalance REAL DEFAULT 0;