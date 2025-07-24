"""
This is the readme file for the nutrition project, I want to extract data from spoonacular api and build a simple pipeline to then report and investigate the relationship between ingredients and the nutrients they contain, as well as the functional effects on the body
"""

# Nutrition Project

This project aims to extract nutritional data from the Spoonacular API and build a simple data pipeline to analyze the relationship between ingredients, their nutrient content, and their functional effects on the body.

## Project Structure

- `scripts/`: Contains Python scripts for data extraction, processing, and analysis.
- `data/`: Stores raw and processed data.
  - `data/raw/`: Raw data extracted from APIs.
  - `data/processed/`: Processed and cleaned data.
- `notebooks/`: Jupyter notebooks for exploratory data analysis and model development.
- `reports/`: Generated reports and visualizations.
- `requirements.txt`: Lists all project dependencies.
- `.gitignore`: Specifies files and directories to be ignored by Git.

## Setup and Installation

1. **Clone the repository:**
   ```bash
   git clone https://github.com/your-username/nutrition-project.git
   cd nutrition-project
   ```

2. **Create a virtual environment (recommended):**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: `venv\Scripts\activate`
   ```

3. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

4. **Obtain Spoonacular API Key:**
   - Sign up for a free API key at [Spoonacular API](https://spoonacular.com/food-api).
   - Replace `'YOUR_SPOONACULAR_API_KEY'` in `scripts/get_spoonacular_data.py` with your actual API key.

## Usage

### 1. Extract Data from Spoonacular API

Run the script to fetch recipe data from the Spoonacular API:

```bash
python scripts/get_spoonacular_data.py
