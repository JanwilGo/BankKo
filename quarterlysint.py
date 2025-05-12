import tkinter as tk
from tkinter import messagebox
import mysql.connector

DB_CONFIG = {
    'host': 'sql12.freesqldatabase.com',
    'user': 'sql12773881',
    'password': 'isUcpBumwQ',
    'database': 'sql12773881',
    'port': 3306
}

def open_quarterly_sint(user_id, back_func):
    window = tk.Toplevel()
    window.title("Quarterly Simple Interest Loan")
    window.geometry("600x540")
    window.configure(bg="#f0f2f5")
    # Back button
    back_btn = tk.Button(window, text="Back", command=lambda: [window.destroy(), back_func()], bg="#2f80ed", fg="white", font=("Arial", 10, "bold"))
    back_btn.pack(anchor="nw", padx=10, pady=10)
    # Header
    header = tk.Frame(window, bg="#2f80ed", padx=20, pady=18)
    header.pack(fill=tk.X, pady=(0, 18))
    tk.Label(header, text="Quarterly Simple Interest Loan (1.5%)", font=("Arial", 20, "bold"), fg="white", bg="#2f80ed").pack()
    # Main content boxed
    main_box = tk.Frame(window, bg="white", bd=1, relief=tk.SOLID, padx=30, pady=30)
    main_box.pack(padx=40, pady=10, fill=tk.BOTH, expand=True)
    tk.Label(main_box, text="Enter amount to borrow:", font=("Arial", 13), bg="white").pack(pady=(0, 10))
    amount_entry = tk.Entry(main_box, font=("Arial", 15), justify="center", width=18)
    amount_entry.pack(pady=5, ipadx=5, ipady=4)
    result_label = tk.Label(main_box, text="", font=("Arial", 12), bg="white")
    result_label.pack(pady=10)
    def calculate():
        try:
            principal = float(amount_entry.get())
            interest = principal * 0.015
            total_due = principal + interest
            result_label.config(text=f"Interest (1 quarter): ₱{interest:,.2f}\nTotal Due: ₱{total_due:,.2f}")
        except ValueError:
            result_label.config(text="Enter a valid amount.")
    calc_btn = tk.Button(main_box, text="Calculate", command=calculate, bg="#2f80ed", fg="white", font=("Arial", 12, "bold"), relief=tk.FLAT)
    calc_btn.pack(pady=10)
    def confirm_loan():
        try:
            principal = float(amount_entry.get())
            interest = principal * 0.015
            total_due = principal + interest
            conn = mysql.connector.connect(**DB_CONFIG)
            cursor = conn.cursor()
            cursor.execute("UPDATE users SET balance = balance + %s WHERE user_id = %s", (principal, user_id))
            cursor.execute("INSERT INTO loans (user_id, principal, interest_rate, interest_type, total_due, status, last_interest_applied) VALUES (%s, %s, %s, %s, %s, %s, NOW())",
                (user_id, principal, 1.5, 'quarterly', total_due, 'debt'))
            conn.commit()
            cursor.close()
            conn.close()
            window.destroy()
            back_func()
        except Exception as e:
            messagebox.showerror("Error", str(e))
    confirm_btn = tk.Button(main_box, text="Confirm Loan", command=confirm_loan, bg="#4CAF50", fg="white", font=("Arial", 14, "bold"), relief=tk.FLAT)
    confirm_btn.pack(pady=15)
    window.mainloop() 