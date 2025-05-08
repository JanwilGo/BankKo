import tkinter as tk
from tkinter import messagebox
import mysql.connector
import re
import bcrypt
import subprocess, sys

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
        subprocess.Popen([sys.executable, "login.py"])

    except mysql.connector.Error as err:
        messagebox.showerror("Database Error", f"Error: {err}")
    finally:
        cursor.close()
        conn.close()

# Go back to login
def go_to_login():
    root.destroy()
    import login  # Ensure login is imported after destroying the root window

# Center window
def center_window(window):
    window.update_idletasks()
    width = window.winfo_width()
    height = window.winfo_height()
    x = (window.winfo_screenwidth() // 2) - (width // 2)
    y = (window.winfo_screenheight() // 2) - (height // 2)
    window.geometry(f'{width}x{height}+{x}+{y}')

def on_enter(e):
    e.widget['background'] = '#2c3e50'

def on_leave(e):
    e.widget['background'] = '#34495e'

# UI setup
root = tk.Tk()
root.title("BanKo - Create Account")
root.geometry("500x650")
root.resizable(False, False)
root.configure(bg='#ffffff')
center_window(root)

# Custom title bar
bar = tk.Frame(root, bg='#34495e', height=30)
bar.pack(fill=tk.X)
bar.bind('<Button-1>', lambda e: root.focus_set())
bar.bind('<B1-Motion>', lambda e: root.geometry(f'+{e.x_root}+{e.y_root}'))

# Add back arrow button to the left
back_btn = tk.Button(bar, text='←', font=('Arial', 13), bg='#34495e', fg='white', bd=0, padx=10, command=root.destroy)
back_btn.pack(side=tk.LEFT)
back_btn.bind('<Enter>', lambda e: back_btn.configure(bg='#e0e0e0', fg='#34495e'))
back_btn.bind('<Leave>', lambda e: back_btn.configure(bg='#34495e', fg='white'))

close_btn = tk.Button(bar, text='×', font=('Arial', 13), bg='#34495e', fg='white', bd=0, padx=10, command=root.destroy)
close_btn.pack(side=tk.RIGHT)
close_btn.bind('<Enter>', lambda e: close_btn.configure(bg='#e74c3c'))
close_btn.bind('<Leave>', lambda e: close_btn.configure(bg='#34495e'))

# --- Scrollable content setup ---
scrollable_container = tk.Frame(root, bg='#ffffff')
scrollable_container.pack(side=tk.TOP, fill=tk.BOTH, expand=True)

canvas = tk.Canvas(scrollable_container, bg='#ffffff', highlightthickness=0, width=440)
canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

scrollbar = tk.Scrollbar(scrollable_container, orient="vertical", command=canvas.yview)
scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

canvas.configure(yscrollcommand=scrollbar.set)
canvas.bind('<Configure>', lambda e: canvas.configure(scrollregion=canvas.bbox('all')))

content = tk.Frame(canvas, bg='#ffffff', padx=20, pady=20)
canvas.create_window((0, 0), window=content, anchor='nw', width=440)

# Title
tk.Label(content, text="Create Your BanKo Account", font=("Helvetica", 20, "bold"), fg="#34495e", bg="#ffffff").pack(pady=(0, 20))

def labeled_entry(parent, label, show=None, height=1):
    field_frame = tk.Frame(parent, bg="#f8f9fa", bd=0, highlightbackground="#bdc3c7", highlightthickness=1)
    field_frame.pack(fill=tk.X, pady=6, padx=2, expand=True)
    label_widget = tk.Label(field_frame, text=label, font=("Helvetica", 10), bg="#f8f9fa", fg="#7f8c8d", anchor="w")
    label_widget.pack(anchor="w", padx=8, pady=(6, 0))
    if height == 1:
        entry_widget = tk.Entry(field_frame, font=("Helvetica", 12), show=show, bg="white", relief=tk.FLAT, width=60, bd=0)
        entry_widget.pack(padx=8, pady=(2, 8), fill=tk.X)
        return entry_widget
    else:
        entry_widget = tk.Text(field_frame, font=("Helvetica", 12), height=height, bg="white", relief=tk.FLAT, width=60, bd=0)
        entry_widget.pack(padx=8, pady=(2, 8), fill=tk.X)
        return entry_widget

entry_fname = labeled_entry(content, "First Name *")
entry_mi = labeled_entry(content, "Middle Initial")
entry_lname = labeled_entry(content, "Family Name *")
entry_email = labeled_entry(content, "Email Address *")
entry_password = labeled_entry(content, "Password *", show="*")
entry_confirm_password = labeled_entry(content, "Confirm Password *", show="*")
entry_address = labeled_entry(content, "Address *", height=3)
entry_phone = labeled_entry(content, "Phone Number *")

register_button = tk.Button(content, text="Register", font=("Helvetica", 14, "bold"), bg="#34495e", fg="white",
                            command=register, relief=tk.FLAT, pady=10, bd=0)
register_button.pack(pady=20, fill=tk.X)
register_button.bind('<Enter>', on_enter)
register_button.bind('<Leave>', on_leave)

# --- Bottom frame for navigation and exit ---
bottom_frame = tk.Frame(root, bg="#ffffff", pady=10)
bottom_frame.pack(side=tk.BOTTOM, fill=tk.X)

login_button = tk.Button(bottom_frame, text="Already have an account? Login here", font=("Helvetica", 10),
                         bg="#ffffff", fg="#3498db", bd=0, command=go_to_login, cursor="hand2")
login_button.pack(fill=tk.X, pady=(0, 5))
login_button.bind('<Enter>', lambda e: login_button.configure(fg="#2980b9"))
login_button.bind('<Leave>', lambda e: login_button.configure(fg="#3498db"))

root.protocol("WM_DELETE_WINDOW", root.destroy)

# Enable mousewheel scrolling for the canvas
content.bind('<Enter>', lambda e: canvas.bind_all('<MouseWheel>', lambda event: canvas.yview_scroll(int(-1*(event.delta/120)), 'units')))
content.bind('<Leave>', lambda e: canvas.unbind_all('<MouseWheel>'))

if __name__ == "__main__":
    root.mainloop()