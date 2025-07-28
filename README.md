# Nutrition Project

This project aims to extract nutritional data from the Spoonacular API and build a simple data pipeline to analyze the relationship between ingredients, their nutrient content, and their functional effects on the body.

## Project Structure

- `scripts/`: Contains Python scripts for the data pipeline.
  - `scripts/extract/`: Scripts for fetching raw data from APIs.
  - `scripts/transform/`: Scripts for cleaning, flattening, and transforming raw data.
- `data/`: Stores raw and processed data.
  - `data/raw/spoonacular_ingredients/`: Raw ingredient JSON files from Spoonacular.
  - `data/processed/`: Processed and cleaned data, including the final `ingredients.csv`.
- `notebooks/`: Jupyter notebooks for exploratory data analysis.
- `requirements.txt`: Lists all project dependencies.
- `.env`: Environment file for storing secrets like API keys (must be created locally).
- `.gitignore`: Specifies files and directories to be ignored by Git.

## Setup and Installation

1. **Clone the repository:**
   ```bash
   git clone <your-repository-url>
   cd nutrition-project
   ```

2. **Create a virtual environment (recommended):**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On macOS/Linux
   # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

4. **Set up Environment Variables:**
   - Sign up for a free API key at [Spoonacular API](https://spoonacular.com/food-api).
   - Create a file named `.env` in the root of the project directory.
   - Add your API key to the `.env` file like this:
     ```
     SPOONACULAR_API_KEY='your_actual_api_key_here'
     ```

## Usage

The data pipeline is a two-step process.

### 1. Extract Raw Data

Run the extraction script to fetch ingredient data from the Spoonacular API. This script searches for ingredients alphabetically, fetches detailed information, and saves each one as a separate JSON file.
```bash
python scripts/extract/get_spoonacular_data.py
