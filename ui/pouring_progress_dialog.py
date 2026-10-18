import tkinter as tk
from tkinter import ttk
import threading
from drink_dispenser import DrinkDispenser


class PouringProgressDialog:

    def __init__(self, parent, recipe, glass_size, on_complete=None):
        self.parent = parent
        self.recipe = recipe
        self.glass_size = glass_size
        self.on_complete = on_complete

        self.dialog = tk.Toplevel(parent)
        self.dialog.attributes("-fullscreen", True)
        self.dialog.transient(parent)
        self.dialog.grab_set()
        self.dialog.configure(bg="#f0f0f0")

        self.dialog.rowconfigure(0, weight=1)
        self.dialog.columnconfigure(0, weight=1)

        # Main centered card container
        self.content_frame = tk.Frame(self.dialog, bg="#ffffff", bd=2, relief="groove")
        self.content_frame.grid(row=0, column=0, sticky="nsew", padx=60, pady=60)

        self.content_frame.rowconfigure(0, weight=1)
        self.content_frame.rowconfigure(1, weight=1)
        self.content_frame.rowconfigure(2, weight=1)
        self.content_frame.columnconfigure(0, weight=1)

        self.lbl_title = tk.Label(
            self.content_frame,
            text=f"Pouring: {recipe.name}",
            font=("Arial", 32, "bold"),
            bg="#ffffff",
        )
        self.lbl_title.grid(row=0, column=0, pady=20)

        # Progress bar configuration
        self.progress_var = tk.IntVar(value=0)
        self.progress_bar = ttk.Progressbar(
            self.content_frame,
            orient="horizontal",
            length=600,
            mode="determinate",
            variable=self.progress_var,
        )
        self.progress_bar.grid(row=1, column=0, padx=40, pady=20, sticky="ew")

        # Status percentage label
        self.lbl_status = tk.Label(
            self.content_frame,
            text="Initializing pumps...",
            font=("Arial", 20),
            bg="#ffffff",
            fg="#555555",
        )
        self.lbl_status.grid(row=2, column=0, pady=20)

        # Kick off background pouring task
        self.start_dispensing()

    def start_dispensing(self):
        def run_dispenser():
            def update_progress(percent):
                self.dialog.after(0, lambda: self.set_progress(percent))

            DrinkDispenser.make_drink(
                self.recipe,
                self.glass_size,
                progress_callback=update_progress
            )

            # Transition to the enjoy screen on the main thread once done
            self.dialog.after(0, self.show_enjoy_screen)

        threading.Thread(target=run_dispenser, daemon=True).start()

    def set_progress(self, percent):
        self.progress_var.set(percent)
        self.lbl_status.config(text=f"Pouring in progress... {percent}%")

    def show_enjoy_screen(self):
        # Hide the progress bar
        self.progress_bar.grid_forget()

        # Update text to greet the user
        self.lbl_title.config(text=f"Enjoy your {self.recipe.name}!")
        self.lbl_status.config(text="Please take your drink. Returning shortly...")

        # Wait 5 seconds (5000 ms) before finally closing and returning
        self.dialog.after(5000, self.finish_pouring)

    def finish_pouring(self):
        print("PouringProgressDialog: Finished, returning to dashboard.")
        if self.on_complete:
            self.on_complete()
        self.dialog.destroy()