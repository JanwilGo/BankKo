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
    window.geometry("800x800")
    window.configure(bg="white")
    window.iconbitmap("")
    window.resizable(False, False)  # Prevent window resizing
    window.attributes('-toolwindow', True)  # Remove minimize/maximize buttons (Windows only)
    
    # Center the window
    window.update_idletasks()
    width = window.winfo_width()
    height = window.winfo_height()
    x = (window.winfo_screenwidth() // 2) - (width // 2)
    y = (window.winfo_screenheight() // 2) - (height // 2)
    window.geometry(f'{width}x{height}+{x}+{y}')
    
    # Blue bar at the top
    title_bar = tk.Frame(window, bg='#34495e', height=30)
    title_bar.pack(fill=tk.X)
    
    # Back button in blue bar
    back_btn = tk.Button(title_bar, text='←', font=('Arial', 13), bg='#34495e', fg='white', bd=0, padx=10, command=lambda: [window.destroy(), back_func()])
    back_btn.pack(side=tk.LEFT)
    
    # Main content
    main_frame = tk.Frame(window, bg="white")
    main_frame.pack(fill=tk.BOTH, expand=True, padx=40, pady=20)
    
    # Balance display
    balance_frame = tk.Frame(main_frame, bg="white")
    balance_frame.pack(fill=tk.X, pady=(0, 10))
    try:
        conn = mysql.connector.connect(**DB_CONFIG)
        cursor = conn.cursor()
        cursor.execute("SELECT balance FROM users WHERE user_id = %s", (user_id,))
        balance = cursor.fetchone()[0]
        cursor.close()
        conn.close()
    except Exception:
        balance = 0.0
    
    tk.Label(balance_frame, text="Your Balance", font=("Arial", 14), bg="white").pack(side=tk.LEFT)
    balance_label = tk.Label(balance_frame, text=f"₱{balance:,.2f}", font=("Arial", 24, "bold"), fg="#2f80ed", bg="white")
    balance_label.pack(side=tk.LEFT, padx=(10, 0))

    # Loan selection table
    table_frame = tk.Frame(main_frame, bg="white")
    table_frame.pack(fill=tk.BOTH, expand=True, pady=10)
    
    columns = ("Loan ID", "Total Due", "Status")
    tree = ttk.Treeview(table_frame, columns=columns, show="headings", height=6)
    
    style = ttk.Style()
    style.configure("Treeview", 
                   background="white",
                   foreground="black",
                   fieldbackground="white",
                   borderwidth=0,
                   font=('Arial', 10),
                   rowheight=30)
    style.configure("Treeview.Heading",
                   background="#34495e",
                   foreground="black",
                   relief="flat",
                   font=('Arial', 10, 'bold'))
    style.map("Treeview.Heading",
             background=[('active', '#2c3e50')])
    
    # Configure column widths and alignments
    tree.heading("Loan ID", text="Loan ID", anchor=tk.CENTER)
    tree.heading("Total Due", text="Total Due", anchor=tk.CENTER)
    tree.heading("Status", text="Status", anchor=tk.CENTER)
    
    tree.column("Loan ID", width=200, anchor=tk.CENTER)
    tree.column("Total Due", width=300, anchor=tk.CENTER)
    tree.column("Status", width=200, anchor=tk.CENTER)
    
    def load_loans():
        tree.delete(*tree.get_children())
        try:
            conn = mysql.connector.connect(**DB_CONFIG)
            cursor = conn.cursor(dictionary=True)
            cursor.execute("SELECT * FROM loans WHERE user_id = %s AND status = 'debt'", (user_id,))
            for i, loan in enumerate(cursor.fetchall()):
                cursor2 = conn.cursor()
                cursor2.execute("SELECT COALESCE(SUM(amount), 0) FROM loan_payments WHERE loan_id = %s", (loan['loan_id'],))
                paid = cursor2.fetchone()[0]
                cursor2.close()
                remaining_due = max(loan['total_due'] - paid, 0)
                tag = 'evenrow' if i % 2 == 0 else 'oddrow'
                status_tag = 'debt' if loan['status'] == 'debt' else 'paid'
                tree.insert("", "end", values=(
                    loan['loan_id'],
                    f"₱{remaining_due:,.2f}",
                    loan['status'].capitalize()
                ), tags=(tag, status_tag))
            cursor.close()
            conn.close()
        except Exception as e:
            messagebox.showerror("Database Error", str(e))
    
    # Configure row tags for alternating colors and status colors
    tree.tag_configure('evenrow', background='white')
    tree.tag_configure('oddrow', background='#f8f9fa')  # Light gray for odd rows
    tree.tag_configure('debt', foreground='red')
    tree.tag_configure('paid', foreground='black')
    
    load_loans()
    tree.pack(fill=tk.X, padx=5)

    # Amount entry and numpad
    entry_frame = tk.Frame(main_frame, bg="white")
    entry_frame.pack(fill=tk.X, pady=10)
    
    tk.Label(entry_frame, text="Amount to pay:", font=("Arial", 13), bg="white").pack()
    amount_entry = tk.Entry(entry_frame, font=("Arial", 15), justify="center", width=18)
    amount_entry.pack(pady=5)

    # Numpad frame
    numpad_frame = tk.Frame(entry_frame, bg="white")
    numpad_frame.pack(pady=10)

    def add_digit(digit):
        current = amount_entry.get()
        amount_entry.delete(0, tk.END)
        amount_entry.insert(0, current + str(digit))

    def backspace():
        current = amount_entry.get()
        amount_entry.delete(0, tk.END)
        amount_entry.insert(0, current[:-1])

    # Create numpad buttons
    buttons = [
        ['1', '2', '3'],
        ['4', '5', '6'],
        ['7', '8', '9'],
        ['0', '<']
    ]

    for i, row in enumerate(buttons):
        for j, digit in enumerate(row):
            if digit == '<':
                btn = tk.Button(numpad_frame, text=digit, width=5, height=2, 
                              command=backspace, bg="#34495e", fg="white",
                              font=("Arial", 12))
            else:
                btn = tk.Button(numpad_frame, text=digit, width=5, height=2,
                              command=lambda d=digit: add_digit(d), bg="#34495e", fg="white",
                              font=("Arial", 12))
            btn.grid(row=i, column=j, padx=2, pady=2)

    def show_success_banner(window, amount):
        # Create a banner frame at the top of the window
        banner = tk.Frame(window, bg="#4CAF50")  # Green background
        banner.pack(fill=tk.X)
        banner.place(relx=0.5, rely=0.1, anchor="n")  # Position below the title bar
        
        # Success message
        message = tk.Label(
            banner,
            text=f"Successfully paid ₱{amount:,.2f}!",
            font=("Arial", 12, "bold"),
            fg="white",
            bg="#4CAF50",
            padx=20,
            pady=10
        )
        message.pack()
        
        # Auto-hide the banner after 2 seconds
        window.after(2000, banner.destroy)

    def update_balance_display():
        try:
            conn = mysql.connector.connect(**DB_CONFIG)
            cursor = conn.cursor()
            cursor.execute("SELECT balance FROM users WHERE user_id = %s", (user_id,))
            balance = cursor.fetchone()[0]
            balance_label["text"] = f"₱{balance:,.2f}"
            cursor.close()
            conn.close()
        except Exception as e:
            print(f"Error updating balance display: {e}")

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
            show_success_banner(window, amount)
            update_balance_display()  # Update balance display after payment
            load_loans()
            amount_entry.delete(0, tk.END)  # Clear the amount entry
        except Exception as e:
            messagebox.showerror("Error", str(e))

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
            show_success_banner(window, remaining_due)
            update_balance_display()  # Update balance display after payment
            load_loans()
        except Exception as e:
            messagebox.showerror("Error", str(e))

    # Button frame for consistent width
    button_frame = tk.Frame(main_frame, bg="white")
    button_frame.pack(fill=tk.X, pady=5)

    # Pay Loan button
    pay_btn = tk.Button(button_frame, text="Pay Loan", command=pay_selected_loan,
                     bg="#2C3E50", fg="white",
                     font=("Arial", 12),
                     relief=tk.FLAT,
                     width=20,
                     height=2)
    pay_btn.pack(pady=(5,2), expand=True)

    # Pay Exact Amount button
    pay_exact_btn = tk.Button(button_frame, text="Pay Exact Amount", command=pay_exact_amount,
                           bg="#2C3E50", fg="white",
                           font=("Arial", 12),
                           relief=tk.FLAT,
                           width=20,
                           height=2)
    pay_exact_btn.pack(pady=(2,5), expand=True)

    window.mainloop() 