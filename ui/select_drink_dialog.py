import tkinter as tk
from recipe_store import RecipeStore
from pump_store import PumpStore
from ui.drink_confirmation_dialog import DrinkConfirmationDialog


class SelectDrinkDialog:

    def __init__(self, parent, glass_size, on_drink_selected):
        self.parent = parent
        self.glass_size = glass_size
        self.on_drink_selected = on_drink_selected
        self.timer_id = None

        self.dialog = tk.Toplevel(parent)
        self.dialog.attributes("-fullscreen", True)
        self.dialog.transient(parent)
        self.dialog.grab_set()
        self.dialog.configure(bg="#f0f0f0")

        # Title Label showing glass size context
        title_text = f"Select Drink ({glass_size['name']})"
        title_label = tk.Label(
            self.dialog,
            text=title_text,
            font=("Arial", 28, "bold"),
            bg="#f0f0f0",
            pady=20,
        )
        title_label.pack(side=tk.TOP, fill=tk.X)

        # Cancel / Back Button at the bottom
        btn_back = tk.Button(
            self.dialog,
            text="Cancel",
            font=("Arial", 20, "bold"),
            bg="#f8d7da",
            command=self.cancel_and_close,
            height=2,
        )
        btn_back.pack(side=tk.BOTTOM, fill=tk.X, padx=20, pady=20)

        # Scrollable container frame for touch devices
        container = tk.Frame(self.dialog, bg="#f0f0f0")
        container.pack(fill=tk.BOTH, expand=True, padx=20, pady=10)

        canvas = tk.Canvas(container, bg="#ffffff", highlightthickness=0)
        scrollbar = tk.Scrollbar(container, orient="vertical", command=canvas.yview)
        scrollbar.config(width=40)

        self.scrollable_frame = tk.Frame(canvas, bg="#ffffff")

        self.scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )

        canvas.create_window((0, 0), window=self.scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)

        canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        canvas.bind("<ButtonPress-1>", lambda event: canvas.scan_mark(event.x, event.y))
        canvas.bind("<B1-Motion>", lambda event: canvas.scan_dragto(event.x, event.y, gain=1))

        self.dialog.bind("<Any-ButtonPress>", self.reset_timeout)
        self.dialog.bind("<Any-KeyPress>", self.reset_timeout)

        self.populate_drinks()
        self.reset_timeout()

    def reset_timeout(self, event=None):
        if self.timer_id:
            self.dialog.after_cancel(self.timer_id)
        self.timer_id = self.dialog.after(60000, self.auto_cancel)

    def auto_cancel(self):
        print("SelectDrinkDialog: Timed out due to inactivity, auto-canceling.")
        self.dialog.destroy()

    def cancel_and_close(self):
        if self.timer_id:
            self.dialog.after_cancel(self.timer_id)
        self.dialog.destroy()

    def get_loaded_ingredients(self):
        return set(PumpStore.get_all_pumps().values())

    def populate_drinks(self):
        recipes = RecipeStore.get_recipes()
        loaded_ingredients = self.get_loaded_ingredients()
        normalized_loaded = {ing.lower() for ing in loaded_ingredients}

        if not recipes:
            lbl = tk.Label(
                self.scrollable_frame,
                text="No recipes found. Please update recipes.",
                font=("Arial", 18),
                bg="#ffffff",
                fg="#666666",
            )
            lbl.pack(pady=40, padx=20)
            return

        drink_items = []
        glass_capacity = self.glass_size.get("capacity_ml", 250)

        for recipe in recipes:
            recipe_ingredients = {ing.name.lower() for ing in recipe.ingredients}
            is_available = recipe_ingredients.issubset(normalized_loaded)

            # Re-calculating size volume check if capacity metric is available
            total_volume_ml = sum(ing.amount_ml for ing in recipe.ingredients)
            exceeds_90_percent = total_volume_ml > (glass_capacity * 0.9)

            drink_items.append({
                "recipe": recipe,
                "is_available": is_available,
                "exceeds_90_percent": exceeds_90_percent
            })

        # Sort by availability first, then alphabetically by name
        drink_items.sort(key=lambda x: (not x["is_available"], x["recipe"].name.lower()))

        for item in drink_items:
            recipe = item["recipe"]
            is_available = item["is_available"]
            exceeds_90_percent = item["exceeds_90_percent"]

            # Determine fill color based on rules
            if not is_available:
                fill_color = "#dc3545"  # Red (Missing ingredients)
            elif exceeds_90_percent:
                fill_color = "#ffc107"  # Amber (Exceeds 90% capacity)
            else:
                fill_color = "#28a745"  # Green (Valid and fits)

            row_frame = tk.Frame(self.scrollable_frame, bg="#ffffff")
            row_frame.pack(fill=tk.X, padx=10, pady=6)

            # If red or amber, we bypass selection action entirely by passing a no-op command,
            # or handling it gracefully inside select_drink.
            btn = tk.Button(
                row_frame,
                text=recipe.name,
                font=("Arial", 22),
                bg="#e0e0e0" if is_available and not exceeds_90_percent else "#f5f5f5",
                fg="#000000" if is_available and not exceeds_90_percent else "#888888",
                activebackground="#d0d0d0",
                anchor="w",
                padx=20,
                pady=15,
                command=lambda r=recipe, avail=is_available, warn=exceeds_90_percent: self.select_drink(r, avail, warn),
            )
            btn.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(0, 10))

            light_canvas = tk.Canvas(row_frame, width=40, height=40, bg="#ffffff", highlightthickness=0)
            light_canvas.pack(side=tk.RIGHT, padx=10)
            light_canvas.create_oval(8, 8, 32, 32, fill=fill_color, outline="")

    def select_drink(self, recipe, is_available, exceeds_90_percent):
        if self.timer_id:
            self.dialog.after_cancel(self.timer_id)

        # Ignore selection if the drink is Red (unavailable) or Amber (exceeds 90% capacity)
        if not is_available or exceeds_90_percent:
            print(
                f"Ignored selection for '{recipe.name}' (Available: {is_available}, Warning/Amber: {exceeds_90_percent})")
            # Restart timer and return without doing anything
            self.reset_timeout()
            return

        print(f"Drink selected: {recipe.name} with glass size {self.glass_size['name']}")

        DrinkConfirmationDialog(
            self.parent,
            recipe,
            self.glass_size,
            on_complete=self.dialog.destroy
        )
        self.dialog.destroy()