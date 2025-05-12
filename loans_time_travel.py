import mysql.connector
from datetime import timedelta
import tkinter as tk
from tkinter import messagebox

DB_CONFIG = {
    'host': 'sql12.freesqldatabase.com',
    'user': 'sql12773881',
    'password': 'isUcpBumwQ',
    'database': 'sql12773881',
    'port': 3306
}

def time_travel_loans(period='yearly', loan_id=None):
    conn = mysql.connector.connect(**DB_CONFIG)
    cursor = conn.cursor()
    if period == 'yearly':
        delta = timedelta(days=366)  # Leap year safe
    elif period == 'quarterly':
        delta = timedelta(days=92)
    else:
        messagebox.showerror('Error', 'Invalid period. Use "yearly" or "quarterly".')
        return
    if loan_id:
        cursor.execute("SELECT created_at, last_interest_applied FROM loans WHERE loan_id = %s", (loan_id,))
        loans = cursor.fetchall()
        ids = [loan_id]
    else:
        cursor.execute("SELECT loan_id, created_at, last_interest_applied FROM loans")
        loans = cursor.fetchall()
        ids = [row[0] for row in loans]
    for row in loans:
        if loan_id:
            created_at, last_interest_applied = row
        else:
            _, created_at, last_interest_applied = row
        new_created = created_at - delta
        new_last = (last_interest_applied - delta) if last_interest_applied else None
        if new_last:
            cursor.execute("UPDATE loans SET created_at = %s, last_interest_applied = %s WHERE loan_id = %s", (new_created, new_last, loan_id if loan_id else row[0]))
        else:
            cursor.execute("UPDATE loans SET created_at = %s WHERE loan_id = %s", (new_created, loan_id if loan_id else row[0]))
    conn.commit()
    cursor.close()
    conn.close()
    messagebox.showinfo("Success", f"Loans time-traveled {period} earlier.")

def open_time_travel_ui():
    root = tk.Tk()
    root.title("Loans Time Travel Tool")
    root.geometry("400x250")
    root.configure(bg="#ffffff")
    tk.Label(root, text="Loans Time Travel", font=("Helvetica", 16, "bold"), bg="#ffffff").pack(pady=15)
    # Period selection
    period_var = tk.StringVar(value="yearly")
    frame = tk.Frame(root, bg="#ffffff")
    frame.pack(pady=5)
    tk.Label(frame, text="Period:", font=("Helvetica", 12), bg="#ffffff").pack(side=tk.LEFT)
    tk.Radiobutton(frame, text="Yearly", variable=period_var, value="yearly", bg="#ffffff", font=("Helvetica", 12)).pack(side=tk.LEFT, padx=10)
    tk.Radiobutton(frame, text="Quarterly", variable=period_var, value="quarterly", bg="#ffffff", font=("Helvetica", 12)).pack(side=tk.LEFT)
    # Loan ID entry
    id_frame = tk.Frame(root, bg="#ffffff")
    id_frame.pack(pady=5)
    tk.Label(id_frame, text="Loan ID (optional):", font=("Helvetica", 12), bg="#ffffff").pack(side=tk.LEFT)
    loan_id_entry = tk.Entry(id_frame, font=("Helvetica", 12), width=10)
    loan_id_entry.pack(side=tk.LEFT, padx=10)
    # Button
    def on_time_travel():
        period = period_var.get()
        loan_id = loan_id_entry.get().strip()
        if loan_id == "":
            loan_id_val = None
        else:
            try:
                loan_id_val = int(loan_id)
            except ValueError:
                messagebox.showerror("Error", "Loan ID must be an integer.")
                return
        time_travel_loans(period, loan_id_val)
    btn = tk.Button(root, text="Time Travel!", command=on_time_travel, bg="#34495e", fg="white", font=("Helvetica", 14, "bold"), padx=20, pady=10)
    btn.pack(pady=20)
    root.mainloop()

if __name__ == "__main__":
    open_time_travel_ui() 