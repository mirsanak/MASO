# MASO - The Food & Waste Management System

## Deployed link - https://maso-b289.onrender.com , it may take up to 1 minute to load intially as it's deployed on a free service.

## Overview

MASO is a comprehensive system designed for managing excess food, food waste, donation requests, and donation orders. It provides a user-friendly interface through Streamlit for web-based interactions and a command-line interface (CLI) for terminal-based interactions.

## Features

- **User Authentication**: Secure login and registration.
- **Excess Food Management**: Track and manage excess food donations.
- **Food Waste Management**: Report and manage food waste.
- **Donation Requests**: Create and manage requests for food donations.
- **Donation Orders**: View and manage details of donation orders.

## Files

1. **`app.py`**: Streamlit-based web application interface.
2. **`main.py`**: Command-line interface for managing food records and user authentication.
3. **`create_dummy_db_with_data.py`**: Script to create and populate the SQLite database with sample data.

## Setup

### Prerequisites

- Python 3.x
- Required Python packages:
  - `streamlit`
  - `sqlite3` (part of the Python standard library)
  - `pandas`
  - `Pillow`

### Installation

1. **Clone the Repository**:

    ```bash
    git clone https://github.com/your-repo-url/maso.git
    cd maso
    ```

2. **Install Required Packages**:

    ```bash
    pip install streamlit pandas Pillow
    ```

3. **Create and Populate the Database**:

    Run the script to create the database and insert sample data:

    ```bash
    python create_dummy_db_with_data.py
    ```

### Running the Streamlit App

1. **Start the Streamlit App**:

    ```bash
    streamlit run app.py
    ```

2. **Access the App**:

    Open your web browser and go to `http://localhost:8501`.

### Running the CLI

1. **Run the Command-Line Interface**:

    ```bash
    python main.py
    ```

2. **Follow the Prompts**:

    Follow the on-screen prompts to interact with the CLI for user registration, login, and record management.

## Database Schema

- **users**: Table to store user credentials (username and password).
- **foodrecordd**: Table to manage excess food records.
- **wasterecordd**: Table to manage food waste records.
- **donationrecordd**: Table to manage donation requests.
- **donationdetail**: Table to manage details of donation orders.

## Functions

- **`validate_password(password)`**: Checks if the password meets the minimum length requirement.
- **`validate_link(address)`**: Validates if the provided URL is in a proper format.
- **`validate_phone_number(phone)`**: Checks if the phone number is a valid 10-digit number.
- **`validate_quantity(value)`**: Checks if the quantity is a valid integer.

## Contributions

Feel free to contribute to the project by opening issues or submitting pull requests.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Contact

For any queries, please contact [mirsanak.m12@gmail.com](mirsanak.m12@gmail.com).

