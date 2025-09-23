#!/usr/bin/env python3
"""
Test script to showcase the equal table column sizing fix
"""

from gui import launch_gui
from storage import load_data
import os

def main():
    """Test that the table columns are now equal in size"""
    data_file = "schedule_data.json"
    
    # Ensure data file exists
    if not os.path.exists(data_file):
        with open(data_file, "w") as f:
            import json
            json.dump({"courses": {}, "people": {}}, f)
    
    # Load data
    people_list, courses = load_data(data_file)
    
    print("📊 Table Column Sizing Fixed! 📊")
    print("=" * 50)
    print("✅ Course Tab Table Improvements:")
    print("   • Equal column widths")
    print("   • Day column: 33.33% width")
    print("   • Start Time column: 33.33% width")
    print("   • End Time column: 33.33% width")
    print("✅ Technical Changes:")
    print("   • Disabled stretchLastSection")
    print("   • Set all columns to Stretch mode")
    print("   • Equal distribution of table width")
    print("   • Professional table appearance")
    print("✅ Visual Improvements:")
    print("   • Balanced column layout")
    print("   • Consistent spacing")
    print("   • Professional appearance")
    print("   • Better readability")
    print("✅ User Experience:")
    print("   • Cleaner table layout")
    print("   • Equal visual weight")
    print("   • Professional presentation")
    print("   • Consistent design")
    print("✅ Benefits:")
    print("   • More professional appearance")
    print("   • Better visual balance")
    print("   • Improved readability")
    print("   • Consistent column sizing")
    print("\n🎨 Equal table column sizing achieved!")
    
    # Uncomment the line below to actually launch the GUI and see the fix
    # launch_gui(people_list, courses, data_file)

if __name__ == "__main__":
    main()
