# F1 Analytics Pipeline

A Formula 1 data analytics project that fetches live race data from the OpenF1 API, processes it using Python and Pandas, and performs exploratory analysis on pit stop performance and driver data.

---

## Current Features

- Fetches live driver and pit stop data from the OpenF1 API
- Parses JSON race data into structured datasets
- Saves API data into CSV format
- Cleans missing/null pit stop records
- Performs pit stop analytics using Pandas
- Uses SQL queries for aggregation and analysis

---

## Analytics Included

### Pit Stop Analysis
- Average pit stop duration by team
- Fastest individual pit stop
- Driver-wise pit stop comparisons

### Driver Data
- Driver names and team extraction
- Structured driver datasets

---

## Tech Stack

- Python
- Pandas
- SQL
- OpenF1 API

---

## Project Structure

```bash
f1-analytics/
│
├── fetch_api_data.py
├── parse_drivers.py
├── save_drivers_csv.py
├── fetch_pit_stops.py
├── analysis.py
├── sql/
│   ├── pit_stop_analysis.sql
│   ├── driver_stats.sql
│
├── drivers.csv
├── pit_stops.csv
├── README.md
```

---

## How to Run

Install dependencies:

```bash
pip install pandas requests
```

Run scripts:

```bash
python3 fetch_pit_stops.py
python3 analysis.py
```

---

## Planned Improvements

- PostgreSQL integration
- Apache Airflow orchestration
- Automated ETL pipeline
- Interactive dashboard
- Historical race analytics

---

## Learning Focus

This project is part of my hands-on learning in:

- Data Engineering
- SQL Analytics
- API Integration
- ETL Development
