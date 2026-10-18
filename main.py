import tkinter as tk

from status_dialog import StatusDialog
from recipe_updater import RecipeUpdater
from recipe_loader import RecipeLoader

from pathlib import Path
from ui.recipe_update_dialogue import RecipeUpdateWindow
BASE_DIR = Path(__file__).resolve().parent
recipe_directory = BASE_DIR / "data"


class DrinksMachineApp:

    def __init__(self, root):
        self.root = root
        self.load_recipies()
        self.generate_main_screen()

    def generate_main_screen(self):
        root = self.root
        root.title("Drink Management System")

        # Make the window fullscreen
        root.attributes("-fullscreen", True)

        # Allow the grid cells to expand and fill the screen
        root.rowconfigure(0, weight=1)
        root.rowconfigure(1, weight=1)
        root.columnconfigure(0, weight=1)
        root.columnconfigure(1, weight=1)

        # Common styling for large, touch-friendly buttons
        btn_font = ("Arial", 24, "bold")

        # Top Left: Configure drinks
        btn_configure = tk.Button(
            root,
            text="Configure drinks",
            font=btn_font,
            command=self.configure_drinks,
            bg="#e0e0e0",
        )
        btn_configure.grid(row=0, column=0, sticky="nsew", padx=10, pady=10)

        # Top Right: Make drinks
        btn_make = tk.Button(
            root,
            text="Make drinks",
            font=btn_font,
            command=self.make_drinks,
            bg="#d1e7dd",
        )
        btn_make.grid(row=0, column=1, sticky="nsew", padx=10, pady=10)

        # Bottom Left: Update recipes
        btn_recipes = tk.Button(
            root,
            text="Update recipes",
            font=btn_font,
            command=self.update_recipes,
            bg="#fff3cd",
        )
        btn_recipes.grid(row=1, column=0, sticky="nsew", padx=10, pady=10)

        # Bottom Right: Settings
        btn_settings = tk.Button(
            root,
            text="Settings",
            font=btn_font,
            command=self.settings,
            bg="#f8d7da",
        )
        btn_settings.grid(row=1, column=1, sticky="nsew", padx=10, pady=10)

    def configure_drinks(self):
        print("Configure drinks clicked")

    def update_recipes(self):
        RecipeUpdateWindow(self.root)

    def load_recipies(self):
        loader = RecipeLoader()
        self.recipes = loader.load(recipe_directory / "drinksRecipes.txt")

    def make_drinks(self):
        print("Make drinks clicked")

    def settings(self):
        print("Settings clicked")


def main():
    root = tk.Tk()

    app = DrinksMachineApp(root)

    root.mainloop()


if __name__ == "__main__":
    main()
