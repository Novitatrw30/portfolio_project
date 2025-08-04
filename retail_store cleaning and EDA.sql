select *
FROM retail_store_sales;

ALTER TABLE retail_store_sales
RENAME COLUMN `Transaction ID` TO `Transaction_ID`;
ALTER TABLE retail_store_sales
RENAME COLUMN `Customer ID` TO `Customer_ID`;
ALTER TABLE retail_store_sales
RENAME COLUMN `Price Per Unit` TO `Price_Per_Unit`;
ALTER TABLE retail_store_sales
RENAME COLUMN `Total Spent` TO `Total_Spent`;
ALTER TABLE retail_store_sales
RENAME COLUMN `Payment Method` TO `Payment_Method`;
ALTER TABLE retail_store_sales
RENAME COLUMN `Transaction Date` TO `Transaction_Date`;
ALTER TABLE retail_store_sales
RENAME COLUMN `Discount Applied` TO `Discount_Applied`;

CREATE TABLE retail_staging
LIKE retail_store_sales;

INSERT retail_staging
select *
FROM retail_store_sales;

select * FROM retail_staging;

-- 1. REMOVE DUPLICATES IF ANY

SELECT *,
ROW_NUMBER() OVER (
PARTITION BY Transaction_ID, Customer_ID, Category, Item, Price_Per_Unit, Quantity, Total_Spent, Payment_Method, Location,
Transaction_Date, Discount_Applied) AS row_num
FROM retail_staging;

WITH duplicat_retail AS
(
SELECT *,
ROW_NUMBER() OVER (
PARTITION BY Transaction_ID, Customer_ID, Category, Item, Price_Per_Unit, Quantity, Total_Spent, Payment_Method, Location,
Transaction_Date, Discount_Applied) AS row_num
FROM retail_staging
)

Select * FROM duplicat_retail
WHERE row_num > 1;

-- there is no duplicate data, so we continue to the next step

-- 2. Standardize the Data
select *
FROM retail_staging;

SELECT DISTINCT Transaction_ID
FROM retail_staging
ORDER BY 1;

SELECT *
FROM retail_staging
WHERE Transaction_ID LIKE "TXN%";

SELECT DISTINCT Customer_ID
FROM retail_staging
ORDER BY 1;

SELECT DISTINCT Category
FROM retail_staging
ORDER BY 1;

SELECT DISTINCT Item
FROM retail_staging
ORDER BY 1;

-- we will leave the null values into the next step

SELECT DISTINCT Payment_Method
FROM retail_staging
ORDER BY 1;

SELECT DISTINCT Location
FROM retail_staging
ORDER BY 1;

-- 3. Filling Null values or blank values or mybe delete them
Select *
FROM retail_staging;

SELECT *
FROM retail_staging
WHERE Price_Per_Unit = '';

UPDATE retail_staging
SET Price_Per_Unit = 0
WHERE Price_Per_Unit = '';

UPDATE retail_staging
SET Quantity = 0
WHERE Quantity = '';

UPDATE retail_staging
SET Total_Spent = 0
WHERE Total_Spent = '';

SELECT *
FROM retail_staging;

ALTER TABLE retail_staging
MODIFY Price_Per_Unit DOUBLE;

ALTER TABLE retail_staging
MODIFY Quantity DOUBLE;

ALTER TABLE retail_staging
MODIFY Total_Spent DOUBLE;

SELECT Price_Per_unit, Total_Spent/Quantity AS Unit_Price
FROM retail_staging
WHERE Price_Per_Unit = 0;

UPDATE retail_staging
SET Price_Per_Unit = Total_Spent/Quantity
WHERE Price_Per_Unit = 0;

SELECT *
FROM retail_staging
WHERE Quantity = 0;

-- since the null quantity followed by the total spent also being null,
-- so the data is meaningless, we can removed them from the table

DELETE
FROM retail_staging
WHERE Total_Spent = 0;

SELECt DISTINCT Price_Per_Unit
FROM retail_staging
WHERE Item = '';

SELECt Item, Category, Price_Per_Unit
FROM retail_staging
WHERE Item Like "Item_10%"
ORDER BY 1;

SELECT Category, Item, Price_Per_Unit
FROM retail_staging
WHERE Price_Per_Unit = 5
ORDER BY 1;

SELECT DISTINCT Category
FROM retail_staging
ORDER BY 1;

UPDATE retail_staging
SET Item = NULL
WHERE Item = '';

SELECT distinct Category, Item, Price_Per_Unit
FROM retail_staging
WHERE Item is not null
ORDER BY 3;

SELECT DISTINCT Price_Per_Unit, Category, SUBSTRING(Item, 6,7) AS cat_code
FROM retail_staging
WHERE Item IS NOT NULL
ORDER BY 1;

SELECT Category,Item, Price_Per_Unit,
CASE
	WHEN Price_Per_Unit = 5 THEN "Item_1_"
    WHEN Price_Per_Unit = 6.5 THEN "Item_2_"
    WHEN Price_Per_Unit = 8 THEN "Item_3_"
    WHEN Price_Per_Unit = 9.5 THEN "Item_4_"
    WHEN Price_Per_Unit = 11 THEN "Item_5_"
	WHEN Price_Per_Unit = 12.5 THEN "Item_6_"
    WHEN Price_Per_Unit = 14 THEN "Item_7_"
    WHEN Price_Per_Unit = 15.5 THEN "Item_8_"
    WHEN Price_Per_Unit = 17 THEN "Item_9_"
    WHEN Price_Per_Unit = 18.5 THEN "Item_10_"
    WHEN Price_Per_Unit = 20 THEN "Item_11_"
    WHEN Price_Per_Unit = 21.5 THEN "Item_12_"
    WHEN Price_Per_Unit = 23 THEN "Item_13_"
    WHEN Price_Per_Unit = 24.5 THEN "Item_14_"
    WHEN Price_Per_Unit = 26 THEN "Item_15_"
    WHEN Price_Per_Unit = 27.5 THEN "Item_16_"
    WHEN Price_Per_Unit = 29 THEN "Item_17_"
    WHEN Price_Per_Unit = 30.5 THEN "Item_18_"
    WHEN Price_Per_Unit = 32 THEN "Item_19_"
    WHEN Price_Per_Unit = 33.5 THEN "Item_20_"
    WHEN Price_Per_Unit = 35 THEN "Item_21_"
    WHEN Price_Per_Unit = 36.5 THEN "Item_22_"
    WHEN Price_Per_Unit = 38 THEN "Item_23_"
    WHEN Price_Per_Unit = 39.5 THEN "Item_24_"
    WHEN Price_Per_Unit = 41 THEN "Item_25_"
END AS Item_code
FROM retail_staging;

SELECT Category,Item, Price_Per_Unit,
CASE
	WHEN Category = "Beverages" THEN "BAV"
    WHEN Category = "Butchers" THEN "BUT"
    WHEN Category = "Computers and electric accessories" THEN "CEA"
    WHEN Category = "Electric household essentials" THEN "EHE"
    WHEN Category = "Food" THEN "FOOD"
    WHEN Category = "Furniture" THEN "FUR"
    WHEN Category = "Milk Products" THEN "MILK"
    WHEN Category = "Patisserie" THEN "PAT"
END AS Cat_code
FROM retail_staging;

CREATE TABLE `retail_staging_2` (
  `Transaction_ID` text,
  `Customer_ID` text,
  `Category` text,
  `Item` text,
  `Price_Per_Unit` double DEFAULT NULL,
  `Quantity` double DEFAULT NULL,
  `Total_Spent` double DEFAULT NULL,
  `Payment_Method` text,
  `Location` text,
  `Transaction_Date` text,
  `Discount_Applied` text,
  `Item_code` text,
  `Cat_code` text
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

INSERT INTO retail_staging_2
SELECT *,
CASE
	WHEN Price_Per_Unit = 5 THEN "Item_1_"
    WHEN Price_Per_Unit = 6.5 THEN "Item_2_"
    WHEN Price_Per_Unit = 8 THEN "Item_3_"
    WHEN Price_Per_Unit = 9.5 THEN "Item_4_"
    WHEN Price_Per_Unit = 11 THEN "Item_5_"
	WHEN Price_Per_Unit = 12.5 THEN "Item_6_"
    WHEN Price_Per_Unit = 14 THEN "Item_7_"
    WHEN Price_Per_Unit = 15.5 THEN "Item_8_"
    WHEN Price_Per_Unit = 17 THEN "Item_9_"
    WHEN Price_Per_Unit = 18.5 THEN "Item_10_"
    WHEN Price_Per_Unit = 20 THEN "Item_11_"
    WHEN Price_Per_Unit = 21.5 THEN "Item_12_"
    WHEN Price_Per_Unit = 23 THEN "Item_13_"
    WHEN Price_Per_Unit = 24.5 THEN "Item_14_"
    WHEN Price_Per_Unit = 26 THEN "Item_15_"
    WHEN Price_Per_Unit = 27.5 THEN "Item_16_"
    WHEN Price_Per_Unit = 29 THEN "Item_17_"
    WHEN Price_Per_Unit = 30.5 THEN "Item_18_"
    WHEN Price_Per_Unit = 32 THEN "Item_19_"
    WHEN Price_Per_Unit = 33.5 THEN "Item_20_"
    WHEN Price_Per_Unit = 35 THEN "Item_21_"
    WHEN Price_Per_Unit = 36.5 THEN "Item_22_"
    WHEN Price_Per_Unit = 38 THEN "Item_23_"
    WHEN Price_Per_Unit = 39.5 THEN "Item_24_"
    WHEN Price_Per_Unit = 41 THEN "Item_25_"
END AS Item_code,
CASE
	WHEN Category = "Beverages" THEN "BEV"
    WHEN Category = "Butchers" THEN "BUT"
    WHEN Category = "Computers and electric accessories" THEN "CEA"
    WHEN Category = "Electric household essentials" THEN "EHE"
    WHEN Category = "Food" THEN "FOOD"
    WHEN Category = "Furniture" THEN "FUR"
    WHEN Category = "Milk Products" THEN "MILK"
    WHEN Category = "Patisserie" THEN "PAT"
END AS Cat_code
FROM retail_staging;

SELECT *
FROM retail_staging_2;

SELECT *, CONCAT(Item_code, Cat_code) AS Item_all
FROM retail_staging_2
WHERE Item IS NULL;

UPDATE retail_staging_2
SET Item = CONCAT(Item_code, Cat_code);

SELECT *
FROM retail_staging_2
WHERE Item IS NULL;

SELECT *
FROM retail_staging_2;

SELECT DISTINCT Payment_Method
FROM retail_staging_2;

SELECT DISTINCT Location
FROM retail_staging_2;

SELECT Transaction_Date,
STR_TO_DATE(Transaction_Date, '%Y-%m-%d') AS Formated_Date
FROM retail_staging_2;

UPDATE retail_staging_2
SET Transaction_Date = STR_TO_DATE(Transaction_Date, '%Y-%m-%d');

SELECT Transaction_Date
FROM retail_staging_2
WHERE Transaction_Date IS NULL;

SELECT Discount_Applied, COUNT(Discount_Applied) AS Num_of_data
FROM retail_staging_2
GROUP BY Discount_Applied
;

SELECT *
FROM retail_staging_2
WHERE Discount_Applied = "True";

-- there is no difference in Total_Spent on transactions that use discounts and those that don't, so we can delete the column
ALTER TABLE retail_staging_2
DROP COLUMN Discount_Applied;

-- 4. Remove any column (unnecessery)

ALTER TABLE retail_staging_2
DROP COLUMN Item_code,
DROP COLUMN Cat_code;

SELECT *
FROM retail_staging_2
;

-- CLeaning data is done, now lets continue to EDA
SELECT *
FROM retail_staging_2;

-- Who are the customers who shop most often?
SELECT Customer_ID, COUNT(Customer_ID) AS Num_transactions
FROM retail_staging_2
GROUP BY Customer_ID
ORDER BY 2 DESC
;

-- What is the total amount spent by each customer?
SELECT Customer_ID, SUM(Total_Spent) AS Sum_of_Total_Spent
FROM retail_staging_2
GROUP BY Customer_ID
ORDER BY 2 DESC
;

-- What categories are most purchased?
SELECT Category, COUNT(Category) AS Total_Purchased, SUM(Total_Spent)
FROM retail_staging_2
GROUP BY Category
ORDER BY 2 DESC
;

-- Which category has the largest number of sales?
SELECT Category, SUM(Total_Spent) AS Total_Spent_per_Category
FROM retail_staging_2
GROUP BY Category
ORDER BY 2 DESC
;

-- What is the most frequently purchased category by each customer?
SELECT Customer_ID, Category, COUNT(*) AS Most_Frequent_Category, ROW_NUMBER() OVER (PARTITION BY Customer_ID) AS rank_category
FROM retail_staging_2
GROUP BY Customer_ID, Category
ORDER BY 1
;

SELECT Customer_ID, Category , (Most_Frequent_Category)
FROM (SELECT Customer_ID, Category, COUNT(*) AS Most_Frequent_Category, ROW_NUMBER() OVER (PARTITION BY Customer_ID) AS rank_category
FROM retail_staging_2
GROUP BY Customer_ID, Category) AS Agg_category
WHERE rank_category = 1
ORDER BY 1;

-- What are the most frequently purchased items?
SELECT Item, COUNT(Item) AS Total_Purchased, SUM(Total_Spent)
FROM retail_staging_2
GROUP BY Item
ORDER BY 2 DESC
;

SELECT Item, SUM(Total_Spent) AS Total_Spent_per_Item
FROM retail_staging_2
GROUP BY Item
ORDER BY 2 DESC
;

-- What are the most frequently purchased items by each customer?
SELECT Customer_ID, Item , (Most_Frequent_Item)
FROM (SELECT Customer_ID, Item, COUNT(*) AS Most_Frequent_Item, ROW_NUMBER() OVER (PARTITION BY Customer_ID) AS rank_Item
FROM retail_staging_2
GROUP BY Customer_ID, Item) AS Agg_Item
WHERE rank_Item = 1
ORDER BY 1;

-- What is the highest purchase quantity a customer makes per transaction?
SELECT Customer_ID, MAX(Quantity)
FROM retail_staging_2
GROUP BY Customer_ID
ORDER BY 1;

-- What are the most frequently purchased items?
SELECT Item, SUM(Quantity)
FROM retail_staging_2
GROUP BY Item
ORDER BY 2
LIMIT 5;

-- What are the most frequently used payment method?
SELECT Payment_Method, COUNT(Payment_Method)
FROM retail_staging_2
GROUP BY Payment_Method
ORDER BY 2 DESC
;

-- What is the most frequent sales locations?
SELECT Location, COUNT(Location)
FROM retail_staging_2
GROUP BY Location
ORDER BY 2 DESC
;

-- Which year has the highest sales?
SELECT MIN(Transaction_Date), MAX(Transaction_Date)
FROM retail_staging_2;

SELECT YEAR(Transaction_Date), SUM(Total_Spent)
FROM retail_staging_2
GROUP BY YEAR(Transaction_Date)
ORDER BY 2 DESC;

-- How are the sales each month?
WITH Rolling_Total AS
(
SELECT SUBSTRING(Transaction_Date, 1, 7) AS Month, SUM(Total_Spent) AS total_spent_month
FROM retail_staging_2
WHERE SUBSTRING(Transaction_Date, 1, 7) IS NOT NULL
GROUP BY Month
ORDER BY 1
)
SELECT month, total_spent_month, SUM(total_spent_month) OVER(ORDER BY Month) AS rolling_total
FROM Rolling_Total;