import os, pandas as pd, matplotlib.pyplot as plt
from sqlalchemy import create_engine
import glob
import shutil

# Create reports directory if it doesn't exist
REPORTS_DIR = "reports"
os.makedirs(REPORTS_DIR, exist_ok=True)

# ---------- 0. cleanup existing reports ----------
print("Cleaning up existing basic reports...")
for file in glob.glob(os.path.join(REPORTS_DIR, "travel_reports.xlsx")):
    os.remove(file)
for file in glob.glob(os.path.join(REPORTS_DIR, "customer_spend.png")):
    os.remove(file)
for file in glob.glob(os.path.join(REPORTS_DIR, "trip_duration.png")):
    os.remove(file)

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
    # A.  Top customers by lifetime spend
    "customer_spend": """
        SELECT  c.user_id,
                CONCAT(c.First_Name,' ',c.Last_Name)   AS customer,
                ROUND(SUM(p.Amount),2)                 AS total_spend_usd
        FROM    Customer c
        JOIN    Payment  p USING (user_id)
        GROUP   BY c.user_id
        ORDER   BY total_spend_usd DESC
        LIMIT 20;
    """,

    # B.  Average trip duration per travel type
    "trip_duration": """
        SELECT  ti.Travel_Type,
                ROUND(AVG(DATEDIFF(t.end_date,t.start_date)),1) AS avg_days
        FROM    Trips t
        JOIN    User_Trips        ut ON ut.trip_id = t.trip_id
        JOIN    Basic_Travel      bt ON bt.user_id = ut.user_id
        JOIN    Transportation_Info ti USING (transportation_id)
        GROUP   BY ti.Travel_Type;
    """
}

# ---------- 3. fetch + save ----------
output_file = os.path.join(REPORTS_DIR, "travel_reports.xlsx")
with pd.ExcelWriter(output_file) as writer:
    for sheet, sql in reports.items():
        df = pd.read_sql(sql, engine)
        df.to_excel(writer, sheet_name=sheet, index=False)

        # quick bar-chart for any numeric report <optional>
        if df.shape[1] == 3 and df.dtypes.iloc[2].kind in "fi":
            ax = df.plot(kind="bar", x=df.columns[1], y=df.columns[2], legend=False)
            ax.set_xlabel(""); ax.set_ylabel(""); ax.set_title(sheet.replace('_',' ').title())
            plt.tight_layout()
            chart_file = os.path.join(REPORTS_DIR, f"{sheet}.png")
            plt.savefig(chart_file)
            plt.close()

print(f"✔  Reports saved to {REPORTS_DIR}/travel_reports.xlsx with PNG charts") 