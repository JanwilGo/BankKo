import tkinter as tk
from tkinter import ttk

# Function to handle logout
def logout(dashboard_window):
    dashboard_window.destroy()
    import login

# Function to open the dashboard with user's name
def open_dashboard(full_name):
    dashboard_window = tk.Tk()
    dashboard_window.title("Banking System Dashboard")
    dashboard_window.geometry("600x500")
    dashboard_window.resizable(False, False)

    # Header Section
    header = tk.Frame(dashboard_window, bg="#2f80ed", padx=20, pady=15)
    header.pack(fill=tk.X)

    welcome_label = tk.Label(
        header,
        text=f"Welcome, {full_name}",
        font=("Arial", 20, "bold"),
        fg="white",
        bg="#2f80ed"
    )
    welcome_label.pack(side=tk.LEFT)

    logout_button = tk.Button(
        header,
        text="Log Out",
        command=lambda: logout(dashboard_window),
        bg="white",
        fg="#2f80ed",
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
        command=lambda: print("Deposit Button Pressed"),
        bg="#4CAF50",
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
        command=lambda: print("Withdraw Button Pressed"),
        bg="#F44336",
        fg="white",
        font=("Arial", 16, "bold"),
        relief=tk.FLAT,
        bd=0,
        padx=20,
        pady=15,
        cursor="hand2"
    )
    withdraw_button.pack(side=tk.LEFT, expand=True, fill=tk.X, padx=5)

    # View Transaction History Button
    history_button = tk.Button(
        button_frame,
        text="Transaction History",
        command=lambda: print("View History Button Pressed"),
        bg="#2196F3",
        fg="white",
        font=("Arial", 16, "bold"),
        relief=tk.FLAT,
        bd=0,
        padx=20,
        pady=15,
        cursor="hand2"
    )
    history_button.pack(side=tk.LEFT, expand=True, fill=tk.X, padx=5)

    # Settings Button
    settings_button = tk.Button(
        button_frame,
        text="Settings",
        command=lambda: print("Settings Button Pressed"),
        bg="#FF9800",
        fg="white",
        font=("Arial", 16, "bold"),
        relief=tk.FLAT,
        bd=0,
        padx=20,
        pady=15,
        cursor="hand2"
    )
    settings_button.pack(side=tk.LEFT, expand=True, fill=tk.X, padx=5)

    dashboard_window.mainloop()

# For testing
if __name__ == "__main__":
    open_dashboard("janwil")
