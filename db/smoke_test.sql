USE travel_db;

-- 1) Top 5 customers by spend
SELECT c.user_id,
       CONCAT(c.First_Name,' ',c.Last_Name) AS customer,
       ROUND(SUM(p.Amount),2)               AS total_spend
FROM   Customer c
JOIN   Payment  p USING (user_id)
GROUP  BY c.user_id
ORDER  BY total_spend DESC
LIMIT  5;

-- 2) Avg trip duration by travel type
SELECT ti.Travel_Type,
       ROUND(AVG(DATEDIFF(t.end_date,t.start_date)),1) AS avg_days
FROM   Trips t
JOIN   User_Trips ut USING (trip_id)
JOIN   Basic_Travel bt ON bt.user_id = ut.user_id
JOIN   Transportation_Info ti USING (transportation_id)
GROUP  BY ti.Travel_Type; 