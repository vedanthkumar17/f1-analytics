-- F1 Analytics views (PostgreSQL / Neon)
-- Idempotent: safe to run multiple times.
-- Lap filters match the current data.py: exclude pit-out laps, drop rows with
-- null sector times or lap_duration, and exclude lap_duration >= 150.

-- Fastest lap per driver per session.
CREATE OR REPLACE VIEW v_fastest_lap_per_driver AS
SELECT
    session_key,
    driver_number,
    MIN(lap_duration) AS fastest_lap
FROM laps
WHERE is_pit_out_lap = FALSE
  AND duration_sector_1 IS NOT NULL
  AND duration_sector_2 IS NOT NULL
  AND duration_sector_3 IS NOT NULL
  AND lap_duration IS NOT NULL
  AND lap_duration < 150
GROUP BY session_key, driver_number;

-- Average pit stop per driver per session.
CREATE OR REPLACE VIEW v_avg_pit_stop_per_driver AS
SELECT
    session_key,
    driver_number,
    AVG(stop_duration) AS avg_stop,
    COUNT(*)           AS total_stops
FROM pit_stops
WHERE stop_duration IS NOT NULL
GROUP BY session_key, driver_number;

-- Average lap time per team per session.
CREATE OR REPLACE VIEW v_avg_lap_time_per_team AS
SELECT
    l.session_key,
    d.team_name,
    AVG(l.lap_duration) AS avg_lap_time
FROM laps l
JOIN drivers d
    ON d.session_key = l.session_key
   AND d.driver_number = l.driver_number
WHERE l.is_pit_out_lap = FALSE
  AND l.duration_sector_1 IS NOT NULL
  AND l.duration_sector_2 IS NOT NULL
  AND l.duration_sector_3 IS NOT NULL
  AND l.lap_duration IS NOT NULL
  AND l.lap_duration < 150
GROUP BY l.session_key, d.team_name;
