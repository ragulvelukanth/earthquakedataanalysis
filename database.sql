SELECT * FROM earthquake_db.earthquakeneww;
SELECT id, magnitude, location
FROM earthquake_db.earthquakeneww
ORDER BY magnitude DESC;
SELECT id, magnitude, location
FROM earthquake_db.earthquakeneww
ORDER BY magnitude DESC;
SELECT id, depth, location
FROM earthquake_db.earthquakeneww
ORDER BY depth DESC;
SELECT id, magnitude, depth, location
FROM earthquake_db.earthquakeneww
WHERE depth < 50 AND magnitude > 7.5;
SELECT continent, AVG(depth) AS average_depth
FROM earthquake_db.earthquakeneww
GROUP BY continent;
SELECT magType, AVG(magnitude) AS average_magnitude
FROM earthquake_db.earthquakeneww
GROUP BY magType;
SELECT Year, COUNT(*) AS earthquake_count
FROM earthquake_db.earthquakeneww
GROUP BY Year
ORDER BY earthquake_count DESC;
SELECT month, COUNT(*) AS earthquake_count
FROM earthquake_db.earthquakeneww
GROUP BY month
ORDER BY earthquake_count DESC;
SELECT day_of_week, COUNT(*) AS earthquake_count
FROM earthquake_db.earthquakeneww
GROUP BY day_of_week
ORDER BY earthquake_count DESC;
SELECT HOUR(event_time) AS hour_of_day, COUNT(*) AS earthquake_count
FROM earthquake_db.earthquakeneww
GROUP BY hour_of_day
ORDER BY hour_of_day;
SELECT net, COUNT(*) AS event_count
FROM earthquake_db.earthquakeneww
GROUP BY net
ORDER BY event_count DESC;
SELECT location, SUM(Casualty_Felt_Reports) AS total_felt_reports
FROM earthquake_db.earthquakeneww
GROUP BY location
ORDER BY total_felt_reports DESC;
SELECT continent, SUM(Economic_Loss_Significance) AS total_economic_loss_significance
FROM earthquake_db.earthquakeneww
GROUP BY continent;
SELECT alert, AVG(Economic_Loss_Significance) AS average_economic_loss_significance
FROM earthquake_db.earthquakeneww
GROUP BY alert;
SELECT status, COUNT(*) AS earthquake_count
FROM earthquake_db.earthquakeneww
GROUP BY status;
SELECT event_type, COUNT(*) AS earthquake_count
FROM earthquake_db.earthquakeneww
GROUP BY event_type;
SELECT types, COUNT(*) AS earthquake_count
FROM earthquake_db.earthquakeneww
GROUP BY types;
SELECT continent, AVG(rms) AS average_rms, AVG(gap) AS average_gap
FROM earthquake_db.earthquakeneww
GROUP BY continent;
SELECT id, location, nst, magnitude
FROM earthquake_db.earthquakeneww
WHERE nst > 100;
SELECT Year, COUNT(*) AS tsunami_count
FROM earthquake_db.earthquakeneww
WHERE tsunami = 1
GROUP BY Year
ORDER BY Year;
SELECT alert, COUNT(*) AS earthquake_count
FROM earthquake_db.earthquakeneww
GROUP BY alert;
SELECT country, AVG(magnitude) AS average_magnitude
FROM earthquake_db.earthquakeneww
WHERE Year >= YEAR(CURDATE()) - 10
GROUP BY country
ORDER BY average_magnitude DESC;
SELECT DISTINCT country
FROM (
    SELECT country, Year, month, depth_category
    FROM earthquake_db.earthquakeneww
    WHERE depth_category IN ('Shallow', 'Deep')
) AS monthly_depth_categories
GROUP BY country, Year, month
HAVING
    SUM(CASE WHEN depth_category = 'Shallow' THEN 1 ELSE 0 END) > 0
    AND SUM(CASE WHEN depth_category = 'Deep' THEN 1 ELSE 0 END) > 0;
    SELECT
    current_year.Year,
    current_year.total_earthquakes,
    previous_year.total_earthquakes AS previous_year_earthquakes,
    (current_year.total_earthquakes - previous_year.total_earthquakes) / previous_year.total_earthquakes * 100 AS growth_rate_percent
FROM
    (SELECT Year, COUNT(*) AS total_earthquakes FROM earthquake_db.earthquakeneww GROUP BY Year) AS current_year
JOIN
    (SELECT Year, COUNT(*) AS total_earthquakes FROM earthquake_db.earthquakeneww GROUP BY Year) AS previous_year
    ON current_year.Year = previous_year.Year + 1
WHERE previous_year.total_earthquakes > 0; 
SELECT
    country,
    COUNT(*) AS frequency,
    AVG(magnitude) AS average_magnitude
FROM earthquake_db.earthquakeneww
GROUP BY country
ORDER BY frequency DESC, average_magnitude DESC;
use earthquake_db;
show tables;
SELECT * FROM earthquakeneww LIMIT 10;
USE earthquake_db;
DESCRIBE earthquake_db.earthquakeneww;






















