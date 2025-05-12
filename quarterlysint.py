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
    window.geometry("700x700")
    window.configure(bg="white")
    window.iconbitmap("")
    
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
    
    # Section header
    section_header = tk.Label(main_frame, text="Quarterly Simple Interest Loan (1.5%)", font=("Helvetica", 18, "bold"), fg="#34495e", bg="white")
    section_header.pack(pady=(0, 15))
    
    tk.Label(main_frame, text="Enter amount to borrow:", font=("Arial", 13), bg="white").pack(pady=(0, 5))
    amount_entry = tk.Entry(main_frame, font=("Arial", 15), justify="center", width=18)
    amount_entry.pack(pady=5, ipadx=5, ipady=4)
    
    result_label = tk.Label(main_frame, text="", font=("Arial", 12), bg="white")
    result_label.pack(pady=5)

    # Numpad frame
    numpad_frame = tk.Frame(main_frame, bg="white")
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

    def calculate():
        try:
            principal = float(amount_entry.get())
            interest = principal * 0.015
            total_due = principal + interest
            result_label.config(text=f"Interest (1 quarter): ₱{interest:,.2f}\nTotal Due: ₱{total_due:,.2f}")
        except ValueError:
            result_label.config(text="Enter a valid amount.")

    # Button frame for consistent width
    button_frame = tk.Frame(main_frame, bg="white")
    button_frame.pack(fill=tk.X, pady=5)

    calc_btn = tk.Button(button_frame, text="Calculate", command=calculate, 
                      bg="#2C3E50", fg="white", 
                      font=("Arial", 12), 
                      relief=tk.FLAT,
                      width=20,
                      height=2)
    calc_btn.pack(pady=(5,2), expand=True)

    def show_success_banner(window, amount):
        # Create a banner frame at the top of the window
        banner = tk.Frame(window, bg="#4CAF50")  # Green background
        banner.pack(fill=tk.X)
        banner.place(relx=0.5, rely=0.1, anchor="n")  # Position below the title bar
        
        # Success message
        message = tk.Label(
            banner,
            text=f"Successfully borrowed ₱{amount:,.2f}!",
            font=("Arial", 12, "bold"),
            fg="white",
            bg="#4CAF50",
            padx=20,
            pady=10
        )
        message.pack()
        
        # Auto-hide the banner after 2 seconds
        window.after(2000, banner.destroy)

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
            show_success_banner(window, principal)
            window.after(2100, lambda: [window.destroy(), back_func()])
        except Exception as e:
            messagebox.showerror("Error", str(e))

    confirm_btn = tk.Button(button_frame, text="Confirm Loan", command=confirm_loan, 
                         bg="#2C3E50", fg="white", 
                         font=("Arial", 12), 
                         relief=tk.FLAT,
                         width=20,
                         height=2)
    confirm_btn.pack(pady=(2,5), expand=True)

    window.mainloop() 