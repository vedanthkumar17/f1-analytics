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