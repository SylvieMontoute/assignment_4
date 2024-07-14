import mysql.connector
import re

class AppointmentSystem:
    def __init__(self):
        self.db = mysql.connector.connect(
            host="localhost",
            user="root",
            password="Berklin21",
            database="appointment_system"
        )
        self.cursor = self.db.cursor()
        self.available_dates = ["2024-01-15", "2024-02-20", "2024-03-10"]

    def sanitize_input(self, email, password):
        email = email.strip().lower()
        password = password.strip()
        if not re.match(r"[^@]+@[^@]+\.[^@]+", email):
            raise ValueError("Invalid email address")
        return email, password

    def signup_input(self):
        email = input("Enter your email: ")
        confirm_email = input("Confirm your email: ")
        password = input("Enter your password: ")
        confirm_password = input("Confirm your password: ")
        
        if email != confirm_email:
            return "Emails do not match"
        if password != confirm_password:
            return "Passwords do not match"

        email, password = self.sanitize_input(email, password)
        
        # Check if email already exists
        self.cursor.execute("SELECT * FROM users WHERE email=%s", (email,))
        if self.cursor.fetchone():
            return "Email already registered"
        
        # Insert into users table
        self.cursor.execute("INSERT INTO users (email, password) VALUES (%s, %s)", (email, password))
        self.db.commit()
        return "Signup successful!"

    def login_auth(self, email, password):
        email, password = self.sanitize_input(email, password)
        self.cursor.execute("SELECT * FROM users WHERE email=%s AND password=%s", (email, password))
        return self.cursor.fetchone() is not None

    def book_appointment(self, email, selected_date):
        if selected_date not in self.available_dates:
            return "Selected date is not available"
        
        # Insert into appointments table
        self.cursor.execute("INSERT INTO appointments (email, appointment_date) VALUES (%s, %s)", (email, selected_date))
        self.db.commit()
        return f"Appointment booked for {selected_date}"

    def user_appointments(self, email):
        self.cursor.execute("SELECT appointment_date FROM appointments WHERE email=%s", (email,))
        appointments = self.cursor.fetchall()
        return [appointment[0].strftime('%Y-%m-%d') for appointment in appointments]

    def update_appointment(self, email, old_date, new_date):
        if new_date not in self.available_dates:
            return "New date is not available"
        
        # Update appointment in appointments table
        self.cursor.execute("UPDATE appointments SET appointment_date=%s WHERE email=%s AND appointment_date=%s", (new_date, email, old_date))
        self.db.commit()
        return f"Appointment updated to {new_date}"

    def __iter__(self):
        self._iterator_index = 0
        return self

    def __next__(self):
        if self._iterator_index < len(self.available_dates):
            result = self.available_dates[self._iterator_index]
            self._iterator_index += 1
            return result
        else:
            raise StopIteration
        
# Example usage
system = AppointmentSystem()

# Sign up process
print(system.signup_input())

# Log in process
email = input("Enter your email: ")
password = input("Enter your password: ")
if system.login_auth(email, password):
    print("Login successful!")
else:
    print("Login failed!")

# Book appointment
selected_date = input("Enter the date you want to book (YYYY-MM-DD): ")
print(system.book_appointment(email, selected_date))

# View appointments
print("Your appointments: ", system.user_appointments(email))

# Update appointment
old_date = input("Enter the date you want to update (YYYY-MM-DD): ")
new_date = input("Enter the new date you want to book (YYYY-MM-DD): ")
print(system.update_appointment(email, old_date, new_date))

