"""
People Management Tab
"""

from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit, 
    QPushButton, QTableWidget, QTableWidgetItem, QGroupBox, QGridLayout
)
from PyQt6.QtCore import Qt


class PeopleTab(QWidget):
    """People management tab"""
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.main_window = parent
        self.setup_ui()
    
    def setup_ui(self):
        """Setup the people tab UI"""
        layout = QVBoxLayout(self)
        layout.setContentsMargins(8, 8, 8, 8)
        layout.setSpacing(8)
        
        # Title
        title = QLabel("People Management")
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
        
        # Add person section
        add_group = QGroupBox("Add New Person")
        add_layout = QGridLayout(add_group)
        
        add_layout.addWidget(QLabel("Name:"), 0, 0)
        self.new_person_name = QLineEdit()
        add_layout.addWidget(self.new_person_name, 0, 1)
        
        self.add_person_btn_tab = QPushButton("Add Person")
        self.add_person_btn_tab.clicked.connect(self.add_person_from_tab)
        add_layout.addWidget(self.add_person_btn_tab, 0, 2)
        
        layout.addWidget(add_group)
        
        # People list
        people_group = QGroupBox("Current People")
        people_layout = QVBoxLayout(people_group)
        
        self.people_table = QTableWidget()
        self.people_table.setColumnCount(2)
        self.people_table.setHorizontalHeaderLabels(["Name", "Courses"])
        self.people_table.horizontalHeader().setStretchLastSection(True)
        from PyQt6.QtWidgets import QAbstractItemView
        self.people_table.setSelectionBehavior(QAbstractItemView.SelectionBehavior.SelectRows)
        
        people_layout.addWidget(self.people_table)
        
        # People buttons
        people_btn_layout = QHBoxLayout()
        self.remove_person_btn_tab = QPushButton("Remove Selected")
        self.remove_person_btn_tab.clicked.connect(self.remove_person_from_tab)
        self.import_ics_btn = QPushButton("Import ICS File")
        self.import_ics_btn.clicked.connect(self.import_ics_file)
        
        people_btn_layout.addWidget(self.remove_person_btn_tab)
        people_btn_layout.addWidget(self.import_ics_btn)
        people_btn_layout.addStretch()
        
        people_layout.addLayout(people_btn_layout)
        layout.addWidget(people_group)
    
    def refresh_people_table(self):
        """Refresh the people table"""
        self.people_table.setRowCount(len(self.main_window.people_list))
        
        for row, person in enumerate(self.main_window.people_list):
            # Name
            name_item = QTableWidgetItem(person.name)
            self.people_table.setItem(row, 0, name_item)
            
            # Courses
            course_names = []
            for course_slots in person.schedule:
                for course_name, stored_slots in self.main_window.courses.items():
                    if stored_slots == course_slots:
                        course_names.append(course_name)
                        break
            
            courses_item = QTableWidgetItem(", ".join(course_names))
            self.people_table.setItem(row, 1, courses_item)
    
    def add_person_from_tab(self):
        """Add person from the people tab"""
        name = self.new_person_name.text().strip()
        if name:
            try:
                import storage as st
                st.add_person(self.main_window.people_list, name)
                st.save_data(self.main_window.people_list, self.main_window.courses, self.main_window.data_file)
                self.main_window.refresh_displays()
                self.new_person_name.clear()
                self.main_window.statusBar().showMessage(f"Added person: {name}")
            except ValueError as e:
                from PyQt6.QtWidgets import QMessageBox
                QMessageBox.warning(self, "Error", str(e))
        else:
            from PyQt6.QtWidgets import QMessageBox
            QMessageBox.warning(self, "Error", "Please enter a name")
    
    def remove_person_from_tab(self):
        """Remove person from the people tab"""
        current_row = self.people_table.currentRow()
        if current_row >= 0:
            name = self.people_table.item(current_row, 0).text()
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
    
    def import_ics_file(self):
        """Import ICS file"""
        from PyQt6.QtWidgets import QFileDialog, QInputDialog, QMessageBox
        file_path, _ = QFileDialog.getOpenFileName(
            self, "Select ICS Calendar File", "", "ICS Files (*.ics);;All Files (*)"
        )
        
        if file_path:
            name, ok = QInputDialog.getText(self, "Import ICS", "Enter person name:")
            if ok and name.strip():
                try:
                    import storage as st
                    st.import_ics_file(file_path, self.main_window.courses, name.strip(), self.main_window.people_list)
                    st.save_data(self.main_window.people_list, self.main_window.courses, self.main_window.data_file)
                    self.main_window.refresh_displays()
                    self.main_window.statusBar().showMessage(f"Imported ICS file for: {name.strip()}")
                except Exception as e:
                    QMessageBox.critical(self, "Error", f"Failed to import ICS file: {str(e)}")
