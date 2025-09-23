"""
Time Slot Dialog - Popup window for adding time slots
"""

from PyQt6.QtWidgets import (
    QDialog, QVBoxLayout, QHBoxLayout, QLabel, QPushButton, 
    QComboBox, QGridLayout, QMessageBox
)
from PyQt6.QtCore import Qt
from .time_picker import TimePickerWidget


class TimeSlotDialog(QDialog):
    """Dialog for adding time slots to persons or courses"""
    
    def __init__(self, days, parent=None, title="Add Time Slot"):
        super().__init__(parent)
        self.days = days
        self.title = title
        self.setup_ui()
    
    def setup_ui(self):
        """Setup the dialog UI"""
        self.setWindowTitle(self.title)
        self.setModal(True)
        self.setFixedSize(450, 250)
        
        layout = QVBoxLayout(self)
        layout.setContentsMargins(20, 20, 20, 20)
        layout.setSpacing(15)
        
        # Title
        title_label = QLabel(self.title)
        title_label.setStyleSheet("""
            font-size: 18px;
            font-weight: 600;
            color: #007ACC;
            margin-bottom: 10px;
        """)
        layout.addWidget(title_label)
        
        # Form layout
        form_layout = QGridLayout()
        form_layout.setSpacing(15)
        form_layout.setColumnMinimumWidth(1, 120)
        form_layout.setColumnMinimumWidth(3, 120)
        
        # Day selection
        form_layout.addWidget(QLabel("Day:"), 0, 0)
        self.day_combo = QComboBox()
        self.day_combo.addItems(self.days)
        self.day_combo.setMinimumWidth(120)
        form_layout.addWidget(self.day_combo, 0, 1)
        
        # Start time
        form_layout.addWidget(QLabel("Start Time:"), 0, 2)
        self.start_time = TimePickerWidget("09:00")
        self.start_time.setMinimumWidth(120)
        form_layout.addWidget(self.start_time, 0, 3)
        
        # End time
        form_layout.addWidget(QLabel("End Time:"), 1, 0)
        self.end_time = TimePickerWidget("10:00")
        self.end_time.setMinimumWidth(120)
        form_layout.addWidget(self.end_time, 1, 1)
        
        layout.addLayout(form_layout)
        
        # Buttons
        button_layout = QHBoxLayout()
        button_layout.setSpacing(10)
        
        self.cancel_btn = QPushButton("Cancel")
        self.cancel_btn.clicked.connect(self.reject)
        
        self.add_btn = QPushButton("Add Time Slot")
        self.add_btn.clicked.connect(self.accept)
        self.add_btn.setDefault(True)
        
        button_layout.addStretch()
        button_layout.addWidget(self.cancel_btn)
        button_layout.addWidget(self.add_btn)
        
        layout.addLayout(button_layout)
    
    def get_time_slot_data(self):
        """Get the time slot data from the dialog"""
        return {
            'day': self.day_combo.currentText(),
            'start_time': self.start_time.get_time(),
            'end_time': self.end_time.get_time()
        }
    
    def validate_times(self):
        """Validate the time inputs"""
        start_time = self.start_time.get_time()
        end_time = self.end_time.get_time()
        
        try:
            start_hour, start_min = map(int, start_time.split(":"))
            end_hour, end_min = map(int, end_time.split(":"))
            
            start_minutes = start_hour * 60 + start_min
            end_minutes = end_hour * 60 + end_min
            
            if start_minutes >= end_minutes:
                QMessageBox.warning(self, "Invalid Time", "Start time must be before end time.")
                return False
                
        except ValueError:
            QMessageBox.warning(self, "Invalid Time", "Please enter valid times in HH:MM format.")
            return False
        
        return True
    
    def accept(self):
        """Override accept to validate before closing"""
        if self.validate_times():
            super().accept()
