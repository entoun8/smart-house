import time
print("\n" + "="*50)
print("ESP32 Boot - Waiting 2 seconds...")
print("="*50)
time.sleep(2)

print("Starting ALL tasks (Task 1 + 2 + 3 + 4 + 5 + 6 + 7)...")
try:
    import main
except Exception as e:
    print(f"Error loading main: {e}")
    print("Fallback: System not starting...")
