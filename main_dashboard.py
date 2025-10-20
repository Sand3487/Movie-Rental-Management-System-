import tkinter as tk
from tkinter import messagebox

def dashboard_window(username):
    # Create main window
    window = tk.Tk()
    window.title("Movie Rental Management System")
    window.geometry("600x700")
    window.config(bg="#e8f0f8")

    # ------------------------------
    # Top Bar (Title + Logout)
    # ------------------------------
    top_frame = tk.Frame(window, bg="#0078D7", height=60)
    top_frame.pack(fill="x")

    # Dashboard Title (Left)
    tk.Label(
        top_frame,
        text=f" Main Dashboard",
        font=("Arial", 35, "bold"),
        bg="#0078D7",
        fg="white"
    ).pack(side="top", padx=20, pady=10)

    # Logout Function
    def logout():
        messagebox.showinfo("Logout", "Logging out...")
        window.destroy()
        import login
        login.login_window()

    # Logout Button (Right)
    logout_button = tk.Button(
        top_frame,
        text="🔒 Logout",
        bg="#DC3545",
        fg="black",
        font=("Arial", 11, "bold"),
        relief="flat",
        cursor="hand2",
        command=logout
    )
    logout_button.pack(side="right", padx=20, pady=10)

    # Hover effect for logout button
    def on_logout_enter(e):
        e.widget["background"] = "#b02a37"
    def on_logout_leave(e):
        e.widget["background"] = "#DC3545"
    logout_button.bind("<Enter>", on_logout_enter)
    logout_button.bind("<Leave>", on_logout_leave)

    # ------------------------------
    # Welcome Section
    # ------------------------------
    tk.Label(
        window,
        text=f"Welcome, {username}",
        font=("Arial", 18, "bold"),
        bg="#e8f0f8",
        fg="#2c3e50"
    ).pack(pady=25)

    tk.Label(
        window,
        text="Select Management Option",
        font=("Arial", 35, "bold"),
        bg="#e8f0f8",
        fg="#2c3e50"
    ).pack(pady=15)

    # ------------------------------
    # Main Buttons (Center)
    # ------------------------------
    button_frame = tk.Frame(window, bg="#e8f0f8")
    button_frame.pack(pady=30)

    BUTTON_WIDTH = 40
    BUTTON_HEIGHT = 3
    BUTTON_FONT = ("Arial", 16, "bold")
    BUTTON_BG = "#0078D7"
    BUTTON_FG = "black"

    def on_enter(e):
        e.widget["background"] = "#005bb5"
    def on_leave(e):
        e.widget["background"] = BUTTON_BG

    # Placeholder functions for other management sections
    def open_movie_management():
        messagebox.showinfo("Movie Management", "Open Movie Management Window")

    def open_customer_management():
        messagebox.showinfo("Customer Management", "Open Customer Management Window")

    def open_rental_management():
        messagebox.showinfo("Rental Management", "Open Rental Management Window")

    # Buttons List (Single Column)
    buttons = [
        ("🎬  Movie Management", open_movie_management),
        ("👤  Customer Management", open_customer_management),
        ("🎟  Rental Management", open_rental_management)
    ]

    for text, command in buttons:
        btn = tk.Button(
            button_frame,
            text=text,
            bg=BUTTON_BG,
            fg=BUTTON_FG,
            width=BUTTON_WIDTH,
            height=BUTTON_HEIGHT,
            font=BUTTON_FONT,
            relief="flat",
            cursor="hand2",
            command=command
        )
        btn.pack(pady=15)
        btn.bind("<Enter>", on_enter)
        btn.bind("<Leave>", on_leave)

    # ------------------------------
    # Footer
    # ------------------------------
    tk.Label(
        window,
        text="© 2025 Movie Rental Management System",
        font=("Arial", 10),
        bg="#e8f0f8",
        fg="gray"
    ).pack(side="bottom", pady=20)

    window.mainloop()


# Run standalone for testing
if __name__ == "__main__":
    dashboard_window("Admin")
