import tkinter as tk
from tkinter import ttk, messagebox
import mysql.connector
from datetime import datetime
import os
import re

DB_CONFIG = {
    'host': 'sql12.freesqldatabase.com',
    'user': 'sql12773881',
    'password': 'isUcpBumwQ',
    'database': 'sql12773881',
    'port': 3306
}

def center_window(window):
    window.update_idletasks()
    width = window.winfo_width()
    height = window.winfo_height()
    x = (window.winfo_screenwidth() // 2) - (width // 2)
    y = (window.winfo_screenheight() // 2) - (height // 2)
    window.geometry(f'{width}x{height}+{x}+{y}')

def get_user_details(user_id):
    conn = mysql.connector.connect(**DB_CONFIG)
    cursor = conn.cursor()
    cursor.execute('''
        SELECT first_name, middle_initial, family_name, email, address, phone_number
        FROM users WHERE user_id = %s
    ''', (user_id,))
    user = cursor.fetchone()
    conn.close()
    return user

def open_profile(user_id, first_name, back_callback):
    profile_window = tk.Tk()
    profile_window.title(f"Profile - {first_name}")
    profile_window.geometry("800x600")
    profile_window.resizable(False, False)
    profile_window.configure(bg='#ffffff')
    profile_window.overrideredirect(True)
    center_window(profile_window)

    # Title bar
    title_bar = tk.Frame(profile_window, bg='#34495e', height=40)
    title_bar.pack(fill=tk.X)
    title_bar.pack_propagate(False)

    # Title
    title_label = tk.Label(title_bar, text=f"Profile - {first_name}", font=('Helvetica', 12, 'bold'),
                          bg='#34495e', fg='white')
    title_label.pack(side=tk.LEFT, padx=10)

    # Close button
    close_btn = tk.Button(title_bar, text='×', font=('Helvetica', 13), bg='#34495e', fg='white',
                         bd=0, padx=10, command=lambda: [profile_window.destroy(), back_callback()])
    close_btn.pack(side=tk.RIGHT, padx=10)

    # Main content frame
    main_frame = tk.Frame(profile_window, bg='#ffffff')
    main_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)

    # Get user details
    user_details = get_user_details(user_id)
    if not user_details:
        messagebox.showerror("Error", "Could not fetch user details")
        profile_window.destroy()
        back_callback()
        return

    # Create labels for user details
    details_frame = tk.Frame(main_frame, bg='#ffffff')
    details_frame.pack(fill=tk.BOTH, expand=True, pady=20)

    # Style for labels
    label_font = ('Helvetica', 12)
    value_font = ('Helvetica', 12)

    # Create and pack labels with user details
    fields = [
        ("First Name", user_details[0]),
        ("Middle Initial", user_details[1]),
        ("Family Name", user_details[2]),
        ("Email", user_details[3]),
        ("Address", user_details[4]),
        ("Phone Number", user_details[5])
    ]

    for i, (label, value) in enumerate(fields):
        frame = tk.Frame(details_frame, bg='#ffffff')
        frame.pack(fill=tk.X, pady=5)
        
        label_widget = tk.Label(frame, text=f"{label}:", font=label_font, bg='#ffffff', width=15, anchor='w')
        label_widget.pack(side=tk.LEFT, padx=(0, 10))
        
        value_widget = tk.Label(frame, text=value, font=value_font, bg='#ffffff')
        value_widget.pack(side=tk.LEFT)

    # Edit Profile button
    edit_btn = tk.Button(main_frame, text='Edit Profile', font=('Helvetica', 12),
                        bg='#3498db', fg='white', bd=0, padx=20, pady=10,
                        command=lambda: [profile_window.destroy(), open_edit_profile(user_id, first_name, lambda: open_profile(user_id, first_name, back_callback))])
    edit_btn.pack(pady=20)

    # Make window draggable
    def start_move(event):
        profile_window.x = event.x
        profile_window.y = event.y

    def stop_move(event):
        profile_window.x = None
        profile_window.y = None

    def do_move(event):
        deltax = event.x - profile_window.x
        deltay = event.y - profile_window.y
        x = profile_window.winfo_x() + deltax
        y = profile_window.winfo_y() + deltay
        profile_window.geometry(f"+{x}+{y}")

    title_bar.bind("<ButtonPress-1>", start_move)
    title_bar.bind("<ButtonRelease-1>", stop_move)
    title_bar.bind("<B1-Motion>", do_move)

    profile_window.mainloop()

def open_edit_profile(user_id, first_name, back_callback):
    edit_window = tk.Tk()
    edit_window.title(f"Edit Profile - {first_name}")
    edit_window.geometry("800x600")
    edit_window.resizable(False, False)
    edit_window.configure(bg='#ffffff')
    edit_window.overrideredirect(True)
    center_window(edit_window)

    # Title bar
    title_bar = tk.Frame(edit_window, bg='#34495e', height=40)
    title_bar.pack(fill=tk.X)
    title_bar.pack_propagate(False)

    # Title
    title_label = tk.Label(title_bar, text=f"Edit Profile - {first_name}", font=('Helvetica', 12, 'bold'),
                          bg='#34495e', fg='white')
    title_label.pack(side=tk.LEFT, padx=10)

    # Close button
    close_btn = tk.Button(title_bar, text='×', font=('Helvetica', 13), bg='#34495e', fg='white',
                         bd=0, padx=10, command=lambda: [edit_window.destroy(), back_callback()])
    close_btn.pack(side=tk.RIGHT, padx=10)

    # Main content frame
    main_frame = tk.Frame(edit_window, bg='#ffffff')
    main_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)

    # Get user details
    user_details = get_user_details(user_id)
    if not user_details:
        messagebox.showerror("Error", "Could not fetch user details")
        edit_window.destroy()
        back_callback()
        return

    # Create entry fields for user details
    entries = {}
    fields = [
        ("First Name", user_details[0]),
        ("Middle Initial", user_details[1]),
        ("Family Name", user_details[2]),
        ("Email", user_details[3]),
        ("Address", user_details[4]),
        ("Phone Number", user_details[5])
    ]

    for i, (label, value) in enumerate(fields):
        frame = tk.Frame(main_frame, bg='#ffffff')
        frame.pack(fill=tk.X, pady=5)
        
        label_widget = tk.Label(frame, text=f"{label}:", font=('Helvetica', 12), bg='#ffffff', width=15, anchor='w')
        label_widget.pack(side=tk.LEFT, padx=(0, 10))
        
        entry = tk.Entry(frame, font=('Helvetica', 12), width=60)
        entry.insert(0, value)
        entry.pack(side=tk.LEFT)
        entries[label] = entry

    def save_changes():
        try:
            conn = mysql.connector.connect(**DB_CONFIG)
            cursor = conn.cursor()
            # Update user details
            cursor.execute('''
                UPDATE users SET
                first_name = %s,
                middle_initial = %s,
                family_name = %s,
                email = %s,
                address = %s,
                phone_number = %s
                WHERE user_id = %s
            ''', (
                entries["First Name"].get(),
                entries["Middle Initial"].get(),
                entries["Family Name"].get(),
                entries["Email"].get(),
                entries["Address"].get(),
                entries["Phone Number"].get(),
                user_id
            ))
            conn.commit()
            conn.close()
            messagebox.showinfo("Success", "Profile updated successfully!")
            edit_window.destroy()
            back_callback()
        except Exception as e:
            messagebox.showerror("Error", f"Failed to update profile: {str(e)}")

    # Save button
    save_btn = tk.Button(main_frame, text='Save Changes', font=('Helvetica', 12),
                        bg='#2ecc71', fg='white', bd=0, padx=20, pady=10,
                        command=save_changes)
    save_btn.pack(pady=20)

    # Make window draggable
    def start_move(event):
        edit_window.x = event.x
        edit_window.y = event.y

    def stop_move(event):
        edit_window.x = None
        edit_window.y = None

    def do_move(event):
        deltax = event.x - edit_window.x
        deltay = event.y - edit_window.y
        x = edit_window.winfo_x() + deltax
        y = edit_window.winfo_y() + deltay
        edit_window.geometry(f"+{x}+{y}")

    title_bar.bind("<ButtonPress-1>", start_move)
    title_bar.bind("<ButtonRelease-1>", stop_move)
    title_bar.bind("<B1-Motion>", do_move)

    edit_window.mainloop() 