import sqlite3

# Connect to SQLite database (or create it if it doesn't exist)
conn = sqlite3.connect("maso_data.db")
c = conn.cursor()

def create_tables():
    c.execute("""
        CREATE TABLE IF NOT EXISTS users (
            username TEXT PRIMARY KEY, 
            password TEXT
        )
    """)
    c.execute("""
        CREATE TABLE IF NOT EXISTS foodrecordd (
            id INTEGER PRIMARY KEY AUTOINCREMENT, 
            name TEXT, 
            address TEXT, 
            phone_number INTEGER, 
            maps TEXT, 
            food_name TEXT, 
            quantity INTEGER, 
            date DATE, 
            available_time TEXT
        )
    """)
    c.execute("""
        CREATE TABLE IF NOT EXISTS wasterecordd (
            id INTEGER PRIMARY KEY AUTOINCREMENT, 
            name TEXT, 
            address TEXT, 
            phone_number INTEGER, 
            maps TEXT, 
            waste_type TEXT, 
            quantity INTEGER, 
            reusable TEXT, 
            date DATE
        )
    """)
    c.execute("""
        CREATE TABLE IF NOT EXISTS donationrecordd (
            id INTEGER PRIMARY KEY AUTOINCREMENT, 
            name TEXT, 
            address TEXT, 
            phone_number INTEGER, 
            maps TEXT, 
            date_of_requirement TEXT, 
            time INTEGER, 
            quantity TEXT
        )
    """)
    c.execute("""
        CREATE TABLE IF NOT EXISTS donationdetail (
            id INTEGER PRIMARY KEY AUTOINCREMENT, 
            donor_name TEXT, 
            donor_phone INTEGER, 
            recipient_name TEXT, 
            recipient_phone INTEGER, 
            quantity TEXT
        )
    """)

def insert_sample_data():
    users = [
        ("alice", "password123"),
        ("bob", "securepassword"),
        ("charlie", "password456")
    ]
    c.executemany("INSERT INTO users (username, password) VALUES (?, ?)", users)

    food_records = [
        ("John Doe", "123 Elm Street", 1234567890, "http://example.com", "Apples", 10, "2024-07-25", "09:00-12:00"),
        ("Jane Smith", "456 Oak Avenue", 2345678901, "http://example.com", "Bread", 20, "2024-07-26", "13:00-16:00"),
        ("Alice Johnson", "789 Pine Road", 3456789012, "http://example.com", "Milk", 15, "2024-07-27", "08:00-11:00")
    ]
    c.executemany("""
        INSERT INTO foodrecordd (name, address, phone_number, maps, food_name, quantity, date, available_time) 
        VALUES (?, ?, ?, ?, ?, ?, ?, ?)
    """, food_records)

    waste_records = [
        ("Alice Johnson", "789 Pine Road", 3456789012, "http://example.com", "Food", 5, "Yes", "2024-07-25"),
        ("Bob", "456 Oak Avenue", 2345678901, "http://example.com", "Food", 7, "No", "2024-07-26")
    ]
    c.executemany("""
        INSERT INTO wasterecordd (name, address, phone_number, maps, waste_type, quantity, reusable, date) 
        VALUES (?, ?, ?, ?, ?, ?, ?, ?)
    """, waste_records)

    donation_requests = [
        ("John Doe", "123 Elm Street", 1234567890, "http://example.com", "2024-07-30", 1, "10"),
        ("Jane Smith", "456 Oak Avenue", 2345678901, "http://example.com", "2024-08-01", 2, "5")
    ]
    c.executemany("""
        INSERT INTO donationrecordd (name, address, phone_number, maps, date_of_requirement, time, quantity) 
        VALUES (?, ?, ?, ?, ?, ?, ?)
    """, donation_requests)

    donation_details = [
        ("John Doe", 1234567890, "Alice Johnson", 3456789012, "10"),
        ("Jane Smith", 2345678901, "Bob", 4567890123, "5")
    ]
    c.executemany("""
        INSERT INTO donationdetail (donor_name, donor_phone, recipient_name, recipient_phone, quantity) 
        VALUES (?, ?, ?, ?, ?)
    """, donation_details)

create_tables()
insert_sample_data()

conn.commit()
conn.close()

print("Database created and populated with sample data successfully.")
