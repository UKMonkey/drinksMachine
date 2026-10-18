import tkinter as tk
from recipe_updater import RecipeUpdater
from recipe_store import RecipeStore


class RecipeUpdateDialog:

    def __init__(self, parent):
        self.parent = parent
        self.dialog = tk.Toplevel(parent)

        # Make fullscreen and modal
        self.dialog.attributes("-fullscreen", True)
        self.dialog.transient(parent)
        self.dialog.grab_set()

        # Initial processing state styling
        self.bg_colour = "#fff3cd"
        self.dialog.configure(bg=self.bg_colour)

        self.label = tk.Label(
            self.dialog,
            text="Updating recipes, please wait...",
            font=("Arial", 28, "bold"),
            bg=self.bg_colour,
            wraplength=700,
        )
        self.label.pack(expand=True)

        # Force window to render the processing state before executing code
        self.dialog.update_idletasks()
        self.parent.after(100, self.run_update)

    def run_update(self):
        try:
            updater = RecipeUpdater()
            source, destination = updater.update()

            # Reload the global recipes after a successful update
            RecipeStore.load()

            message = f"Recipes updated successfully\n\n{destination}"
            bg_colour = "#d1e7dd"  # Success green
            self.show_result(message, bg_colour)

        except Exception as ex:
            print(f"Recipe update failed: {ex}")
            message = f"Recipe update failed\n\n{ex}"
            bg_colour = "#f8d7da"  # Error red
            self.show_result(message, bg_colour)

    def show_result(self, message, bg_colour):
        # Update window background and message
        self.dialog.configure(bg=bg_colour)
        self.label.configure(text=message, bg=bg_colour)

        # Add OK button to dismiss and return to main window
        btn_ok = tk.Button(
            self.dialog,
            text="OK",
            font=("Arial", 24, "bold"),
            command=self.dialog.destroy,
            width=12,
        )
        btn_ok.pack(pady=40)