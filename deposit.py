def deposit_action(amount, user_id, balance_label):
    print("\n=== DEBUG: STARTING DEPOSIT ===")
    print(f"User ID: {user_id}, Amount: {amount}")
    
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
        print("DEBUG: Database connection established")

        # Get current balance before deposit
        cursor.execute("SELECT `balance` FROM `users` WHERE `user_id` = %s", (user_id,))
        old_balance = cursor.fetchone()[0]
        print(f"DEBUG: Old balance: ₱{old_balance:,.2f}")

        # Update balance
        cursor.execute("UPDATE `users` SET `balance` = `balance` + %s WHERE `user_id` = %s", (amount, user_id))
        print("DEBUG: Balance updated in users table")

        # Record transaction
        cursor.execute("""
            INSERT INTO `transactions` 
            (`user_id`, `type`, `amount`, `timestamp`) 
            VALUES (%s, 'deposit', %s, NOW())
        """, (user_id, amount))
        print("DEBUG: Transaction record inserted")

        conn.commit()
        print("DEBUG: Changes committed to database")

        # Verify transaction was recorded
        cursor.execute("""
            SELECT COUNT(*) FROM `transactions` 
            WHERE `user_id` = %s AND `type` = 'deposit' AND `amount` = %s
        """, (user_id, amount))
        match_count = cursor.fetchone()[0]
        print(f"DEBUG: Found {match_count} matching transaction records")

        # Get new balance
        cursor.execute("SELECT `balance` FROM `users` WHERE `user_id` = %s", (user_id,))
        new_balance = cursor.fetchone()[0]
        print(f"DEBUG: New balance: ₱{new_balance:,.2f}")

        balance_label["text"] = f"₱{new_balance:,.2f}"
        messagebox.showinfo("Success", f"Successfully deposited ₱{amount:,.2f}")

    except ValueError:
        print("DEBUG: Invalid amount entered")
        messagebox.showerror("Error", "Invalid amount entered. Please enter a valid number.")
    except mysql.connector.Error as err:
        print(f"DEBUG: Database error: {err}")
        messagebox.showerror("Database Error", f"Error: {err}")
        conn.rollback()
    except Exception as e:
        print(f"DEBUG: Unexpected error: {e}")
        messagebox.showerror("Error", f"An unexpected error occurred: {e}")
    finally:
        try:
            cursor.close()
            conn.close()
            print("DEBUG: Database connection closed")
        except:
            pass
    print("=== DEBUG: DEPOSIT COMPLETE ===\n")