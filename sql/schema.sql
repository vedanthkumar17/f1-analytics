-- F1 Analytics schema (PostgreSQL / Neon)
-- Idempotent: safe to run multiple times.

CREATE TABLE IF NOT EXISTS sessions (
    session_key         INTEGER PRIMARY KEY,
    circuit_short_name  TEXT NOT NULL,
    country_name        TEXT,
    session_name        TEXT,
    year                INTEGER
);

CREATE TABLE IF NOT EXISTS drivers (
    session_key     INTEGER NOT NULL REFERENCES sessions (session_key) ON DELETE CASCADE,
    driver_number   INTEGER NOT NULL,
    full_name       TEXT,
    name_acronym    TEXT,
    first_name      TEXT,
    last_name       TEXT,
    team_name       TEXT,
    PRIMARY KEY (session_key, driver_number)
);

CREATE TABLE IF NOT EXISTS laps (
    id                  BIGSERIAL PRIMARY KEY,
    session_key         INTEGER NOT NULL,
    driver_number       INTEGER NOT NULL,
    lap_number          INTEGER NOT NULL,
    duration_sector_1   DOUBLE PRECISION,
    duration_sector_2   DOUBLE PRECISION,
    duration_sector_3   DOUBLE PRECISION,
    lap_duration        DOUBLE PRECISION,
    st_speed            DOUBLE PRECISION,
    is_pit_out_lap      BOOLEAN DEFAULT FALSE,
    CONSTRAINT laps_driver_fk
        FOREIGN KEY (session_key, driver_number)
        REFERENCES drivers (session_key, driver_number)
        ON DELETE CASCADE,
    CONSTRAINT laps_unique
        UNIQUE (session_key, driver_number, lap_number)
);

CREATE TABLE IF NOT EXISTS pit_stops (
    id                  BIGSERIAL PRIMARY KEY,
    session_key         INTEGER NOT NULL,
    driver_number       INTEGER NOT NULL,
    lap_number          INTEGER NOT NULL,
    stop_duration       DOUBLE PRECISION,
    lane_duration       DOUBLE PRECISION,
    CONSTRAINT pit_stops_driver_fk
        FOREIGN KEY (session_key, driver_number)
        REFERENCES drivers (session_key, driver_number)
        ON DELETE CASCADE,
    CONSTRAINT pit_stops_unique
        UNIQUE (session_key, driver_number, lap_number)
);

CREATE INDEX IF NOT EXISTS idx_laps_session_driver ON laps (session_key, driver_number);
CREATE INDEX IF NOT EXISTS idx_pit_stops_session_driver ON pit_stops (session_key, driver_number);
