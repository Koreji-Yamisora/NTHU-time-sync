"""
Schedule Management Tab
"""

from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QListWidget, 
    QPushButton, QTextEdit, QGroupBox, QSplitter, QComboBox,
    QGridLayout, QMessageBox, QDialog
)
from PyQt6.QtCore import Qt
from .time_picker import TimePickerWidget


class ScheduleTab(QWidget):
    """Schedule management tab"""
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.main_window = parent
        self.setup_ui()
    
    def setup_ui(self):
        """Setup the schedule tab UI"""
        layout = QVBoxLayout(self)
        layout.setContentsMargins(8, 8, 8, 8)
        layout.setSpacing(8)
        
        # Title
        title = QLabel("Schedule Management")
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
        
        # People list section
        people_group = QGroupBox("People")
        people_layout = QVBoxLayout(people_group)
        people_layout.setContentsMargins(8, 8, 8, 8)
        people_layout.setSpacing(8)
        
        # People list
        self.people_list_widget = QListWidget()
        self.people_list_widget.setMinimumHeight(150)
        people_layout.addWidget(self.people_list_widget)
        
        # People buttons
        people_btn_layout = QHBoxLayout()
        people_btn_layout.setSpacing(8)
        self.add_person_btn = QPushButton("Add Person")
        self.add_person_btn.clicked.connect(self.add_person)
        self.remove_person_btn = QPushButton("Remove Person")
        self.remove_person_btn.clicked.connect(self.remove_person)
        
        people_btn_layout.addWidget(self.add_person_btn)
        people_btn_layout.addWidget(self.remove_person_btn)
        people_btn_layout.addStretch()
        people_layout.addLayout(people_btn_layout)
        
        layout.addWidget(people_group)
        
        # Personal period section
        personal_group = QGroupBox("Personal Periods")
        personal_layout = QHBoxLayout(personal_group)
        personal_layout.setContentsMargins(8, 8, 8, 8)
        personal_layout.setSpacing(8)
        
        # Add personal period button
        self.add_personal_period_btn = QPushButton("Add Personal Period")
        self.add_personal_period_btn.clicked.connect(self.add_personal_period)
        personal_layout.addWidget(self.add_personal_period_btn)
        personal_layout.addStretch()
        
        layout.addWidget(personal_group)
        
        # Schedule display section
        schedule_group = QGroupBox("Schedule Details")
        schedule_layout = QVBoxLayout(schedule_group)
        schedule_layout.setContentsMargins(8, 8, 8, 8)
        schedule_layout.setSpacing(8)
        
        # Schedule text with beautiful styling
        self.schedule_text = QTextEdit()
        self.schedule_text.setReadOnly(True)
        self.schedule_text.setMinimumHeight(200)
        self.schedule_text.setStyleSheet("""
            QTextEdit {
                font-family: 'Segoe UI', 'Arial', sans-serif;
                font-size: 12px;
                line-height: 1.4;
                padding: 12px;
                background-color: #2a2a2a;
                color: #ffffff;
                border: none;
                border-radius: 6px;
                selection-background-color: #007ACC;
            }
        """)
        schedule_layout.addWidget(self.schedule_text)
        
        layout.addWidget(schedule_group)
        
        # Connect signals
        self.people_list_widget.currentItemChanged.connect(self.on_person_select)
    
    def refresh_people_list(self):
        """Refresh the people list widget"""
        self.people_list_widget.clear()
        for person in self.main_window.people_list:
            from PyQt6.QtWidgets import QListWidgetItem
            item = QListWidgetItem(person.name)
            self.people_list_widget.addItem(item)
    
    def on_person_select(self, current, previous):
        """Handle person selection"""
        if current:
            self.show_person_schedule(current.text())
    
    def show_person_schedule(self, person_name):
        """Show selected person's schedule"""
        self.schedule_text.clear()
        
        person = next((p for p in self.main_window.people_list if p.name == person_name), None)
        if not person:
            return
        
        # Start building HTML content
        html_content = f"""
        <div style="margin-bottom: 20px;">
            <h2 style="color: #007ACC; margin: 0 0 10px 0; font-size: 24px; font-weight: 600;">
                Schedule for {person_name}
            </h2>
        </div>
        """
        
        # Group schedule by day
        schedule_by_day = {}
        course_names = {}
        
        # Find course names for each set of slots
        for course_name, course_slots in self.main_window.courses.items():
            for person_course in person.schedule:
                if person_course == course_slots:
                    course_names[id(person_course)] = course_name
        
        # Organize by day
        for course_slots in person.schedule:
            course_name = course_names.get(id(course_slots), "Individual Slots")
            for slot in course_slots:
                if slot.day not in schedule_by_day:
                    schedule_by_day[slot.day] = []
                schedule_by_day[slot.day].append({
                    "time": f"{slot.start_time} - {slot.end_time}",
                    "course": course_name,
                })
        
        # Display schedule with beautiful HTML formatting
        for day in self.main_window.days:
            html_content += f"""
            <div style="margin-bottom: 16px;">
                <h3 style="color: #ffffff; margin: 0 0 8px 0; font-size: 18px; font-weight: 600;">
                    {day}
                </h3>
            """
            
            if day in schedule_by_day:
                # Sort by start time
                day_slots = sorted(schedule_by_day[day], key=lambda x: x["time"])
                html_content += '<div style="margin-left: 20px;">'
                for slot_info in day_slots:
                    html_content += f"""
                    <div style="margin-bottom: 8px; padding: 8px 0;">
                        <span style="color: #007ACC; font-weight: 600; font-size: 14px;">{slot_info['time']}</span>
                        <span style="color: #ffffff; margin-left: 12px;">{slot_info['course']}</span>
                    </div>
                    """
                html_content += '</div>'
            else:
                html_content += """
                <div style="margin-left: 20px; padding: 8px 0;">
                    <span style="color: #666666; font-style: italic;">Free day</span>
                </div>
                """
            
            html_content += '</div>'
        
        html_content += '</div>'
        
        self.schedule_text.setHtml(html_content)
    
    def add_personal_period(self):
        """Add a personal period to the selected person"""
        current_item = self.people_list_widget.currentItem()
        if not current_item:
            QMessageBox.warning(self, "No Selection", "Please select a person first.")
            return
        
        person_name = current_item.text()
        person = next((p for p in self.main_window.people_list if p.name == person_name), None)
        if not person:
            return
        
        # Show popup dialog
        from .time_slot_dialog import TimeSlotDialog
        dialog = TimeSlotDialog(self.main_window.days, self, f"Add Personal Period for {person_name}")
        
        if dialog.exec() == QDialog.DialogCode.Accepted:
            # Get the time slot data
            data = dialog.get_time_slot_data()
            day = data['day']
            start_time = data['start_time']
            end_time = data['end_time']
            
            # Create the time slot
            from models import TimeSlot
            time_slot = TimeSlot(start_time, end_time, day)
            
            # Check for conflicts with existing schedule
            for course_slots in person.schedule:
                for existing_slot in course_slots:
                    if (existing_slot.day == day and 
                        existing_slot.start_time == start_time and 
                        existing_slot.end_time == end_time):
                        QMessageBox.warning(self, "Duplicate Period", 
                                          f"This time slot already exists for {person_name}.")
                        return
            
            # Create a new individual course for this personal period
            individual_slots = [time_slot]
            person.schedule.append(individual_slots)
            person.busy_time = person._create_busy_time_dict()
            
            # Save data
            import storage as st
            st.save_data(self.main_window.people_list, self.main_window.courses, self.main_window.data_file)
            
            # Refresh display
            self.show_person_schedule(person_name)
            self.main_window.statusBar().showMessage(f"Added personal period for {person_name}")
    
    def add_person(self):
        """Add a new person"""
        from PyQt6.QtWidgets import QInputDialog
        name, ok = QInputDialog.getText(self, "Add Person", "Enter person name:")
        if ok and name.strip():
            try:
                import storage as st
                st.add_person(self.main_window.people_list, name.strip())
                st.save_data(self.main_window.people_list, self.main_window.courses, self.main_window.data_file)
                self.main_window.refresh_displays()
                self.main_window.statusBar().showMessage(f"Added person: {name.strip()}")
            except ValueError as e:
                from PyQt6.QtWidgets import QMessageBox
                QMessageBox.warning(self, "Error", str(e))
    
    def remove_person(self):
        """Remove selected person"""
        current_item = self.people_list_widget.currentItem()
        if current_item:
            name = current_item.text()
            from PyQt6.QtWidgets import QMessageBox
            reply = QMessageBox.question(self, "Confirm", f"Remove person '{name}'?", 
                                       QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No)
            if reply == QMessageBox.StandardButton.Yes:
                try:
                    import storage as st
                    st.remove_person(self.main_window.people_list, name)
                    st.save_data(self.main_window.people_list, self.main_window.courses, self.main_window.data_file)
                    self.main_window.refresh_displays()
                    self.main_window.statusBar().showMessage(f"Removed person: {name}")
                except ValueError as e:
                    QMessageBox.warning(self, "Error", str(e))
        else:
            from PyQt6.QtWidgets import QMessageBox
            QMessageBox.warning(self, "Error", "Please select a person to remove")
