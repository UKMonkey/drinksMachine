import tkinter as tk


class StatusDialog:

    @staticmethod
    def show(parent, message, bg_colour="#d1e7dd"):
        dialog = tk.Toplevel(parent)

        # Remove title bar
        dialog.overrideredirect(True)

        # Make modal
        dialog.transient(parent)
        dialog.grab_set()

        # Centre on screen
        width = 800
        height = 400

        screen_width = dialog.winfo_screenwidth()
        screen_height = dialog.winfo_screenheight()

        x = (screen_width - width) // 2
        y = (screen_height - height) // 2

        dialog.geometry(f"{width}x{height}+{x}+{y}")

        dialog.configure(bg=bg_colour)

        tk.Label(
            dialog,
            text=message,
            font=("Arial", 24, "bold"),
            bg=bg_colour,
            wraplength=700,
        ).pack(expand=True)

        tk.Button(
            dialog,
            text="OK",
            font=("Arial", 20, "bold"),
            command=dialog.destroy,
            width=10,
        ).pack(pady=30)

        parent.wait_window(dialog)
