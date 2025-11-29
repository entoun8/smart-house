from TestingSuite import PicoTestBase
from components.actuators.door import DoorServo

class DoorServoTest(PicoTestBase):
    def test_door_servo_initialization(self):
        door = DoorServo()
        assert door is not None
        assert door.current_angle is not None

    def test_door_set_angle(self):
        door = DoorServo()
        door.set_angle(90)
        assert door.current_angle == 90

    def test_door_open(self):
        door = DoorServo()
        door.open()
        assert door.current_angle == 180

    def test_door_close(self):
        door = DoorServo()
        door.close()
        assert door.current_angle == 0

    def test_door_angle_range(self):
        door = DoorServo()
        door.set_angle(0)
        assert door.current_angle == 0
        door.set_angle(180)
        assert door.current_angle == 180
        door.set_angle(90)
        assert door.current_angle == 90
