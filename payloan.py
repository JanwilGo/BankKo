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
    window.geometry("600x500")
    window.configure(bg="#f0f2f5")
    # Back button
    back_btn = tk.Button(window, text="Back", command=lambda: [window.destroy(), back_func()], bg="#2f80ed", fg="white", font=("Arial", 10, "bold"))
    back_btn.pack(anchor="nw", padx=10, pady=10)
    # Header
    header = tk.Frame(window, bg="#2f80ed", padx=20, pady=15)
    header.pack(fill=tk.X)
    tk.Label(header, text="Pay Loan", font=("Arial", 18, "bold"), fg="white", bg="#2f80ed").pack()
    # Table Frame (boxed look)
    table_outer = tk.Frame(window, bg="#f0f2f5", padx=20, pady=10)
    table_outer.pack(fill=tk.BOTH, expand=True)
    table_box = tk.Frame(table_outer, bg="white", bd=1, relief=tk.SOLID)
    table_box.pack(fill=tk.BOTH, expand=True)
    columns = ("Loan ID", "Total Due", "Status")
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
    entry_frame = tk.Frame(window, bg="#f0f2f5")
    entry_frame.pack(fill=tk.X, pady=(0, 10))
    tk.Label(entry_frame, text="Amount to pay:", font=("Arial", 12), bg="#f0f2f5").pack(pady=5)
    amount_entry = tk.Entry(entry_frame, font=("Arial", 14))
    amount_entry.pack(pady=5, padx=20, fill=tk.X)
    pay_btn = tk.Button(entry_frame, text="Pay Loan", command=lambda: pay_selected_loan(), bg="#4CAF50", fg="white", font=("Arial", 14, "bold"))
    pay_btn.pack(pady=10)
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
    window.mainloop() 