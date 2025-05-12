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
    window.configure(bg="#ffffff")
    # Title bar
    title_bar = tk.Frame(window, bg='#34495e', height=30)
    title_bar.pack(fill=tk.X)
    title_bar.bind('<Button-1>', lambda e: window.focus_set())
    title_bar.bind('<B1-Motion>', lambda e: window.geometry(f'+{e.x_root}+{e.y_root}'))
    # Back button
    back_btn = tk.Button(title_bar, text='←', font=('Arial', 13), bg='#34495e', fg='white', bd=0, padx=10, command=lambda: [window.destroy(), back_func()])
    back_btn.pack(side=tk.LEFT)
    back_btn.bind('<Enter>', lambda e: back_btn.configure(bg='#2c3e50'))
    back_btn.bind('<Leave>', lambda e: back_btn.configure(bg='#34495e'))
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