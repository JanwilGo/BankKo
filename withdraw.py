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

def show_success_banner(window, amount):
    # Create a banner frame at the top of the window
    banner = tk.Frame(window, bg="#4CAF50")  # Green background
    banner.pack(fill=tk.X)
    banner.place(relx=0.5, rely=0.1, anchor="n")  # Position below the title bar
    
    # Success message
    message = tk.Label(
        banner,
        text=f"Successfully withdrew ₱{amount:,.2f}!",
        font=("Arial", 12, "bold"),
        fg="white",
        bg="#4CAF50",
        padx=20,
        pady=10
    )
    message.pack()
    
    # Auto-hide the banner after 2 seconds
    window.after(2000, banner.destroy)

def withdraw_action(amount, user_id, window, back_func):
    try:
        amount = float(amount)
        if amount <= 0:
            messagebox.showerror("Error", "Withdrawal amount must be positive.")
            return
        conn = mysql.connector.connect(**DB_CONFIG)
        cursor = conn.cursor()
        cursor.execute("SELECT `balance` FROM `users` WHERE `user_id` = %s", (user_id,))
        current_balance = cursor.fetchone()[0]
        if current_balance < amount:
            messagebox.showerror("Error", "Insufficient funds.")
            return
        cursor.execute("UPDATE `users` SET `balance` = `balance` - %s WHERE `user_id` = %s", (amount, user_id))
        conn.commit()
        cursor.execute(
            "INSERT INTO transactions (user_id, type, amount) VALUES (%s, %s, %s)",
            (user_id, 'withdrawal', amount)
        )
        conn.commit()
        show_success_banner(window, amount)
        window.after(2100, lambda: [window.destroy(), back_func()])
    except ValueError:
        messagebox.showerror("Error", "Invalid amount entered. Please enter a valid number.")
    except mysql.connector.Error as err:
        messagebox.showerror("Database Error", f"Error: {err}")
    finally:
        cursor.close()
        conn.close()

def open_withdraw(user_id, balance_label, back_func):
    window = tk.Toplevel()
    window.title("Withdraw Money")
    window.geometry("550x550")
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
    
    # Balance display in title bar
    try:
        conn = mysql.connector.connect(**DB_CONFIG)
        cursor = conn.cursor()
        cursor.execute("SELECT balance FROM users WHERE user_id = %s", (user_id,))
        balance = cursor.fetchone()[0]
        cursor.close()
        conn.close()
    except Exception:
        balance = 0.0
    
    balance_frame = tk.Frame(title_bar, bg='#34495e')
    balance_frame.pack(side=tk.RIGHT, padx=10)
    tk.Label(balance_frame, text="Balance: ", font=("Arial", 11), bg='#34495e', fg='white').pack(side=tk.LEFT)
    tk.Label(balance_frame, text=f"₱{balance:,.2f}", font=("Arial", 11, "bold"), bg='#34495e', fg='white').pack(side=tk.LEFT)
    
    # Main content
    main_frame = tk.Frame(window, bg="white")
    main_frame.pack(fill=tk.BOTH, expand=True, padx=40, pady=20)
    
    # Section header
    section_header = tk.Label(main_frame, text="Withdraw Money", font=("Helvetica", 18, "bold"), fg="#34495e", bg="white")
    section_header.pack(pady=(0, 15))
    
    # Amount entry and numpad
    entry_frame = tk.Frame(main_frame, bg="white")
    entry_frame.pack(fill=tk.X, pady=10)
    
    tk.Label(entry_frame, text="Amount to withdraw:", font=("Arial", 13), bg="white").pack()
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

    # Button frame for consistent width
    button_frame = tk.Frame(main_frame, bg="white")
    button_frame.pack(fill=tk.X, pady=5)

    # Withdraw button
    withdraw_btn = tk.Button(button_frame, text="Withdraw", 
                         command=lambda: withdraw_action(amount_entry.get(), user_id, window, back_func),
                         bg="#2C3E50", fg="white",
                         font=("Arial", 12),
                         relief=tk.FLAT,
                         width=20,
                         height=2)
    withdraw_btn.pack(pady=5, expand=True)

    window.mainloop()
