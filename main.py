import sqlite3
import os
import re
import tabulate
import datetime

conn = sqlite3.connect("maso_data.db")
c = conn.cursor()

# Create tables
c.execute("CREATE TABLE IF NOT EXISTS users (username TEXT, password TEXT)")
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

def sign_up():
    username = input("Username: ")
    password = input("Password: ")
    c.execute("INSERT INTO users VALUES (?, ?)", (username, password))
    conn.commit()
    print("Registered successfully")

def login():
    username = input("Username: ")
    password = input("Password: ")
    c.execute("SELECT * FROM users WHERE username = ? AND password = ?", (username, password))
    row = c.fetchone()
    if row:
        print("Login successful")
        return True
    else:
        print("Invalid username or password")
        return False

def clear():
    os.system("cls")

def generate_id(table_name):
    c.execute(f"SELECT MAX(id) FROM {table_name}")
    result = c.fetchone()
    if result[0]:
        return str(int(result[0]) + 1)
    return '1'

def get_user_input(prompt, validation_func):
    while True:
        value = input(prompt)
        if validation_func(value):
            return value
        else:
            print("Invalid input. Please enter a valid value.")

def validate_link(address):
    pattern = r"^(https?://)?[\w.-]+\.[a-zA-Z]{2,}(?:/[\w.-]*)*/?$"
    return re.match(pattern, address) is not None

def food_name():
    return get_user_input("Food name: ", lambda name: re.match(r'^[a-zA-Z0-9\s]+$', name) is not None)

def food_quantity():
    while True:
        try:
            return int(input("Quantity: "))
        except ValueError:
            print("Invalid input. Please enter a valid quantity.")

def date():
    return datetime.date.today().strftime("%d/%m/%Y")

def available_time():
    print("Note: Please specify the valid time range for the slot, indicating the 'from' and 'to' times.")
    return input("Slot time: ")

def table(data, headers):
    print(tabulate.tabulate([data], headers=headers, tablefmt="grid"))

def save_to_database(table_name, data):
    try:
        cursor = conn.cursor()
        placeholders = ", ".join(["?"] * len(data))
        cursor.execute(f"INSERT INTO {table_name} VALUES ({placeholders})", data)
        conn.commit()
        cursor.close()
        print("Data saved successfully!")
        return True
    except Exception as e:
        print(f"An error occurred while saving data: {str(e)}")
        return False

def display_table(table_name, headers):
    c.execute(f"SELECT * FROM {table_name}")
    rows = c.fetchall()
    table_data = [list(row) for row in rows]
    print(tabulate.tabulate(table_data, headers=headers, tablefmt="grid"))

def sign_up_login():
    while True:
        print("1. Sign Up")
        print("2. Login")
        choice = input("Choose an option (1-2): ")
        if choice == '1':
            sign_up()
        elif choice == '2':
            if login():
                return
        else:
            print("Invalid choice. Please try again.")

def excess_food_management():
    clear()
    print("------------------------------")
    print("| User details               |")
    print("------------------------------")
    id = generate_id("foodrecordd")
    name = get_user_input("Name: ", lambda x: x.replace(" ", "").isalnum())
    address = get_user_input("Address: ", lambda x: x.replace(" ", "").isalnum())
    phone_number = int(get_user_input("Phone number: ", lambda x: x.isdigit() and len(x) == 10))
    maps = get_user_input("Share location (link): ", validate_link)
    
    clear()
    print("------------------------------")
    print("| Food details               |")
    print("------------------------------")
    food_name_val = food_name()
    quantity = food_quantity()
    date_val = date()
    available_time_val = available_time()
    
    array1 = [id, name, address, phone_number, maps, food_name_val, quantity, date_val, available_time_val]
    headers = ['ID', 'Name', 'Address', 'Phone Number', 'Maps', 'Food Name', 'Quantity', 'Date', 'Available Time']
    table(array1, headers)
    
    choice = input("Make changes (Y/N): ")
    if choice.lower() == 'n':
        if save_to_database("foodrecordd", array1):
            print("Data saved successfully!")
    elif choice.lower() == 'y':
        # Handle changes if needed
        pass

def waste_quantity():
    while True:
        try:
            return int(input("Quantity: "))
        except ValueError:
            print("Invalid input. Please enter a valid quantity.")

def food_waste():
    clear()
    print("------------------------------")
    print("| User details               |")
    print("------------------------------")
    id = generate_id("wasterecordd")
    name = get_user_input("Name: ", lambda x: x.replace(" ", "").isalnum())
    address = get_user_input("Address: ", lambda x: x.replace(" ", "").isalnum())
    phone_number = int(get_user_input("Phone number: ", lambda x: x.isdigit() and len(x) == 10))
    maps = get_user_input("Share location (link): ", validate_link)
    
    clear()
    print("------------------------------")
    print("| Food waste                 |")
    print("------------------------------")
    waste_type = "Food"
    quantity = waste_quantity()
    reusable = input("Reusable (Yes/No): ")
    date_val = date()
    
    array = [id, name, address, phone_number, maps, waste_type, quantity, reusable, date_val]
    headers = ['ID', 'Name', 'Address', 'Phone Number', 'Map', 'Waste Type', 'Quantity', 'Reusable', 'Date']
    table(array, headers)
    
    choice = input("Make changes (Y/N): ")
    if choice.lower() == 'n':
        if save_to_database("wasterecordd", array):
            print("Request sent successfully. The authority will reach you soon.")
    elif choice.lower() == 'y':
        # Handle changes if needed
        pass

def donation_request():
    print("------------------------------")
    print("| User details               |")
    print("------------------------------")
    id = generate_id("donationrecordd")
    name = get_user_input("Name: ", lambda x: x.replace(" ", "").isalnum())
    address = get_user_input("Address: ", lambda x: x.replace(" ", "").isalnum())
    phone_number = int(get_user_input("Phone number: ", lambda x: x.isdigit() and len(x) == 10))
    maps = get_user_input("Share location (link): ", validate_link)
    
    print("------------------------------")
    print("| Pre-food request           |")
    print("------------------------------")
    date_val = input("Date of requirement (dd-mm-yyyy): ")
    time_options = {1: "Breakfast", 2: "Lunch", 3: "Dinner"}
    while True:
        time_choice = int(input("Select your choice (1-3): "))
        if time_choice in time_options:
            time_val = time_options[time_choice]
            break
        else:
            print("Invalid choice. Please try again.")
    
    quantity = food_quantity()
    
    array2 = [id, name, address, phone_number, maps, date_val, time_val, quantity]
    headers = ['ID', 'Name', 'Address', 'Phone Number', 'Map', 'Date of Requirement', 'Time', 'Quantity']
    table(array2, headers)
    
    choice = input("Make changes (Y/N): ")
    if choice.lower() == 'n':
        if save_to_database("donationrecordd", array2):
            print("Request sent successfully. Someone is waiting to see this.")
    elif choice.lower() == 'y':
        # Handle changes if needed
        pass

def donation_order():
    display_table("donationrecordd", ['ID', 'Name', 'Address', 'Phone Number', 'Map', 'Date of Requirement', 'Time', 'Quantity'])
    print("")
    while True:
        print("------------------------------")
        print("| Request details            |")
        print("------------------------------")
        donor_name = get_user_input("Donor name: ", lambda x: x.replace(" ", "").isalnum())
        donor_phone = int(get_user_input("Donor phone number: ", lambda x: x.isdigit() and len(x) == 10))
        recipient_name = get_user_input("Recipient name: ", lambda x: x.replace(" ", "").isalnum())
        recipient_phone = int(get_user_input("Recipient phone number: ", lambda x: x.isdigit() and len(x) == 10))
        quantity = input("Quantity: ")
        
        array3 = [donor_name, donor_phone, recipient_name, recipient_phone, quantity]
        headers = ['Donor Name', 'Donor Phone', 'Recipient Name', 'Recipient Phone', 'Quantity']
        table(array3, headers)
        
        choice = input("Make changes (Y/N): ")
        if choice.lower() == 'n':
            if save_to_database("donationdetail", array3):
                print("Donation detail saved successfully!")
        elif choice.lower() == 'y':
            # Handle changes if needed
            pass

def main():
    sign_up_login()
    while True:
        print("1. Excess Food Management")
        print("2. Food Waste")
        print("3. Donation Request")
        print("4. Donation Order")
        print("5. Exit")
        choice = input("Enter your choice (1-5): ")
        if choice == '1':
            excess_food_management()
        elif choice == '2':
            food_waste()
        elif choice == '3':
            donation_request()
        elif choice == '4':
            donation_order()
        elif choice == '5':
            conn.close()
            break
        else:
            print("Invalid choice. Please try again.")

if __name__ == "__main__":
    main()
