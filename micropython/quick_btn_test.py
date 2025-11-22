from machine import Pin
from components import Fan, RGBStrip
import time

fan = Fan()
rgb = RGBStrip()
btn_left = Pin(16, Pin.IN, Pin.PULL_UP)

print('Press LEFT button to test fan and RGB...')
while True:
    if btn_left.value() == 0:
        print('LEFT pressed! Fan ON, RGB RED')
        fan.on()
        rgb.red()
        time.sleep(3)
        fan.off()
        rgb.off()
        print('Done')
        break
    time.sleep(0.1)
