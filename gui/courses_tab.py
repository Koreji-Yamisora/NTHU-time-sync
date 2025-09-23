"""
Courses Management Tab
"""

from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit, 
    QPushButton, QListWidget, QTableWidget, QTableWidgetItem, 
    QGroupBox, QGridLayout, QSplitter, QDialog, QMessageBox
)
from PyQt6.QtCore import Qt


class CoursesTab(QWidget):
    """Courses management tab"""
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.main_window = parent
        self.setup_ui()
    
    def setup_ui(self):
        """Setup the courses tab UI"""
        layout = QVBoxLayout(self)
        layout.setContentsMargins(8, 8, 8, 8)
        layout.setSpacing(8)
        
        # Title
        title = QLabel("Courses Management")
        title.setStyleSheet("""
            font-size: 14px; 
            font-weight: 600; 
            color: #ffffff; 
            margin: 1px 0; 
            padding: 4px 8px; 
            background-color: #404040; 
            border-radius: 3px; 
        """)
        layout.addWidget(title)
        
        # Add course section - just a button
        add_group = QGroupBox("Add New Course")
        add_layout = QHBoxLayout(add_group)
        add_layout.setContentsMargins(8, 8, 8, 8)
        add_layout.setSpacing(8)
        
        self.add_course_btn = QPushButton("Add Course")
        self.add_course_btn.clicked.connect(self.add_course)
        self.add_course_btn.setMaximumWidth(120)
        add_layout.addWidget(self.add_course_btn)
        add_layout.addStretch()
        
        layout.addWidget(add_group)
        
        # Courses list section
        courses_group = QGroupBox("Current Courses")
        courses_layout = QVBoxLayout(courses_group)
        courses_layout.setContentsMargins(8, 8, 8, 8)
        courses_layout.setSpacing(8)
        
        # Courses list
        self.courses_list_widget = QListWidget()
        self.courses_list_widget.setMinimumHeight(150)
        courses_layout.addWidget(self.courses_list_widget)
        
        # Course buttons
        course_btn_layout = QHBoxLayout()
        course_btn_layout.setSpacing(8)
        self.add_time_slot_btn = QPushButton("Add Time Slot")
        self.add_time_slot_btn.clicked.connect(self.add_time_slot_to_course)
        self.remove_course_btn = QPushButton("Remove Course")
        self.remove_course_btn.clicked.connect(self.remove_course)
        
        course_btn_layout.addWidget(self.add_time_slot_btn)
        course_btn_layout.addWidget(self.remove_course_btn)
        course_btn_layout.addStretch()
        courses_layout.addLayout(course_btn_layout)
        
        layout.addWidget(courses_group)
        
        # Course details section
        details_group = QGroupBox("Course Details")
        details_layout = QVBoxLayout(details_group)
        details_layout.setContentsMargins(8, 8, 8, 8)
        details_layout.setSpacing(8)
        
        self.course_name_label = QLabel("Select a course to view details")
        self.course_name_label.setStyleSheet("""
            font-size: 16px; 
            font-weight: 600; 
            color: #ffffff;
            padding: 12px 16px;
            background-color: #404040;
            border-radius: 8px;
            margin: 4px 0;
        """)
        details_layout.addWidget(self.course_name_label)
        
        # Course slots table with balanced styling
        self.course_slots_table = QTableWidget()
        self.course_slots_table.setColumnCount(3)
        self.course_slots_table.setHorizontalHeaderLabels(["Day", "Start Time", "End Time"])
        self.course_slots_table.horizontalHeader().setStretchLastSection(False)
        self.course_slots_table.setMinimumHeight(180)
        
        # Set equal column widths
        header = self.course_slots_table.horizontalHeader()
        header.setSectionResizeMode(0, header.ResizeMode.Stretch)  # Day column
        header.setSectionResizeMode(1, header.ResizeMode.Stretch)  # Start Time column
        header.setSectionResizeMode(2, header.ResizeMode.Stretch)  # End Time column
        self.course_slots_table.setStyleSheet("""
            QTableWidget {
                font-size: 11px;
                background-color: #2a2a2a;
                color: #ffffff;
                border: none;
                border-radius: 4px;
                padding: 4px;
            }
            QTableWidget::item {
                padding: 6px 10px;
                border-bottom: 1px solid #404040;
            }
            QTableWidget::item:selected {
                background-color: #007ACC;
            }
            QHeaderView::section {
                padding: 6px 10px;
                font-weight: 600;
                background-color: #404040;
                color: #ffffff;
                border-bottom: 1px solid #666666;
            }
        """)
        details_layout.addWidget(self.course_slots_table)
        
        layout.addWidget(details_group)
        
        # Connect signals
        self.courses_list_widget.currentItemChanged.connect(self.on_course_select)
    
    def refresh_courses_list(self):
        """Refresh the courses list widget"""
        self.courses_list_widget.clear()
        for course_name in self.main_window.courses.keys():
            from PyQt6.QtWidgets import QListWidgetItem
            item = QListWidgetItem(course_name)
            self.courses_list_widget.addItem(item)
    
    def on_course_select(self, current, previous):
        """Handle course selection"""
        if current:
            self.show_course_details(current.text())
    
    def show_course_details(self, course_name):
        """Show selected course's details"""
        if course_name not in self.main_window.courses:
            return
        
        self.course_name_label.setText(f"Course: {course_name}")
        
        # Clear and populate course slots table
        course_slots = self.main_window.courses[course_name]
        self.course_slots_table.setRowCount(len(course_slots))
        
        for row, slot in enumerate(sorted(course_slots, key=lambda x: (self.main_window.days.index(x.day), x.start_time))):
            self.course_slots_table.setItem(row, 0, QTableWidgetItem(slot.day))
            self.course_slots_table.setItem(row, 1, QTableWidgetItem(slot.start_time))
            self.course_slots_table.setItem(row, 2, QTableWidgetItem(slot.end_time))
    
    def add_time_slot_to_course(self):
        """Add a time slot to the selected course"""
        current_item = self.courses_list_widget.currentItem()
        if not current_item:
            QMessageBox.warning(self, "No Selection", "Please select a course first.")
            return
        
        course_name = current_item.text()
        if course_name not in self.main_window.courses:
            return
        
        # Show popup dialog
        from .time_slot_dialog import TimeSlotDialog
        dialog = TimeSlotDialog(self.main_window.days, self, f"Add Time Slot to {course_name}")
        
        if dialog.exec() == QDialog.DialogCode.Accepted:
            # Get the time slot data
            data = dialog.get_time_slot_data()
            day = data['day']
            start_time = data['start_time']
            end_time = data['end_time']
            
            # Create the time slot
            from models import TimeSlot
            time_slot = TimeSlot(start_time, end_time, day)
            
            # Check for conflicts with existing time slots
            course_slots = self.main_window.courses[course_name]
            for existing_slot in course_slots:
                if (existing_slot.day == day and 
                    existing_slot.start_time == start_time and 
                    existing_slot.end_time == end_time):
                    QMessageBox.warning(self, "Duplicate Time Slot", 
                                      f"This time slot already exists for {course_name}.")
                    return
            
            # Add the time slot to the course
            course_slots.append(time_slot)
            
            # Update all people who have this course
            for person in self.main_window.people_list:
                for person_course in person.schedule:
                    if person_course == course_slots:
                        person.busy_time = person._create_busy_time_dict()
                        break
            
            # Save data
            import storage as st
            st.save_data(self.main_window.people_list, self.main_window.courses, self.main_window.data_file)
            
            # Refresh display
            self.show_course_details(course_name)
            self.main_window.statusBar().showMessage(f"Added time slot to {course_name}")
    
    def add_course(self):
        """Add a new course"""
        from PyQt6.QtWidgets import QInputDialog, QMessageBox
        name, ok = QInputDialog.getText(self, "Add Course", "Enter course name:")
        if ok and name.strip():
            try:
                import storage as st
                st.add_course(self.main_window.courses, name.strip(), [])
                st.save_data(self.main_window.people_list, self.main_window.courses, self.main_window.data_file)
                self.main_window.refresh_displays()
                self.main_window.statusBar().showMessage(f"Added course: {name.strip()}")
            except ValueError as e:
                QMessageBox.warning(self, "Error", str(e))
    
    def remove_course(self):
        """Remove selected course"""
        current_item = self.courses_list_widget.currentItem()
        if current_item:
            name = current_item.text()
            from PyQt6.QtWidgets import QMessageBox
            reply = QMessageBox.question(self, "Confirm", f"Remove course '{name}'?", 
                                       QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No)
            if reply == QMessageBox.StandardButton.Yes:
                try:
                    import storage as st
                    st.remove_course(self.main_window.courses, name)
                    st.save_data(self.main_window.people_list, self.main_window.courses, self.main_window.data_file)
                    self.main_window.refresh_displays()
                    self.main_window.statusBar().showMessage(f"Removed course: {name}")
                except ValueError as e:
                    QMessageBox.warning(self, "Error", str(e))
        else:
            from PyQt6.QtWidgets import QMessageBox
            QMessageBox.warning(self, "Error", "Please select a course to remove")
