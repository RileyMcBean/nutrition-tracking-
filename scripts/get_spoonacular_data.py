"""
This file is a script to request nutrient data from the spoonacular api
"""

import requests
import json
import os

DATA_DIR = "/Users/rileymcbean/nutrition-project/data/raw"
SPOONACULAR_API_KEY = '22c3d08e9c1e45c0a3d2176515d5dd3c'
SPOONACULAR_URL = f"https://api.spoonacular.com/recipes/716429/information?apiKey={SPOONACULAR_API_KEY}"

try:
    response = requests.get(SPOONACULAR_URL)
    response.raise_for_status()  # Raise HTTPError for bad responses (4xx or 5xx)
    data = response.json()

    # Ensure the directory exists
    os.makedirs(DATA_DIR, exist_ok=True)

    file_path = os.path.join(DATA_DIR, "recipe_716429.json")

    with open(file_path, "w") as f:
        json.dump(data, f, indent=4)

    print("Data saved!")
    print(data)

except requests.exceptions.RequestException as e:
    print(f"Error during API request: {e}")
except json.JSONDecodeError as e:
    print(f"Error decoding JSON response: {e}")
except OSError as e:
    print(f"Error writing to file: {e}")
except Exception as e:
    print(f"An unexpected error occurred: {e}")
