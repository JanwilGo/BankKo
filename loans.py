import tkinter as tk
from tkinter import messagebox, ttk
import mysql.connector
from loans_interest_checker import start_interest_checker

DB_CONFIG = {
    'host': 'sql12.freesqldatabase.com',
    'user': 'sql12773881',
    'password': 'isUcpBumwQ',
    'database': 'sql12773881',
    'port': 3306
}

def center_window(window):
    window.update_idletasks()
    width = window.winfo_width()
    height = window.winfo_height()
    x = (window.winfo_screenwidth() // 2) - (width // 2)
    y = (window.winfo_screenheight() // 2) - (height // 2)
    window.geometry(f'{width}x{height}+{x}+{y}')

def on_enter(e):
    e.widget['background'] = '#2c3e50'

def on_leave(e):
    e.widget['background'] = '#34495e'

def open_loans_dashboard(user_id, back_func=None):
    window = tk.Toplevel()
    window.title("Loans Dashboard")
    window.geometry("900x600")
    window.configure(bg="#ffffff")
    window.attributes('-toolwindow', True)  # Minimal title bar (Windows only)
    center_window(window)
    # Title bar
    title_bar = tk.Frame(window, bg='#34495e', height=30)
    title_bar.pack(fill=tk.X)
    title_bar.bind('<Button-1>', lambda e: window.focus_set())
    title_bar.bind('<B1-Motion>', lambda e: window.geometry(f'+{e.x_root}+{e.y_root}'))
    # Back button
    if back_func:
        back_btn = tk.Button(title_bar, text='←', font=('Arial', 13), bg='#34495e', fg='white',
                            bd=0, padx=10, command=lambda: [window.destroy(), back_func()])
        back_btn.pack(side=tk.LEFT)
        back_btn.bind('<Enter>', on_enter)
        back_btn.bind('<Leave>', on_leave)
    # Content
    content = tk.Frame(window, bg='#ffffff', padx=40, pady=30)
    content.pack(fill=tk.BOTH, expand=True)
    # Title
    tk.Label(
        content,
        text="Your Loans",
        font=("Helvetica", 24, "bold"),
        fg="#34495e",
        bg="#ffffff"
    ).pack(pady=(0, 30), anchor="w")
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
    balance_frame = tk.Frame(content, bg="#ffffff")
    balance_frame.pack(fill=tk.X, pady=(0, 10))
    tk.Label(balance_frame, text="Your Balance", font=("Helvetica", 14), bg="#ffffff").pack(anchor="w", side=tk.LEFT)
    tk.Label(balance_frame, text=f"₱{balance:,.2f}", font=("Helvetica", 24, "bold"), fg="#2f80ed", bg="#ffffff").pack(anchor="w", pady=(0, 10), side=tk.LEFT)
    payloan_btn = tk.Button(balance_frame, text="Pay Loan", bg="#34495e", fg="white", font=("Helvetica", 12, "bold"), relief=tk.FLAT, padx=20, pady=8, command=lambda: [window.destroy(), open_payloan(user_id, lambda: open_loans_dashboard(user_id, back_func))])
    payloan_btn.pack(side=tk.RIGHT, padx=10, pady=5)
    payloan_btn.bind('<Enter>', on_enter)
    payloan_btn.bind('<Leave>', on_leave)
    # Loans Table
    table_outer = tk.Frame(content, bg='#ffffff')
    table_outer.pack(fill=tk.BOTH, expand=True)
    table_box = tk.Frame(table_outer, bg='#ffffff', bd=0, highlightbackground="#bdc3c7", highlightthickness=1)
    table_box.pack(fill=tk.BOTH, expand=True)
    columns = ("Loan ID", "Principal", "Interest Rate", "Type", "Total Due", "Status", "Created At")
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
    vsb = ttk.Scrollbar(table_box, orient="vertical", command=tree.yview)
    hsb = ttk.Scrollbar(table_box, orient="horizontal", command=tree.xview)
    tree.configure(yscrollcommand=vsb.set, xscrollcommand=hsb.set)
    tree.grid(row=0, column=0, sticky="nsew")
    vsb.grid(row=0, column=1, sticky="ns")
    hsb.grid(row=1, column=0, sticky="ew")
    table_box.grid_rowconfigure(0, weight=1)
    table_box.grid_columnconfigure(0, weight=1)
    for col in columns:
        tree.heading(col, text=col)
        tree.column(col, anchor=tk.CENTER, width=120)
    try:
        conn = mysql.connector.connect(**DB_CONFIG)
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT * FROM loans WHERE user_id = %s ORDER BY created_at DESC", (user_id,))
        for i, loan in enumerate(cursor.fetchall()):
            cursor2 = conn.cursor()
            cursor2.execute("SELECT COALESCE(SUM(amount), 0) FROM loan_payments WHERE loan_id = %s", (loan['loan_id'],))
            paid = cursor2.fetchone()[0]
            cursor2.close()
            remaining_due = max(loan['total_due'] - paid, 0)
            tag = 'evenrow' if i % 2 == 0 else 'oddrow'
            tree.insert("", "end", values=(
                loan['loan_id'],
                f"₱{loan['principal']:,.2f}",
                f"{loan['interest_rate']}%",
                loan['interest_type'].capitalize(),
                f"₱{remaining_due:,.2f}" if loan['status'] != 'paid' else "₱0.00",
                loan['status'].capitalize(),
                loan['created_at'].strftime("%Y-%m-%d %H:%M:%S")
            ), tags=(tag,))
        tree.tag_configure('evenrow', background='#ffffff')
        tree.tag_configure('oddrow', background='#f8f9fa')
        cursor.close()
        conn.close()
    except Exception as e:
        messagebox.showerror("Database Error", str(e))
    # Buttons
    button_frame = tk.Frame(content, bg="#ffffff")
    button_frame.pack(fill=tk.X, pady=10)
    btn_yearly = tk.Button(button_frame, text="Yearly Simple Interest", bg="#34495e", fg="white", font=("Helvetica", 14, "bold"), relief=tk.FLAT, padx=20, pady=10, command=lambda: [window.destroy(), open_yearly_sint(user_id, lambda: open_loans_dashboard(user_id, back_func))])
    btn_yearly.pack(side=tk.LEFT, expand=True, fill=tk.X, padx=5)
    btn_yearly.bind('<Enter>', on_enter)
    btn_yearly.bind('<Leave>', on_leave)
    btn_quarterly = tk.Button(button_frame, text="Quarterly Simple Interest", bg="#34495e", fg="white", font=("Helvetica", 14, "bold"), relief=tk.FLAT, padx=20, pady=10, command=lambda: [window.destroy(), open_quarterly_sint(user_id, lambda: open_loans_dashboard(user_id, back_func))])
    btn_quarterly.pack(side=tk.LEFT, expand=True, fill=tk.X, padx=5)
    btn_quarterly.bind('<Enter>', on_enter)
    btn_quarterly.bind('<Leave>', on_leave)
    btn_history = tk.Button(button_frame, text="Loan Payment History", bg="#34495e", fg="white", font=("Helvetica", 14, "bold"), relief=tk.FLAT, padx=20, pady=10, command=lambda: [window.destroy(), open_loanhistory(user_id, lambda: open_loans_dashboard(user_id, back_func))])
    btn_history.pack(side=tk.LEFT, expand=True, fill=tk.X, padx=5)
    btn_history.bind('<Enter>', on_enter)
    btn_history.bind('<Leave>', on_leave)

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
    start_interest_checker()
    open_loans_dashboard(1)
    root.mainloop() 