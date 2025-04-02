import tkinter as tk
from tkinter import messagebox
import dashboard  # Import dashboard module

def login():
    username = entry_username.get()
    password = entry_password.get()
    
    # Hardcoded credentials (Replace with DB check in real application)
    if username == "admin" and password == "password":
        messagebox.showinfo("Login Success", "Welcome to the Banking System!")
        root.destroy()  # Close login window
        dashboard.open_dashboard()  # Open dashboard
    else:
        messagebox.showerror("Login Failed", "Invalid username or password.")

# Initialize main window
root = tk.Tk()
root.title("Banking System Login")
root.geometry("300x200")

# Username Label and Entry
label_username = tk.Label(root, text="Username:")
label_username.pack(pady=5)
entry_username = tk.Entry(root)
entry_username.pack(pady=5)

# Password Label and Entry
label_password = tk.Label(root, text="Password:")
label_password.pack(pady=5)
entry_password = tk.Entry(root, show="*")
entry_password.pack(pady=5)

# Login Button
btn_login = tk.Button(root, text="Login", command=login)
btn_login.pack(pady=10)

# Run the Tkinter event loop
root.mainloop()
