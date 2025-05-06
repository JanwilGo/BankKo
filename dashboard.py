import tkinter as tk
from tkinter import messagebox
import mysql.connector

# Function to handle logout
def logout(dashboard_window):
    dashboard_window.destroy()
    import login  # Ensure login module exists for proper navigation

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

        # Fetch the new balance to update the UI
        cursor.execute("SELECT `balance` FROM `users` WHERE `user_id` = %s", (user_id,))
        new_balance = cursor.fetchone()[0]

        balance_label["text"] = f"₱{new_balance:,.2f}"
        messagebox.showinfo("Success", f"Successfully deposited ₱{amount:,.2f}")
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

            # Fetch the new balance to update the UI
            cursor.execute("SELECT `balance` FROM `users` WHERE `user_id` = %s", (user_id,))
            new_balance = cursor.fetchone()[0]

            balance_label["text"] = f"₱{new_balance:,.2f}"
            messagebox.showinfo("Success", f"Successfully withdrew ₱{amount:,.2f}")
    except ValueError:
        messagebox.showerror("Error", "Invalid amount entered. Please enter a valid number.")
    except mysql.connector.Error as err:
        messagebox.showerror("Database Error", f"Error: {err}")
    finally:
        cursor.close()
        conn.close()

# Function to open the dashboard with user's name
def open_dashboard(first_name, user_id):
    dashboard_window = tk.Tk()
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
        command=lambda: open_deposit_window(user_id, balance_label),
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
        command=lambda: open_withdraw_window(user_id, balance_label),
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

    # Transaction History Button (No functionality yet)
    history_button = tk.Button(
        button_frame,
        text="Transaction History",
        command=lambda: print("Transaction History Button Pressed"),
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

    dashboard_window.mainloop()

# Function to open deposit window
def open_deposit_window(user_id, balance_label):
    deposit_window = tk.Toplevel()
    deposit_window.title("Deposit Money")
    deposit_window.geometry("400x300")

    amount_label = tk.Label(deposit_window, text="Amount to Deposit:", font=("Arial", 14))
    amount_label.pack(pady=10)

    amount_entry = tk.Entry(deposit_window, font=("Arial", 14))
    amount_entry.pack(pady=10)

    def handle_deposit():
        amount = amount_entry.get()
        deposit_action(amount, user_id, balance_label)
        deposit_window.destroy()

    deposit_button = tk.Button(deposit_window, text="Deposit", command=handle_deposit, bg="#4CAF50", fg="white", font=("Arial", 16, "bold"))
    deposit_button.pack(pady=20)

# Function to open withdraw window
def open_withdraw_window(user_id, balance_label):
    withdraw_window = tk.Toplevel()
    withdraw_window.title("Withdraw Money")
    withdraw_window.geometry("400x300")

    amount_label = tk.Label(withdraw_window, text="Amount to Withdraw:", font=("Arial", 14))
    amount_label.pack(pady=10)

    amount_entry = tk.Entry(withdraw_window, font=("Arial", 14))
    amount_entry.pack(pady=10)

    def handle_withdraw():
        amount = amount_entry.get()
        withdraw_action(amount, user_id, balance_label)
        withdraw_window.destroy()

    withdraw_button = tk.Button(withdraw_window, text="Withdraw", command=handle_withdraw, bg="#F44336", fg="white", font=("Arial", 16, "bold"))
    withdraw_button.pack(pady=20)

# For testing
if __name__ == "__main__":
    open_dashboard("janwil", 1)  # Replace with actual user_id
