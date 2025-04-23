/* ----------  DATABASE  ---------- */
DROP   DATABASE IF EXISTS travel_db;
CREATE DATABASE        travel_db;
USE    travel_db;

/* ----------  TABLES  ---------- */

/* 1. Address  (PK first so Customer can FK) */
CREATE TABLE Address (
    AddressID     INT AUTO_INCREMENT PRIMARY KEY,
    Address       VARCHAR(50),
    Address2      VARCHAR(50),
    Postal_Code   VARCHAR(10),
    Phone         VARCHAR(20),
    City          VARCHAR(50),
    Country       VARCHAR(50)
);

/* 2. Customer */
CREATE TABLE Customer (
    user_id       INT AUTO_INCREMENT PRIMARY KEY,
    AddressID     INT NULL,
    First_Name    VARCHAR(255),
    Last_Name     VARCHAR(255),
    Email         VARCHAR(50),
    Create_Date   DATETIME DEFAULT CURRENT_TIMESTAMP,
    CONSTRAINT fk_cust_address
        FOREIGN KEY (AddressID) REFERENCES Address(AddressID)
);

/* 3. Transportation_Info */
CREATE TABLE Transportation_Info (
    RentalID          INT AUTO_INCREMENT PRIMARY KEY,
    Travel_Type       VARCHAR(30),
    Cost              INT,               -- stored in USD cents for simplicity
    Time_hours        INT,
    transportation_id INT,               -- retained for parity w/ dict (FK below)
    INDEX idx_transportation_id (transportation_id)  -- Add index for foreign key constraint
);

/* 4. Basic_Travel  (one-to-one with Transportation_Info) */
CREATE TABLE Basic_Travel (
    transportation_id INT PRIMARY KEY,
    Budget            INT,
    user_id           INT,
    State             VARCHAR(30),
    Num_People        INT,
    CONSTRAINT fk_bt_trans  FOREIGN KEY (transportation_id)
                REFERENCES Transportation_Info(transportation_id),
    CONSTRAINT fk_bt_cust   FOREIGN KEY (user_id)
                REFERENCES Customer(user_id)
);

/* 5. Trips */
CREATE TABLE Trips (
    trip_id     INT AUTO_INCREMENT PRIMARY KEY,
    trip_name   VARCHAR(100),
    start_date  DATE,
    end_date    DATE
);

/* 6. User_Trips  (link table) */
CREATE TABLE User_Trips (
    user_trip_id INT AUTO_INCREMENT PRIMARY KEY,
    user_id      INT,
    trip_id      INT,
    CONSTRAINT fk_ut_cust  FOREIGN KEY (user_id) REFERENCES Customer(user_id),
    CONSTRAINT fk_ut_trip  FOREIGN KEY (trip_id) REFERENCES Trips(trip_id)
);

/* 7. Staff */
CREATE TABLE Staff (
    staff_id    INT AUTO_INCREMENT PRIMARY KEY,
    AddressID   INT,
    First_Name  VARCHAR(255),
    Last_Name   VARCHAR(255),
    Email       VARCHAR(50),
    CONSTRAINT fk_staff_addr FOREIGN KEY (AddressID)
             REFERENCES Address(AddressID)
);

/* 8. Payment */
CREATE TABLE Payment (
    payment_id  INT AUTO_INCREMENT PRIMARY KEY,
    user_id     INT,
    RentalID    INT,
    Amount      DECIMAL(19,2),
    Payment_Date DATETIME DEFAULT CURRENT_TIMESTAMP,
    staff_id    INT,
    CONSTRAINT fk_pay_cust   FOREIGN KEY (user_id)  REFERENCES Customer(user_id),
    CONSTRAINT fk_pay_rental FOREIGN KEY (RentalID) REFERENCES Transportation_Info(RentalID),
    CONSTRAINT fk_pay_staff  FOREIGN KEY (staff_id) REFERENCES Staff(staff_id)
); 