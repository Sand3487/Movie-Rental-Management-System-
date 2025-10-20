import tkinter as tk
from tkinter import messagebox, ttk
from database_connection import create_connection

def movie_management_window(username):
    window = tk.Toplevel()
    window.title("🎬 Movie Management")
    window.geometry("900x600")
    window.config(bg="#e8f0f8")

    # ------------------------------
    # Top Bar
    # ------------------------------
    top_frame = tk.Frame(window, bg="#0078D7", height=60)
    top_frame.pack(fill="x")

    tk.Label(
        top_frame,
        text="🎬 Movie Management",
        font=("Arial", 24, "bold"),
        bg="#0078D7",
        fg="white"
    ).pack(pady=10)

    # ------------------------------
    # Form Section
    # ------------------------------
    form_frame = tk.Frame(window, bg="#e8f0f8")
    form_frame.pack(pady=20)

    labels = ["Movie ID:", "Title:", "Genre:", "Release Year:", "Rental Price:", "Producer ID:"]
    entries = {}

    for i, label_text in enumerate(labels):
        tk.Label(form_frame, text=label_text, font=("Arial", 12, "bold"), bg="#e8f0f8", fg="#2c3e50").grid(row=i, column=0, pady=5, sticky="e")
        entry = tk.Entry(form_frame, width=30, font=("Arial", 12))
        entry.grid(row=i, column=1, pady=5, padx=10)
        entries[label_text[:-1].lower().replace(" ", "_")] = entry

    # ------------------------------
    # Database Functions
    # ------------------------------
    def refresh_movies():
        for row in movie_table.get_children():
            movie_table.delete(row)
        conn = create_connection()
        if not conn:
            messagebox.showerror("Database Error", "Unable to connect to database.")
            return
        try:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM movies")
            for movie in cursor.fetchall():
                movie_table.insert("", "end", values=movie)
        except Exception as e:
            messagebox.showerror("Error", f"Error fetching movies: {e}")
        finally:
            conn.close()

    def add_movie():
        data = {key: entry.get() for key, entry in entries.items()}
        if not all(data.values()):
            messagebox.showwarning("Input Error", "All fields are required.")
            return
        conn = create_connection()
        if not conn:
            messagebox.showerror("Database Error", "Unable to connect to database.")
            return
        try:
            cursor = conn.cursor()
            query = """
            INSERT INTO movies (MovieID, Title, Genre, ReleaseYear, RentalPrice, ProducerID)
            VALUES (%s, %s, %s, %s, %s, %s)
            """
            cursor.execute(query, (
                data["movie_id"], data["title"], data["genre"], 
                data["release_year"], data["rental_price"], data["producer_id"]
            ))
            conn.commit()
            messagebox.showinfo("Success", "Movie added successfully.")
            refresh_movies()
        except Exception as e:
            messagebox.showerror("Error", f"Error adding movie: {e}")
        finally:
            conn.close()

    def update_movie():
        selected = movie_table.selection()
        if not selected:
            messagebox.showwarning("Selection Error", "Select a movie to update.")
            return
        movie_id = movie_table.item(selected[0])["values"][0]
        data = {key: entry.get() for key, entry in entries.items()}
        if not all(data.values()):
            messagebox.showwarning("Input Error", "All fields are required.")
            return
        conn = create_connection()
        if not conn:
            messagebox.showerror("Database Error", "Unable to connect to database.")
            return
        try:
            cursor = conn.cursor()
            query = """
            UPDATE movies 
            SET Title=%s, Genre=%s, ReleaseYear=%s, RentalPrice=%s, ProducerID=%s 
            WHERE MovieID=%s
            """
            cursor.execute(query, (
                data["title"], data["genre"], data["release_year"], data["rental_price"], data["producer_id"], movie_id
            ))
            conn.commit()
            messagebox.showinfo("Success", "Movie updated successfully.")
            refresh_movies()
        except Exception as e:
            messagebox.showerror("Error", f"Error updating movie: {e}")
        finally:
            conn.close()

    def delete_movie():
        selected = movie_table.selection()
        if not selected:
            messagebox.showwarning("Selection Error", "Select a movie to delete.")
            return
        movie_id = movie_table.item(selected[0])["values"][0]
        conn = create_connection()
        if not conn:
            messagebox.showerror("Database Error", "Unable to connect to database.")
            return
        try:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM rentals WHERE MovieID=%s", (movie_id,))
            if cursor.fetchone():
                messagebox.showwarning("Cannot Delete", "Movie has active rentals.")
                return
            cursor.execute("DELETE FROM movies WHERE MovieID=%s", (movie_id,))
            conn.commit()
            messagebox.showinfo("Success", "Movie deleted successfully.")
            refresh_movies()
        except Exception as e:
            messagebox.showerror("Error", f"Error deleting movie: {e}")
        finally:
            conn.close()

    # ------------------------------
    # Buttons
    # ------------------------------
    button_frame = tk.Frame(window, bg="#e8f0f8")
    button_frame.pack(pady=10)

    buttons = [
        ("Add Movie", add_movie),
        ("Update Movie", update_movie),
        ("Delete Movie", delete_movie)
    ]

    for text, command in buttons:
        btn = tk.Button(button_frame, text=text, bg="#0078D7", fg="black", width=15, height=2,
                        font=("Arial", 12, "bold"), relief="flat", cursor="hand2", command=command)
        btn.pack(side="left", padx=10)
        btn.bind("<Enter>", lambda e, b=btn: b.config(bg="#005bb5"))
        btn.bind("<Leave>", lambda e, b=btn: b.config(bg="#0078D7"))

    # Back Button
    def back_to_dashboard():
        window.destroy()
        import main_dashboard as dashboard
        dashboard.dashboard_window(username)

    back_button = tk.Button(button_frame, text="⬅ Back to Dashboard", bg="#28a745", fg="black",
                            width=20, height=2, font=("Arial", 12, "bold"), relief="flat", cursor="hand2",
                            command=back_to_dashboard)
    back_button.pack(side="left", padx=10)
    back_button.bind("<Enter>", lambda e: back_button.config(bg="#218838"))
    back_button.bind("<Leave>", lambda e: back_button.config(bg="#28a745"))

    # ------------------------------
    # Movie Table
    # ------------------------------
    table_frame = tk.Frame(window)
    table_frame.pack(pady=20, fill="both", expand=True)

    columns = ("MovieID", "Title", "Genre", "ReleaseYear", "RentalPrice", "ProducerID")
    movie_table = ttk.Treeview(table_frame, columns=columns, show="headings")
    for col in columns:
        movie_table.heading(col, text=col)
        movie_table.column(col, width=120)
    movie_table.pack(fill="both", expand=True)

    refresh_movies()
    window.mainloop()
