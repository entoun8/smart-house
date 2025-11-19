-- ============================================
-- Smart House Database Schema
-- ============================================
-- Complete database setup for ESP32 Smart House IoT system
--
-- Run this in Supabase SQL Editor:
-- https://ktpswojqtskcnqlxzhwa.supabase.co/project/ktpswojqtskcnqlxzhwa/sql/new
--
-- This file includes:
-- - 5 core tables (users, temperature_logs, motion_logs, gas_logs, rfid_scans)
-- - Indexes for performance
-- - Views for common queries
-- - Permissions setup
-- - Sample test data
--
-- Version: 1.0
-- Last Updated: 2025-11-18
-- ============================================


-- ============================================
-- SECTION 1: CLEAN START (Optional)
-- ============================================
-- Uncomment these lines to completely reset the database
-- WARNING: This will delete ALL data!

-- DROP SCHEMA public CASCADE;
-- CREATE SCHEMA public;
-- GRANT ALL ON SCHEMA public TO postgres;
-- GRANT ALL ON SCHEMA public TO public;


-- ============================================
-- SECTION 2: CREATE TABLES
-- ============================================

-- Table 1: users
-- Stores authorized users and their RFID cards
-- Used in: Task 7 (RFID Access Control)
CREATE TABLE IF NOT EXISTS users (
    id BIGSERIAL PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    rfid_card VARCHAR(50) UNIQUE NOT NULL,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- Table 2: temperature_logs
-- Stores temperature and humidity readings from DHT11 sensor
-- Used in: Task 2 (Temperature logging every 30 min)
--          Task 6 (Asthma alert calculation)
CREATE TABLE IF NOT EXISTS temperature_logs (
    id BIGSERIAL PRIMARY KEY,
    temp DECIMAL(5,2) NOT NULL,
    humidity DECIMAL(5,2) NOT NULL,
    timestamp TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- Table 3: motion_logs
-- Records PIR motion detection events
-- Used in: Task 3 (Motion detection → RGB orange → Database log)
CREATE TABLE IF NOT EXISTS motion_logs (
    id BIGSERIAL PRIMARY KEY,
    timestamp TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- Table 4: gas_logs
-- Records gas sensor readings (0 = normal, 1 = detected)
-- Used in: Task 5 (Gas detection → Fan + RGB red → Database log)
CREATE TABLE IF NOT EXISTS gas_logs (
    id BIGSERIAL PRIMARY KEY,
    value INTEGER NOT NULL CHECK (value IN (0, 1)),
    timestamp TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- Table 5: rfid_scans
-- Records all RFID card scan attempts (successful and failed)
-- Used in: Task 7 (RFID access control)
CREATE TABLE IF NOT EXISTS rfid_scans (
    id BIGSERIAL PRIMARY KEY,
    card_id VARCHAR(50) NOT NULL,
    success BOOLEAN NOT NULL,
    user_id BIGINT REFERENCES users(id),
    timestamp TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);


-- ============================================
-- SECTION 3: CREATE INDEXES
-- ============================================
-- Indexes improve query performance for common operations

CREATE INDEX IF NOT EXISTS idx_users_rfid ON users(rfid_card);
CREATE INDEX IF NOT EXISTS idx_temperature_timestamp ON temperature_logs(timestamp DESC);
CREATE INDEX IF NOT EXISTS idx_motion_timestamp ON motion_logs(timestamp DESC);
CREATE INDEX IF NOT EXISTS idx_gas_timestamp ON gas_logs(timestamp DESC);
CREATE INDEX IF NOT EXISTS idx_rfid_timestamp ON rfid_scans(timestamp DESC);
CREATE INDEX IF NOT EXISTS idx_rfid_card ON rfid_scans(card_id);
CREATE INDEX IF NOT EXISTS idx_rfid_user ON rfid_scans(user_id);


-- ============================================
-- SECTION 4: CREATE VIEWS
-- ============================================
-- Views provide convenient access to commonly needed data

-- View 1: latest_temperature
-- Returns the most recent temperature and humidity reading
CREATE OR REPLACE VIEW latest_temperature AS
SELECT temp, humidity, timestamp
FROM temperature_logs
ORDER BY timestamp DESC
LIMIT 1;

-- View 2: today_motion_count
-- Counts motion detections for the current day
CREATE OR REPLACE VIEW today_motion_count AS
SELECT COUNT(*) as motion_count
FROM motion_logs
WHERE timestamp >= CURRENT_DATE;

-- View 3: asthma_risk
-- Checks if current conditions trigger asthma alert
-- Alert triggers when: humidity > 50% AND temperature > 27°C
CREATE OR REPLACE VIEW asthma_risk AS
SELECT
    temp,
    humidity,
    timestamp,
    CASE
        WHEN humidity > 50 AND temp > 27 THEN true
        ELSE false
    END as is_risk
FROM temperature_logs
ORDER BY timestamp DESC
LIMIT 1;


-- ============================================
-- SECTION 5: CONFIGURE PERMISSIONS
-- ============================================
-- Allow IoT devices to access the database

-- Disable Row Level Security for all tables
ALTER TABLE users DISABLE ROW LEVEL SECURITY;
ALTER TABLE temperature_logs DISABLE ROW LEVEL SECURITY;
ALTER TABLE motion_logs DISABLE ROW LEVEL SECURITY;
ALTER TABLE gas_logs DISABLE ROW LEVEL SECURITY;
ALTER TABLE rfid_scans DISABLE ROW LEVEL SECURITY;

-- Grant full access to anonymous role (for IoT devices)
GRANT ALL ON users TO anon;
GRANT ALL ON temperature_logs TO anon;
GRANT ALL ON motion_logs TO anon;
GRANT ALL ON gas_logs TO anon;
GRANT ALL ON rfid_scans TO anon;

-- Grant sequence access for auto-increment IDs
GRANT USAGE, SELECT ON ALL SEQUENCES IN SCHEMA public TO anon;


-- ============================================
-- SECTION 6: INSERT SAMPLE DATA
-- ============================================

-- Add default user
INSERT INTO users (name, rfid_card) VALUES
    ('Tonis', 'CARD_001')
ON CONFLICT (rfid_card) DO NOTHING;

-- Add test users for RFID testing
INSERT INTO users (name, rfid_card) VALUES
    ('Alice Johnson', 'CARD_123'),
    ('Bob Smith', 'CARD_456'),
    ('Carol White', 'CARD_789'),
    ('David Brown', 'CARD_ABC')
ON CONFLICT (rfid_card) DO NOTHING;

-- Add sample temperature readings
INSERT INTO temperature_logs (temp, humidity) VALUES
    (23.5, 41.2),
    (24.0, 43.5),
    (22.8, 39.7);

-- Add sample motion event
INSERT INTO motion_logs DEFAULT VALUES;

-- Add sample gas reading (0 = normal)
INSERT INTO gas_logs (value) VALUES (0);


-- ============================================
-- SECTION 7: VERIFICATION QUERIES
-- ============================================

-- Verify tables were created (should show 5 tables)
SELECT 'TABLES' as type, COUNT(*) as count
FROM information_schema.tables
WHERE table_schema = 'public' AND table_type = 'BASE TABLE'
UNION ALL
SELECT 'VIEWS', COUNT(*)
FROM information_schema.views
WHERE table_schema = 'public';

-- Show all table names
SELECT table_name
FROM information_schema.tables
WHERE table_schema = 'public' AND table_type = 'BASE TABLE'
ORDER BY table_name;

-- Count rows in each table
SELECT 'users' as table_name, COUNT(*) as row_count FROM users
UNION ALL SELECT 'temperature_logs', COUNT(*) FROM temperature_logs
UNION ALL SELECT 'motion_logs', COUNT(*) FROM motion_logs
UNION ALL SELECT 'gas_logs', COUNT(*) FROM gas_logs
UNION ALL SELECT 'rfid_scans', COUNT(*) FROM rfid_scans
ORDER BY table_name;

-- Verify permissions (should show grants for 'anon' role)
SELECT grantee, table_name, privilege_type
FROM information_schema.role_table_grants
WHERE grantee = 'anon' AND table_schema = 'public'
ORDER BY table_name, privilege_type;


-- ============================================
-- SECTION 8: USEFUL QUERIES
-- ============================================

-- Get latest temperature
-- SELECT * FROM latest_temperature;

-- Get today's motion count
-- SELECT * FROM today_motion_count;

-- Check asthma risk
-- SELECT * FROM asthma_risk;

-- Get recent RFID scans with user names
-- SELECT
--     r.timestamp,
--     r.card_id,
--     r.success,
--     u.name as user_name
-- FROM rfid_scans r
-- LEFT JOIN users u ON r.user_id = u.id
-- ORDER BY r.timestamp DESC
-- LIMIT 10;

-- Get last hour of motion detections
-- SELECT COUNT(*) as motion_count
-- FROM motion_logs
-- WHERE timestamp >= NOW() - INTERVAL '1 hour';


-- ============================================
-- DONE! ✅
-- ============================================
-- Database setup complete!
--
-- You should now have:
-- - 5 tables: users, temperature_logs, motion_logs, gas_logs, rfid_scans
-- - 3 views: latest_temperature, today_motion_count, asthma_risk
-- - Indexes for performance
-- - Permissions configured
-- - Sample data loaded
--
-- Next steps:
-- 1. Connect your ESP32 via the bridge script
-- 2. Start logging sensor data
-- 3. View data on the web dashboard at http://localhost:3000
-- ============================================
