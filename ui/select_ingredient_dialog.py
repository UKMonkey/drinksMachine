import tkinter as tk
from recipe_store import RecipeStore
from pump_store import PumpStore


class SelectIngredientDialog:

    def __init__(self, parent, pump_number, on_ingredient_selected):
        self.parent = parent
        self.pump_number = pump_number
        self.on_ingredient_selected = on_ingredient_selected

        self.dialog = tk.Toplevel(parent)
        self.dialog.attributes("-fullscreen", True)
        self.dialog.transient(parent)
        self.dialog.grab_set()
        self.dialog.configure(bg="#f0f0f0")

        # Title Label
        title_label = tk.Label(
            self.dialog,
            text=f"Select Ingredient for Pump {pump_number}",
            font=("Arial", 24, "bold"),
            bg="#f0f0f0",
            pady=20,
        )
        title_label.pack(side=tk.TOP, fill=tk.X)

        # Back / Cancel Button at the bottom
        btn_back = tk.Button(
            self.dialog,
            text="Cancel",
            font=("Arial", 20, "bold"),
            bg="#f8d7da",
            command=self.dialog.destroy,
            height=2,
        )
        btn_back.pack(side=tk.BOTTOM, fill=tk.X, padx=20, pady=20)

        # Create a scrollable frame container for touch devices
        container = tk.Frame(self.dialog, bg="#f0f0f0")
        container.pack(fill=tk.BOTH, expand=True, padx=20, pady=10)

        canvas = tk.Canvas(container, bg="#ffffff", highlightthickness=0)
        scrollbar = tk.Scrollbar(container, orient="vertical", command=canvas.yview)

        # Make scrollbar thick enough for touch screen usage
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

        # Enable drag-to-scroll / touch scrolling on canvas
        canvas.bind("<ButtonPress-1>", lambda event: canvas.scan_mark(event.x, event.y))
        canvas.bind("<B1-Motion>", lambda event: canvas.scan_dragto(event.x, event.y, gain=1))

        # Populate the unique ingredients list
        self.populate_ingredients()

    def get_all_ingredients(self):
        # Extract unique ingredient names from all known recipes in RecipeStore
        ingredients_set = set()
        for recipe in RecipeStore.get_recipes():
            for ingredient in recipe.ingredients:
                ingredients_set.add(ingredient.name)
        return sorted(list(ingredients_set))

    def populate_ingredients(self):
        ingredients = self.get_all_ingredients()

        if not ingredients:
            lbl = tk.Label(
                self.scrollable_frame,
                text="No ingredients found. Check recipes.",
                font=("Arial", 18),
                bg="#ffffff",
                fg="#666666",
            )
            lbl.pack(pady=40, padx=20)
            return

        for ingredient_name in ingredients:
            btn = tk.Button(
                self.scrollable_frame,
                text=ingredient_name,
                font=("Arial", 22),
                bg="#e0e0e0",
                anchor="w",
                padx=20,
                pady=15,
                command=lambda name=ingredient_name: self.select_ingredient(name),
            )
            btn.pack(fill=tk.X, padx=10, pady=5)

    def select_ingredient(self, ingredient_name):
        PumpStore.set_pump(self.pump_number, ingredient_name)

        if self.on_ingredient_selected:
            self.on_ingredient_selected(self.pump_number, ingredient_name)

        self.dialog.destroy()