import tkinter as tk
from ui.select_ingredient_dialog import SelectIngredientDialog
from pump_store import PumpStore


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

        self.btn_font = ("Arial", 20, "bold")
        self.pump_buttons = {}

        # Create 6 pump selection buttons
        for pump_index in range(1, 7):
            row = (pump_index - 1) // 2
            col = (pump_index - 1) % 2

            btn = tk.Button(
                self.dialog,
                text=self.get_button_text(pump_index),
                font=self.btn_font,
                bg="#e0e0e0",
                command=lambda p=pump_index: self.select_drink_for_pump(p),
            )
            btn.grid(row=row, column=0 if col == 0 else 1, sticky="nsew", padx=10, pady=10)
            self.pump_buttons[pump_index] = btn

        # Return / Back button spanning both columns at the bottom
        btn_back = tk.Button(
            self.dialog,
            text="Back",
            font=self.btn_font,
            bg="#f8d7da",
            command=self.dialog.destroy,
            height=2,
        )
        btn_back.grid(row=3, column=0, columnspan=2, sticky="nsew", padx=10, pady=10)

    def get_button_text(self, pump_number):
        assigned_ingredient = PumpStore.get_pump(pump_number)
        if assigned_ingredient:
            return f"Pump {pump_number}\n[{assigned_ingredient}]"
        return f"Pump {pump_number}\n(Unassigned)"

    def select_drink_for_pump(self, pump_number):
        SelectIngredientDialog(self.dialog, pump_number, self.on_ingredient_chosen)

    def on_ingredient_chosen(self, pump_number, ingredient_name):
        # Refresh the button text to show the newly assigned ingredient
        if pump_number in self.pump_buttons:
            self.pump_buttons[pump_number].config(text=self.get_button_text(pump_number))