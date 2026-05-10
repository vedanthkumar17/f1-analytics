# F1 Analytics Pipeline
A data pipeline that fetches live F1 race data from the OpenF1 API, 
cleans and transforms it using Pandas, and analyzes pit stop strategies.
## What it does right now
- Fetches the driver and pit stop data from OpenF1 API
- Cleans missing data and merges datasets
- Analyzes pit stop counts per driver
- Shows the fastest driver in each sector
## Tech Stack
- Python
- Pandas
- OpenF1 API

## Planned Features
- PostgreSQL database integration
- Apache Airflow automation
- Race strategy dashboard
## How to run
pip install requests pandas
python3 day4_merge.py
