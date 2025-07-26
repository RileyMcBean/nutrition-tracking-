"""
This script iteratively fetches ingredient data from the Spoonacular API.
It searches for ingredients for each letter of the alphabet, gets detailed
information for each ingredient, and saves it to a JSON file.
It keeps track of fetched ingredients to avoid duplicate requests.
"""

import requests
import json
import os
import string
import time
import logging
from dotenv import load_dotenv

# --- Configuration ---
load_dotenv()

# Set up basic logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# API and Path Configuration
BASE_URL = "https://api.spoonacular.com"
API_KEY = os.getenv("SPOONACULAR_API_KEY")

# Construct a path relative to the script file for better portability
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_ROOT = os.path.dirname(SCRIPT_DIR)
DATA_DIR = os.path.join(PROJECT_ROOT, "data", "raw", "spoonacular_ingredients")

# --- Helper Functions ---

def fetch_ingredients(query, limit=10):
    """Fetches a list of ingredients using a search term."""
    if not API_KEY:
        logging.error("SPOONACULAR_API_KEY not found. Please set it in your .env file.")
        return None

    url = f"{BASE_URL}/food/ingredients/search"
    params = {"query": query, "number": limit, "apiKey": API_KEY}
    try:
        response = requests.get(url, params=params)
        response.raise_for_status()
        return response.json().get("results", [])
    except requests.exceptions.RequestException as e:
        logging.error(f"API request failed for ingredient search '{query}': {e}")
        return None
    except json.JSONDecodeError:
        logging.error(f"Failed to decode JSON for ingredient search '{query}'. Response: {response.text}")
        return None

def fetch_ingredient_info(ingredient_id, amount=100, unit="grams"):
    """Gets detailed nutritional information for a given ingredient ID."""
    if not API_KEY:
        logging.error("SPOONACULAR_API_KEY not found.")
        return None

    url = f"{BASE_URL}/food/ingredients/{ingredient_id}/information"
    params = {"amount": amount, "unit": unit, "apiKey": API_KEY}
    try:
        response = requests.get(url, params=params)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        logging.error(f"API request failed for ingredient info ID {ingredient_id}: {e}")
        return None
    except json.JSONDecodeError:
        logging.error(f"Failed to decode JSON for ingredient info ID {ingredient_id}. Response: {response.text}")
        return None

# --- Main Execution ---

def main():
    """Main function to orchestrate the ingredient data fetching process."""
    os.makedirs(DATA_DIR, exist_ok=True)

    # Load the set of already fetched ingredient IDs to avoid re-fetching
    fetched_ids_file = os.path.join(DATA_DIR, "fetched_ids.json")
    fetched_ids = set()
    if os.path.exists(fetched_ids_file):
        try:
            with open(fetched_ids_file, "r") as f:
                fetched_ids = set(json.load(f))
            logging.info(f"Loaded {len(fetched_ids)} previously fetched ingredient IDs.")
        except (json.JSONDecodeError, TypeError):
             logging.warning(f"Could not read {fetched_ids_file}. Starting with an empty set of fetched IDs.")

    # Iterate over the alphabet to find a variety of ingredients
    for letter in list(string.ascii_lowercase):
        logging.info(f"--- Searching for ingredients starting with '{letter}' ---")
        ingredients = fetch_ingredients(letter, limit=5) # Adjust limit as needed

        if ingredients is None:
            continue

        for ing in ingredients:
            ing_id = ing.get("id")
            if ing_id and ing_id not in fetched_ids:
                logging.info(f"Fetching details for new ingredient: {ing.get('name')} (ID: {ing_id})")
                details = fetch_ingredient_info(ing_id)
                if details:
                    file_path = os.path.join(DATA_DIR, f"ingredient_{ing_id}.json")
                    with open(file_path, "w") as f:
                        json.dump(details, f, indent=4)
                    fetched_ids.add(ing_id)
                    logging.info(f"Successfully saved data for: {details.get('name')}")
                time.sleep(1) # Be a good API citizen

    # Save the updated set of fetched IDs
    with open(fetched_ids_file, "w") as f:
        json.dump(list(fetched_ids), f, indent=4)
    logging.info(f"Finished. Total unique ingredients fetched: {len(fetched_ids)}. Updated fetched_ids.json.")

if __name__ == "__main__":
    main()
