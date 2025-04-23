import os, pandas as pd, matplotlib.pyplot as plt
import seaborn as sns
from sqlalchemy import create_engine
from datetime import datetime
import glob
import shutil

# Create reports directory if it doesn't exist
REPORTS_DIR = "reports"
os.makedirs(REPORTS_DIR, exist_ok=True)

# ---------- 0. cleanup existing reports ----------
print("Cleaning up existing advanced reports...")
# Remove any existing advanced reports
for file in glob.glob(os.path.join(REPORTS_DIR, "travel_insights_*.xlsx")):
    os.remove(file)
# Remove any existing PNG files from advanced reports
for file in glob.glob(os.path.join(REPORTS_DIR, "vip_customers.png")):
    os.remove(file)
for file in glob.glob(os.path.join(REPORTS_DIR, "travel_preferences*.png")):
    os.remove(file)
for file in glob.glob(os.path.join(REPORTS_DIR, "popular_destinations*.png")):
    os.remove(file)
for file in glob.glob(os.path.join(REPORTS_DIR, "monthly_revenue.png")):
    os.remove(file)

# Set up nice styling for our plots
plt.style.use('ggplot')
sns.set_palette("deep")

# ---------- 1. connection ----------
url = (
    f"mysql+mysqlconnector://{os.getenv('MYSQL_USER','travel_admin')}:"
    f"{os.getenv('MYSQL_PASSWORD','travel_pw')}@"
    f"{os.getenv('MYSQL_HOST','localhost')}:"
    f"{os.getenv('MYSQL_PORT',3307)}/"
    f"{os.getenv('MYSQL_DATABASE','travel_db')}"
)
engine = create_engine(url)

# ---------- 2. report queries ----------
reports = {
    # A. Top customers by lifetime spend (with address details)
    "vip_customers": """
        SELECT  c.user_id,
                CONCAT(c.First_Name,' ',c.Last_Name) AS customer,
                ROUND(SUM(p.Amount),2) AS total_spend_usd,
                COUNT(DISTINCT p.payment_id) AS transactions,
                a.City,
                a.Country
        FROM    Customer c
        JOIN    Payment p USING (user_id)
        LEFT JOIN Address a ON c.AddressID = a.AddressID
        GROUP BY c.user_id, c.First_Name, c.Last_Name, a.City, a.Country
        ORDER BY total_spend_usd DESC
        LIMIT 15;
    """,
    
    # B. Travel preference analysis - which types are most popular
    "travel_preferences": """
        SELECT  ti.Travel_Type,
                COUNT(*) AS booking_count,
                ROUND(AVG(ti.Cost)/100, 2) AS avg_cost_usd,
                ROUND(AVG(ti.Time_hours), 1) AS avg_travel_hours,
                ROUND(AVG(bt.Num_People), 1) AS avg_group_size
        FROM    Transportation_Info ti
        JOIN    Basic_Travel bt USING (transportation_id)
        GROUP BY ti.Travel_Type
        ORDER BY booking_count DESC;
    """,
    
    # C. Destination popularity by state
    "popular_destinations": """
        SELECT  bt.State,
                COUNT(*) AS visitor_count,
                ROUND(AVG(bt.Budget)/100, 2) AS avg_budget_usd,
                ROUND(AVG(bt.Num_People), 1) AS avg_group_size
        FROM    Basic_Travel bt
        WHERE   bt.State IS NOT NULL AND bt.State != ''
        GROUP BY bt.State
        ORDER BY visitor_count DESC
        LIMIT 10;
    """,
    
    # D. Monthly payment trends
    "monthly_revenue": """
        SELECT  DATE_FORMAT(p.Payment_Date, '%Y-%m') AS month,
                ROUND(SUM(p.Amount), 2) AS monthly_revenue,
                COUNT(*) AS transaction_count
        FROM    Payment p
        GROUP BY DATE_FORMAT(p.Payment_Date, '%Y-%m')
        ORDER BY month;
    """
}

# ---------- 3. fetch + visualize + save ----------
timestamp = datetime.now().strftime("%Y%m%d_%H%M")
output_file = os.path.join(REPORTS_DIR, f"travel_insights_{timestamp}.xlsx")

with pd.ExcelWriter(output_file) as writer:
    for sheet, sql in reports.items():
        print(f"Generating {sheet} report...")
        df = pd.read_sql(sql, engine)
        df.to_excel(writer, sheet_name=sheet, index=False)
        
        # Create visualizations based on report type
        plt.figure(figsize=(10, 6))
        
        if sheet == "vip_customers":
            # Top 10 customers bar chart
            top_customers = df.head(10)
            sns.barplot(x='customer', y='total_spend_usd', data=top_customers)
            plt.title('Top 10 Customers by Spending')
            plt.xticks(rotation=45, ha='right')
            plt.tight_layout()
            plt.savefig(os.path.join(REPORTS_DIR, f"{sheet}.png"), dpi=300)
            
        elif sheet == "travel_preferences":
            # Transport type comparison
            ax = df.plot(kind='bar', x='Travel_Type', y=['booking_count', 'avg_cost_usd', 'avg_travel_hours'], 
                      figsize=(10, 6))
            plt.title('Travel Type Analysis')
            plt.tight_layout()
            plt.savefig(os.path.join(REPORTS_DIR, f"{sheet}.png"), dpi=300)
            
            # Secondary visualization - radar chart for travel types
            plt.figure(figsize=(8, 8))
            categories = ['booking_count', 'avg_cost_usd', 'avg_travel_hours', 'avg_group_size']
            
            # Normalize data for radar chart
            radar_data = df[categories].copy()
            for col in categories:
                radar_data[col] = (radar_data[col] - radar_data[col].min()) / (radar_data[col].max() - radar_data[col].min())
            
            # Plot each travel type
            for i, row in radar_data.iterrows():
                values = row[categories].tolist()
                # Close the loop
                values += [values[0]]
                
                # Plot
                angles = [n / float(len(categories)) * 2 * 3.14159 for n in range(len(categories))]
                angles += [angles[0]]
                
                ax = plt.subplot(111, polar=True)
                ax.plot(angles, values, linewidth=2, label=df.iloc[i]['Travel_Type'])
                ax.fill(angles, values, alpha=0.25)
            
            # Set category labels
            plt.xticks(angles[:-1], categories)
            plt.legend(loc='upper right')
            plt.title('Travel Types Comparison (Normalized)')
            plt.savefig(os.path.join(REPORTS_DIR, f"{sheet}_radar.png"), dpi=300)
            
        elif sheet == "popular_destinations":
            # Top destinations
            plt.figure(figsize=(12, 6))
            sns.barplot(x='State', y='visitor_count', data=df)
            plt.title('Most Popular Destinations')
            plt.xticks(rotation=45, ha='right')
            plt.tight_layout()
            plt.savefig(os.path.join(REPORTS_DIR, f"{sheet}.png"), dpi=300)
            
            # Budget by destination
            plt.figure(figsize=(12, 6))
            sns.scatterplot(x='visitor_count', y='avg_budget_usd', 
                          size='avg_group_size', sizes=(100, 500),
                          hue='State', data=df)
            plt.title('Destination Popularity vs. Budget')
            plt.tight_layout()
            plt.savefig(os.path.join(REPORTS_DIR, f"{sheet}_budget.png"), dpi=300)
            
        elif sheet == "monthly_revenue":
            # Monthly revenue trend
            plt.figure(figsize=(12, 6))
            ax1 = plt.gca()
            ax2 = ax1.twinx()
            
            df['month'] = pd.to_datetime(df['month'] + '-01')
            ax1.plot(df['month'], df['monthly_revenue'], 'b-', linewidth=2, marker='o')
            ax2.plot(df['month'], df['transaction_count'], 'r--', linewidth=1.5, marker='s')
            
            ax1.set_xlabel('Month')
            ax1.set_ylabel('Monthly Revenue (USD)', color='b')
            ax2.set_ylabel('Transaction Count', color='r')
            
            plt.title('Monthly Revenue and Transaction Trends')
            plt.xticks(rotation=45)
            plt.tight_layout()
            plt.savefig(os.path.join(REPORTS_DIR, f"{sheet}.png"), dpi=300)
        
        plt.close('all')

# Create an executive summary with key metrics
print("Generating executive summary...")
with engine.connect() as conn:
    # Total customers
    total_customers = pd.read_sql("SELECT COUNT(*) AS total FROM Customer", conn).iloc[0, 0]
    
    # Total revenue
    total_revenue = pd.read_sql("SELECT ROUND(SUM(Amount), 2) AS total FROM Payment", conn).iloc[0, 0]
    
    # Average trip duration
    avg_trip_days = pd.read_sql("""
        SELECT ROUND(AVG(DATEDIFF(end_date, start_date)), 1) AS avg_days 
        FROM Trips
    """, conn).iloc[0, 0]
    
    # Most popular travel type
    pop_travel_type = pd.read_sql("""
        SELECT Travel_Type, COUNT(*) AS count
        FROM Transportation_Info
        GROUP BY Travel_Type
        ORDER BY count DESC
        LIMIT 1
    """, conn).iloc[0, 0]

# Create a summary sheet with the key metrics
summary_df = pd.DataFrame({
    'Metric': ['Total Customers', 'Total Revenue (USD)', 'Avg Trip Duration (days)', 'Most Popular Travel Type'],
    'Value': [total_customers, total_revenue, avg_trip_days, pop_travel_type]
})

# Add the summary to the Excel file
with pd.ExcelWriter(output_file, mode='a') as writer:
    summary_df.to_excel(writer, sheet_name='Executive_Summary', index=False)

print(f"✅ Reports and visualizations complete! Output saved to {output_file}")
print(f"   PNG charts also available in the {REPORTS_DIR} directory") 