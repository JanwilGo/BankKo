import tkinter as tk
from tkinter import messagebox
import mysql.connector
import dashboard  # Import the dashboard module

# Function to create a database connection
def create_connection():
    return mysql.connector.connect(
        host="sql12.freesqldatabase.com",
        user="sql12770916",
        password="yvZr32MFBS",
        database="sql12770916",
        port=3306
    )

# Function to handle login
def login():
    username = entry_username.get()
    password = entry_password.get()

    conn = create_connection()
    cursor = conn.cursor()

    try:
        cursor.execute("SELECT * FROM users WHERE email = %s", (username,))
        user = cursor.fetchone()

        if user and user[3] == password:  # Assuming password is in the 4th column (index 3)
            messagebox.showinfo("Login Success", "Welcome to the Banking System!")
            root.destroy()  # Close login window
            dashboard.open_dashboard()  # Open dashboard
        else:
            messagebox.showerror("Login Failed", "Invalid username or password.")
    except mysql.connector.Error as err:
        messagebox.showerror("Database Error", f"Error: {err}")
    finally:
        cursor.close()
        conn.close()

# Initialize the main Tkinter window
root = tk.Tk()
root.title("Banking System Login")
root.geometry("350x250")
root.resizable(False, False)

# Username Label and Entry
tk.Label(root, text="Username (Email):", font=("Arial", 12)).pack(pady=5)
entry_username = tk.Entry(root, font=("Arial", 12))
entry_username.pack(pady=5)

# Password Label and Entry
tk.Label(root, text="Password:", font=("Arial", 12)).pack(pady=5)
entry_password = tk.Entry(root, show="*", font=("Arial", 12))
entry_password.pack(pady=5)

# Login Button
btn_login = tk.Button(root, text="Login", font=("Arial", 12, "bold"), bg="#3399ff", fg="white", command=login)
btn_login.pack(pady=10)

# Run Tkinter main loop
root.mainloop()
