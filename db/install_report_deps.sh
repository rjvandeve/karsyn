#!/bin/bash

echo "🔧 Installing required Python packages for travel database reporting..."

# Install the base packages needed for both basic and advanced reporting
pip install pandas openpyxl matplotlib sqlalchemy mysql-connector-python

# Install additional packages for the advanced reporting
pip install seaborn

echo "✅ Installation complete! You can now run the reporting scripts:"
echo "   - python make_reports.py    (for basic reports)"
echo "   - python advanced_reports.py (for advanced reports with detailed visualizations)" 