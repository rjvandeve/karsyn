#!/bin/bash

echo "🚀 Setting up Travel Database System and generating reports"

# Check if running Docker
if ! docker info > /dev/null 2>&1; then
  echo "❌ Docker is not running. Please start Docker Desktop and try again."
  exit 1
fi

# Create reports directory if it doesn't exist
echo "📁 Creating reports directory..."
mkdir -p reports

# Step 1: Set up the database
echo "📊 Step 1: Setting up the database..."
./setup_all.sh

# Step 2: Install reporting dependencies
echo "📊 Step 2: Installing reporting dependencies..."
./install_report_deps.sh

# Step 3: Generate basic reports
echo "📊 Step 3: Generating basic reports..."
python3 make_reports.py

# Step 4: Generate advanced reports
echo "📊 Step 4: Generating advanced reports..."
python3 advanced_reports.py

echo "✅ All done! The following outputs have been generated:"
echo "   - reports/travel_reports.xlsx (Basic reports with two sheets)"
echo "   - reports/travel_insights_*.xlsx (Advanced reports with multiple sheets)"
echo "   - Several PNG chart files in the reports directory"
echo ""
echo "You can view these files in Excel or any spreadsheet software."
echo "The PNG files can be viewed directly or imported into presentation software." 