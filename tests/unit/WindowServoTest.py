from TestingSuite import PicoTestBase
from components.actuators.window import WindowServo

class WindowServoTest(PicoTestBase):
    def test_window_servo_initialization(self):
        window = WindowServo()
        assert window is not None
        assert window.current_angle is not None

    def test_window_set_angle(self):
        window = WindowServo()
        window.set_angle(90)
        assert window.current_angle == 90

    def test_window_open(self):
        window = WindowServo()
        window.open()
        assert window.current_angle == 180

    def test_window_close(self):
        window = WindowServo()
        window.close()
        assert window.current_angle == 0

    def test_window_angle_range(self):
        window = WindowServo()
        window.set_angle(0)
        assert window.current_angle == 0
        window.set_angle(180)
        assert window.current_angle == 180
        window.set_angle(90)
        assert window.current_angle == 90
