# Fintech Review Analytics

Analyzing Google Play Store reviews for Ethiopian banking apps.

## Banks Analyzed
- Commercial Bank of Ethiopia (CBE)
- Bank of Abyssinia (BOA)
- Dashen Bank

## Setup
pip install -r requirements.txt

## Project Structure
- data/raw/ - Scraped review data
- notebooks/ - Analysis notebooks
- src/ - Reusable Python modules
- tests/ - Unit tests
- scripts/ - Helper scripts

## Database
- Schema: `data/schema.sql` (PostgreSQL compatible)
- Script: `src/database_postgres.py`
- Run: `python src/database_postgres.py`

## Visualizations
All charts in `reports/` folder:
- sentiment_by_bank.png
- rating_distribution.png
- theme_frequency.png
