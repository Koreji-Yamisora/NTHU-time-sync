"""
Time Picker Widget - Modern time selection component
"""

from PyQt6.QtWidgets import QWidget, QHBoxLayout, QTimeEdit
from PyQt6.QtCore import QTime, QTimer


class TimePickerWidget(QWidget):
    """A modern time picker widget using QTimeEdit"""
    
    def __init__(self, initial_time="09:00", parent=None):
        super().__init__(parent)
        self.setup_ui(initial_time)
    
    def setup_ui(self, initial_time):
        layout = QHBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        
        # Parse initial time
        try:
            hour, minute = initial_time.split(":")
            time = QTime(int(hour), int(minute))
        except:
            time = QTime(9, 0)
        
        self.time_edit = QTimeEdit()
        self.time_edit.setTime(time)
        self.time_edit.setDisplayFormat("HH:mm")
        # Set minute interval to 10 minutes
        self.time_edit.setTimeRange(QTime(0, 0), QTime(23, 50))
        
        # Connect signal to enforce 10-minute intervals
        self.time_edit.timeChanged.connect(self._enforce_ten_minute_intervals)
        self.time_edit.setStyleSheet("""
            QTimeEdit {
                padding: 8px 12px;
                border: 2px solid #404040;
                border-radius: 6px;
                background-color: #2d2d2d;
                color: #ffffff;
                font-size: 12px;
                min-height: 16px;
                min-width: 100px;
            }
            QTimeEdit:focus {
                border-color: #0d7377;
                background-color: #333333;
            }
            QTimeEdit::up-button {
                background-color: #404040;
                border: none;
                border-radius: 4px;
                width: 20px;
            }
            QTimeEdit::down-button {
                background-color: #404040;
                border: none;
                border-radius: 4px;
                width: 20px;
            }
            QTimeEdit::up-arrow {
                image: none;
                border-left: 4px solid transparent;
                border-right: 4px solid transparent;
                border-bottom: 4px solid #ffffff;
            }
            QTimeEdit::down-arrow {
                image: none;
                border-left: 4px solid transparent;
                border-right: 4px solid transparent;
                border-top: 4px solid #ffffff;
            }
        """)
        
        layout.addWidget(self.time_edit)
    
    def _enforce_ten_minute_intervals(self, time):
        """Enforce 10-minute intervals by rounding minutes to nearest 10"""
        minute = time.minute()
        rounded_minute = round(minute / 10) * 10
        
        if rounded_minute == 60:
            # Round up to next hour
            new_hour = time.hour() + 1
            if new_hour > 23:
                new_hour = 23
                rounded_minute = 50
            new_time = QTime(new_hour, rounded_minute)
        else:
            new_time = QTime(time.hour(), rounded_minute)
        
        # Only update if the time actually changed to avoid infinite loops
        if new_time != time:
            self.time_edit.blockSignals(True)
            self.time_edit.setTime(new_time)
            self.time_edit.blockSignals(False)
    
    def get_time(self):
        """Get the selected time as HH:MM string"""
        return self.time_edit.time().toString("HH:mm")
    
    def set_time(self, time_str):
        """Set the time from HH:MM string"""
        try:
            hour, minute = time_str.split(":")
            time = QTime(int(hour), int(minute))
            self.time_edit.setTime(time)
        except:
            pass
