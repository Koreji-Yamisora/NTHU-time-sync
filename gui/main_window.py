"""
Main Window - PyQt6 Schedule Manager
"""

import sys
from PyQt6.QtWidgets import QApplication, QMainWindow, QWidget, QVBoxLayout, QTabWidget
from PyQt6.QtCore import Qt

from .schedule_tab import ScheduleTab
from .people_tab import PeopleTab
from .courses_tab import CoursesTab
from .common_times_tab import CommonTimesTab


class ScheduleManagerPyQt6(QMainWindow):
    """Main PyQt6 application window"""
    
    def __init__(self, people_list, courses, data_file="schedule_data.json"):
        super().__init__()
        self.people_list = people_list
        self.courses = courses
        self.data_file = data_file
        
        # Days of the week
        self.days = [
            "Monday", "Tuesday", "Wednesday", "Thursday", 
            "Friday", "Saturday", "Sunday"
        ]
        
        self.setup_ui()
        self.setup_modern_style()
        self.refresh_displays()
    
    def setup_ui(self):
        """Setup the main UI"""
        self.setWindowTitle("Schedule Manager - PyQt6")
        self.setGeometry(100, 100, 1400, 900)
        self.setMinimumSize(1200, 700)
        
        # Central widget
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        
        # Main layout
        main_layout = QVBoxLayout(central_widget)
        main_layout.setContentsMargins(10, 10, 10, 10)
        main_layout.setSpacing(10)
        
        # Create tab widget
        self.tab_widget = QTabWidget()
        self.tab_widget.setStyleSheet("""
            QTabWidget::pane {
                border: none;
                border-radius: 8px;
                background-color: #252525;
                color: #ffffff;
                margin-top: 8px;
            }
            QTabBar::tab {
                background-color: #404040;
                color: #ffffff;
                padding: 8px 16px;
                margin-right: 6px;
                border-radius: 8px;
                font-weight: 600;
                font-size: 12px;
                min-width: 80px;
                border: none;
            }
            QTabBar::tab:hover {
                background-color: #555555;
                color: #ffffff;
                border-radius: 8px;
            }
            QTabBar::tab:selected {
                background-color: #007ACC;
                color: #ffffff;
                border-radius: 8px;
            }
            QTabBar::tab:selected:hover {
                background-color: #007ACC;
                color: #ffffff;
                border-radius: 8px;
            }
        """)
        
        # Create tabs
        self.schedule_tab = ScheduleTab(self)
        self.people_tab = PeopleTab(self)
        self.courses_tab = CoursesTab(self)
        self.common_times_tab = CommonTimesTab(self)
        
        self.tab_widget.addTab(self.schedule_tab, "Schedule")
        self.tab_widget.addTab(self.people_tab, "People")
        self.tab_widget.addTab(self.courses_tab, "Courses")
        self.tab_widget.addTab(self.common_times_tab, "Common Times")
        
        main_layout.addWidget(self.tab_widget)
        
        # Status bar
        self.statusBar().showMessage("Ready")
    
    def setup_modern_style(self):
        """Setup modern dark theme styling for the application"""
        # Set application style with dark theme
        self.setStyleSheet("""
            QMainWindow {
                background-color: #1e1e1e;
                color: #ffffff;
            }
            QWidget {
                font-family: 'Segoe UI', 'Arial', sans-serif;
                color: #ffffff;
                background-color: #1e1e1e;
            }
            QLabel {
                color: #ffffff;
                background-color: transparent;
            }
            QPushButton {
                background-color: #404040;
                color: white;
                border: none;
                padding: 6px 12px;
                border-radius: 4px;
                font-weight: 600;
                font-size: 11px;
                min-height: 14px;
            }
            QPushButton:hover {
                background-color: #555555;
            }
            QPushButton:pressed {
                background-color: #333333;
            }
            QPushButton:disabled {
                background-color: #404040;
                color: #888888;
            }
            QLineEdit, QComboBox {
                padding: 6px 10px;
                border: none;
                border-radius: 4px;
                background-color: #2a2a2a;
                color: #ffffff;
                font-size: 11px;
                min-height: 14px;
            }
            QLineEdit:hover, QComboBox:hover {
                background-color: #353535;
            }
            QLineEdit:focus, QComboBox:focus {
                background-color: #3a3a3a;
            }
            QComboBox::drop-down {
                border: none;
                background-color: #404040;
                width: 20px;
            }
            QComboBox::down-arrow {
                image: none;
                border-left: 5px solid transparent;
                border-right: 5px solid transparent;
                border-top: 5px solid #ffffff;
                margin-right: 5px;
            }
            QTextEdit {
                border: none;
                border-radius: 4px;
                background-color: #2a2a2a;
                color: #ffffff;
                font-family: 'Consolas', 'Monaco', 'Courier New', monospace;
                font-size: 11px;
                padding: 8px;
                line-height: 1.3;
            }
            QTextEdit:hover {
                background-color: #353535;
            }
            QTextEdit:focus {
                background-color: #3a3a3a;
            }
            QListWidget {
                border: none;
                border-radius: 4px;
                background-color: #2a2a2a;
                color: #ffffff;
                font-size: 11px;
                padding: 3px;
            }
            QListWidget::item {
                padding: 6px 10px;
                border-bottom: 1px solid #404040;
                color: #ffffff;
                background-color: transparent;
                border-radius: 3px;
                margin: 1px;
            }
            QListWidget::item:selected {
                background-color: #007ACC;
                color: #ffffff;
            }
            QListWidget::item:hover {
                background-color: #404040;
            }
            QListWidget::item:selected:hover {
                background-color: #007ACC;
            }
            QTableWidget {
                border: none;
                border-radius: 4px;
                background-color: #2a2a2a;
                color: #ffffff;
                gridline-color: #404040;
                font-size: 11px;
                padding: 3px;
            }
            QTableWidget::item {
                padding: 6px 10px;
                color: #ffffff;
                background-color: transparent;
                border-bottom: 1px solid #404040;
            }
            QTableWidget::item:selected {
                background-color: #007ACC;
                color: #ffffff;
            }
            QTableWidget::item:hover {
                background-color: #404040;
            }
            QTableWidget::item:selected:hover {
                background-color: #007ACC;
            }
            QHeaderView::section {
                background-color: #404040;
                color: #ffffff;
                padding: 8px 12px;
                border: none;
                font-weight: 600;
                border-bottom: 2px solid #666666;
            }
            QGroupBox {
                font-weight: 600;
                font-size: 12px;
                color: #ffffff;
                background-color: #252525;
                border: none;
                border-radius: 6px;
                margin-top: 4px;
                padding-top: 4px;
            }
            QGroupBox::title {
                subcontrol-origin: margin;
                left: 12px;
                padding: 0 8px 0 8px;
                color: #ffffff;
                background-color: #1e1e1e;
            }
            QCheckBox {
                color: #ffffff;
                background-color: transparent;
                spacing: 8px;
            }
            QCheckBox::indicator {
                width: 20px;
                height: 20px;
                border-radius: 4px;
            }
            QCheckBox::indicator:unchecked {
                border: 2px solid #404040;
                background-color: #2d2d2d;
            }
            QCheckBox::indicator:checked {
                border: 2px solid #007ACC;
                background-color: #2d2d2d;
                image: url(data:image/svg+xml;base64,PHN2ZyB3aWR0aD0iMTIiIGhlaWdodD0iMTIiIHZpZXdCb3g9IjAgMCAxMiAxMiIgZmlsbD0ibm9uZSIgeG1sbnM9Imh0dHA6Ly93d3cudzMub3JnLzIwMDAvc3ZnIj4KPHBhdGggZD0iTTEwIDNMNC41IDguNUwyIDYiIHN0cm9rZT0iIzAwN0FDQyIgc3Ryb2tlLXdpZHRoPSIyIiBzdHJva2UtbGluZWNhcD0icm91bmQiIHN0cm9rZS1saW5lam9pbj0icm91bmQiLz4KPC9zdmc+Cg==);
            }
            QCheckBox::indicator:hover {
                border: 2px solid #555555;
                background-color: #404040;
            }
            QCheckBox::indicator:checked:hover {
                border: 2px solid #007ACC;
                background-color: #404040;
            }
            QScrollBar:vertical {
                background-color: #2d2d2d;
                width: 12px;
                border-radius: 6px;
            }
            QScrollBar::handle:vertical {
                background-color: #404040;
                border-radius: 6px;
                min-height: 20px;
            }
            QScrollBar::handle:vertical:hover {
                background-color: #007ACC;
            }
            QScrollBar:horizontal {
                background-color: #2d2d2d;
                height: 12px;
                border-radius: 6px;
            }
            QScrollBar::handle:horizontal {
                background-color: #404040;
                border-radius: 6px;
                min-width: 20px;
            }
            QScrollBar::handle:horizontal:hover {
                background-color: #007ACC;
            }
        """)
    
    def refresh_displays(self):
        """Refresh all displays"""
        self.schedule_tab.refresh_people_list()
        self.people_tab.refresh_people_table()
        self.courses_tab.refresh_courses_list()
        self.common_times_tab.refresh_people_checkboxes()


def launch_pyqt6_gui(people_list, courses, data_file="schedule_data.json"):
    """Launch the PyQt6 schedule manager GUI"""
    app = QApplication(sys.argv)
    
    # Set application properties
    app.setApplicationName("Schedule Manager")
    app.setApplicationVersion("2.0")
    app.setOrganizationName("Schedule Manager")
    
    # Create and show main window
    window = ScheduleManagerPyQt6(people_list, courses, data_file)
    window.show()
    
    # Run the application
    sys.exit(app.exec())
