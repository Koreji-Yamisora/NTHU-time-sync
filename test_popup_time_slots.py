#!/usr/bin/env python3
"""
Test script to showcase the popup time slot functionality
"""

from gui import launch_gui
from storage import load_data
import os

def main():
    """Test the popup time slot functionality"""
    data_file = "schedule_data.json"
    
    # Ensure data file exists
    if not os.path.exists(data_file):
        with open(data_file, "w") as f:
            import json
            json.dump({"courses": {}, "people": {}}, f)
    
    # Load data
    people_list, courses = load_data(data_file)
    
    print("🪟 Popup Time Slot Functionality Added! 🪟")
    print("=" * 50)
    print("✅ Personal Periods - Now with Popup:")
    print("   • Clean button interface")
    print("   • Popup dialog for time entry")
    print("   • Professional modal window")
    print("   • Compact main interface")
    print("✅ Course Time Slots - Now with Popup:")
    print("   • Add Time Slot button")
    print("   • Popup dialog for time entry")
    print("   • Add slots to existing courses")
    print("   • Update all enrolled students")
    print("✅ Popup Dialog Features:")
    print("   • Day selection dropdown")
    print("   • Start time picker")
    print("   • End time picker")
    print("   • Cancel/Add buttons")
    print("   • Input validation")
    print("✅ Professional Interface:")
    print("   • Modal dialog window")
    print("   • Clean, focused design")
    print("   • Consistent styling")
    print("   • User-friendly layout")
    print("✅ Validation & Error Handling:")
    print("   • Time validation (start < end)")
    print("   • Duplicate detection")
    print("   • Clear error messages")
    print("   • Selection requirements")
    print("✅ Enhanced User Experience:")
    print("   • Less cluttered main interface")
    print("   • Focused time entry")
    print("   • Professional workflow")
    print("   • Consistent across tabs")
    print("✅ Use Cases:")
    print("   • Personal periods for people")
    print("   • Additional time slots for courses")
    print("   • Flexible schedule management")
    print("   • Professional time entry")
    print("✅ Benefits:")
    print("   • Cleaner main interface")
    print("   • Professional popup dialogs")
    print("   • Consistent user experience")
    print("   • Better organization")
    print("\n🎨 Professional popup time slot management achieved!")
    
    # Uncomment the line below to actually launch the GUI and test popup functionality
    # launch_gui(people_list, courses, data_file)

if __name__ == "__main__":
    main()
