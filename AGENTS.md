# AGENTS.md

## Commands
- Run Streamlit dashboard: `streamlit run dashboard.py`
- Run data pipeline: `python pipeline.py`
- Install dependencies: `pip install -r requirements.txt`

## Architecture & Data Flow
- **Data Source:** OpenF1 API (`https://api.openf1.org/v1/`)
- **Pipeline (`pipeline.py`):** Fetches session data (drivers, pit stops, laps) and loads structured data into PostgreSQL (`f1_analytics`).
- **Dashboard (`dashboard.py` & `data.py`):** Interactive Streamlit + Plotly application fetching cached data directly from OpenF1 API endpoints for 2025 F1 races.

## Environment & Gotchas
- PostgreSQL database required locally for pipeline execution (`localhost`, db: `f1_analytics`, user: `postgres`).
- Streamlit secrets and config located in `.streamlit/`.
