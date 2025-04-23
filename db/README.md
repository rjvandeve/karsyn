# Travel Database System

This project sets up a MySQL database with tables for managing travel data, including customers, addresses, transportation information, trips, and payments. It also includes reporting capabilities to generate Excel reports and visualizations.

> **🔰 New to this project?** Check out [GETTING_STARTED.md](GETTING_STARTED.md) for a beginner-friendly guide, or run `./check_env.py` to verify your system is ready.

## Setup Instructions

### Prerequisites
- Docker Desktop installed and running
- Python 3.x with pip

### One-Command Setup (Recommended)

For a complete end-to-end setup including database and both report types:

```bash
chmod +x run_all.sh
./run_all.sh
```

This script will:
1. Check if Docker is running
2. Create a reports directory if it doesn't exist
3. Set up the database (via setup_all.sh)
4. Install reporting dependencies
5. Generate both basic and advanced reports in the reports directory
6. Output Excel files and visualization PNGs to the reports directory

### Quick Database Setup

For just setting up the database without generating reports:

```bash
chmod +x setup_all.sh
./setup_all.sh
```

This script will:
1. Check if Docker is running
2. Start a MySQL container
3. Create the database schema
4. Install Python dependencies
5. Seed the database with test data
6. Run smoke test queries

### Manual Setup

If you prefer to run each step manually:

1. **Start MySQL in Docker**:
   ```bash
   chmod +x start_db.sh
   ./start_db.sh
   ```

2. **Create Schema**:
   ```bash
   docker exec -i travel-mysql \
     mysql -utravel_admin -ptravel_pw travel_db < schema.sql
   ```

3. **Install Python Dependencies**:
   ```bash
   pip install faker mysql-connector-python
   ```

4. **Seed Database with Test Data**:
   ```bash
   python3 seed_db.py
   ```

5. **Run Smoke Test Queries**:
   ```bash
   docker exec -i travel-mysql \
     mysql -utravel_admin -ptravel_pw travel_db < smoke_test.sql
   ```

## Database Structure

The database consists of the following tables:
- `Address`: Stores location information
- `Customer`: Customer details with foreign key to Address
- `Transportation_Info`: Information about travel methods
- `Basic_Travel`: Core travel data linked to customers
- `Trips`: Trip details including dates
- `User_Trips`: Links customers to trips
- `Staff`: Staff member information
- `Payment`: Payment records

## Reporting Capabilities

This system includes powerful reporting capabilities that generate Excel outputs and visualizations without requiring additional BI tools. All reports are saved to the `reports` directory.

### Setting Up Reporting

Install the necessary dependencies:

```bash
chmod +x install_report_deps.sh
./install_report_deps.sh
```

This will install:
- pandas, openpyxl, matplotlib, sqlalchemy, mysql-connector-python
- seaborn (for advanced visualizations)

### Basic Reports

For simple Excel reports and charts:

```bash
python3 make_reports.py
```

This generates:
- `reports/travel_reports.xlsx` with two sheets:
  - `customer_spend`: Top 20 customers by lifetime spending
  - `trip_duration`: Average trip duration by travel type
- PNG charts for each report:
  - `reports/customer_spend.png`
  - `reports/trip_duration.png`

### Advanced Reports

For detailed reports with more sophisticated visualizations:

```bash
python3 advanced_reports.py
```

This generates:
- `reports/travel_insights_[timestamp].xlsx` with multiple sheets:
  - `Executive_Summary`: Key metrics overview
  - `vip_customers`: Top customers with location data
  - `travel_preferences`: Analysis of transportation types
  - `popular_destinations`: Most visited states with budget analysis
  - `monthly_revenue`: Revenue trends by month
- Multiple visualization PNG files in the reports directory:
  - `reports/vip_customers.png`
  - `reports/travel_preferences.png` and `reports/travel_preferences_radar.png`
  - `reports/popular_destinations.png` and `reports/popular_destinations_budget.png`
  - `reports/monthly_revenue.png`

### Report Types

1. **Customer Spending Analysis**
   - Identifies top customers by revenue
   - Useful for targeting loyalty programs and promotions

2. **Travel Pattern Analysis**
   - Reveals preferred transportation methods
   - Shows average trip durations and costs

3. **Destination Analysis**
   - Highlights popular destinations
   - Correlates budget with destination popularity

4. **Revenue Trends**
   - Tracks revenue patterns over time
   - Helps identify seasonal trends

## Connecting to MySQL

To connect to the MySQL server manually:
```bash
docker exec -it travel-mysql mysql -utravel_admin -ptravel_pw travel_db
```

## Project Files

```
db/
│  .env                  # local creds & ports
│  schema.sql            # DDL – tables & FK constraints
│  seed_db.py            # populates test data (~100-250 rows per table)
│  make_reports.py       # generates basic reports
│  advanced_reports.py   # generates detailed reports and visualizations
│  smoke_test.sql        # validation queries
│  setup_all.sh          # automated database setup
│  start_db.sh           # starts the MySQL Docker container
│  install_report_deps.sh # installs reporting dependencies
│  run_all.sh            # all-in-one setup and reporting
│  requirements.txt      # Python dependencies
│  README.md             # documentation
└─ reports/              # directory containing all generated reports and visualizations
```

# Travel DB Demo – Developer On‑Ramp

> _Prepared by: Senior Full‑Stack Engineering_

Welcome aboard! 👋 This repo demonstrates how to stand up a small MySQL‑backed application locally, seed it with realistic data, and generate example reports with **Python + pandas**. Use it as your playground for learning SQL, ETL tooling and data visualization.

---

## 1  Tech Stack

| Layer | Tool | Why we chose it |
|-------|------|-----------------|
| Database | **MySQL 8** (Docker container) | Works everywhere, no licence fuss, identical on CI & prod.
| Seed data | **faker**, **mysql‑connector‑python** | Rapidly produces realistic but fake PII for demos.
| Data access & analysis | **SQLAlchemy**, **pandas** | Pythonic; analysts can reuse notebooks; engineers can embed in services.
| Reporting output | **Excel (`openpyxl`)** & **matplotlib/seaborn** visualizations | Excel stays the lingua‑franca for the biz; PNGs slot straight into slides.
| Container runtime | **Docker Desktop** | Zero‑install DB; throwaway environments.

---

## 2  Quick‑Start (5 steps)

> **Assumes:** Docker Desktop & Python 3.x are already installed.

```bash
# 1 — clone & cd
cd db

# 2 — all-in-one setup and reporting
./run_all.sh

# 3 — view the generated reports
# - reports/travel_reports.xlsx (Basic reports)
# - reports/travel_insights_[timestamp].xlsx (Advanced reports)
# - Various PNG files in the reports directory
```

You can also run individual components:

```bash
# Database setup only
./setup_all.sh

# Install reporting dependencies
./install_report_deps.sh

# Generate basic reports
python3 make_reports.py

# Generate advanced reports
python3 advanced_reports.py
```

---

## 3  Report Details

### 3.1  Basic Reports (make_reports.py)

* **Customer Spend Report**
  * **Goal:** Show which travelers are worth the most in aggregate
  * **Logic:** JOIN Customer → Payment, GROUP BY user_id, SUM Amount
  * **Output:** Table + bar chart of top 20 customers by total spend

* **Trip Duration Report**
  * **Goal:** See which transportation modes correlate with longer trips
  * **Logic:** JOIN trip tables, calculate DATEDIFF, AVG by Travel_Type
  * **Output:** Table + bar chart of average days per travel type

### 3.2  Advanced Reports (advanced_reports.py)

* **VIP Customers Analysis**
  * **Goal:** Detailed view of top customers with location information
  * **Output:** Table + bar chart of top 15 customers with city/country

* **Travel Preferences Analysis**
  * **Goal:** Compare booking patterns across transportation types
  * **Output:** Multi-metric comparison + radar chart showing relative strengths

* **Popular Destinations Analysis**
  * **Goal:** Identify most visited states and spending patterns
  * **Output:** Bar chart of top locations + scatter plot of budget vs. popularity

* **Monthly Revenue Trends**
  * **Goal:** Track business performance over time
  * **Output:** Line chart showing revenue and transaction count by month

---

## 4  Troubleshooting FAQ

| Issue | Solution |
|--------|-----------|
| `MySQL connection refused` | Docker not running or port clash (edit `.env` & container mapping) |
| `OperationalError: (1045)` | Wrong credentials – make sure `.env` matches container environment variables |
| `Empty Excel sheets` | Run `seed_db.py` to populate the database first |
| `seaborn/matplotlib errors` | Run `./install_report_deps.sh` to install visualization dependencies |
| `Docker image won't start on Apple Silicon` | Use `mysql/mysql-server:8.0` which has ARM layers, or add `--platform linux/amd64` flag |
