from TestingSuite import PicoTestBase
from components.actuators.door import DoorServo

class DoorServoTest(PicoTestBase):
    """Unit tests for Door Servo component"""

    def test_door_servo_initialization(self):
        """Test DoorServo can be created"""
        door = DoorServo()
        assert door is not None
        assert door.current_angle is not None

    def test_door_set_angle(self):
        """Test Door sets angle"""
        door = DoorServo()
        door.set_angle(90)
        assert door.current_angle == 90

    def test_door_open(self):
        """Test Door opens"""
        door = DoorServo()
        door.open()
        assert door.current_angle == 180

    def test_door_close(self):
        """Test Door closes"""
        door = DoorServo()
        door.close()
        assert door.current_angle == 0

    def test_door_angle_range(self):
        """Test Door angle range"""
        door = DoorServo()
        door.set_angle(0)
        assert door.current_angle == 0
        door.set_angle(180)
        assert door.current_angle == 180
        door.set_angle(90)
        assert door.current_angle == 90
