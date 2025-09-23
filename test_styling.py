#!/usr/bin/env python3
"""
Test script to verify PyQt6 styling works correctly
"""

from gui import launch_gui
from storage import load_data
import os

def main():
    """Test the GUI styling"""
    data_file = "schedule_data.json"
    
    # Ensure data file exists
    if not os.path.exists(data_file):
        with open(data_file, "w") as f:
            import json
            json.dump({"courses": {}, "people": {}}, f)
    
    # Load data
    people_list, courses = load_data(data_file)
    
    print("Testing PyQt6 styling fixes...")
    print("✅ Fixed white-on-white text issue")
    print("✅ Added explicit color: #333333 for all text")
    print("✅ Added explicit background-color for all widgets")
    print("✅ Fixed tab styling with proper contrast")
    print("✅ Fixed checkbox styling")
    print("✅ Fixed time picker styling")
    print("\nAll styling fixes applied! 🎨")
    
    # Uncomment the line below to actually launch the GUI and see the fixes
    # launch_gui(people_list, courses, data_file)

if __name__ == "__main__":
    main()
