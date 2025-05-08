import tkinter as tk
from tkinter import messagebox
import mysql.connector
import dashboard  # Import the dashboard module
import bcrypt

# Function to center window on screen
def center_window(window):
    window.update_idletasks()
    width = window.winfo_width()
    height = window.winfo_height()
    x = (window.winfo_screenwidth() // 2) - (width // 2)
    y = (window.winfo_screenheight() // 2) - (height // 2)
    window.geometry(f'{width}x{height}+{x}+{y}')

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

        if user and bcrypt.checkpw(password.encode('utf-8'), user[5].encode('utf-8')):  # user[5] is password_hash
            # messagebox.showinfo("Login Success", "Welcome to the Banking System!")
            root.withdraw()  # Hide login window
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
    # messagebox.showinfo("Signup", "Redirecting to signup window...")
    root.withdraw()
    import signup  # You should have a signup.py file

# Function to handle button hover effects
def on_enter(e):
    e.widget['background'] = '#2c3e50'

def on_leave(e):
    e.widget['background'] = '#34495e'

# Initialize the main Tkinter window
root = tk.Tk()
root.title("BanKo Login")
root.geometry("400x500")
root.resizable(False, False)
root.configure(bg='#ffffff')
root.attributes('-toolwindow', True)  # Minimal title bar (Windows only)
center_window(root)
# root.overrideredirect(True)  # Removed to restore normal window behavior

# Create a frame for dragging the window
title_bar = tk.Frame(root, bg='#34495e', height=30)
title_bar.pack(fill=tk.X)
title_bar.bind('<Button-1>', lambda e: root.focus_set())
title_bar.bind('<B1-Motion>', lambda e: root.geometry(f'+{e.x_root}+{e.y_root}'))

# Close button
close_btn = tk.Button(title_bar, text='×', font=('Arial', 13), bg='#34495e', fg='white',
                     bd=0, padx=10, command=root.destroy)
close_btn.pack(side=tk.RIGHT)
close_btn.bind('<Enter>', lambda e: close_btn.configure(bg='#e74c3c'))
close_btn.bind('<Leave>', lambda e: close_btn.configure(bg='#34495e'))

# Main content frame
content = tk.Frame(root, bg='#ffffff', padx=40, pady=30)
content.pack(fill=tk.BOTH, expand=True)

# Logo/Title
title_label = tk.Label(
    content,
    text="BanKo",
    font=("Helvetica", 24, "bold"),
    fg="#34495e",
    bg="#ffffff"
)
title_label.pack(pady=(0, 30))

# Username
tk.Label(content, text="Email", font=("Helvetica", 10), bg="#ffffff", fg="#7f8c8d").pack(anchor="w")
entry_username = tk.Entry(content, font=("Helvetica", 12), bd=0, highlightthickness=1,
                         highlightbackground="#bdc3c7", highlightcolor="#3498db")
entry_username.pack(pady=(5, 20), fill=tk.X)

# Password
tk.Label(content, text="Password", font=("Helvetica", 10), bg="#ffffff", fg="#7f8c8d").pack(anchor="w")
entry_password = tk.Entry(content, show="•", font=("Helvetica", 12), bd=0, highlightthickness=1,
                         highlightbackground="#bdc3c7", highlightcolor="#3498db")
entry_password.pack(pady=(5, 20), fill=tk.X)

# Buttons Frame
button_frame = tk.Frame(content, bg="#ffffff")
button_frame.pack(pady=20, fill=tk.X)

# Login button
btn_login = tk.Button(
    button_frame,
    text="Login",
    font=("Helvetica", 12),
    bg="#34495e",
    fg="white",
    bd=0,
    padx=20,
    pady=10,
    cursor="hand2",
    command=login
)
btn_login.pack(fill=tk.X, pady=(0, 10))
btn_login.bind('<Enter>', on_enter)
btn_login.bind('<Leave>', on_leave)

# Sign Up button
btn_signup = tk.Button(
    button_frame,
    text="Create Account",
    font=("Helvetica", 12),
    bg="#34495e",
    fg="white",
    bd=0,
    padx=20,
    pady=10,
    cursor="hand2",
    command=signup
)
btn_signup.pack(fill=tk.X)
btn_signup.bind('<Enter>', on_enter)
btn_signup.bind('<Leave>', on_leave)

# Run Tkinter main loop
root.mainloop()
root.protocol("WM_DELETE_WINDOW", root.destroy)
