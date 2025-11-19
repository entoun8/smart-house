from machine import Pin, PWM
import config


class DoorServo:
    """Door servo motor"""
    def __init__(self):
        self.pwm = PWM(Pin(config.DOOR_SERVO_PIN), freq=50)
        self.current_angle = 0

    def set_angle(self, angle):
        duty = int(26 + (angle / 180) * 102)
        self.pwm.duty(duty)
        self.current_angle = angle

    def open(self):
        self.set_angle(180)

    def close(self):
        self.set_angle(0)
