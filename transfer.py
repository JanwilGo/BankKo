import tkinter as tk
from tkinter import messagebox
import mysql.connector

# Database configuration
DB_CONFIG = {
    'host': 'sql12.freesqldatabase.com',
    'user': 'sql12773881',
    'password': 'isUcpBumwQ',
    'database': 'sql12773881',
    'port': 3306
}

# Function to center window on screen
def center_window(window):
    window.update_idletasks()
    width = window.winfo_width()
    height = window.winfo_height()
    x = (window.winfo_screenwidth() // 2) - (width // 2)
    y = (window.winfo_screenheight() // 2) - (height // 2)
    window.geometry(f'{width}x{height}+{x}+{y}')

# Function to handle button hover effects
def on_enter(e):
    e.widget['background'] = '#2c3e50'

def on_leave(e):
    e.widget['background'] = '#34495e'

def transfer_funds(sender_id, recipient_email, amount, balance_label):
    try:
        amount = float(amount)
        if amount <= 0:
            messagebox.showerror("Error", "Transfer amount must be positive.")
            return
        conn = mysql.connector.connect(**DB_CONFIG)
        cursor = conn.cursor()
        # Get recipient user_id
        cursor.execute("SELECT user_id FROM users WHERE email = %s", (recipient_email,))
        recipient = cursor.fetchone()
        if not recipient:
            messagebox.showerror("Error", "Recipient not found.")
            return
        recipient_id = recipient[0]
        if recipient_id == sender_id:
            messagebox.showerror("Error", "Cannot transfer to yourself.")
            return
        # Check sender balance
        cursor.execute("SELECT balance FROM users WHERE user_id = %s", (sender_id,))
        sender_balance = cursor.fetchone()[0]
        if sender_balance < amount:
            messagebox.showerror("Error", "Insufficient funds.")
            return
        # Perform transfer
        cursor.execute("UPDATE users SET balance = balance - %s WHERE user_id = %s", (amount, sender_id))
        cursor.execute("UPDATE users SET balance = balance + %s WHERE user_id = %s", (amount, recipient_id))
        # Log transaction (only once, for sender)
        cursor.execute("""
            INSERT INTO transactions (user_id, type, amount, recipient_id) VALUES (%s, 'transfer', %s, %s)
        """, (sender_id, amount, recipient_id))
        conn.commit()
        # Update balance label
        # balance_label["text"] = f"₱{new_balance:,.2f}"
    except ValueError:
        messagebox.showerror("Error", "Invalid amount entered.")
    except mysql.connector.Error as err:
        messagebox.showerror("Database Error", f"Error: {err}")
    finally:
        if 'cursor' in locals():
            cursor.close()
        if 'conn' in locals() and conn.is_connected():
            conn.close()

def open_transfer_window(user_id, balance_label, first_name, back_func):
    transfer_window = tk.Toplevel()
    transfer_window.title("Transfer Funds")
    transfer_window.geometry("400x500")
    transfer_window.configure(bg='#ffffff')
    transfer_window.attributes('-toolwindow', True)  # Minimal title bar (Windows only)
    center_window(transfer_window)

    # Title bar
    title_bar = tk.Frame(transfer_window, bg='#34495e', height=30)
    title_bar.pack(fill=tk.X)
    title_bar.bind('<Button-1>', lambda e: transfer_window.focus_set())
    title_bar.bind('<B1-Motion>', lambda e: transfer_window.geometry(f'+{e.x_root}+{e.y_root}'))

    # Back button
    back_btn = tk.Button(title_bar, text='←', font=('Arial', 13), bg='#34495e', fg='white', bd=0, padx=10, command=lambda: [transfer_window.destroy(), back_func()])
    back_btn.pack(side=tk.LEFT)
    back_btn.bind('<Enter>', on_enter)
    back_btn.bind('<Leave>', on_leave)

    # Content
    content = tk.Frame(transfer_window, bg='#ffffff', padx=40, pady=30)
    content.pack(fill=tk.BOTH, expand=True)

    # Title
    tk.Label(
        content,
        text="Transfer Money",
        font=("Helvetica", 24, "bold"),
        fg="#34495e",
        bg="#ffffff"
    ).pack(pady=(0, 30))

    # Recipient Email
    tk.Label(
        content,
        text="Recipient Email",
        font=("Helvetica", 10),
        fg="#7f8c8d",
        bg="#ffffff"
    ).pack(anchor="w")

    email_entry = tk.Entry(
        content,
        font=("Helvetica", 12),
        bd=0,
        highlightthickness=1,
        highlightbackground="#bdc3c7",
        highlightcolor="#3498db"
    )
    email_entry.pack(pady=(5, 20), fill=tk.X)

    # Amount
    tk.Label(
        content,
        text="Amount to Transfer",
        font=("Helvetica", 10),
        fg="#7f8c8d",
        bg="#ffffff"
    ).pack(anchor="w")

    amount_entry = tk.Entry(
        content,
        font=("Helvetica", 12),
        bd=0,
        highlightthickness=1,
        highlightbackground="#bdc3c7",
        highlightcolor="#3498db"
    )
    amount_entry.pack(pady=(5, 20), fill=tk.X)

    # Transfer button
    transfer_button = tk.Button(
        content,
        text="Transfer",
        command=lambda: [transfer_funds(user_id, email_entry.get().strip(), amount_entry.get().strip(), balance_label), transfer_window.destroy(), back_func()],
        bg="#34495e",
        fg="white",
        font=("Helvetica", 12),
        bd=0,
        padx=20,
        pady=10,
        cursor="hand2"
    )
    transfer_button.pack(fill=tk.X, pady=(20, 0))
    transfer_button.bind('<Enter>', on_enter)
    transfer_button.bind('<Leave>', on_leave)
