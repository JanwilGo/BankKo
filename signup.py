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
root.title("BanKo Create Account")
root.geometry("500x650")
root.resizable(False, False)
root.configure(bg='#ffffff')
# Remove or comment out overrideredirect(True) to keep the native window header
# root.overrideredirect(True)
center_window(root)

# Custom title bar
header = tk.Frame(root, bg='#34495e', height=30)
header.pack(fill=tk.X)
header.bind('<Button-1>', lambda e: root.focus_set())
header.bind('<B1-Motion>', lambda e: root.geometry(f'+{e.x_root}+{e.y_root}'))
# Back button in title bar
back_btn = tk.Button(header, text='←', font=('Arial', 13), bg='#34495e', fg='white', bd=0, padx=10, command=go_to_login)
back_btn.pack(side=tk.LEFT)
back_btn.bind('<Enter>', on_enter)
back_btn.bind('<Leave>', on_leave)

# Main content frame with scrolling
canvas = tk.Canvas(root, bg='#ffffff', highlightthickness=0)
scrollbar = tk.Scrollbar(root, orient="vertical", command=canvas.yview)
canvas.configure(yscrollcommand=scrollbar.set)
scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

content = tk.Frame(canvas, bg='#ffffff', padx=40, pady=30)
content_id = canvas.create_window((0, 0), window=content, anchor="nw")

def on_configure(event):
    canvas.configure(scrollregion=canvas.bbox('all'))
content.bind('<Configure>', on_configure)

def on_canvas_configure(event):
    canvas.itemconfig(content_id, width=event.width)
canvas.bind('<Configure>', on_canvas_configure)

def _on_mousewheel(event):
    canvas.yview_scroll(int(-1*(event.delta/120)), "units")
canvas.bind_all('<MouseWheel>', _on_mousewheel)

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

# Add the section header to the content area, centered and above the first name field
section_header = tk.Label(content, text="BanKo Create Account", font=("Helvetica", 20, "bold"), fg="#34495e", bg="#ffffff")
section_header.pack(pady=(0, 20))

entry_fname = labeled_entry(content, "First Name *")
entry_mi = labeled_entry(content, "Middle Initial")
entry_lname = labeled_entry(content, "Family Name *")
entry_email = labeled_entry(content, "Email Address *")
entry_password = labeled_entry(content, "Password *", show="*")
entry_confirm_password = labeled_entry(content, "Confirm Password *", show="*")
entry_address = labeled_entry(content, "Address *", height=3)
entry_phone = labeled_entry(content, "Phone Number *")

# Add 'Already have an account? Log in' link above the Create Account button
link_frame = tk.Frame(content, bg="#ffffff")
link_frame.pack(pady=(10, 0), fill=tk.X)
link_label = tk.Label(link_frame, text="Already have an account? ", font=("Helvetica", 10), bg="#ffffff", fg="#7f8c8d")
link_label.pack(side=tk.LEFT)
login_link = tk.Label(link_frame, text="Log in", font=("Helvetica", 10, "underline"), fg="#2f80ed", bg="#ffffff", cursor="hand2")
login_link.pack(side=tk.LEFT)
login_link.bind("<Button-1>", lambda e: go_to_login())

register_button = tk.Button(content, text="Create Account", font=("Helvetica", 14, "bold"), bg="#34495e", fg="white",
                            command=register, relief=tk.FLAT, pady=10, bd=0, height=2)
register_button.pack(pady=20, fill=tk.X)
register_button.bind('<Enter>', on_enter)
register_button.bind('<Leave>', on_leave)

root.protocol("WM_DELETE_WINDOW", root.destroy)

if __name__ == "__main__":
    root.mainloop()