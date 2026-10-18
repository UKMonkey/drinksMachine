import json
from pathlib import Path


class PumpStore:
    _pumps = {}  # Dictionary mapping pump_number (int) -> ingredient_name (str)

    # Define file path in the data directory
    BASE_DIR = Path(__file__).resolve().parent
    DATA_DIR = BASE_DIR / "data"
    CONFIG_FILE = DATA_DIR / "pump_config.json"

    @classmethod
    def _ensure_data_dir(cls):
        cls.DATA_DIR.mkdir(parents=True, exist_ok=True)

    @classmethod
    def load(cls):
        """Load pump configurations from the JSON file if it exists."""
        cls._pumps = {}
        if cls.CONFIG_FILE.exists():
            try:
                with open(cls.CONFIG_FILE, "r", encoding="utf-8") as f:
                    data = json.load(f)
                    # Convert string keys back to integers (JSON stores keys as strings)
                    cls._pumps = {int(k): v for k, v in data.items()}
                print(f"PumpStore: Loaded pump configuration from {cls.CONFIG_FILE}")
            except Exception as ex:
                print(f"PumpStore: Failed to load config file: {ex}")
        return cls._pumps

    @classmethod
    def save(cls):
        """Save current pump configurations to the JSON file."""
        cls._ensure_data_dir()
        try:
            with open(cls.CONFIG_FILE, "w", encoding="utf-8") as f:
                json.dump(cls._pumps, f, indent=4)
            print(f"PumpStore: Saved pump configuration to {cls.CONFIG_FILE}")
        except Exception as ex:
            print(f"PumpStore: Failed to save config file: {ex}")

    @classmethod
    def set_pump(cls, pump_number: int, ingredient_name: str):
        cls._pumps[pump_number] = ingredient_name
        cls.save()  # Automatically persist changes to disk
        print(f"PumpStore: Pump {pump_number} assigned to '{ingredient_name}'")

    @classmethod
    def get_pump(cls, pump_number: int):
        if not cls._pumps:
            cls.load()
        return cls._pumps.get(pump_number, None)

    @classmethod
    def get_all_pumps(cls):
        if not cls._pumps:
            cls.load()
        return cls._pumps