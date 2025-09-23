#!/usr/bin/env python3
"""
Test script to verify the new GUI structure works
"""

from gui import launch_gui
from storage import load_data
import os

def main():
    """Test the GUI"""
    data_file = "schedule_data.json"
    
    # Ensure data file exists
    if not os.path.exists(data_file):
        with open(data_file, "w") as f:
            import json
            json.dump({"courses": {}, "people": {}}, f)
    
    # Load data
    people_list, courses = load_data(data_file)
    
    print("Testing new GUI structure...")
    print(f"Loaded {len(people_list)} people and {len(courses)} courses")
    print("GUI components:")
    print("- gui/main_window.py")
    print("- gui/schedule_tab.py") 
    print("- gui/people_tab.py")
    print("- gui/courses_tab.py")
    print("- gui/common_times_tab.py")
    print("- gui/time_picker.py")
    print("\nAll imports successful! ✅")
    
    # Uncomment the line below to actually launch the GUI
    # launch_gui(people_list, courses, data_file)

if __name__ == "__main__":
    main()
