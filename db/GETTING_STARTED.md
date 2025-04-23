# Getting Started Guide

Welcome to the Travel Database project! This simple guide will walk you through setting up the project on your local machine, even if you're new to database projects.

## Prerequisites

Before you begin, make sure you have:

1. **Docker Desktop** installed 
   - [Download Docker Desktop](https://www.docker.com/products/docker-desktop)
   - Make sure it's running before you start this project

2. **Python 3.x** installed
   - You can check by running `python3 --version` in your terminal
   - If not installed, [download Python](https://www.python.org/downloads/)

## Step-by-Step Installation

### 1. Clone this repository

```bash
git clone <repository-url>
cd <repository-name>/db
```

### 2. One-Command Setup (Easiest Method)

If you want to set up everything with a single command:

```bash
# Make the script executable
chmod +x run_all.sh

# Run the all-in-one setup script
./run_all.sh
```

This will:
- Create a MySQL database in Docker
- Build the database structure
- Fill it with sample data
- Generate Excel reports and visualizations

### 3. Check your results

When the script completes, you should have:
- A running MySQL container
- Database populated with sample data
- Reports generated in the `reports` folder

To view the reports, open:
- `reports/travel_reports.xlsx`
- `reports/travel_insights_*.xlsx`

You can also view the visualizations as PNG files in the `reports` folder.

## Common Issues for Beginners

### "Docker is not running" error
Make sure Docker Desktop is open and running before running any scripts.

### "Command not found: python3"
If you get this error, try using `python` instead of `python3` in the commands, or check that Python is properly installed.

### "Permission denied" when running scripts
You need to make the scripts executable:
```bash
chmod +x *.sh
```

### Database connection issues
If you can't connect to MySQL, the most common reasons are:
- Docker isn't running
- The container failed to start
- Port 3307 is already in use (change the port in the .env file)

## Learning Opportunities

This project is designed to teach you:
1. How to use Docker for database development
2. Basic SQL table structure and relationships
3. How to generate data reports with Python
4. Data visualization techniques

Feel free to explore the code and modify it. Don't worry about breaking things – you can always re-run the setup script!

## Next Steps

Once you've got this working:
1. Try writing your own SQL queries to explore the data
2. Add a new report to one of the Python scripts
3. Try modifying the database schema to add a new table

## Getting Help

If you get stuck, here are some troubleshooting tips:
1. Check the README.md for detailed documentation
2. Read error messages carefully - they often tell you exactly what's wrong
3. Google any error messages you don't understand
4. Ask a team member for help if you're still stuck after trying the above 