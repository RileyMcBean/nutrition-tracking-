"""
This script reads all the flattened ingredient JSON files from the processed
data directory, combines them into a single pandas DataFrame, and exports
the result to a CSV file for easy analysis.
"""

import json
import os
import pandas as pd
from dotenv import load_dotenv
import logging

# Load environment variables from .env file
load_dotenv()

# Set up basic logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# --- Configuration ---

# Construct paths relative to the script's location for portability
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_ROOT = os.path.dirname(os.path.dirname(SCRIPT_DIR)) # Go up two levels from scripts/transform

# The input should be the raw data directory
INPUT_DIR = os.path.join(PROJECT_ROOT, "data", "raw", "spoonacular_ingredients")
OUTPUT_DIR = os.path.join(PROJECT_ROOT, "data", "processed")
OUTPUT_CSV_FILE = os.path.join(OUTPUT_DIR, "ingredients.csv")

# --- Helper Functions ---

def flatten_ingredient_json(data):
    """
    Flattens the nested Spoonacular ingredient JSON into a single-level dictionary.

    Args:
        data (dict): The raw ingredient data loaded from a JSON file.

    Returns:
        dict: A flattened dictionary containing the most relevant fields.
    """
    flat_data = {
        "id": data.get("id"),
        "name": data.get("name"),
        "aisle": data.get("aisle"),
        "consistency": data.get("consistency"),
        "amount": data.get("amount"),
        "unit": data.get("unit"),
    }

    # Flatten the nested nutrition data
    nutrition = data.get("nutrition", {})

    # Extract nutrients, creating a key for each nutrient name and unit
    for nutrient in nutrition.get("nutrients", []):
        key = f"nutrient_{nutrient.get('name', 'unknown').replace(' ', '_')}_{nutrient.get('unit', 'unknown')}"
        flat_data[key] = nutrient.get("amount")

    # Extract properties
    for prop in nutrition.get("properties", []):
        key = f"property_{prop.get('name', 'unknown').replace(' ', '_')}"
        flat_data[key] = prop.get("amount")

    # Extract caloric breakdown
    for key, value in nutrition.get("caloricBreakdown", {}).items():
        flat_data[f"caloricBreakdown_{key}"] = value

    return flat_data

def main():
    """
    Main function to read raw JSONs, flatten them, combine into a DataFrame,
    and save as a single CSV file.
    """
    if not os.path.isdir(INPUT_DIR):
        logger.error(f"Input directory not found: {INPUT_DIR}")
        logger.error("Please run the 'get_spoonacular_data.py' script first to fetch raw data.")
        return

    os.makedirs(OUTPUT_DIR, exist_ok=True)
    logger.info(f"Reading raw JSON files from: {INPUT_DIR}")

    all_flattened_data = []
    json_files = [f for f in os.listdir(INPUT_DIR) if f.startswith("ingredient_") and f.endswith(".json")]

    for filename in json_files:
        file_path = os.path.join(INPUT_DIR, filename)
        try:
            with open(file_path, "r") as f:
                raw_data = json.load(f)
            flattened_data = flatten_ingredient_json(raw_data)
            all_flattened_data.append(flattened_data)
        except json.JSONDecodeError:
            logger.warning(f"Could not decode JSON from {filename}. Skipping file.")
        except Exception as e:
            logger.error(f"An unexpected error occurred while processing {filename}: {e}. Skipping file.")

    if not all_flattened_data:
        logger.warning("No ingredient data found to process.")
        return

    df = pd.DataFrame(all_flattened_data)
    df.to_csv(OUTPUT_CSV_FILE, index=False)
    logger.info(f"Successfully created CSV with {len(df)} ingredients at: {OUTPUT_CSV_FILE}")

if __name__ == "__main__":
    main()