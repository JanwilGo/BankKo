import mysql.connector
from tkinter import messagebox

def withdraw_action(amount, user_id, balance_label=None):
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

        # Get current balance
        cursor.execute("SELECT balance FROM users WHERE user_id = %s", (user_id,))
        current_balance = cursor.fetchone()[0]

        if current_balance < amount:
            messagebox.showerror("Error", "Insufficient funds.")
            return

        # Deduct amount
        cursor.execute("UPDATE users SET balance = balance - %s WHERE user_id = %s", (amount, user_id))
        conn.commit()

        # Log to transaction history
        cursor.execute("INSERT INTO transactions (user_id, type, amount) VALUES (%s, %s, %s)", (user_id, "withdraw", amount))
        conn.commit()

        # Update balance label if provided
        if balance_label:
            cursor.execute("SELECT balance FROM users WHERE user_id = %s", (user_id,))
            new_balance = cursor.fetchone()[0]
            balance_label["text"] = f"₱{new_balance:,.2f}"

        messagebox.showinfo("Success", f"Successfully withdrew ₱{amount:,.2f}")
    except ValueError:
        messagebox.showerror("Error", "Please enter a valid number.")
    except mysql.connector.Error as err:
        messagebox.showerror("Database Error", f"Error: {err}")
    finally:
        if conn.is_connected():
            cursor.close()
            conn.close()
