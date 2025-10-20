import tkinter as tk
from tkinter import messagebox
from database_connection import create_connection

# Function to verify credentials
def verify_login(username, password):
    conn = create_connection()
    if not conn:
        messagebox.showerror("Database Error", "Unable to connect to database.")
        return False

    try:
        cursor = conn.cursor()
        query = "SELECT * FROM employees WHERE EmployeeID=%s AND Password=%s"
        cursor.execute(query, (username, password))
        user = cursor.fetchone()

        if user:
            return True
        else:
            messagebox.showerror("Login Failed", "User not found.")
            return False

    except Exception as e:
        messagebox.showerror("Error", f"Error during login: {e}")
        return False
    finally:
        conn.close()

# ------------------------------
# Main Login GUI
# ------------------------------
def login_window():
    window = tk.Tk()
    window.title("Movie Rental Management System - Login")
    window.geometry("400x300")
    window.config(bg="#f5f5f5")

    tk.Label(window, text="Employee Login", font=("Arial", 16, "bold"), bg="#f5f5f5").pack(pady=20)

    tk.Label(window, text="Username:", bg="#f5f5f5").pack()
    username_entry = tk.Entry(window, width=30)
    username_entry.pack(pady=5)

    tk.Label(window, text="Password:", bg="#f5f5f5").pack()
    password_entry = tk.Entry(window, show="*", width=30)
    password_entry.pack(pady=5)

    def handle_login():
        username = username_entry.get()
        password = password_entry.get()

        if verify_login(username, password):
            messagebox.showinfo("Login Successful", f"Welcome, {username}!")
            window.destroy()
            import gui.main_dashboard as dashboard
            dashboard.dashboard_window(username)

    tk.Button(window, text="Login", bg="#0078D7", fg="white", width=15, command=handle_login).pack(pady=20)

    window.mainloop()

# Entry point
if __name__ == "__main__":
    login_window()
