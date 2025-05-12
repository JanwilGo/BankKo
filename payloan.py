import tkinter as tk
from tkinter import messagebox, ttk
import mysql.connector

DB_CONFIG = {
    'host': 'sql12.freesqldatabase.com',
    'user': 'sql12773881',
    'password': 'isUcpBumwQ',
    'database': 'sql12773881',
    'port': 3306
}

def open_payloan(user_id, back_func):
    window = tk.Toplevel()
    window.title("Pay Loan")
    window.geometry("600x650")
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
    # Title
    title_label = tk.Label(title_bar, text="Pay Loan", font=('Helvetica', 12, 'bold'), bg='#34495e', fg='white')
    title_label.pack(side=tk.LEFT, padx=10)
    # Close button
    close_btn = tk.Button(title_bar, text='×', font=('Arial', 13), bg='#34495e', fg='white', bd=0, padx=10, command=lambda: [window.destroy(), back_func()])
    close_btn.pack(side=tk.RIGHT)
    close_btn.bind('<Enter>', lambda e: close_btn.configure(bg='#e74c3c'))
    close_btn.bind('<Leave>', lambda e: close_btn.configure(bg='#34495e'))
    # Fetch and show balance
    try:
        conn = mysql.connector.connect(**DB_CONFIG)
        cursor = conn.cursor()
        cursor.execute("SELECT balance FROM users WHERE user_id = %s", (user_id,))
        balance = cursor.fetchone()[0]
        cursor.close()
        conn.close()
    except Exception:
        balance = 0.0
    balance_frame = tk.Frame(window, bg="#ffffff")
    balance_frame.pack(fill=tk.X, pady=(0, 10))
    tk.Label(balance_frame, text="Your Balance", font=("Helvetica", 14), bg="#ffffff").pack(anchor="w", side=tk.LEFT, padx=(20,0))
    tk.Label(balance_frame, text=f"₱{balance:,.2f}", font=("Helvetica", 24, "bold"), fg="#2f80ed", bg="#ffffff").pack(anchor="w", pady=(0, 10), side=tk.LEFT)
    # Table Frame (boxed look)
    table_outer = tk.Frame(window, bg="#ffffff", padx=20, pady=10)
    table_outer.pack(fill=tk.BOTH, expand=True)
    table_box = tk.Frame(table_outer, bg="#ffffff", bd=0, highlightbackground="#bdc3c7", highlightthickness=1)
    table_box.pack(fill=tk.BOTH, expand=True)
    columns = ("Loan ID", "Total Due", "Status")
    style = ttk.Style()
    style.configure("Treeview", 
                   background="#ffffff",
                   foreground="#000000",
                   fieldbackground="#ffffff",
                   borderwidth=0,
                   font=('Helvetica', 10))
    style.configure("Treeview.Heading",
                   background="#34495e",
                   foreground="#000000",
                   relief="flat",
                   font=('Helvetica', 10, 'bold'))
    style.map("Treeview.Heading",
             background=[('active', '#2c3e50')])
    tree = ttk.Treeview(table_box, columns=columns, show="headings")
    for col in columns:
        tree.heading(col, text=col)
        tree.column(col, anchor=tk.CENTER, width=140)
    tree.pack(fill=tk.BOTH, expand=True)
    def load_loans():
        tree.delete(*tree.get_children())
        try:
            conn = mysql.connector.connect(**DB_CONFIG)
            cursor = conn.cursor(dictionary=True)
            cursor.execute("SELECT * FROM loans WHERE user_id = %s AND status = 'debt'", (user_id,))
            for loan in cursor.fetchall():
                cursor2 = conn.cursor()
                cursor2.execute("SELECT COALESCE(SUM(amount), 0) FROM loan_payments WHERE loan_id = %s", (loan['loan_id'],))
                paid = cursor2.fetchone()[0]
                cursor2.close()
                remaining_due = max(loan['total_due'] - paid, 0)
                tree.insert("", "end", values=(loan['loan_id'], f"₱{remaining_due:,.2f}", loan['status'].capitalize()))
            cursor.close()
            conn.close()
        except Exception as e:
            messagebox.showerror("Database Error", str(e))
    load_loans()
    # Amount Entry Frame (boxed look)
    entry_frame = tk.Frame(window, bg="#ffffff")
    entry_frame.pack(fill=tk.X, pady=(0, 10))
    tk.Label(entry_frame, text="Amount to pay:", font=("Helvetica", 12), bg="#ffffff").pack(pady=5)
    amount_entry = tk.Entry(entry_frame, font=("Helvetica", 14))
    amount_entry.pack(pady=5, padx=20, fill=tk.X)
    pay_btn = tk.Button(entry_frame, text="Pay Loan", command=lambda: pay_selected_loan(), bg="#2ecc71", fg="white", font=("Helvetica", 14, "bold"), bd=0, padx=20, pady=10, cursor="hand2")
    pay_btn.pack(pady=10)
    pay_btn.bind('<Enter>', lambda e: pay_btn.configure(bg='#27ae60'))
    pay_btn.bind('<Leave>', lambda e: pay_btn.configure(bg='#2ecc71'))
    def pay_selected_loan():
        selected = tree.selection()
        if not selected:
            messagebox.showwarning("No Selection", "Select a loan to pay.")
            return
        loan_id = tree.item(selected[0])['values'][0]
        try:
            amount = float(amount_entry.get())
            conn = mysql.connector.connect(**DB_CONFIG)
            cursor = conn.cursor(dictionary=True)
            cursor.execute("SELECT total_due FROM loans WHERE loan_id = %s", (loan_id,))
            loan = cursor.fetchone()
            if not loan:
                messagebox.showerror("Error", "Loan not found.")
                return
            cursor.execute("SELECT COALESCE(SUM(amount), 0) as paid FROM loan_payments WHERE loan_id = %s", (loan_id,))
            paid = cursor.fetchone()['paid']
            remaining_due = max(loan['total_due'] - paid, 0)
            cursor.execute("SELECT balance FROM users WHERE user_id = %s", (user_id,))
            balance = cursor.fetchone()['balance']
            if amount > balance:
                messagebox.showerror("Error", "Insufficient balance.")
                return
            if amount > remaining_due:
                messagebox.showerror("Error", "Cannot pay more than total due.")
                return
            cursor.execute("UPDATE users SET balance = balance - %s WHERE user_id = %s", (amount, user_id))
            cursor.execute("INSERT INTO loan_payments (loan_id, user_id, amount) VALUES (%s, %s, %s)", (loan_id, user_id, amount))
            cursor.execute("SELECT SUM(amount) as paid FROM loan_payments WHERE loan_id = %s", (loan_id,))
            paid = cursor.fetchone()['paid']
            if paid >= loan['total_due']:
                cursor.execute("UPDATE loans SET status = 'paid', paid_at = NOW() WHERE loan_id = %s", (loan_id,))
            conn.commit()
            cursor.close()
            conn.close()
            load_loans()
        except Exception as e:
            messagebox.showerror("Error", str(e))

    # Add 'Pay Exact Amount' button at the bottom
    def pay_exact_amount():
        selected = tree.selection()
        if not selected:
            messagebox.showwarning("No Selection", "Select a loan to pay.")
            return
        loan_id = tree.item(selected[0])['values'][0]
        try:
            conn = mysql.connector.connect(**DB_CONFIG)
            cursor = conn.cursor(dictionary=True)
            cursor.execute("SELECT total_due FROM loans WHERE loan_id = %s", (loan_id,))
            loan = cursor.fetchone()
            if not loan:
                messagebox.showerror("Error", "Loan not found.")
                return
            cursor.execute("SELECT COALESCE(SUM(amount), 0) as paid FROM loan_payments WHERE loan_id = %s", (loan_id,))
            paid = cursor.fetchone()['paid']
            remaining_due = max(loan['total_due'] - paid, 0)
            cursor.execute("SELECT balance FROM users WHERE user_id = %s", (user_id,))
            balance = cursor.fetchone()['balance']
            if remaining_due > balance:
                messagebox.showerror("Error", "Insufficient balance.")
                return
            if remaining_due <= 0:
                messagebox.showinfo("Info", "Loan is already fully paid.")
                return
            cursor.execute("UPDATE users SET balance = balance - %s WHERE user_id = %s", (remaining_due, user_id))
            cursor.execute("INSERT INTO loan_payments (loan_id, user_id, amount) VALUES (%s, %s, %s)", (loan_id, user_id, remaining_due))
            cursor.execute("SELECT SUM(amount) as paid FROM loan_payments WHERE loan_id = %s", (loan_id,))
            paid = cursor.fetchone()['paid']
            if paid >= loan['total_due']:
                cursor.execute("UPDATE loans SET status = 'paid', paid_at = NOW() WHERE loan_id = %s", (loan_id,))
            conn.commit()
            cursor.close()
            conn.close()
            load_loans()
        except Exception as e:
            messagebox.showerror("Error", str(e))

    pay_exact_btn = tk.Button(window, text="Pay Exact Amount", command=pay_exact_amount, bg="#34495e", fg="white", font=("Helvetica", 14, "bold"), bd=0, padx=20, pady=10, cursor="hand2")
    pay_exact_btn.pack(side=tk.BOTTOM, fill=tk.X, padx=40, pady=20)

    window.mainloop() 