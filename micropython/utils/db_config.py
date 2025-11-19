SUPABASE_URL = "https://ktpswojqtskcnqlxzhwa.supabase.co"
SUPABASE_KEY = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6Imt0cHN3b2pxdHNrY25xbHh6aHdhIiwicm9sZSI6ImFub24iLCJpYXQiOjE3NjIyOTMyNDgsImV4cCI6MjA3Nzg2OTI0OH0.A0qUts3FYeOicpLlLoEkz9YpIFhjYTMKrN3jif_lHG4"

SUPABASE_REST_URL = SUPABASE_URL + "/rest/v1"

TABLE_TEMPERATURE = "temperature_logs"
TABLE_MOTION = "motion_logs"
TABLE_GAS = "gas_logs"
TABLE_WATER = "water_logs"
TABLE_RFID = "rfid_scans"
TABLE_DEVICE_STATUS = "device_status"
TABLE_ALERTS = "alerts"
TABLE_SYSTEM_LOGS = "system_logs"

def get_headers():
    """Returns headers needed for Supabase API requests"""
    return {
        'apikey': SUPABASE_KEY,
        'Authorization': f'Bearer {SUPABASE_KEY}',
        'Content-Type': 'application/json',
        'Prefer': 'return=minimal'  
    }
