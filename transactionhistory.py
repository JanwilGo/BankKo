import tkinter as tk
import mysql.connector
from tkinter import ttk, messagebox

# Database configuration
DB_CONFIG = {
    'host': 'sql12.freesqldatabase.com',
    'user': 'sql12773881',
    'password': 'isUcpBumwQ',
    'database': 'sql12773881',
    'port': 3306
}

def show_transaction_history(user_id, back_func=None):
    print(f"\n[History] Loading transactions for user {user_id}")
    try:
        conn = mysql.connector.connect(**DB_CONFIG)
        cursor = conn.cursor(dictionary=True)  # Use dictionary cursor for clearer debugging
        
        # First verify user exists
        cursor.execute("SELECT user_id FROM users WHERE user_id = %s", (user_id,))
        if not cursor.fetchone():
            messagebox.showerror("Error", f"User ID {user_id} not found!")
            return

        # Create window
        history_window = tk.Toplevel()
        history_window.title(f"Transaction History (User {user_id})")
        history_window.geometry("1100x600")
        history_window.configure(bg="#f0f2f5")
        
        # Back button
        if back_func:
            back_btn = tk.Button(history_window, text="Back", command=lambda: [history_window.destroy(), back_func()], bg="#2f80ed", fg="white", font=("Arial", 10, "bold"))
            back_btn.pack(anchor="nw", padx=10, pady=10)
        
        # Header
        header = tk.Frame(history_window, bg="#2f80ed", padx=20, pady=20)
        header.pack(fill=tk.X, pady=(0, 20))
        tk.Label(header, text="Transaction History", font=("Arial", 24, "bold"), fg="white", bg="#2f80ed").pack()
        
        # Table Frame (with border and background)
        table_outer = tk.Frame(history_window, bg="#f0f2f5", padx=20, pady=10)
        table_outer.pack(fill=tk.BOTH, expand=True)
        table_box = tk.Frame(table_outer, bg="white", bd=1, relief=tk.SOLID)
        table_box.pack(fill=tk.BOTH, expand=True)
        
        tree = ttk.Treeview(table_box, columns=("ID", "Type", "Direction", "Amount", "Sender", "Recipient", "Date"), show="headings")
        vsb = ttk.Scrollbar(table_box, orient="vertical", command=tree.yview)
        hsb = ttk.Scrollbar(table_box, orient="horizontal", command=tree.xview)
        tree.configure(yscrollcommand=vsb.set, xscrollcommand=hsb.set)
        
        # Layout
        tree.grid(row=0, column=0, sticky="nsew")
        vsb.grid(row=0, column=1, sticky="ns")
        hsb.grid(row=1, column=0, sticky="ew")
        table_box.grid_rowconfigure(0, weight=1)
        table_box.grid_columnconfigure(0, weight=1)
        
        # Configure columns
        tree.heading("ID", text="TXN ID")
        tree.heading("Type", text="Type")
        tree.heading("Direction", text="Direction")
        tree.heading("Amount", text="Amount (₱)")
        tree.heading("Sender", text="Sender")
        tree.heading("Recipient", text="Recipient")
        tree.heading("Date", text="Date/Time")
        
        for col in ("ID", "Type", "Direction", "Amount", "Sender", "Recipient", "Date"):
            tree.column(col, anchor="center", width=140)
        
        # Get transactions with error handling
        try:
            cursor.execute("""
                SELECT transaction_id, type, amount, user_id, recipient_id, created_at 
                FROM transactions 
                WHERE user_id = %s OR recipient_id = %s
                ORDER BY created_at DESC
                LIMIT 100
            """, (user_id, user_id))
            
            transactions = cursor.fetchall()
            print(f"[History] Found {len(transactions)} transactions")
            
            if not transactions:
                # Show the treeview with no rows, but still display the table
                pass
            else:
                for i, txn in enumerate(transactions):
                    sender = '-'
                    recipient = '-'
                    txn_type = txn['type']
                    if txn_type.lower() == 'withdrawal':
                        display_type = 'WITHDRAW'
                        direction = ''
                    elif txn_type.lower() == 'deposit':
                        display_type = 'DEPOSIT'
                        direction = ''
                    elif txn_type.lower() == 'transfer':
                        display_type = 'TRANSFER'
                        if txn['user_id'] == user_id:
                            direction = 'Sent'
                            sender = '(You)'
                            recipient = '-'
                            if txn.get('recipient_id'):
                                cursor.execute("SELECT email FROM users WHERE user_id = %s", (txn['recipient_id'],))
                                rec = cursor.fetchone()
                                if rec:
                                    recipient = rec['email']
                        elif txn.get('recipient_id') == user_id:
                            direction = 'Received'
                            recipient = '(You)'
                            sender = '-'
                            cursor.execute("SELECT email FROM users WHERE user_id = %s", (txn['user_id'],))
                            snd = cursor.fetchone()
                            if snd:
                                sender = snd['email']
                        else:
                            direction = ''
                            sender = '-'
                            recipient = '-'
                    else:
                        display_type = txn_type.upper()
                        direction = ''
                        sender = '-'
                        recipient = '-'
                    tag = 'evenrow' if i % 2 == 0 else 'oddrow'
                    tree.insert("", "end", values=(
                        txn['transaction_id'],
                        display_type,
                        direction,
                        f"{txn['amount']:,.2f}",
                        sender,
                        recipient,
                        txn['created_at'].strftime("%Y-%m-%d %H:%M:%S")
                    ), tags=(tag,))
                tree.tag_configure('evenrow', background='#f7fafd')
                tree.tag_configure('oddrow', background='#e3eaf3')
                
        except mysql.connector.Error as err:
            print(f"[History] Query failed: {err}")
            messagebox.showerror("Database Error", 
                f"Failed to load transactions:\n{err}\n\n"
                "Please check:\n"
                "1. Database connection\n"
                "2. Table structure\n"
                "3. User permissions")
            
    except Exception as e:
        print(f"[History] Unexpected error: {e}")
        messagebox.showerror("Error", f"Critical error: {e}")
    finally:
        if 'conn' in locals() and conn.is_connected():
            cursor.close()
            conn.close()