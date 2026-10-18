import tkinter as tk
from ui.glass_size_dialog import GlassSizeDialog
from ui.select_drink_dialog import SelectDrinkDialog


class MakeDrinksDialog:

    def __init__(self, parent):
        self.parent = parent
        self.dialog = tk.Toplevel(parent)

        # Make fullscreen and modal
        self.dialog.attributes("-fullscreen", True)
        self.dialog.transient(parent)
        self.dialog.grab_set()

        self.dialog.configure(bg="#f0f0f0")

        # Layout hierarchy: major top section for 'New Drink', minor bottom section for 'Back'
        self.dialog.rowconfigure(0, weight=4)
        self.dialog.rowconfigure(1, weight=1)
        self.dialog.columnconfigure(0, weight=1)

        # Very prominent 'New Drink' button
        btn_new_drink = tk.Button(
            self.dialog,
            text="New Drink",
            font=("Arial", 36, "bold"),
            bg="#d1e7dd",  # Welcoming success green
            activebackground="#b8e2ce",
            command=self.start_new_drink,
        )
        btn_new_drink.grid(row=0, column=0, sticky="nsew", padx=50, pady=(50, 20))

        # Much less prominent 'Back' button
        btn_back = tk.Button(
            self.dialog,
            text="Back",
            font=("Arial", 16),
            bg="#e0e0e0",
            fg="#555555",
            activebackground="#d0d0d0",
            command=self.dialog.destroy,
            width=12,
            height=1,
        )
        btn_back.grid(row=1, column=0, sticky="s", pady=(0, 40))

    def start_new_drink(self):
        # Step 1: Open Glass Size selection and hand it a callback
        GlassSizeDialog(self.dialog, self.on_glass_size_chosen)

    def on_glass_size_chosen(self, size_info):
        print(f"Glass size chosen: {size_info['name']}. Opening drink selector...")
        # Step 2: Once glass size is returned, open the drink selector window
        SelectDrinkDialog(self.dialog, size_info, self.on_drink_chosen_complete)

    def on_drink_chosen_complete(self, recipe, size_info):
        print(f"Ready to pour: '{recipe.name}' into '{size_info['name']}' (multiplier: {size_info['multiplier']})")
        # Step 3: Trigger pump hardware dispensing logic here next!