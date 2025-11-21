try:
    import urequests as requests
except ImportError:
    import requests

import ujson as json
import gc
from utils.db_config import *

class Database:
    def __init__(self):
        self.base_url = SUPABASE_REST_URL
        self.headers = get_headers()

    def _free_memory(self):
        """Free memory before HTTP requests"""
        gc.collect()

    # ============================================
    # TEMPERATURE LOGGING (Task 2)
    # ============================================

    def log_temperature(self, temp, humidity):
        """
        Record temperature and humidity reading

        Used for: Task 2 (Temperature & humidity logging every 30 min)

        Args:
            temp: Temperature in celsius
            humidity: Humidity percentage

        Returns:
            True if successful, False otherwise
        """
        url = f"{self.base_url}/temperature_logs"
        data = {"temp": temp, "humidity": humidity}

        try:
            self._free_memory()
            response = requests.post(url, json=data, headers=self.headers)
            success = response.status_code in [200, 201]
            response.close()
            self._free_memory()
            return success
        except Exception as e:
            print(f"[DB] Temp error: {e}")
            return False

    # ============================================
    # MOTION LOGGING (Task 3)
    # ============================================

    def log_motion(self):
        """
        Record motion detection event

        Used for: Task 3 (PIR movement detected → log to database)

        Returns:
            True if successful, False otherwise
        """
        url = f"{self.base_url}/motion_logs"
        try:
            self._free_memory()
            response = requests.post(url, json={}, headers=self.headers)
            success = response.status_code in [200, 201]
            response.close()
            self._free_memory()
            return success
        except Exception as e:
            print(f"[DB] Motion error: {e}")
            return False

    # ============================================
    # GAS LOGGING (Task 5)
    # ============================================

    def log_gas(self, value):
        """
        Record gas sensor reading

        Used for: Task 5 (Gas detection → log every detection)

        Args:
            value: 0 (normal) or 1 (gas detected)

        Returns:
            True if successful, False otherwise
        """
        url = f"{self.base_url}/gas_logs"
        try:
            self._free_memory()
            response = requests.post(url, json={"value": value}, headers=self.headers)
            success = response.status_code in [200, 201]
            response.close()
            self._free_memory()
            return success
        except Exception as e:
            print(f"[DB] Gas error: {e}")
            return False

    # ============================================
    # RFID LOGGING (Task 7)
    # ============================================

    def log_rfid_scan(self, card_id, success):
        """
        Record RFID card scan

        Used for: Task 7 (RFID logs ALL scans - success or fail)

        Args:
            card_id: The RFID card ID that was scanned
            success: True if authorized, False if denied

        Returns:
            True if successful, False otherwise
        """
        url = f"{self.base_url}/rfid_scans"
        try:
            self._free_memory()
            response = requests.post(url, json={"card_id": card_id, "success": success}, headers=self.headers)
            success_status = response.status_code in [200, 201]
            response.close()
            self._free_memory()
            return success_status
        except Exception as e:
            print(f"[DB] RFID error: {e}")
            return False

    # ============================================
    # QUERY DATA (Read from database)
    # ============================================

    def get_latest_temperature(self):
        """
        Get the most recent temperature reading

        Returns:
            Dictionary with temp and humidity, or None if error
        """
        url = f"{self.base_url}/temperature_logs?order=timestamp.desc&limit=1"

        try:
            response = requests.get(url, headers=self.headers)
            if response.status_code == 200:
                data = response.json()
                response.close()
                return data[0] if data else None
            response.close()
            return None
        except Exception as e:
            print(f"[ERROR] Failed to get temperature: {e}")
            return None

    def check_asthma_risk(self):
        """
        Check if current conditions trigger asthma alert
        Task 6: humidity >50% + temp >27°C

        Returns:
            True if asthma risk conditions met, False otherwise
        """
        latest = self.get_latest_temperature()
        if latest:
            temp = float(latest['temp'])
            humidity = float(latest['humidity'])
            return humidity > 50 and temp > 27
        return False

    def get_motion_count_last_hour(self):
        """
        Get number of motion detections in the last hour

        Used for: Web app display requirement

        Returns:
            Integer count, or None if error
        """
        url = f"{self.base_url}/motion_logs?timestamp=gte.{self._get_one_hour_ago()}"

        try:
            response = requests.get(url, headers=self.headers)
            if response.status_code == 200:
                data = response.json()
                count = len(data)
                response.close()
                return count
            response.close()
            return None
        except Exception as e:
            print(f"[ERROR] Failed to get motion count: {e}")
            return None

    def _get_one_hour_ago(self):
        """Helper function to get timestamp from 1 hour ago"""
        import time
        one_hour_ago = time.time() - 3600
        t = time.localtime(int(one_hour_ago))
        return f"{t[0]:04d}-{t[1]:02d}-{t[2]:02d}T{t[3]:02d}:{t[4]:02d}:{t[5]:02d}"

    # ============================================
    # RFID AUTHORIZATION (Task 7)
    # ============================================

    def check_rfid_authorization(self, card_id):
        """
        Check if RFID card is authorized

        Args:
            card_id: The RFID card ID to check

        Returns:
            tuple: (is_authorized, user_name) or (False, None) if not found
        """
        url = f"{self.base_url}/users?rfid_card=eq.{card_id}"
        try:
            self._free_memory()
            response = requests.get(url, headers=self.headers)
            if response.status_code == 200:
                data = response.json()
                response.close()
                self._free_memory()
                if data and len(data) > 0:
                    return (True, data[0].get('name', 'Unknown'))
                return (False, None)
            response.close()
            self._free_memory()
            return (False, None)
        except Exception as e:
            print(f"[DB] Auth error: {e}")
            return (False, None)

