-- The fastest pit stops in 2025 Australian GP
SELECT d.full_name, p.lap_number, p.stop_duration
FROM pit_stops p
JOIN drivers d ON p.driver_number = d.driver_number
WHERE p.stop_duration IS NOT NULL
ORDER BY p.stop_duration ASC
LIMIT 5;

-- The average pit stop duration by team
SELECT d.team_name, ROUND(AVG(p.stop_duration)::numeric, 3) AS avg_stop
FROM pit_stops p
JOIN drivers d ON p.driver_number = d.driver_number
WHERE p.stop_duration IS NOT NULL
GROUP BY d.team_name
ORDER BY avg_stop ASC;

-- The total number of pit stops for each driver
SELECT d.full_name, COUNT(*) AS total_stops
FROM pit_stops p
JOIN drivers d ON p.driver_number = d.driver_number
GROUP BY d.full_name
ORDER BY total_stops DESC;

-- The fastest lap times for each driver in the 2025 Australian GP
select d.full_name, min(l.lap_duration) as fastest_lap
from laps l join drivers d on l.driver_number = d.driver_number
group by d.full_name
order by fastest_lap asc
limit 5;

-- A query that shows both fastest lap AND average pit stop for each driver in the same result
select d.full_name as name, min(l.lap_duration) as fastest_lap,round( avg(p.stop_duration)::numeric, 2) as avg_stop_duration
from laps l
join drivers d on l.driver_number = d.driver_number
join pit_stops p on l.driver_number = p.driver_number
group by name order by fastest_lap;
