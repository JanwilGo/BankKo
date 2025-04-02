import tkinter as tk

def logout(dashboard_window):
    dashboard_window.destroy()
    import login  # Reopen the login screen

def open_dashboard():
    dashboard_window = tk.Tk()
    dashboard_window.title("Banking System Dashboard")
    dashboard_window.geometry("300x200")
    
    tk.Label(dashboard_window, text="Welcome to Your Dashboard", font=("Arial", 12)).pack(pady=20)
    
    btn_logout = tk.Button(dashboard_window, text="Logout", command=lambda: logout(dashboard_window))
    btn_logout.pack(pady=10)
    
    dashboard_window.mainloop()

if __name__ == "__main__":
    open_dashboard()
