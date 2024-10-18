# ET color constants
from enum import Enum

class Colors(Enum):
    ORANGE = "#E76A31"
    GREEN_DEVELOP = "#39FF14"
    NEON_RED = "#fd080a"
    GRAY = ("gray75", "gray30")

MAIN_COLOR = Colors.GREEN_DEVELOP.value

# Test status constants
class TestStatus(Enum):
    TEST_RUNNING = "Test running"
    TEST_PAUSED = "Test paused"
    TEST_STOPPED = "Test stopped"
    TEST_COMPLETED = "Test completed"
    TEST_FAILED = "Test failed"

# Test constants
class TestConstants(Enum):
    VOLTAGE_500 = 500
    VOLTAGE_1530 = 1530
    VOLTAGE_1540 = 1540
    VOLTAGE_1602 = 1602
    CURRENT_CUT_OFF = 5.2
    RUNTIME = 1.5
    PAUSE_TIME = 1
    TIMEOUT = 10
