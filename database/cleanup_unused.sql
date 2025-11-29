-- ============================================
-- Clean Up Unused Tables and Views
-- ============================================
-- Run this in Supabase SQL Editor to remove unused tables/views

-- Drop unused views
DROP VIEW IF EXISTS asthma_risk;
DROP VIEW IF EXISTS latest_temperature;
DROP VIEW IF EXISTS today_motion_count;

-- Drop unused tables (not referenced in web app code)
DROP TABLE IF EXISTS led_logs;
DROP TABLE IF EXISTS steam_logs;

-- Verify what remains
SELECT
    schemaname,
    tablename as name,
    'table' as type
FROM pg_tables
WHERE schemaname = 'public'
UNION ALL
SELECT
    schemaname,
    viewname as name,
    'view' as type
FROM pg_views
WHERE schemaname = 'public'
ORDER BY type, name;
