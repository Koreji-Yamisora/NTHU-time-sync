"""
Schedule Manager GUI Package
Modern PyQt6-based GUI components
"""

from .main_window import ScheduleManagerPyQt6, launch_pyqt6_gui
from .time_picker import TimePickerWidget
from .schedule_tab import ScheduleTab
from .people_tab import PeopleTab
from .courses_tab import CoursesTab
from .common_times_tab import CommonTimesTab

# Export the main function for backward compatibility
launch_gui = launch_pyqt6_gui

__all__ = [
    'ScheduleManagerPyQt6',
    'launch_pyqt6_gui',
    'launch_gui',
    'TimePickerWidget',
    'ScheduleTab',
    'PeopleTab',
    'CoursesTab',
    'CommonTimesTab'
]
