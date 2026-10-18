import tkinter as tk
from drink_dispenser import DrinkDispenser


class DrinkConfirmationDialog:

    def __init__(self, parent, recipe, glass_size, on_complete=None):
        self.parent = parent
        self.recipe = recipe
        self.glass_size = glass_size
        self.on_complete = on_complete
        self.timer_id = None

        self.dialog = tk.Toplevel(parent)
        self.dialog.attributes("-fullscreen", True)
        self.dialog.transient(parent)
        self.dialog.grab_set()
        self.dialog.configure(bg="#f0f0f0")

        self.dialog.rowconfigure(0, weight=0)
        self.dialog.rowconfigure(1, weight=1)
        self.dialog.rowconfigure(2, weight=0)
        self.dialog.columnconfigure(0, weight=1)
        self.dialog.columnconfigure(1, weight=1)

        title_label = tk.Label(
            self.dialog,
            text="Confirm Your Order",
            font=("Arial", 28, "bold"),
            bg="#f0f0f0",
            pady=20,
        )
        title_label.grid(row=0, column=0, columnspan=2, sticky="ew")

        details_frame = tk.Frame(self.dialog, bg="#ffffff", bd=2, relief="groove")
        details_frame.grid(row=1, column=0, columnspan=2, sticky="nsew", padx=40, pady=20)

        lbl_drink_title = tk.Label(
            details_frame,
            text=f"Drink: {recipe.name}",
            font=("Arial", 24, "bold"),
            bg="#ffffff",
            anchor="w",
        )
        lbl_drink_title.pack(fill=tk.X, padx=30, pady=(30, 10))

        lbl_size_title = tk.Label(
            details_frame,
            text=f"Glass: {glass_size['name']}",
            font=("Arial", 20),
            bg="#ffffff",
            anchor="w",
            fg="#555555",
        )
        lbl_size_title.pack(fill=tk.X, padx=30, pady=(0, 20))

        lbl_ing_header = tk.Label(
            details_frame,
            text="Ingredients:",
            font=("Arial", 18, "bold"),
            bg="#ffffff",
            anchor="w",
        )
        lbl_ing_header.pack(fill=tk.X, padx=30, pady=(10, 5))

        for ing in recipe.ingredients:
            lbl_ing = tk.Label(
                details_frame,
                text=f"• {ing.name}: {ing.amount_ml:.0f} ml",
                font=("Arial", 18),
                bg="#ffffff",
                anchor="w",
                fg="#333333",
            )
            lbl_ing.pack(fill=tk.X, padx=50, pady=2)

        # Action buttons using "Back" and "Pour Drink"
        btn_back = tk.Button(
            self.dialog,
            text="Back",
            font=("Arial", 22, "bold"),
            bg="#f8d7da",
            fg="#721c24",
            command=self.cancel_and_close,
            height=2,
        )
        btn_back.grid(row=2, column=0, sticky="nsew", padx=(40, 10), pady=30)

        btn_confirm = tk.Button(
            self.dialog,
            text="Pour Drink",
            font=("Arial", 22, "bold"),
            bg="#d1e7dd",
            fg="#0f5132",
            command=self.confirm_and_pour,
            height=2,
        )
        btn_confirm.grid(row=2, column=1, sticky="nsew", padx=(10, 40), pady=30)

        self.dialog.bind("<Any-ButtonPress>", self.reset_timeout)
        self.dialog.bind("<Any-KeyPress>", self.reset_timeout)
        self.reset_timeout()

    def reset_timeout(self, event=None):
        if self.timer_id:
            self.dialog.after_cancel(self.timer_id)
        self.timer_id = self.dialog.after(60000, self.auto_cancel)

    def auto_cancel(self):
        print("DrinkConfirmationDialog: Timed out due to inactivity, auto-canceling.")
        self.dialog.destroy()

    def cancel_and_close(self):
        if self.timer_id:
            self.dialog.after_cancel(self.timer_id)
        self.dialog.destroy()

    def confirm_and_pour(self):
        if self.timer_id:
            self.dialog.after_cancel(self.timer_id)

        print(f"Confirmed! Launching progress view for '{self.recipe.name}'")

        # Import and launch the progress bar window
        from ui.pouring_progress_dialog import PouringProgressDialog
        PouringProgressDialog(
            self.parent,
            self.recipe,
            self.glass_size,
            on_complete=self.on_complete
        )

        self.dialog.destroy()