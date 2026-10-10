import sqlite3
##Skrypt inicjalizujacy bazę danych
def initialize_database(db_name="data/measurements.db"):
    conn = sqlite3.connect(db_name)
    cursor = conn.cursor()
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS Parts(
        Part_ID TEXT PRIMARY KEY,
        Part_name TEXT,
        Type TEXT,
        Client TEXT
    )""")
    
    #Tworzenie tabeli dla charakterystyk (sztucznie nadane Char_ID żeby nie powielały się rekordy)
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS Characteristics(
        Char_ID INTEGER PRIMARY KEY AUTOINCREMENT,
        Part_ID TEXT,
        Characteristics TEXT,
        Nominal REAL,
        Min_Tol REAL,
        Max_Tol REAL,
        FOREIGN KEY (Part_ID) REFERENCES Parts(Part_ID)
    )""")
    
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS Measurements(
        Measurement_ID INTEGER PRIMARY KEY AUTOINCREMENT,
        Char_ID INTEGER,
        Cavity TEXT,
        Measured_value REAL,
        FOREIGN KEY (Char_ID) REFERENCES Characteristics(Char_ID)
    )""")
    
    conn.commit()
    return conn
if __name__ == "__main__":
    initialize_database()