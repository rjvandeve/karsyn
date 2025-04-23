import os, random, datetime
from faker import Faker
import mysql.connector as mc

fake = Faker()

cfg = {
    "host":     os.getenv("MYSQL_HOST", "localhost"),
    "port":     int(os.getenv("MYSQL_PORT", 3307)),
    "user":     os.getenv("MYSQL_USER", "travel_admin"),
    "password": os.getenv("MYSQL_PASSWORD", "travel_pw"),
    "database": os.getenv("MYSQL_DATABASE", "travel_db"),
}

def execute_many(cursor, sql, data):
    cursor.executemany(sql, data)

cnx = mc.connect(**cfg)
cur = cnx.cursor()

# ---------- Address ----------
addr_rows = []
for _ in range(200):
    addr_rows.append((
        fake.street_address()[:50],
        fake.secondary_address()[:50],
        fake.postcode()[:10],
        fake.phone_number()[:20],
        fake.city()[:50],
        fake.country()[:50]
    ))
execute_many(cur, """
    INSERT INTO Address(Address,Address2,Postal_Code,Phone,City,Country)
    VALUES (%s,%s,%s,%s,%s,%s)
""", addr_rows)
cnx.commit()

# ---------- Customer ----------
cur.execute("SELECT AddressID FROM Address")
addr_ids = [row[0] for row in cur.fetchall()]
cust_rows = []
for _ in range(100):
    cust_rows.append((
        random.choice(addr_ids),
        fake.first_name(),
        fake.last_name(),
        fake.email(),
        fake.date_time_between(start_date='-3y', end_date='now')
    ))
execute_many(cur, """
    INSERT INTO Customer(AddressID,First_Name,Last_Name,Email,Create_Date)
    VALUES (%s,%s,%s,%s,%s)
""", cust_rows)
cnx.commit()

# ---------- Staff ----------
staff_rows = []
for _ in range(15):
    staff_rows.append((
        random.choice(addr_ids),
        fake.first_name(),
        fake.last_name(),
        fake.company_email()
    ))
execute_many(cur, """
    INSERT INTO Staff(AddressID,First_Name,Last_Name,Email)
    VALUES (%s,%s,%s,%s)
""", staff_rows)
cnx.commit()

# ---------- Transportation_Info ----------
trans_rows = []
travel_types = ['Car', 'Train', 'Plane', 'Bus', 'Bike']
for i in range(120):
    travel_type = random.choice(travel_types)
    cost_cents = random.randint(30, 1500) * 100
    hours = random.randint(1, 20)
    trans_rows.append((travel_type, cost_cents, hours, i+1))  # i+1 as transportation_id
execute_many(cur, """
    INSERT INTO Transportation_Info(Travel_Type,Cost,Time_hours,transportation_id)
    VALUES (%s,%s,%s,%s)
""", trans_rows)
cnx.commit()

# ---------- Basic_Travel ----------
cur.execute("SELECT user_id FROM Customer")
user_ids = [row[0] for row in cur.fetchall()]
basic_rows = []
for trans_id in range(1, 120):
    basic_rows.append((
        trans_id,
        random.randint(50000, 500000),             # budget in cents
        random.choice(user_ids),
        fake.state()[:30],
        random.randint(1, 6)
    ))
execute_many(cur, """
    INSERT INTO Basic_Travel(transportation_id,Budget,user_id,State,Num_People)
    VALUES (%s,%s,%s,%s,%s)
""", basic_rows)
cnx.commit()

# ---------- Trips ----------
trip_rows = []
for _ in range(60):
    start = fake.date_between('-1y', '+30d')
    end   = start + datetime.timedelta(days=random.randint(2, 14))
    trip_rows.append((fake.catch_phrase()[:100], start, end))
execute_many(cur, """
    INSERT INTO Trips(trip_name,start_date,end_date)
    VALUES (%s,%s,%s)
""", trip_rows)
cnx.commit()

# ---------- User_Trips ----------
cur.execute("SELECT trip_id FROM Trips")
trip_ids = [row[0] for row in cur.fetchall()]
user_trip_rows = []
for _ in range(180):
    user_trip_rows.append((
        random.choice(user_ids),
        random.choice(trip_ids)
    ))
execute_many(cur, """
    INSERT INTO User_Trips(user_id,trip_id)
    VALUES (%s,%s)
""", user_trip_rows)
cnx.commit()

# ---------- Payments ----------
cur.execute("SELECT RentalID FROM Transportation_Info")
rental_ids = [row[0] for row in cur.fetchall()]
cur.execute("SELECT staff_id FROM Staff")
staff_ids  = [row[0] for row in cur.fetchall()]

pay_rows = []
for _ in range(250):
    pay_rows.append((
        random.choice(user_ids),
        random.choice(rental_ids),
        round(random.uniform(50, 2000), 2),
        fake.date_time_between(start_date='-18m', end_date='now'),
        random.choice(staff_ids)
    ))
execute_many(cur, """
    INSERT INTO Payment(user_id,RentalID,Amount,Payment_Date,staff_id)
    VALUES (%s,%s,%s,%s,%s)
""", pay_rows)
cnx.commit()

print("✔  Seed complete")
cur.close(); cnx.close() 