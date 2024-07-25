import streamlit as st
import sqlite3
import pandas as pd
from PIL import Image
import datetime
import re

# Database setup
conn = sqlite3.connect("maso_data.db")
c = conn.cursor()

def create_tables():
    c.execute("CREATE TABLE IF NOT EXISTS users (username TEXT PRIMARY KEY, password TEXT)")
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

create_tables()

# Helper functions
def validate_password(password):
    return len(password) >= 8

def validate_link(address):
    pattern = r"^(https?://)?[\w.-]+\.[a-zA-Z]{2,}(?:/[\w.-]*)*/?$"
    return re.match(pattern, address) is not None

def validate_phone_number(phone):
    return phone.isdigit() and len(phone) == 10

def validate_quantity(value):
    return value.isdigit()

def check_user(username, password):
    c.execute("SELECT * FROM users WHERE username = ? AND password = ?", (username, password))
    return c.fetchone() is not None

def add_user(username, password):
    c.execute("INSERT INTO users (username, password) VALUES (?, ?)", (username, password))
    conn.commit()

def app():
    st.title("MASO - The Food & Waste Management System")

    st.image("image_files/DT_G62_Food-drink-Animated-GIF-Icon-Pack.webp", caption="Welcome to the App!")




    if "username" not in st.session_state:
        st.session_state.username = None

    if st.session_state.username:
        st.sidebar.write(f"Welcome, {st.session_state.username}!")
        if st.sidebar.button("Logout"):
            st.session_state.username = None
            st.rerun()

    else:


        menu = st.sidebar.radio("Select Option", ["Login", "Sign Up"])

        if menu == "Login":
            username = st.sidebar.text_input("Username", "")
            password = st.sidebar.text_input("Password", type="password")
            if st.sidebar.button("Login"):
                if check_user(username, password):
                    st.session_state.username = username
                    st.sidebar.success("Logged in successfully!")
                    st.rerun()
                else:
                    st.sidebar.error("Invalid username or password")

        elif menu == "Sign Up":
            username = st.sidebar.text_input("Username", "")
            password = st.sidebar.text_input("Password", type="password")
            confirm_password = st.sidebar.text_input("Confirm Password", type="password")
            if st.sidebar.button("Sign Up"):
                if password == confirm_password and validate_password(password):
                    add_user(username, password)
                    st.sidebar.success("User created successfully!")
                else:
                    st.sidebar.error("Passwords do not match or invalid password length")

    if st.session_state.username:
        option = st.selectbox("Select Option", ["Excess Food Management", "Food Waste", "Donation Request", "Donation Order"])

        if option == "Excess Food Management":
            st.subheader("Excess Food Management")
            name = st.text_input("Name")
            address = st.text_input("Address")
            phone_number = st.text_input("Phone Number")
            maps = st.text_input("Share Location (Link)")
            food_name = st.text_input("Food Name")
            quantity = st.text_input("Quantity")
            available_time = st.text_input("Available Time")
            date = datetime.date.today().strftime("%d/%m/%Y")

            if st.button("Save Food Record"):
                if validate_phone_number(phone_number) and validate_link(maps) and validate_quantity(quantity):
                    id = c.execute("SELECT MAX(id) FROM foodrecordd").fetchone()[0] or 0 + 1
                    c.execute("""
                        INSERT INTO foodrecordd (id, name, address, phone_number, maps, food_name, quantity, date, available_time) 
                        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
                    """, (id, name, address, phone_number, maps, food_name, int(quantity), date, available_time))
                    conn.commit()
                    st.success("Food record saved successfully!")
                else:
                    st.error("Please provide valid input.")

        elif option == "Food Waste":
            st.subheader("Food Waste Management")
            name = st.text_input("Name")
            address = st.text_input("Address")
            phone_number = st.text_input("Phone Number")
            maps = st.text_input("Share Location (Link)")
            waste_type = "Food"
            quantity = st.text_input("Quantity")
            reusable = st.selectbox("Reusable", ["Yes", "No"])
            date = datetime.date.today().strftime("%d/%m/%Y")

            if st.button("Save Waste Record"):
                if validate_phone_number(phone_number) and validate_link(maps) and validate_quantity(quantity):
                    id = c.execute("SELECT MAX(id) FROM wasterecordd").fetchone()[0] or 0 + 1
                    c.execute("""
                        INSERT INTO wasterecordd (id, name, address, phone_number, maps, waste_type, quantity, reusable, date) 
                        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
                    """, (id, name, address, phone_number, maps, waste_type, int(quantity), reusable, date))
                    conn.commit()
                    st.success("Waste record saved successfully!")
                else:
                    st.error("Please provide valid input.")

        elif option == "Donation Request":
            st.subheader("Donation Request")
            name = st.text_input("Name")
            address = st.text_input("Address")
            phone_number = st.text_input("Phone Number")
            maps = st.text_input("Share Location (Link)")
            date_of_requirement = st.text_input("Date of Requirement (dd-mm-yyyy)")
            time_options = {1: "Breakfast", 2: "Lunch", 3: "Dinner"}
            time_val = st.selectbox("Time", options=list(time_options.values()))
            quantity = st.text_input("Quantity")

            if st.button("Save Donation Request"):
                if validate_phone_number(phone_number) and validate_link(maps) and validate_quantity(quantity):
                    id = c.execute("SELECT MAX(id) FROM donationrecordd").fetchone()[0] or 0 + 1
                    c.execute("""
                        INSERT INTO donationrecordd (id, name, address, phone_number, maps, date_of_requirement, time, quantity) 
                        VALUES (?, ?, ?, ?, ?, ?, ?, ?)
                    """, (id, name, address, phone_number, maps, date_of_requirement, list(time_options.keys())[list(time_options.values()).index(time_val)], quantity))
                    conn.commit()
                    st.success("Donation request saved successfully!")
                else:
                    st.error("Please provide valid input.")

        elif option == "Donation Order":
            st.subheader("Donation Orders")
            df = pd.read_sql_query("SELECT * FROM donationrecordd", conn)
            st.dataframe(df)

            st.subheader("Donation Detail")
            donor_name = st.text_input("Donor Name")
            donor_phone = st.text_input("Donor Phone Number")
            recipient_name = st.text_input("Recipient Name")
            recipient_phone = st.text_input("Recipient Phone Number")
            quantity = st.text_input("Quantity")

            if st.button("Save Donation Detail"):
                if validate_phone_number(donor_phone) and validate_phone_number(recipient_phone):
                    c.execute("""
                        INSERT INTO donationdetail (donor_name, donor_phone, recipient_name, recipient_phone, quantity) 
                        VALUES (?, ?, ?, ?, ?)
                    """, (donor_name, donor_phone, recipient_name, recipient_phone, quantity))
                    conn.commit()
                    st.success("Donation detail saved successfully!")
                else:
                    st.error("Please provide valid phone numbers.")

if __name__ == "__main__":
    app()
