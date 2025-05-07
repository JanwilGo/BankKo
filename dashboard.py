import tkinter as tk
from tkinter import messagebox
import mysql.connector
from transactionhistory import show_transaction_history  # Make sure this module exists
from transfer import open_transfer_window  # Import transfer window
from loans import open_loans_dashboard  # Import loans dashboard

# Function to handle logout
def logout(dashboard_window):
    dashboard_window.destroy()
    import login
    login.root.deiconify()

# Function to handle the deposit
def deposit_action(amount, user_id, balance_label):
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

        # Update the user's balance
        cursor.execute("UPDATE `users` SET `balance` = `balance` + %s WHERE `user_id` = %s", (amount, user_id))
        conn.commit()

        # Log the transaction
        cursor.execute(
            "INSERT INTO transactions (user_id, type, amount) VALUES (%s, %s, %s)",
            (user_id, 'deposit', amount)
        )
        conn.commit()

        # Fetch the new balance to update the UI
        cursor.execute("SELECT `balance` FROM `users` WHERE `user_id` = %s", (user_id,))
        new_balance = cursor.fetchone()[0]

        balance_label["text"] = f"₱{new_balance:,.2f}"
    except ValueError:
        messagebox.showerror("Error", "Invalid amount entered. Please enter a valid number.")
    except mysql.connector.Error as err:
        messagebox.showerror("Database Error", f"Error: {err}")
    finally:
        cursor.close()
        conn.close()

# Function to handle the withdrawal
def withdraw_action(amount, user_id, balance_label):
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

        # Check if the user has sufficient balance
        cursor.execute("SELECT `balance` FROM `users` WHERE `user_id` = %s", (user_id,))
        current_balance = cursor.fetchone()[0]

        if current_balance < amount:
            messagebox.showerror("Error", "Insufficient funds.")
        else:
            # Update the user's balance
            cursor.execute("UPDATE `users` SET `balance` = `balance` - %s WHERE `user_id` = %s", (amount, user_id))
            conn.commit()

            # Log the transaction
            cursor.execute(
                "INSERT INTO transactions (user_id, type, amount) VALUES (%s, %s, %s)",
                (user_id, 'withdrawal', amount)
            )
            conn.commit()

            # Fetch the new balance to update the UI
            cursor.execute("SELECT `balance` FROM `users` WHERE `user_id` = %s", (user_id,))
            new_balance = cursor.fetchone()[0]

            balance_label["text"] = f"₱{new_balance:,.2f}"
    except ValueError:
        messagebox.showerror("Error", "Invalid amount entered. Please enter a valid number.")
    except mysql.connector.Error as err:
        messagebox.showerror("Database Error", f"Error: {err}")
    finally:
        cursor.close()
        conn.close()

# Function to open the dashboard with user's name
def open_dashboard(first_name, user_id):
    dashboard_window = tk.Toplevel()
    dashboard_window.title("Banking System Dashboard")
    dashboard_window.geometry("600x500")
    dashboard_window.resizable(False, False)

    # Header Section
    header = tk.Frame(dashboard_window, bg="#FFFFFF", padx=20, pady=15)
    header.pack(fill=tk.X)

    welcome_label = tk.Label(
        header,
        text=f"Welcome, {first_name}",
        font=("Arial", 20, "bold"),
        fg="#2f80ed",
        bg="#FFFFFF"
    )
    welcome_label.pack(side=tk.LEFT)

    logout_button = tk.Button(
        header,
        text="Log Out",
        command=lambda: logout(dashboard_window),
        bg="#2f80ed",
        fg="white",
        font=("Arial", 10, "bold"),
        relief=tk.FLAT,
        bd=0,
        padx=10,
        pady=5,
        cursor="hand2"
    )
    logout_button.pack(side=tk.RIGHT)

    # Main Content Section
    content = tk.Frame(dashboard_window, bg="#f0f2f5", padx=20, pady=20)
    content.pack(fill=tk.BOTH, expand=True)

    # Balance Card Section
    balance_card = tk.Frame(
        content,
        bg="white",
        bd=0,
        highlightbackground="#dddddd",
        highlightthickness=1,
        padx=15,
        pady=15
    )
    balance_card.pack(fill=tk.X, pady=10)

    tk.Label(
        balance_card,
        text="Your Balance",
        font=("Arial", 16),
        bg="white"
    ).pack(anchor=tk.W)

    balance_label = tk.Label(
        balance_card,
        text="₱0.00",
        font=("Arial", 28, "bold"),
        fg="#2f80ed",
        bg="white"
    )
    balance_label.pack(anchor=tk.W, pady=10)

    # Action Buttons Section
    button_frame = tk.Frame(content, bg="#f0f2f5")
    button_frame.pack(fill=tk.X, pady=20)

    # Deposit Button
    deposit_button = tk.Button(
        button_frame,
        text="Deposit",
        command=lambda: [dashboard_window.destroy(), open_deposit_window(user_id, balance_label, first_name, lambda: open_dashboard(first_name, user_id))],
        bg="#2f80ed",
        fg="white",
        font=("Arial", 16, "bold"),
        relief=tk.FLAT,
        bd=0,
        padx=20,
        pady=15,
        cursor="hand2"
    )
    deposit_button.pack(side=tk.LEFT, expand=True, fill=tk.X, padx=5)

    # Withdraw Button
    withdraw_button = tk.Button(
        button_frame,
        text="Withdraw",
        command=lambda: [dashboard_window.destroy(), open_withdraw_window(user_id, balance_label, first_name, lambda: open_dashboard(first_name, user_id))],
        bg="#2f80ed",
        fg="white",
        font=("Arial", 16, "bold"),
        relief=tk.FLAT,
        bd=0,
        padx=20,
        pady=15,
        cursor="hand2"
    )
    withdraw_button.pack(side=tk.LEFT, expand=True, fill=tk.X, padx=5)

    # Transfer Button
    transfer_button = tk.Button(
        button_frame,
        text="Transfer",
        command=lambda: [dashboard_window.destroy(), open_transfer_window(user_id, balance_label, first_name, lambda: open_dashboard(first_name, user_id))],
        bg="#2f80ed",
        fg="white",
        font=("Arial", 16, "bold"),
        relief=tk.FLAT,
        bd=0,
        padx=20,
        pady=15,
        cursor="hand2"
    )
    transfer_button.pack(side=tk.LEFT, expand=True, fill=tk.X, padx=5)

    # Move Transaction History and Loans buttons to a new row below
    history_loans_frame = tk.Frame(content, bg="#f0f2f5")
    history_loans_frame.pack(fill=tk.X, pady=(0, 20))

    # Loans Button
    loans_button = tk.Button(
        history_loans_frame,
        text="Loans",
        command=lambda: [dashboard_window.destroy(), open_loans_dashboard(user_id, lambda: open_dashboard(first_name, user_id))],
        bg="#2f80ed",
        fg="white",
        font=("Arial", 16, "bold"),
        relief=tk.FLAT,
        bd=0,
        padx=20,
        pady=15,
        cursor="hand2"
    )
    loans_button.pack(side=tk.LEFT, expand=True, fill=tk.X, padx=5)

    # Transaction History Button (now last in the row)
    history_button = tk.Button(
        history_loans_frame,
        text="Transaction History",
        command=lambda: [dashboard_window.destroy(), show_transaction_history(user_id, lambda: open_dashboard(first_name, user_id))],
        bg="#2f80ed",
        fg="white",
        font=("Arial", 16, "bold"),
        relief=tk.FLAT,
        bd=0,
        padx=20,
        pady=15,
        cursor="hand2"
    )
    history_button.pack(side=tk.LEFT, expand=True, fill=tk.X, padx=5)

    # Fetch and display the current balance
    update_balance(user_id, balance_label)

# Function to open deposit window
def open_deposit_window(user_id, balance_label, first_name, back_func):
    deposit_window = tk.Toplevel()
    deposit_window.title("Deposit Money")
    deposit_window.geometry("400x300")
    back_btn = tk.Button(deposit_window, text="Back", command=lambda: [deposit_window.destroy(), back_func()], bg="#2f80ed", fg="white", font=("Arial", 10, "bold"))
    back_btn.pack(anchor="nw", padx=10, pady=10)

    amount_label = tk.Label(deposit_window, text="Amount to Deposit:", font=("Arial", 14))
    amount_label.pack(pady=10)

    amount_entry = tk.Entry(deposit_window, font=("Arial", 14))
    amount_entry.pack(pady=10)

    def handle_deposit():
        amount = amount_entry.get()
        deposit_action(amount, user_id, balance_label)
        deposit_window.destroy()
        open_dashboard(first_name, user_id)

    deposit_button = tk.Button(deposit_window, text="Deposit", command=handle_deposit, bg="#4CAF50", fg="white", font=("Arial", 16, "bold"))
    deposit_button.pack(pady=20)

# Function to open withdraw window
def open_withdraw_window(user_id, balance_label, first_name, back_func):
    withdraw_window = tk.Toplevel()
    withdraw_window.title("Withdraw Money")
    withdraw_window.geometry("400x300")
    back_btn = tk.Button(withdraw_window, text="Back", command=lambda: [withdraw_window.destroy(), back_func()], bg="#2f80ed", fg="white", font=("Arial", 10, "bold"))
    back_btn.pack(anchor="nw", padx=10, pady=10)

    amount_label = tk.Label(withdraw_window, text="Amount to Withdraw:", font=("Arial", 14))
    amount_label.pack(pady=10)

    amount_entry = tk.Entry(withdraw_window, font=("Arial", 14))
    amount_entry.pack(pady=10)

    def handle_withdraw():
        amount = amount_entry.get()
        withdraw_action(amount, user_id, balance_label)
        withdraw_window.destroy()
        open_dashboard(first_name, user_id)

    withdraw_button = tk.Button(withdraw_window, text="Withdraw", command=handle_withdraw, bg="#F44336", fg="white", font=("Arial", 16, "bold"))
    withdraw_button.pack(pady=20)

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
