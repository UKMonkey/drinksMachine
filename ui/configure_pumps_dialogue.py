import tkinter as tk


class ConfigurePumpsDialog:

    def __init__(self, parent):
        self.parent = parent
        self.dialog = tk.Toplevel(parent)

        # Make fullscreen and modal
        self.dialog.attributes("-fullscreen", True)
        self.dialog.transient(parent)
        self.dialog.grab_set()

        self.dialog.configure(bg="#f0f0f0")

        # Configure layout grid (3 rows, 2 columns for pumps, plus row for Back button)
        self.dialog.rowconfigure(0, weight=1)
        self.dialog.rowconfigure(1, weight=1)
        self.dialog.rowconfigure(2, weight=1)
        self.dialog.rowconfigure(3, weight=0)  # For back button row
        self.dialog.columnconfigure(0, weight=1)
        self.dialog.columnconfigure(1, weight=1)

        btn_font = ("Arial", 22, "bold")

        # Create 6 pump selection buttons
        for pump_index in range(1, 7):
            row = (pump_index - 1) // 2
            col = (pump_index - 1) % 2

            btn = tk.Button(
                self.dialog,
                text=f"Select drink for Pump {pump_index}",
                font=btn_font,
                bg="#e0e0e0",
                command=lambda p=pump_index: self.select_drink_for_pump(p),
            )
            btn.grid(row=row, column=0 if col == 0 else 1, sticky="nsew", padx=10, pady=10)

        # Return / Back button spanning both columns at the bottom
        btn_back = tk.Button(
            self.dialog,
            text="Back",
            font=btn_font,
            bg="#f8d7da",
            command=self.dialog.destroy,
            height=2,
        )
        btn_back.grid(row=3, column=0, columnspan=2, sticky="nsew", padx=10, pady=10)

    def select_drink_for_pump(self, pump_number):
        print(f"Configure clicked for Pump {pump_number}")
        # Placeholder: You can access recipes globally using RecipeStore.get_recipes() here later