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

def show_transaction_history(user_id, back_func=None):
    print(f"\n[History] Loading transactions for user {user_id}")
    try:
        conn = mysql.connector.connect(**DB_CONFIG)
        cursor = conn.cursor(dictionary=True)
        
        cursor.execute("SELECT user_id FROM users WHERE user_id = %s", (user_id,))
        if not cursor.fetchone():
            messagebox.showerror("Error", f"User ID {user_id} not found!")
            return

        # Create window
        history_window = tk.Toplevel()
        history_window.title("Transaction History")
        history_window.geometry("1100x600")
        history_window.configure(bg='#ffffff')
        history_window.resizable(False, False)  # Disable window resizing
        
        # Remove minimize/maximize buttons (Windows)
        history_window.attributes('-toolwindow', 1)
        
        center_window(history_window)

        # Set up window close protocol
        if back_func:
            history_window.protocol("WM_DELETE_WINDOW", lambda: [history_window.destroy(), back_func()])
        
        # Title bar (matching dashboard style)
        title_bar = tk.Frame(history_window, bg='#34495e', height=30)
        title_bar.pack(fill=tk.X)
        title_bar.bind('<Button-1>', lambda e: history_window.focus_set())
        title_bar.bind('<B1-Motion>', lambda e: history_window.geometry(f'+{e.x_root}+{e.y_root}'))

        # Back button in title bar
        if back_func:
            back_btn = tk.Button(title_bar, text='← Back', font=('Helvetica', 10), bg='#34495e', fg='white',
                               bd=0, padx=10, command=lambda: [history_window.destroy(), back_func()])
            back_btn.pack(side=tk.LEFT, padx=10)
            back_btn.bind('<Enter>', on_enter)
            back_btn.bind('<Leave>', on_leave)
        
        # Content
        content = tk.Frame(history_window, bg='#ffffff', padx=40, pady=30)
        content.pack(fill=tk.BOTH, expand=True)

        # Title
        tk.Label(
            content,
            text="Transaction History",
            font=("Helvetica", 24, "bold"),
            fg="#34495e",
            bg="#ffffff"
        ).pack(pady=(0, 30))
        
        # Table Frame
        table_outer = tk.Frame(content, bg='#ffffff')
        table_outer.pack(fill=tk.BOTH, expand=True)
        table_box = tk.Frame(table_outer, bg='#ffffff', bd=0, highlightbackground="#bdc3c7", highlightthickness=1)
        table_box.pack(fill=tk.BOTH, expand=True)
        
        # Configure style
        style = ttk.Style()
        style.configure("Treeview", 
                       background="#ffffff",
                       foreground="#000000",
                       fieldbackground="#ffffff",
                       borderwidth=0,
                       font=('Helvetica', 10))
        style.configure("Treeview.Heading",
                       background="#34495e",
                       foreground="#000000",
                       relief="flat",
                       font=('Helvetica', 10, 'bold'))
        style.map("Treeview.Heading",
                 background=[('active', '#2c3e50')])
        
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
        
        # Get transactions
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
                tree.tag_configure('evenrow', background='#ffffff')
                tree.tag_configure('oddrow', background='#f8f9fa')
                
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