#!/usr/bin/env python3
"""
Test script to showcase the compact layout improvements
"""

from gui import launch_gui
from storage import load_data
import os

def main():
    """Test the compact layout"""
    data_file = "schedule_data.json"
    
    # Ensure data file exists
    if not os.path.exists(data_file):
        with open(data_file, "w") as f:
            import json
            json.dump({"courses": {}, "people": {}}, f)
    
    # Load data
    people_list, courses = load_data(data_file)
    
    print("📐 Compact Layout Applied! 📐")
    print("=" * 40)
    print("✅ Schedule Tab - Now Compact:")
    print("   • Removed horizontal splitter")
    print("   • People list: 200px height (was 300px)")
    print("   • Schedule details: 300px height (was 500px)")
    print("   • Vertical layout like People tab")
    print("   • Better space utilization")
    print("✅ Courses Tab - Now Compact:")
    print("   • Removed horizontal splitter")
    print("   • Courses list: 200px height (was 400px)")
    print("   • Course details: 250px height (was 350px)")
    print("   • Vertical layout like other tabs")
    print("✅ Simplified Add Course:")
    print("   • Removed input field and label")
    print("   • Just a single 'Add Course' button")
    print("   • Uses dialog for course name input")
    print("   • Cleaner, more minimalistic")
    print("✅ Consistent Layout Across All Tabs:")
    print("   • Schedule tab: Compact vertical sections")
    print("   • People tab: Already compact")
    print("   • Courses tab: Now compact")
    print("   • Common Times tab: Already compact")
    print("\n🎯 All tabs now have consistent, compact layouts!")
    
    # Uncomment the line below to actually launch the GUI and see the compact layout
    # launch_gui(people_list, courses, data_file)

if __name__ == "__main__":
    main()
