import tkinter as tk
from tkinter import ttk, messagebox
import mysql.connector

DB_CONFIG = {
    'host': 'sql12.freesqldatabase.com',
    'user': 'sql12773881',
    'password': 'isUcpBumwQ',
    'database': 'sql12773881',
    'port': 3306
}

def open_loanhistory(user_id, back_func):
    window = tk.Toplevel()
    window.title("Loan Payment History")
    window.geometry("600x400")
    window.configure(bg="#f0f2f5")
    back_btn = tk.Button(window, text="Back", command=lambda: [window.destroy(), back_func()], bg="#2f80ed", fg="white", font=("Arial", 10, "bold"))
    back_btn.pack(anchor="nw", padx=10, pady=10)
    header = tk.Frame(window, bg="#2f80ed", padx=20, pady=15)
    header.pack(fill=tk.X)
    tk.Label(header, text="Loan Payment History", font=("Arial", 16, "bold"), fg="white", bg="#2f80ed").pack()
    table_frame = tk.Frame(window, bg="#f0f2f5")
    table_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
    columns = ("Payment ID", "Loan ID", "Amount", "Paid At")
    tree = ttk.Treeview(table_frame, columns=columns, show="headings")
    for col in columns:
        tree.heading(col, text=col)
        tree.column(col, anchor=tk.CENTER, width=120)
    tree.pack(fill=tk.BOTH, expand=True)
    try:
        conn = mysql.connector.connect(**DB_CONFIG)
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT * FROM loan_payments WHERE user_id = %s ORDER BY paid_at DESC", (user_id,))
        for payment in cursor.fetchall():
            tree.insert("", "end", values=(
                payment['payment_id'],
                payment['loan_id'],
                f"₱{payment['amount']:,.2f}",
                payment['paid_at'].strftime("%Y-%m-%d %H:%M:%S")
            ))
        cursor.close()
        conn.close()
    except Exception as e:
        messagebox.showerror("Database Error", str(e))
    window.mainloop() 