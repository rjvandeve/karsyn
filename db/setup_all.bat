@echo off
echo 📦 Setting up Travel Database System

REM Check if Docker is running
docker info >nul 2>&1
if %ERRORLEVEL% NEQ 0 (
    echo ❌ Docker is not running. Please start Docker Desktop and try again.
    exit /b 1
)

REM Load environment variables
set MYSQL_HOST=localhost
set MYSQL_PORT=3307
set MYSQL_DATABASE=travel_db
set MYSQL_USER=travel_admin
set MYSQL_PASSWORD=travel_pw

REM Check if container already exists
docker ps -a | findstr travel-mysql >nul
if %ERRORLEVEL% EQU 0 (
    echo 🔄 Removing existing travel-mysql container...
    docker rm -f travel-mysql >nul
)

REM Start MySQL
echo 🚀 Starting MySQL...
docker run -d --name travel-mysql ^
  -p %MYSQL_PORT%:3306 ^
  -e MYSQL_ROOT_PASSWORD=root_pw ^
  -e MYSQL_DATABASE=%MYSQL_DATABASE% ^
  -e MYSQL_USER=%MYSQL_USER% ^
  -e MYSQL_PASSWORD=%MYSQL_PASSWORD% ^
  mysql:8.0 >nul

echo ⏳ Waiting for MySQL to initialize (15 seconds)...
timeout /t 15 /nobreak > nul

REM Load schema
echo 📝 Creating database schema...
docker exec -i travel-mysql mysql -u%MYSQL_USER% -p%MYSQL_PASSWORD% %MYSQL_DATABASE% < schema.sql

REM Check if Python dependencies are installed
echo 🐍 Checking Python dependencies...
pip install faker mysql-connector-python >nul

REM Seed the database
echo 🌱 Seeding database with test data...
python seed_db.py

REM Run smoke test
echo 🔍 Running smoke tests...
docker exec -i travel-mysql mysql -u%MYSQL_USER% -p%MYSQL_PASSWORD% %MYSQL_DATABASE% < smoke_test.sql

echo ✅ Database setup complete!
echo    - MySQL is running at %MYSQL_HOST%:%MYSQL_PORT%
echo    - Database: %MYSQL_DATABASE%
echo    - User: %MYSQL_USER%
echo    - Password: %MYSQL_PASSWORD%
echo.
echo To connect manually:
echo docker exec -it travel-mysql mysql -u%MYSQL_USER% -p%MYSQL_PASSWORD% %MYSQL_DATABASE% 