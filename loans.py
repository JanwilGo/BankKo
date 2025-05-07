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

def open_loans_dashboard(user_id, back_func=None):
    window = tk.Toplevel()
    window.title("Loans Dashboard")
    window.geometry("900x600")
    window.configure(bg="#f0f2f5")
    window.resizable(False, False)
    # Back button (always visible)
    def do_back():
        window.destroy()
        if back_func:
            back_func()
    back_btn = tk.Button(window, text="Back", command=do_back, bg="#2f80ed", fg="white", font=("Arial", 10, "bold"))
    back_btn.pack(anchor="nw", padx=10, pady=10)
    # Header
    header = tk.Frame(window, bg="#2f80ed", padx=20, pady=15)
    header.pack(fill=tk.X)
    tk.Label(header, text="Your Loans", font=("Arial", 20, "bold"), fg="white", bg="#2f80ed").pack(side=tk.LEFT)
    # Account Balance
    try:
        conn = mysql.connector.connect(**DB_CONFIG)
        cursor = conn.cursor()
        cursor.execute("SELECT balance FROM users WHERE user_id = %s", (user_id,))
        balance = cursor.fetchone()[0]
        cursor.close()
        conn.close()
    except Exception:
        balance = 0.0
    balance_frame = tk.Frame(window, bg="#f0f2f5")
    balance_frame.pack(fill=tk.X, padx=20, pady=(10, 0))
    tk.Label(balance_frame, text="Your Balance", font=("Arial", 14), bg="#f0f2f5").pack(anchor="w", side=tk.LEFT)
    tk.Label(balance_frame, text=f"₱{balance:,.2f}", font=("Arial", 24, "bold"), fg="#2f80ed", bg="#f0f2f5").pack(anchor="w", pady=(0, 10), side=tk.LEFT)
    payloan_btn = tk.Button(balance_frame, text="Pay Loan", bg="#2f80ed", fg="white", font=("Arial", 12, "bold"), relief=tk.FLAT, padx=20, pady=8, command=lambda: [window.destroy(), open_payloan(user_id, lambda: open_loans_dashboard(user_id, back_func))])
    payloan_btn.pack(side=tk.RIGHT, padx=10, pady=5)
    # Loans Table
    table_frame = tk.Frame(window, bg="#f0f2f5")
    table_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
    columns = ("Loan ID", "Principal", "Interest Rate", "Type", "Total Due", "Status", "Created At")
    tree = ttk.Treeview(table_frame, columns=columns, show="headings")
    for col in columns:
        tree.heading(col, text=col)
        tree.column(col, anchor=tk.CENTER, width=120)
    tree.pack(fill=tk.BOTH, expand=True)
    try:
        conn = mysql.connector.connect(**DB_CONFIG)
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT * FROM loans WHERE user_id = %s ORDER BY created_at DESC", (user_id,))
        for loan in cursor.fetchall():
            cursor2 = conn.cursor()
            cursor2.execute("SELECT COALESCE(SUM(amount), 0) FROM loan_payments WHERE loan_id = %s", (loan['loan_id'],))
            paid = cursor2.fetchone()[0]
            cursor2.close()
            remaining_due = max(loan['total_due'] - paid, 0)
            tree.insert("", "end", values=(
                loan['loan_id'],
                f"₱{loan['principal']:,.2f}",
                f"{loan['interest_rate']}%",
                loan['interest_type'].capitalize(),
                f"₱{remaining_due:,.2f}" if loan['status'] != 'paid' else "₱0.00",
                loan['status'].capitalize(),
                loan['created_at'].strftime("%Y-%m-%d %H:%M:%S")
            ))
        cursor.close()
        conn.close()
    except Exception as e:
        messagebox.showerror("Database Error", str(e))
    # Buttons
    button_frame = tk.Frame(window, bg="#f0f2f5")
    button_frame.pack(fill=tk.X, pady=10)
    btn_yearly = tk.Button(button_frame, text="Yearly Simple Interest", bg="#2f80ed", fg="white", font=("Arial", 14, "bold"), relief=tk.FLAT, padx=20, pady=10, command=lambda: [window.destroy(), open_yearly_sint(user_id, lambda: open_loans_dashboard(user_id, back_func))])
    btn_yearly.pack(side=tk.LEFT, expand=True, fill=tk.X, padx=5)
    btn_quarterly = tk.Button(button_frame, text="Quarterly Simple Interest", bg="#2f80ed", fg="white", font=("Arial", 14, "bold"), relief=tk.FLAT, padx=20, pady=10, command=lambda: [window.destroy(), open_quarterly_sint(user_id, lambda: open_loans_dashboard(user_id, back_func))])
    btn_quarterly.pack(side=tk.LEFT, expand=True, fill=tk.X, padx=5)
    btn_history = tk.Button(button_frame, text="Loan Payment History", bg="#2f80ed", fg="white", font=("Arial", 14, "bold"), relief=tk.FLAT, padx=20, pady=10, command=lambda: [window.destroy(), open_loanhistory(user_id, lambda: open_loans_dashboard(user_id, back_func))])
    btn_history.pack(side=tk.LEFT, expand=True, fill=tk.X, padx=5)
    window.mainloop()

# Placeholder navigation functions
def open_yearly_sint(user_id, back_func):
    import yearlysint
    yearlysint.open_yearly_sint(user_id, back_func)
def open_quarterly_sint(user_id, back_func):
    import quarterlysint
    quarterlysint.open_quarterly_sint(user_id, back_func)
def open_payloan(user_id, back_func):
    import payloan
    payloan.open_payloan(user_id, back_func)
def open_loanhistory(user_id, back_func):
    import loanhistory
    loanhistory.open_loanhistory(user_id, back_func)

if __name__ == "__main__":
    root = tk.Tk()
    root.withdraw()
    open_loans_dashboard(1)
    root.mainloop() 