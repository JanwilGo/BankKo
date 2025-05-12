import tkinter as tk
from tkinter import messagebox
import mysql.connector

# Database configuration
DB_CONFIG = {
    'host': 'sql12.freesqldatabase.com',
    'user': 'sql12773881',
    'password': 'isUcpBumwQ',
    'database': 'sql12773881',
    'port': 3306
}

# Function to center window on screen
def center_window(window):
    window.update_idletasks()
    width = window.winfo_width()
    height = window.winfo_height()
    x = (window.winfo_screenwidth() // 2) - (width // 2)
    y = (window.winfo_screenheight() // 2) - (height // 2)
    window.geometry(f'{width}x{height}+{x}+{y}')

# Function to handle button hover effects
def on_enter(e):
    e.widget['background'] = '#2c3e50'

def on_leave(e):
    e.widget['background'] = '#34495e'

def show_success_banner(window, amount):
    # Create a banner frame at the top of the window
    banner = tk.Frame(window, bg="#4CAF50")  # Green background
    banner.pack(fill=tk.X)
    banner.place(relx=0.5, rely=0.1, anchor="n")  # Position below the title bar
    
    # Success message
    message = tk.Label(
        banner,
        text=f"Successfully transferred ₱{amount:,.2f}!",
        font=("Arial", 12, "bold"),
        fg="white",
        bg="#4CAF50",
        padx=20,
        pady=10
    )
    message.pack()
    
    # Auto-hide the banner after 2 seconds
    window.after(2000, banner.destroy)

def transfer_funds(sender_id, recipient_email, amount, balance_label, balance_display=None):
    try:
        amount = float(amount)
        if amount <= 0:
            messagebox.showerror("Error", "Transfer amount must be positive.")
            return False, 0
        conn = mysql.connector.connect(**DB_CONFIG)
        cursor = conn.cursor()
        # Get recipient user_id
        cursor.execute("SELECT user_id FROM users WHERE email = %s", (recipient_email,))
        recipient = cursor.fetchone()
        if not recipient:
            messagebox.showerror("Error", "Recipient not found.")
            return False, 0
        recipient_id = recipient[0]
        if recipient_id == sender_id:
            messagebox.showerror("Error", "Cannot transfer to yourself.")
            return False, 0
        # Check sender balance
        cursor.execute("SELECT balance FROM users WHERE user_id = %s", (sender_id,))
        sender_balance = cursor.fetchone()[0]
        if sender_balance < amount:
            messagebox.showerror("Error", "Insufficient funds.")
            return False, 0
        # Perform transfer
        cursor.execute("UPDATE users SET balance = balance - %s WHERE user_id = %s", (amount, sender_id))
        cursor.execute("UPDATE users SET balance = balance + %s WHERE user_id = %s", (amount, recipient_id))
        # Log transaction
        cursor.execute("""
            INSERT INTO transactions (user_id, type, amount, recipient_id) VALUES (%s, 'transfer', %s, %s)
        """, (sender_id, amount, recipient_id))
        conn.commit()
        
        # Update balance labels
        cursor.execute("SELECT balance FROM users WHERE user_id = %s", (sender_id,))
        new_balance = cursor.fetchone()[0]
        
        # Safely update balance display in transfer window
        if balance_display:
            try:
                balance_display["text"] = f"₱{new_balance:,.2f}"
            except tk.TclError:
                pass  # Widget was destroyed
        
        return True, amount, new_balance  # Return success, amount, and new balance
    except ValueError:
        messagebox.showerror("Error", "Invalid amount entered.")
        return False, 0, 0
    except mysql.connector.Error as err:
        messagebox.showerror("Database Error", f"Error: {err}")
        return False, 0, 0
    finally:
        if 'cursor' in locals():
            cursor.close()
        if 'conn' in locals() and conn.is_connected():
            conn.close()

def open_transfer(user_id, balance_label, back_func):
    window = tk.Toplevel()
    window.title("Transfer Money")
    window.geometry("550x600")
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
    balance_display = tk.Label(balance_frame, text=f"₱{balance:,.2f}", font=("Arial", 11, "bold"), bg='#34495e', fg='white')
    balance_display.pack(side=tk.LEFT)

    def handle_transfer():
        success, amount, new_balance = transfer_funds(user_id, email_entry.get().strip(), amount_entry.get(), balance_label, balance_display)
        if success:
            show_success_banner(window, amount)
            # Update the dashboard balance when returning
            def return_to_dashboard():
                try:
                    if balance_label:
                        balance_label["text"] = f"₱{new_balance:,.2f}"
                except tk.TclError:
                    pass  # Widget was destroyed
                back_func()
            
            window.after(2100, lambda: [window.destroy(), return_to_dashboard()])

    # Main content
    main_frame = tk.Frame(window, bg="white")
    main_frame.pack(fill=tk.BOTH, expand=True, padx=40, pady=20)
    
    # Section header
    section_header = tk.Label(main_frame, text="Transfer Money", font=("Helvetica", 18, "bold"), fg="#34495e", bg="white")
    section_header.pack(pady=(0, 15))
    
    # Recipient Email
    tk.Label(main_frame, text="Recipient Email:", font=("Arial", 13), bg="white").pack(pady=(0, 5))
    email_entry = tk.Entry(main_frame, font=("Arial", 15), justify="center", width=25)
    email_entry.pack(pady=5)
    
    # Amount
    tk.Label(main_frame, text="Enter amount to transfer:", font=("Arial", 13), bg="white").pack(pady=(15, 5))
    amount_entry = tk.Entry(main_frame, font=("Arial", 15), justify="center", width=18)
    amount_entry.pack(pady=5)

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

    # Button frame for consistent width
    button_frame = tk.Frame(main_frame, bg="white")
    button_frame.pack(fill=tk.X, pady=5)

    # Transfer button with updated command
    transfer_btn = tk.Button(button_frame, text="Transfer", 
                         command=handle_transfer,
                         bg="#2C3E50", fg="white",
                         font=("Arial", 12),
                         relief=tk.FLAT,
                         width=20,
                         height=2)
    transfer_btn.pack(pady=5, expand=True)

    window.mainloop()
