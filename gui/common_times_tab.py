"""
Common Free Times Tab
"""

from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QComboBox, 
    QPushButton, QTextEdit, QCheckBox, QGroupBox, QGridLayout
)
from PyQt6.QtCore import Qt
from schedule import common_free_times


class CommonTimesTab(QWidget):
    """Common free times tab"""
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.main_window = parent
        self.setup_ui()
    
    def setup_ui(self):
        """Setup the common times tab UI"""
        layout = QVBoxLayout(self)
        layout.setContentsMargins(8, 8, 8, 8)
        layout.setSpacing(8)
        
        # Title
        title = QLabel("Common Free Times")
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
        
        # Controls
        controls_group = QGroupBox("Find Common Times")
        controls_layout = QGridLayout(controls_group)
        
        # Day selection
        controls_layout.addWidget(QLabel("Day:"), 0, 0)
        self.common_day_combo = QComboBox()
        self.common_day_combo.addItems(self.main_window.days)
        controls_layout.addWidget(self.common_day_combo, 0, 1)
        
        # Buttons
        self.find_common_btn = QPushButton("Find Common Times")
        self.find_common_btn.clicked.connect(self.find_common_times)
        controls_layout.addWidget(self.find_common_btn, 0, 2)
        
        self.find_all_common_btn = QPushButton("Find All Days")
        self.find_all_common_btn.clicked.connect(self.find_all_common_times)
        controls_layout.addWidget(self.find_all_common_btn, 0, 3)
        
        layout.addWidget(controls_group)
        
        # People selection
        people_selection_group = QGroupBox("Select People")
        people_selection_layout = QVBoxLayout(people_selection_group)
        
        # Select all/none buttons
        select_btn_layout = QHBoxLayout()
        self.select_all_btn = QPushButton("Select All")
        self.select_all_btn.clicked.connect(self.select_all_people)
        self.select_none_btn = QPushButton("Select None")
        self.select_none_btn.clicked.connect(self.select_none_people)
        
        select_btn_layout.addWidget(self.select_all_btn)
        select_btn_layout.addWidget(self.select_none_btn)
        select_btn_layout.addStretch()
        
        people_selection_layout.addLayout(select_btn_layout)
        
        # People checkboxes
        self.people_checkboxes_frame = QWidget()
        self.people_checkboxes_layout = QVBoxLayout(self.people_checkboxes_frame)
        people_selection_layout.addWidget(self.people_checkboxes_frame)
        
        layout.addWidget(people_selection_group)
        
        # Results
        results_group = QGroupBox("Results")
        results_layout = QVBoxLayout(results_group)
        results_layout.setContentsMargins(8, 8, 8, 8)
        results_layout.setSpacing(8)
        
        self.results_text = QTextEdit()
        self.results_text.setReadOnly(True)
        self.results_text.setMinimumHeight(250)
        self.results_text.setStyleSheet("""
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
        results_layout.addWidget(self.results_text)
        
        layout.addWidget(results_group)
    
    def refresh_people_checkboxes(self):
        """Refresh the people selection checkboxes"""
        # Clear existing checkboxes
        for i in reversed(range(self.people_checkboxes_layout.count())):
            self.people_checkboxes_layout.itemAt(i).widget().setParent(None)
        
        # Add checkboxes for each person
        for person in self.main_window.people_list:
            checkbox = QCheckBox(person.name)
            checkbox.setChecked(True)  # Default to selected
            self.people_checkboxes_layout.addWidget(checkbox)
    
    def get_selected_people(self):
        """Get list of selected people from checkboxes"""
        selected_people = []
        for i in range(self.people_checkboxes_layout.count()):
            checkbox = self.people_checkboxes_layout.itemAt(i).widget()
            if isinstance(checkbox, QCheckBox) and checkbox.isChecked():
                person_name = checkbox.text()
                person = next((p for p in self.main_window.people_list if p.name == person_name), None)
                if person:
                    selected_people.append(person)
        return selected_people
    
    def find_common_times(self):
        """Find common free times for selected people and selected day"""
        selected_people = self.get_selected_people()
        day = self.common_day_combo.currentText()
        
        if not selected_people:
            html_content = """
            <div style="text-align: center; padding: 40px;">
                <div style="color: #666666; font-size: 16px; margin-bottom: 20px;">
                    No people selected
                </div>
                <div style="color: #888888; font-size: 14px;">
                    Please select at least one person to find common times.
                </div>
            </div>
            """
            self.results_text.setHtml(html_content)
            return
        
        if len(selected_people) == 1:
            # Show individual schedule for single person
            person = selected_people[0]
            
            html_content = f"""
            <div style="margin-bottom: 20px;">
                <h2 style="color: #007ACC; margin: 0 0 10px 0; font-size: 24px; font-weight: 600;">
                    Individual Schedule for {person.name} on {day}
                </h2>
            </div>
            """
            
            # Get person's schedule for the day
            day_slots = []
            for course_slots in person.schedule:
                for slot in course_slots:
                    if slot.day == day:
                        day_slots.append((slot.start_time, slot.end_time))
            
            if day_slots:
                day_slots.sort()
                html_content += f"""
                <div style="margin-bottom: 16px;">
                    <h3 style="color: #ffffff; margin: 0 0 8px 0; font-size: 18px; font-weight: 600;">
                        Busy times on {day}
                    </h3>
                    <div style="margin-left: 20px;">
                """
                for start, end in day_slots:
                    html_content += f"""
                    <div style="margin-bottom: 8px; padding: 8px 0;">
                        <span style="color: #666666; font-weight: 600; font-size: 14px;">{start} - {end}</span>
                    </div>
                    """
                html_content += """
                    </div>
                </div>
                <div style="margin-bottom: 16px;">
                    <h3 style="color: #ffffff; margin: 0 0 8px 0; font-size: 18px; font-weight: 600;">
                        Free times on {day}
                    </h3>
                    <div style="margin-left: 20px; padding: 8px 0;">
                        <span style="color: #888888; font-style: italic;">Times not listed above are generally free</span>
                    </div>
                </div>
                """
            else:
                html_content += f"""
                <div style="text-align: center; padding: 40px;">
                    <div style="color: #007ACC; font-size: 18px; margin-bottom: 10px;">
                        {person.name} is completely free on {day}!
                    </div>
                </div>
                """
            
            self.results_text.setHtml(html_content)
            return
        
        # Multiple people - find common times
        common_times = common_free_times(selected_people, day)
        
        html_content = f"""
        <div style="margin-bottom: 20px;">
            <h2 style="color: #007ACC; margin: 0 0 10px 0; font-size: 24px; font-weight: 600;">
                Common Free Times for {day}
            </h2>
        </div>
        
        <div style="margin-bottom: 16px;">
            <h3 style="color: #ffffff; margin: 0 0 8px 0; font-size: 18px; font-weight: 600;">
                Selected People ({len(selected_people)})
            </h3>
            <div style="margin-left: 20px;">
        """
        
        for person in selected_people:
            html_content += f"""
            <div style="margin-bottom: 4px; padding: 8px 0;">
                <span style="color: #ffffff; font-size: 14px;">{person.name}</span>
            </div>
            """
        
        html_content += """
            </div>
        </div>
        """
        
        if common_times:
            html_content += f"""
            <div style="margin-bottom: 16px;">
                <h3 style="color: #ffffff; margin: 0 0 8px 0; font-size: 18px; font-weight: 600;">
                    Common Free Times on {day}
                </h3>
                <div style="margin-left: 20px;">
            """
            for start, end in common_times:
                html_content += f"""
                <div style="margin-bottom: 8px; padding: 8px 0;">
                    <span style="color: #007ACC; font-weight: 600; font-size: 14px;">{start} - {end}</span>
                </div>
                """
            html_content += """
                </div>
            </div>
            """
        else:
            html_content += f"""
            <div style="text-align: center; padding: 40px;">
                <div style="color: #666666; font-size: 18px; margin-bottom: 10px;">
                    No common free times found on {day}
                </div>
                <div style="color: #888888; font-size: 14px; margin-bottom: 20px;">
                    The selected people have conflicting schedules on this day.
                </div>
                <div style="color: #888888; font-size: 14px;">
                    Try selecting fewer people or checking other days.
                </div>
            </div>
            """
        
        self.results_text.setHtml(html_content)
    
    def find_all_common_times(self):
        """Find common free times for all days with selected people"""
        selected_people = self.get_selected_people()
        
        if not selected_people:
            self.results_text.setPlainText("No people selected. Please select at least one person to find common times.")
            return
        
        result_text = "Common Free Times - Weekly Summary\n"
        result_text += "=" * 50 + "\n"
        result_text += f"Analyzing schedules for {len(selected_people)} selected people:\n"
        for person in selected_people:
            result_text += f"  - {person.name}\n"
        result_text += "\n"
        
        has_common_times = False
        
        for day in self.main_window.days:
            common_times = common_free_times(selected_people, day)
            if common_times:
                has_common_times = True
                result_text += f"{day}:\n"
                for start, end in common_times:
                    result_text += f"   {start} - {end}\n"
                result_text += "\n"
        
        if not has_common_times:
            result_text += "No common free times found across any day.\n"
            result_text += "\nSuggestions:\n"
            result_text += "   • Try selecting fewer people\n"
            result_text += "   • Check if schedules have overlapping busy times\n"
            result_text += "   • Try looking at weekend days (Saturday/Sunday)\n"
        
        self.results_text.setPlainText(result_text)
    
    def select_all_people(self):
        """Select all people checkboxes"""
        for i in range(self.people_checkboxes_layout.count()):
            checkbox = self.people_checkboxes_layout.itemAt(i).widget()
            if isinstance(checkbox, QCheckBox):
                checkbox.setChecked(True)
    
    def select_none_people(self):
        """Deselect all people checkboxes"""
        for i in range(self.people_checkboxes_layout.count()):
            checkbox = self.people_checkboxes_layout.itemAt(i).widget()
            if isinstance(checkbox, QCheckBox):
                checkbox.setChecked(False)
