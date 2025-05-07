import tkinter as tk
from tkinter import messagebox
import mysql.connector
import re
import bcrypt

# DB connection
def create_connection():
    return mysql.connector.connect(
        host="sql12.freesqldatabase.com",
        user="sql12773881",
        password="isUcpBumwQ",
        database="sql12773881",
        port=3306
    )

# Handle registration
def register():
    fname = entry_fname.get().strip()
    minitial = entry_mi.get().strip()
    lname = entry_lname.get().strip()
    email = entry_email.get().strip()
    password = entry_password.get()
    confirm_password = entry_confirm_password.get()
    address = entry_address.get("1.0", tk.END).strip()
    phone = entry_phone.get().strip()

    if not all([fname, lname, email, password, confirm_password, address, phone]):
        messagebox.showerror("Input Error", "All required fields must be filled.")
        return

    if password != confirm_password:
        messagebox.showerror("Password Error", "Passwords do not match.")
        return

    if not re.match(r"[^@]+@[^@]+\.[^@]+", email):
        messagebox.showerror("Email Error", "Invalid email format.")
        return

    if not phone.isdigit() or len(phone) < 7:
        messagebox.showerror("Phone Error", "Invalid phone number.")
        return

    conn = create_connection()
    cursor = conn.cursor()

    try:
        cursor.execute("SELECT * FROM users WHERE email = %s OR phone_number = %s", (email, phone))
        if cursor.fetchone():
            messagebox.showerror("Duplicate", "Email or phone already registered.")
            return

        # Hash the password
        hashed_pw = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')

        cursor.execute(""" 
            INSERT INTO users 
            (first_name, middle_initial, family_name, email, password_hash, address, phone_number) 
            VALUES (%s, %s, %s, %s, %s, %s, %s)
        """, (fname, minitial, lname, email, hashed_pw, address, phone))

        conn.commit()
        messagebox.showinfo("Success", "Account created successfully!")
        root.destroy()
        import login  # After success, go back to the login page

    except mysql.connector.Error as err:
        messagebox.showerror("Database Error", f"Error: {err}")
    finally:
        cursor.close()
        conn.close()

# Go back to login
def go_to_login():
    root.destroy()
    import login  # Ensure login is imported after destroying the root window

# UI setup
root = tk.Tk()
root.title("BankKo - Create Account")
root.geometry("500x600")
root.resizable(True, True)  # Allow resizing the window

# Create a frame for the header
header_frame = tk.Frame(root, bg="#2f80ed", pady=20)
header_frame.pack(fill=tk.X)

# Create the header label
tk.Label(header_frame, text="Create Your BankKo Account", font=("Arial", 16, "bold"),
         fg="white", bg="#2f80ed").pack()

# Create a Canvas to hold the content and allow scrolling
canvas = tk.Canvas(root)
canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

# Add a vertical scrollbar linked to the canvas
scrollbar = tk.Scrollbar(root, orient="vertical", command=canvas.yview)
scrollbar.pack(side=tk.RIGHT, fill="y")
canvas.configure(yscrollcommand=scrollbar.set)

# Create a frame inside the canvas to hold the widgets
content_frame = tk.Frame(canvas, bg="#f0f2f5", padx=20, pady=20)
canvas.create_window((0, 0), window=content_frame, anchor="nw")

# Update the scroll region of the canvas whenever the content frame is resized
content_frame.bind("<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("all")))

# Label and entry helper function
def labeled_entry(parent, label, show=None, height=1):
    label_widget = tk.Label(parent, text=label, font=("Arial", 12), bg="#f0f2f5")
    label_widget.pack(pady=(10, 0), anchor="w")
    
    if height == 1:
        entry_widget = tk.Entry(parent, font=("Arial", 12), show=show) if show else tk.Entry(parent, font=("Arial", 12))
        entry_widget.pack(fill=tk.X, pady=5)
        return entry_widget
    else:
        entry_widget = tk.Text(parent, font=("Arial", 12), height=height)
        entry_widget.pack(fill=tk.X, pady=5)
        return entry_widget

# Call labeled_entry for each field
entry_fname = labeled_entry(content_frame, "First Name *")
entry_mi = labeled_entry(content_frame, "Middle Initial")
entry_lname = labeled_entry(content_frame, "Family Name *")
entry_email = labeled_entry(content_frame, "Email Address *")
entry_password = labeled_entry(content_frame, "Password *", show="*")
entry_confirm_password = labeled_entry(content_frame, "Confirm Password *", show="*")
entry_address = labeled_entry(content_frame, "Address *", height=3)
entry_phone = labeled_entry(content_frame, "Phone Number *")

# Register button
register_button = tk.Button(content_frame, text="Register", font=("Arial", 14, "bold"), bg="#2f80ed", fg="white",
                            command=register, relief=tk.FLAT, pady=10)
register_button.pack(pady=20)

# Already have an account button
login_button = tk.Button(content_frame, text="Already have an account? Login here", font=("Arial", 10),
                         bg="#f0f2f5", fg="#2f80ed", bd=0, command=go_to_login, cursor="hand2")
login_button.pack()

# 🔐 Ensure launch from subprocess
def on_mouse_wheel(event):
    canvas.yview_scroll(int(-1*(event.delta/120)), "units")

# Bind mouse scroll event to the canvas
root.bind_all("<MouseWheel>", on_mouse_wheel)

if __name__ == "__main__":
    root.mainloop()