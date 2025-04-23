@echo off
echo 🚀 Setting up Travel Database System and generating reports

REM Check if Docker is running
docker info >nul 2>&1
if %ERRORLEVEL% NEQ 0 (
    echo ❌ Docker is not running. Please start Docker Desktop and try again.
    exit /b 1
)

REM Create reports directory if it doesn't exist
echo 📁 Creating reports directory...
if not exist reports mkdir reports

REM Step 1: Set up the database
echo 📊 Step 1: Setting up the database...
call setup_all.bat

REM Step 2: Install reporting dependencies
echo 📊 Step 2: Installing reporting dependencies...
pip install pandas openpyxl matplotlib sqlalchemy mysql-connector-python seaborn

REM Step 3: Generate basic reports
echo 📊 Step 3: Generating basic reports...
python make_reports.py

REM Step 4: Generate advanced reports
echo 📊 Step 4: Generating advanced reports...
python advanced_reports.py

echo ✅ All done! The following outputs have been generated:
echo    - reports/travel_reports.xlsx (Basic reports with two sheets)
echo    - reports/travel_insights_*.xlsx (Advanced reports with multiple sheets)
echo    - Several PNG chart files in the reports directory
echo.
echo You can view these files in Excel or any spreadsheet software.
echo The PNG files can be viewed directly or imported into presentation software. 