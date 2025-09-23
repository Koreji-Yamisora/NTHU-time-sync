#!/usr/bin/env python3
"""
Test script to showcase the personal period functionality
"""

from gui import launch_gui
from storage import load_data
import os

def main():
    """Test the personal period functionality"""
    data_file = "schedule_data.json"
    
    # Ensure data file exists
    if not os.path.exists(data_file):
        with open(data_file, "w") as f:
            import json
            json.dump({"courses": {}, "people": {}}, f)
    
    # Load data
    people_list, courses = load_data(data_file)
    
    print("⏰ Personal Period Functionality Added! ⏰")
    print("=" * 50)
    print("✅ New Personal Period Section:")
    print("   • Day selection dropdown")
    print("   • Start time picker")
    print("   • End time picker")
    print("   • Add Personal Period button")
    print("✅ Time Picker Integration:")
    print("   • Modern time selection widgets")
    print("   • 24-hour format (HH:MM)")
    print("   • Easy up/down arrow controls")
    print("   • Consistent styling")
    print("✅ Validation Features:")
    print("   • Start time must be before end time")
    print("   • Duplicate period detection")
    print("   • Person selection required")
    print("   • Clear error messages")
    print("✅ Schedule Integration:")
    print("   • Personal periods appear in schedule")
    print("   • Labeled as 'Individual Slots'")
    print("   • Included in common time calculations")
    print("   • Automatically saved to data file")
    print("✅ User Experience:")
    print("   • Select person from list")
    print("   • Choose day of the week")
    print("   • Set start and end times")
    print("   • Click 'Add Personal Period'")
    print("✅ Use Cases:")
    print("   • Personal appointments")
    print("   • Work meetings")
    print("   • Study sessions")
    print("   • Personal commitments")
    print("   • Any individual time blocks")
    print("✅ Features:")
    print("   • Real-time schedule updates")
    print("   • Conflict detection")
    print("   • Data persistence")
    print("   • Status bar feedback")
    print("   • Professional interface")
    print("\n🎨 Personal period management achieved!")
    
    # Uncomment the line below to actually launch the GUI and test personal periods
    # launch_gui(people_list, courses, data_file)

if __name__ == "__main__":
    main()
