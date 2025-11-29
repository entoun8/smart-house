DROP VIEW IF EXISTS asthma_risk;
DROP VIEW IF EXISTS latest_temperature;
DROP VIEW IF EXISTS today_motion_count;
DROP TABLE IF EXISTS rfid_scans CASCADE;
DROP TABLE IF EXISTS gas_logs CASCADE;
DROP TABLE IF EXISTS motion_logs CASCADE;
DROP TABLE IF EXISTS temperature_logs CASCADE;
DROP TABLE IF EXISTS users CASCADE;

CREATE TABLE users (
    id BIGSERIAL PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    rfid_card VARCHAR(50) UNIQUE NOT NULL,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

CREATE TABLE temperature_logs (
    id BIGSERIAL PRIMARY KEY,
    temp DECIMAL(5,2) NOT NULL,
    humidity DECIMAL(5,2) NOT NULL,
    timestamp TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

CREATE TABLE motion_logs (
    id BIGSERIAL PRIMARY KEY,
    timestamp TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

CREATE TABLE gas_logs (
    id BIGSERIAL PRIMARY KEY,
    value INTEGER NOT NULL CHECK (value IN (0, 1)),
    timestamp TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

CREATE TABLE rfid_scans (
    id BIGSERIAL PRIMARY KEY,
    card_id VARCHAR(50) NOT NULL,
    success BOOLEAN NOT NULL,
    user_id BIGINT REFERENCES users(id),
    timestamp TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

CREATE INDEX idx_users_rfid ON users(rfid_card);
CREATE INDEX idx_temperature_timestamp ON temperature_logs(timestamp DESC);
CREATE INDEX idx_motion_timestamp ON motion_logs(timestamp DESC);
CREATE INDEX idx_gas_timestamp ON gas_logs(timestamp DESC);
CREATE INDEX idx_rfid_timestamp ON rfid_scans(timestamp DESC);
CREATE INDEX idx_rfid_card ON rfid_scans(card_id);
CREATE INDEX idx_rfid_user ON rfid_scans(user_id);

ALTER TABLE users DISABLE ROW LEVEL SECURITY;
ALTER TABLE temperature_logs DISABLE ROW LEVEL SECURITY;
ALTER TABLE motion_logs DISABLE ROW LEVEL SECURITY;
ALTER TABLE gas_logs DISABLE ROW LEVEL SECURITY;
ALTER TABLE rfid_scans DISABLE ROW LEVEL SECURITY;

GRANT ALL ON users TO anon;
GRANT ALL ON temperature_logs TO anon;
GRANT ALL ON motion_logs TO anon;
GRANT ALL ON gas_logs TO anon;
GRANT ALL ON rfid_scans TO anon;
GRANT USAGE, SELECT ON ALL SEQUENCES IN SCHEMA public TO anon;

INSERT INTO users (name, rfid_card) VALUES ('Tonis', '0x7cdab502') ON CONFLICT (rfid_card) DO NOTHING;
