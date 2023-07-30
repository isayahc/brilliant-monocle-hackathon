import json
from pathlib import Path

def load_config(config_file_path):
    try:
        with open(config_file_path, 'r') as config_file:
            return json.load(config_file)
    except FileNotFoundError:
        print(f"Configuration file {config_file_path} not found.")
        return None
    except json.JSONDecodeError:
        print(f"Error decoding JSON from {config_file_path}.")
        return None

def config_exists(config_path):
    return Path(config_path).exists()
