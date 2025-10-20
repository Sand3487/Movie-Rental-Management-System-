import tkinter as tk
from tkinter import messagebox
from database_connection import create_connection
import main_dashboard as dashboard  

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
# Main Login GUI (Matching Dashboard Style)
# ------------------------------
def login_window():
    window = tk.Tk()
    window.title("Movie Rental Management System - Login")
    window.geometry("500x400")
    window.config(bg="#e8f0f8")

    # ------------------------------
    # Top Bar
    # ------------------------------
    top_frame = tk.Frame(window, bg="#0078D7", height=70)
    top_frame.pack(fill="x")

    tk.Label(
        top_frame,
        text="Employee Login",
        font=("Arial", 28, "bold"),
        bg="#0078D7",
        fg="white"
    ).pack(pady=15)

    # ------------------------------
    # Login Section
    # ------------------------------

    form_frame = tk.Frame(window, bg="#e8f0f8")
    form_frame.pack(pady=10)

    tk.Label(form_frame, text="Username:", bg="#e8f0f8", font=("Arial", 12, "bold"), fg="#2c3e50").grid(row=0, column=0, pady=10, sticky="e")
    username_entry = tk.Entry(form_frame, width=30, font=("Arial", 12))
    username_entry.grid(row=0, column=1, pady=10, padx=10)

    tk.Label(form_frame, text="Password:", bg="#e8f0f8", font=("Arial", 12, "bold"), fg="#2c3e50").grid(row=1, column=0, pady=10, sticky="e")
    password_entry = tk.Entry(form_frame, show="*", width=30, font=("Arial", 12))
    password_entry.grid(row=1, column=1, pady=10, padx=10)

    # ------------------------------
    # Handle Login
    # ------------------------------
    def handle_login():
        username = username_entry.get()
        password = password_entry.get()

        if verify_login(username, password):
            messagebox.showinfo("Login Successful", f"Welcome, {username}!")
            window.destroy()
            dashboard.dashboard_window(username)

    # ------------------------------
    # Login Button (Matching Dashboard)
    # ------------------------------
    login_button = tk.Button(
        window,
        text="Login",
        bg="#0078D7",
        fg="black",
        width=20,
        height=2,
        font=("Arial", 13, "bold"),
        relief="flat",
        cursor="hand2",
        command=handle_login
    )
    login_button.pack(pady=30)

    # Hover effect
    def on_enter(e):
        e.widget["background"] = "#005bb5"
    def on_leave(e):
        e.widget["background"] = "#0078D7"
    login_button.bind("<Enter>", on_enter)
    login_button.bind("<Leave>", on_leave)

    # ------------------------------
    # Footer
    # ------------------------------
    tk.Label(
        window,
        text="© 2025 Movie Rental Management System",
        font=("Arial", 10),
        bg="#e8f0f8",
        fg="gray"
    ).pack(side="bottom", pady=15)

    window.mainloop()


# Entry point
if __name__ == "__main__":
    login_window()
