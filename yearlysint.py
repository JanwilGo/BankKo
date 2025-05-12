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

def open_yearly_sint(user_id, back_func):
    window = tk.Toplevel()
    window.title("Yearly Simple Interest Loan")
    window.geometry("600x540")
    window.configure(bg="#f0f2f5")
    # Dashboard-style title bar
    title_bar = tk.Frame(window, bg='#34495e', height=30)
    title_bar.pack(fill=tk.X)
    title_bar.bind('<Button-1>', lambda e: window.focus_set())
    title_bar.bind('<B1-Motion>', lambda e: window.geometry(f'+{e.x_root}+{e.y_root}'))
    # Back button
    back_btn = tk.Button(title_bar, text='←', font=('Arial', 13), bg='#34495e', fg='white', bd=0, padx=10, command=lambda: [window.destroy(), back_func()])
    back_btn.pack(side=tk.LEFT)
    back_btn.bind('<Enter>', lambda e: back_btn.configure(bg='#2c3e50'))
    back_btn.bind('<Leave>', lambda e: back_btn.configure(bg='#34495e'))
    # Title
    title_label = tk.Label(title_bar, text="KoBank - Yearly Simple Interest Loan (6%)", font=('Helvetica', 12, 'bold'), bg='#34495e', fg='white')
    title_label.pack(side=tk.LEFT, padx=10)
    # Close button
    close_btn = tk.Button(title_bar, text='×', font=('Arial', 13), bg='#34495e', fg='white', bd=0, padx=10, command=window.destroy)
    close_btn.pack(side=tk.RIGHT)
    close_btn.bind('<Enter>', lambda e: close_btn.configure(bg='#e74c3c'))
    close_btn.bind('<Leave>', lambda e: close_btn.configure(bg='#34495e'))
    # Main content boxed
    main_box = tk.Frame(window, bg="white", bd=1, relief=tk.SOLID, padx=30, pady=30)
    main_box.pack(padx=40, pady=30, fill=tk.BOTH, expand=True)
    tk.Label(main_box, text="Enter amount to borrow:", font=("Arial", 13), bg="white").pack(pady=(0, 10))
    amount_entry = tk.Entry(main_box, font=("Arial", 15), justify="center", width=18)
    amount_entry.pack(pady=5, ipadx=5, ipady=4)
    result_label = tk.Label(main_box, text="", font=("Arial", 12), bg="white")
    result_label.pack(pady=10)
    def calculate():
        try:
            principal = float(amount_entry.get())
            interest = principal * 0.06
            total_due = principal + interest
            result_label.config(text=f"Interest (1 year): ₱{interest:,.2f}\nTotal Due: ₱{total_due:,.2f}")
        except ValueError:
            result_label.config(text="Enter a valid amount.")
    calc_btn = tk.Button(main_box, text="Calculate", command=calculate, bg="#2f80ed", fg="white", font=("Arial", 12, "bold"), relief=tk.FLAT)
    calc_btn.pack(pady=10)
    def confirm_loan():
        try:
            principal = float(amount_entry.get())
            interest = principal * 0.06
            total_due = principal + interest
            conn = mysql.connector.connect(**DB_CONFIG)
            cursor = conn.cursor()
            cursor.execute("UPDATE users SET balance = balance + %s WHERE user_id = %s", (principal, user_id))
            cursor.execute("INSERT INTO loans (user_id, principal, interest_rate, interest_type, total_due, status, last_interest_applied) VALUES (%s, %s, %s, %s, %s, %s, NOW())",
                (user_id, principal, 6.0, 'yearly', total_due, 'debt'))
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