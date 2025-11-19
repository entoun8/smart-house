from TestingSuite import PicoTestBase
from components.actuators.window import WindowServo

class WindowServoTest(PicoTestBase):
    """Unit tests for Window Servo component"""

    def test_window_servo_initialization(self):
        """Test WindowServo can be created"""
        window = WindowServo()
        assert window is not None
        assert window.current_angle is not None

    def test_window_set_angle(self):
        """Test Window sets angle"""
        window = WindowServo()
        window.set_angle(90)
        assert window.current_angle == 90

    def test_window_open(self):
        """Test Window opens"""
        window = WindowServo()
        window.open()
        assert window.current_angle == 180

    def test_window_close(self):
        """Test Window closes"""
        window = WindowServo()
        window.close()
        assert window.current_angle == 0

    def test_window_angle_range(self):
        """Test Window angle range"""
        window = WindowServo()
        window.set_angle(0)
        assert window.current_angle == 0
        window.set_angle(180)
        assert window.current_angle == 180
        window.set_angle(90)
        assert window.current_angle == 90
