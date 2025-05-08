import tkinter as tk
from tkinter import messagebox
import mysql.connector
from transactionhistory import show_transaction_history  # Make sure this module exists
from transfer import open_transfer_window  # Import transfer window
from loans import open_loans_dashboard  # Import loans dashboard

# Function to handle button hover effects
def on_enter(e):
    e.widget['background'] = '#2c3e50'

def on_leave(e):
    e.widget['background'] = '#34495e'

# Function to handle logout
def logout(dashboard_window):
    dashboard_window.destroy()
    import login
    login.root.deiconify()

# Function to handle the deposit
def deposit_action(amount, user_id):
    try:
        amount = float(amount)
        if amount <= 0:
            messagebox.showerror("Error", "Deposit amount must be positive.")
            return
        conn = mysql.connector.connect(
            host="sql12.freesqldatabase.com",
            user="sql12773881",
            password="isUcpBumwQ",
            database="sql12773881",
            port=3306
        )
        cursor = conn.cursor()
        cursor.execute("UPDATE `users` SET `balance` = `balance` + %s WHERE `user_id` = %s", (amount, user_id))
        conn.commit()
        cursor.execute(
            "INSERT INTO transactions (user_id, type, amount) VALUES (%s, %s, %s)",
            (user_id, 'deposit', amount)
        )
        conn.commit()
    except ValueError:
        messagebox.showerror("Error", "Invalid amount entered. Please enter a valid number.")
    except mysql.connector.Error as err:
        messagebox.showerror("Database Error", f"Error: {err}")
    finally:
        cursor.close()
        conn.close()

# Function to handle the withdrawal
def withdraw_action(amount, user_id):
    try:
        amount = float(amount)
        if amount <= 0:
            messagebox.showerror("Error", "Withdrawal amount must be positive.")
            return
        conn = mysql.connector.connect(
            host="sql12.freesqldatabase.com",
            user="sql12773881",
            password="isUcpBumwQ",
            database="sql12773881",
            port=3306
        )
        cursor = conn.cursor()
        cursor.execute("SELECT `balance` FROM `users` WHERE `user_id` = %s", (user_id,))
        current_balance = cursor.fetchone()[0]
        if current_balance < amount:
            messagebox.showerror("Error", "Insufficient funds.")
        else:
            cursor.execute("UPDATE `users` SET `balance` = `balance` - %s WHERE `user_id` = %s", (amount, user_id))
            conn.commit()
            cursor.execute(
                "INSERT INTO transactions (user_id, type, amount) VALUES (%s, %s, %s)",
                (user_id, 'withdrawal', amount)
            )
            conn.commit()
    except ValueError:
        messagebox.showerror("Error", "Invalid amount entered. Please enter a valid number.")
    except mysql.connector.Error as err:
        messagebox.showerror("Database Error", f"Error: {err}")
    finally:
        cursor.close()
        conn.close()

# Function to center window on screen
def center_window(window):
    window.update_idletasks()
    width = window.winfo_width()
    height = window.winfo_height()
    x = (window.winfo_screenwidth() // 2) - (width // 2)
    y = (window.winfo_screenheight() // 2) - (height // 2)
    window.geometry(f'{width}x{height}+{x}+{y}')

# Function to open the dashboard with user's name
def open_dashboard(first_name, user_id):
    dashboard_window = tk.Toplevel()
    dashboard_window.title("BankKo Dashboard")
    dashboard_window.geometry("800x600")
    dashboard_window.resizable(False, False)
    dashboard_window.configure(bg='#ffffff')
    dashboard_window.attributes('-toolwindow', True)  # Minimal title bar (Windows only)
    center_window(dashboard_window)

    # Title bar
    title_bar = tk.Frame(dashboard_window, bg='#34495e', height=30)
    title_bar.pack(fill=tk.X)
    title_bar.bind('<Button-1>', lambda e: dashboard_window.focus_set())
    title_bar.bind('<B1-Motion>', lambda e: dashboard_window.geometry(f'+{e.x_root}+{e.y_root}'))

    # Close button
    close_btn = tk.Button(title_bar, text='×', font=('Arial', 13), bg='#34495e', fg='white',
                         bd=0, padx=10, command=lambda: logout(dashboard_window))
    close_btn.pack(side=tk.RIGHT)
    close_btn.bind('<Enter>', lambda e: close_btn.configure(bg='#e74c3c'))
    close_btn.bind('<Leave>', lambda e: close_btn.configure(bg='#34495e'))

    # Logout button
    logout_btn = tk.Button(title_bar, text='Logout', font=('Helvetica', 10), bg='#34495e', fg='white',
                          bd=0, padx=10, command=lambda: logout(dashboard_window))
    logout_btn.pack(side=tk.RIGHT, padx=(0, 10))
    logout_btn.bind('<Enter>', on_enter)
    logout_btn.bind('<Leave>', on_leave)

    # Main content frame
    content = tk.Frame(dashboard_window, bg='#ffffff', padx=40, pady=30)
    content.pack(fill=tk.BOTH, expand=True)

    # Welcome section
    welcome_frame = tk.Frame(content, bg='#ffffff')
    welcome_frame.pack(fill=tk.X, pady=(0, 30))

    welcome_label = tk.Label(
        welcome_frame,
        text=f"Welcome back, {first_name}",
        font=("Helvetica", 24, "bold"),
        fg="#34495e",
        bg="#ffffff"
    )
    welcome_label.pack(side=tk.LEFT)

    # Balance Card
    balance_card = tk.Frame(
        content,
        bg='#ffffff',
        bd=0,
        highlightbackground="#bdc3c7",
        highlightthickness=1,
        padx=30,
        pady=30
    )
    balance_card.pack(fill=tk.X, pady=(0, 30))

    tk.Label(
        balance_card,
        text="Available Balance",
        font=("Helvetica", 14),
        fg="#7f8c8d",
        bg="#ffffff"
    ).pack(anchor=tk.W)

    balance_label = tk.Label(
        balance_card,
        text="₱0.00",
        font=("Helvetica", 36, "bold"),
        fg="#34495e",
        bg="#ffffff"
    )
    balance_label.pack(anchor=tk.W, pady=(10, 0))

    # Action Buttons Section
    button_frame = tk.Frame(content, bg="#ffffff")
    button_frame.pack(fill=tk.X, pady=(0, 20))

    # Deposit Button
    deposit_button = tk.Button(
        button_frame,
        text="Deposit",
        command=lambda: [dashboard_window.destroy(), open_deposit_window(user_id, balance_label, first_name, lambda: open_dashboard(first_name, user_id))],
        bg="#34495e",
        fg="white",
        font=("Helvetica", 12),
        bd=0,
        padx=20,
        pady=15,
        cursor="hand2"
    )
    deposit_button.pack(side=tk.LEFT, expand=True, fill=tk.X, padx=5)
    deposit_button.bind('<Enter>', on_enter)
    deposit_button.bind('<Leave>', on_leave)

    # Withdraw Button
    withdraw_button = tk.Button(
        button_frame,
        text="Withdraw",
        command=lambda: [dashboard_window.destroy(), open_withdraw_window(user_id, balance_label, first_name, lambda: open_dashboard(first_name, user_id))],
        bg="#34495e",
        fg="white",
        font=("Helvetica", 12),
        bd=0,
        padx=20,
        pady=15,
        cursor="hand2"
    )
    withdraw_button.pack(side=tk.LEFT, expand=True, fill=tk.X, padx=5)
    withdraw_button.bind('<Enter>', on_enter)
    withdraw_button.bind('<Leave>', on_leave)

    # Transfer Button
    transfer_button = tk.Button(
        button_frame,
        text="Transfer",
        command=lambda: [dashboard_window.destroy(), open_transfer_window(user_id, balance_label, first_name, lambda: open_dashboard(first_name, user_id))],
        bg="#34495e",
        fg="white",
        font=("Helvetica", 12),
        bd=0,
        padx=20,
        pady=15,
        cursor="hand2"
    )
    transfer_button.pack(side=tk.LEFT, expand=True, fill=tk.X, padx=5)
    transfer_button.bind('<Enter>', on_enter)
    transfer_button.bind('<Leave>', on_leave)

    # Second row of buttons
    history_loans_frame = tk.Frame(content, bg="#ffffff")
    history_loans_frame.pack(fill=tk.X)

    # Loans Button
    loans_button = tk.Button(
        history_loans_frame,
        text="Loans",
        command=lambda: [dashboard_window.destroy(), open_loans_dashboard(user_id, lambda: open_dashboard(first_name, user_id))],
        bg="#34495e",
        fg="white",
        font=("Helvetica", 12),
        bd=0,
        padx=20,
        pady=15,
        cursor="hand2"
    )
    loans_button.pack(side=tk.LEFT, expand=True, fill=tk.X, padx=5)
    loans_button.bind('<Enter>', on_enter)
    loans_button.bind('<Leave>', on_leave)

    # Transaction History Button
    history_button = tk.Button(
        history_loans_frame,
        text="Transaction History",
        command=lambda: [dashboard_window.destroy(), show_transaction_history(user_id, lambda: open_dashboard(first_name, user_id))],
        bg="#34495e",
        fg="white",
        font=("Helvetica", 12),
        bd=0,
        padx=20,
        pady=15,
        cursor="hand2"
    )
    history_button.pack(side=tk.LEFT, expand=True, fill=tk.X, padx=5)
    history_button.bind('<Enter>', on_enter)
    history_button.bind('<Leave>', on_leave)

    # Fetch and display the current balance
    update_balance(user_id, balance_label)

# Function to open deposit window
def open_deposit_window(user_id, balance_label, first_name, back_func):
    deposit_window = tk.Toplevel()
    deposit_window.title("Deposit Money")
    deposit_window.geometry("400x500")
    deposit_window.configure(bg='#ffffff')
    deposit_window.attributes('-toolwindow', True)  # Minimal title bar (Windows only)
    center_window(deposit_window)

    # Title bar
    title_bar = tk.Frame(deposit_window, bg='#34495e', height=30)
    title_bar.pack(fill=tk.X)
    title_bar.bind('<Button-1>', lambda e: deposit_window.focus_set())
    title_bar.bind('<B1-Motion>', lambda e: deposit_window.geometry(f'+{e.x_root}+{e.y_root}'))

    # Close button
    close_btn = tk.Button(title_bar, text='×', font=('Arial', 13), bg='#34495e', fg='white',
                         bd=0, padx=10, command=lambda: [deposit_window.destroy(), back_func()])
    close_btn.pack(side=tk.RIGHT)
    close_btn.bind('<Enter>', lambda e: close_btn.configure(bg='#e74c3c'))
    close_btn.bind('<Leave>', lambda e: close_btn.configure(bg='#34495e'))

    # Back button
    back_btn = tk.Button(title_bar, text='←', font=('Arial', 13), bg='#34495e', fg='white',
                        bd=0, padx=10, command=lambda: [deposit_window.destroy(), back_func()])
    back_btn.pack(side=tk.LEFT)
    back_btn.bind('<Enter>', on_enter)
    back_btn.bind('<Leave>', on_leave)

    # Content
    content = tk.Frame(deposit_window, bg='#ffffff', padx=40, pady=30)
    content.pack(fill=tk.BOTH, expand=True)

    # Title
    tk.Label(
        content,
        text="Deposit Money",
        font=("Helvetica", 24, "bold"),
        fg="#34495e",
        bg="#ffffff"
    ).pack(pady=(0, 30))

    # Amount label
    tk.Label(
        content,
        text="Amount to Deposit",
        font=("Helvetica", 10),
        fg="#7f8c8d",
        bg="#ffffff"
    ).pack(anchor="w")

    # Amount entry
    amount_entry = tk.Entry(
        content,
        font=("Helvetica", 12),
        bd=0,
        highlightthickness=1,
        highlightbackground="#bdc3c7",
        highlightcolor="#3498db"
    )
    amount_entry.pack(pady=(5, 20), fill=tk.X)

    # Deposit button
    deposit_button = tk.Button(
        content,
        text="Deposit",
        command=lambda: [deposit_action(amount_entry.get(), user_id), deposit_window.destroy(), back_func()],
        bg="#34495e",
        fg="white",
        font=("Helvetica", 12),
        bd=0,
        padx=20,
        pady=10,
        cursor="hand2"
    )
    deposit_button.pack(fill=tk.X, pady=(20, 0))
    deposit_button.bind('<Enter>', on_enter)
    deposit_button.bind('<Leave>', on_leave)

# Function to open withdraw window
def open_withdraw_window(user_id, balance_label, first_name, back_func):
    withdraw_window = tk.Toplevel()
    withdraw_window.title("Withdraw Money")
    withdraw_window.geometry("400x500")
    withdraw_window.configure(bg='#ffffff')
    withdraw_window.attributes('-toolwindow', True)  # Minimal title bar (Windows only)
    center_window(withdraw_window)

    # Title bar
    title_bar = tk.Frame(withdraw_window, bg='#34495e', height=30)
    title_bar.pack(fill=tk.X)
    title_bar.bind('<Button-1>', lambda e: withdraw_window.focus_set())
    title_bar.bind('<B1-Motion>', lambda e: withdraw_window.geometry(f'+{e.x_root}+{e.y_root}'))

    # Close button
    close_btn = tk.Button(title_bar, text='×', font=('Arial', 13), bg='#34495e', fg='white',
                         bd=0, padx=10, command=lambda: [withdraw_window.destroy(), back_func()])
    close_btn.pack(side=tk.RIGHT)
    close_btn.bind('<Enter>', lambda e: close_btn.configure(bg='#e74c3c'))
    close_btn.bind('<Leave>', lambda e: close_btn.configure(bg='#34495e'))

    # Back button
    back_btn = tk.Button(title_bar, text='←', font=('Arial', 13), bg='#34495e', fg='white',
                        bd=0, padx=10, command=lambda: [withdraw_window.destroy(), back_func()])
    back_btn.pack(side=tk.LEFT)
    back_btn.bind('<Enter>', on_enter)
    back_btn.bind('<Leave>', on_leave)

    # Content
    content = tk.Frame(withdraw_window, bg='#ffffff', padx=40, pady=30)
    content.pack(fill=tk.BOTH, expand=True)

    # Title
    tk.Label(
        content,
        text="Withdraw Money",
        font=("Helvetica", 24, "bold"),
        fg="#34495e",
        bg="#ffffff"
    ).pack(pady=(0, 30))

    # Amount label
    tk.Label(
        content,
        text="Amount to Withdraw",
        font=("Helvetica", 10),
        fg="#7f8c8d",
        bg="#ffffff"
    ).pack(anchor="w")

    # Amount entry
    amount_entry = tk.Entry(
        content,
        font=("Helvetica", 12),
        bd=0,
        highlightthickness=1,
        highlightbackground="#bdc3c7",
        highlightcolor="#3498db"
    )
    amount_entry.pack(pady=(5, 20), fill=tk.X)

    # Withdraw button
    withdraw_button = tk.Button(
        content,
        text="Withdraw",
        command=lambda: [withdraw_action(amount_entry.get(), user_id), withdraw_window.destroy(), back_func()],
        bg="#34495e",
        fg="white",
        font=("Helvetica", 12),
        bd=0,
        padx=20,
        pady=10,
        cursor="hand2"
    )
    withdraw_button.pack(fill=tk.X, pady=(20, 0))
    withdraw_button.bind('<Enter>', on_enter)
    withdraw_button.bind('<Leave>', on_leave)

# Function to update the balance on the dashboard
def update_balance(user_id, balance_label):
    conn = mysql.connector.connect(
        host="sql12.freesqldatabase.com",
        user="sql12773881",
        password="isUcpBumwQ",
        database="sql12773881",
        port=3306
    )
    cursor = conn.cursor()

    cursor.execute("SELECT `balance` FROM `users` WHERE `user_id` = %s", (user_id,))
    balance = cursor.fetchone()[0]
    balance_label["text"] = f"₱{balance:,.2f}"

    cursor.close()
    conn.close()

if __name__ == "__main__":
    open_dashboard("Janwil", 1)  # Replace with actual user_id for testing
