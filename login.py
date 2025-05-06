import tkinter as tk
from tkinter import messagebox
import mysql.connector
import dashboard  # Import the dashboard module

# Function to create a database connection
def create_connection():
    return mysql.connector.connect(
        host="sql12.freesqldatabase.com",
        user="sql12773881",
        password="isUcpBumwQ",
        database="sql12773881",
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

        if user and user[5] == password:  # Assuming password is in the 6th column (index 5)
            messagebox.showinfo("Login Success", "Welcome to the Banking System!")
            root.destroy()  # Close login window
            dashboard.open_dashboard(user[1], user[0])  # Pass first name and user_id (assuming user_id is in index 0)
        else:
            messagebox.showerror("Login Failed", "Invalid username or password.")
    except mysql.connector.Error as err:
        messagebox.showerror("Database Error", f"Error: {err}")
    finally:
        cursor.close()
        conn.close()

# Function to handle signup
def signup():
    messagebox.showinfo("Signup", "Redirecting to signup window...")
    root.destroy()
    import signup  # You should have a signup.py file

# Initialize the main Tkinter window
root = tk.Tk()
root.title("BankKo Login")
root.geometry("400x300")
root.resizable(False, False)

# Header Section
header = tk.Frame(root, bg="#2f80ed", padx=20, pady=15)
header.pack(fill=tk.X)

header_label = tk.Label(
    header,
    text="Welcome to BankKo",
    font=("Arial", 16, "bold"),
    fg="white",
    bg="#2f80ed"
)
header_label.pack()

# Content Section
content = tk.Frame(root, bg="#f0f2f5", padx=20, pady=20)
content.pack(fill=tk.BOTH, expand=True)

# Username
tk.Label(content, text="Username (Email):", font=("Arial", 12), bg="#f0f2f5").pack(pady=5, anchor="w")
entry_username = tk.Entry(content, font=("Arial", 12))
entry_username.pack(pady=5, fill=tk.X)

# Password
tk.Label(content, text="Password:", font=("Arial", 12), bg="#f0f2f5").pack(pady=5, anchor="w")
entry_password = tk.Entry(content, show="*", font=("Arial", 12))
entry_password.pack(pady=5, fill=tk.X)

# Buttons Frame
button_frame = tk.Frame(content, bg="#f0f2f5")
button_frame.pack(pady=15, fill=tk.X)

btn_login = tk.Button(
    button_frame,
    text="Login",
    font=("Arial", 12, "bold"),
    bg="#2f80ed",
    fg="white",
    padx=10,
    pady=8,
    relief=tk.FLAT,
    command=login
)
btn_login.pack(side=tk.LEFT, expand=True, fill=tk.X, padx=5)

btn_signup = tk.Button(
    button_frame,
    text="Sign Up",
    font=("Helvetica", 12, "bold"),
    bg="#4CAF50",
    fg="white",
    padx=10,
    pady=8,
    relief=tk.FLAT,
    command=signup
)
btn_signup.pack(side=tk.LEFT, expand=True, fill=tk.X, padx=5)

# Run Tkinter main loop
root.mainloop()
