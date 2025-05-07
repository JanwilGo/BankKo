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
        # Log transactions
        cursor.execute("""
            INSERT INTO transactions (user_id, type, amount, recipient_id) VALUES (%s, 'transfer', %s, %s)
        """, (sender_id, amount, recipient_id))
        cursor.execute("""
            INSERT INTO transactions (user_id, type, amount, recipient_id) VALUES (%s, 'transfer', %s, %s)
        """, (recipient_id, amount, sender_id))
        conn.commit()
        # Update balance label
        cursor.execute("SELECT balance FROM users WHERE user_id = %s", (sender_id,))
        new_balance = cursor.fetchone()[0]
        balance_label["text"] = f"₱{new_balance:,.2f}"
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
    transfer_window.geometry("400x300")
    back_btn = tk.Button(transfer_window, text="Back", command=lambda: [transfer_window.destroy(), back_func()], bg="#2f80ed", fg="white", font=("Arial", 10, "bold"))
    back_btn.pack(anchor="nw", padx=10, pady=10)
    tk.Label(transfer_window, text="Recipient Email:", font=("Arial", 14)).pack(pady=10)
    email_entry = tk.Entry(transfer_window, font=("Arial", 14))
    email_entry.pack(pady=5)
    tk.Label(transfer_window, text="Amount to Transfer:", font=("Arial", 14)).pack(pady=10)
    amount_entry = tk.Entry(transfer_window, font=("Arial", 14))
    amount_entry.pack(pady=5)
    def handle_transfer():
        recipient_email = email_entry.get().strip()
        amount = amount_entry.get().strip()
        transfer_funds(user_id, recipient_email, amount, balance_label)
        transfer_window.destroy()
        from dashboard import open_dashboard
        open_dashboard(first_name, user_id)
    transfer_btn = tk.Button(transfer_window, text="Transfer", command=handle_transfer, bg="#2f80ed", fg="white", font=("Arial", 16, "bold"))
    transfer_btn.pack(pady=20)
