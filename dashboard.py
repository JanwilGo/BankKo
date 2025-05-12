import tkinter as tk
from tkinter import messagebox
import mysql.connector
from transactionhistory import show_transaction_history
from transfer import open_transfer
from loans import open_loans_dashboard
from profile import open_profile
from deposit import open_deposit
from withdraw import open_withdraw

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
    dashboard_window.title("BanKo Dashboard")
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

    # Logout button
    logout_btn = tk.Button(title_bar, text='Logout', font=('Helvetica', 10), bg='#34495e', fg='white',
                          bd=0, padx=10, command=lambda: logout(dashboard_window))
    logout_btn.pack(side=tk.RIGHT, padx=(0, 10))
    logout_btn.bind('<Enter>', on_enter)
    logout_btn.bind('<Leave>', on_leave)

    # Profile button
    profile_btn = tk.Button(title_bar, text='Profile', font=('Helvetica', 10), bg='#34495e', fg='white',
                          bd=0, padx=10, command=lambda: [dashboard_window.destroy(), open_profile(user_id, first_name, lambda: open_dashboard(first_name, user_id))])
    profile_btn.pack(side=tk.RIGHT, padx=(0, 10))
    profile_btn.bind('<Enter>', on_enter)
    profile_btn.bind('<Leave>', on_leave)

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
        command=lambda: [dashboard_window.destroy(), open_deposit(user_id, balance_label, lambda: open_dashboard(first_name, user_id))],
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
        command=lambda: [dashboard_window.destroy(), open_withdraw(user_id, balance_label, lambda: open_dashboard(first_name, user_id))],
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
        command=lambda: [dashboard_window.destroy(), open_transfer(user_id, balance_label, lambda: open_dashboard(first_name, user_id))],
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
