# Travel Database Project

A starter project for junior developers to learn database development, data reporting, and visualization techniques.

## 🚀 Project Overview

This repository contains a complete MySQL database system with reporting capabilities, designed as a learning resource for developers new to database projects. The project simulates a travel booking system with customers, trips, transportation, and payments.

## ✨ Features

- **Docker-based MySQL Database**: Easy setup with no local database installation required
- **Realistic Test Data**: Auto-generated sample data that mimics real-world scenarios
- **Data Reporting**: Python scripts that generate Excel reports from the database
- **Data Visualization**: Automatically created charts and graphs for insights
- **Cross-Platform Support**: Works on macOS, Linux, and Windows

## 📊 Included Reports

The system generates two levels of reports:

1. **Basic Reports**:
   - Customer spending analysis
   - Trip duration by travel type

2. **Advanced Reports**:
   - VIP customer analysis with geographic data
   - Travel preference comparisons
   - Destination popularity analysis
   - Monthly revenue trends

## 🧰 Tech Stack

- **Database**: MySQL 8.0 (in Docker)
- **Programming**: Python 3.x
- **Data Processing**: Pandas, SQLAlchemy
- **Visualization**: Matplotlib, Seaborn
- **Reporting**: Excel files via openpyxl

## 🔍 Getting Started

Navigate to the `db` directory and explore the [Getting Started Guide](db/GETTING_STARTED.md) for step-by-step instructions.

```bash
cd db
python3 check_env.py  # Check if your environment is ready
./run_all.sh          # Set up everything in one command
```

## 📚 Learning Opportunities

This project is designed to teach:

- Docker-based development
- Database schema design
- SQL querying
- Python data analysis
- Data visualization
- Report generation

## 📋 Directory Structure

- `/db` - Main project directory
  - Database setup scripts
  - Reporting code
  - SQL schema
  - Test data generation

## 🏆 Next Steps

Once you've got the basics working, try:
1. Adding a new report type
2. Creating a simple REST API using Flask
3. Building a basic web dashboard for the data
4. Adding more dimensions to the data model 