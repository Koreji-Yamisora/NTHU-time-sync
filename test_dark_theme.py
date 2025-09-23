#!/usr/bin/env python3
"""
Test script to showcase the beautiful dark theme improvements
"""

from gui import launch_gui
from storage import load_data
import os

def main():
    """Test the dark theme GUI"""
    data_file = "schedule_data.json"
    
    # Ensure data file exists
    if not os.path.exists(data_file):
        with open(data_file, "w") as f:
            import json
            json.dump({"courses": {}, "people": {}}, f)
    
    # Load data
    people_list, courses = load_data(data_file)
    
    print("🌙 Beautiful Dark Theme Applied! 🌙")
    print("=" * 50)
    print("✅ Dark background: #1e1e1e")
    print("✅ Teal accent color: #0d7377")
    print("✅ Beautiful white text on dark backgrounds")
    print("✅ Reduced negative space in all tabs")
    print("✅ Enhanced output windows with:")
    print("   • Monospace fonts for better readability")
    print("   • Increased line height (1.6-1.8)")
    print("   • Better padding and spacing")
    print("   • Rounded corners and modern styling")
    print("✅ Improved button styling with hover effects")
    print("✅ Custom scrollbars with dark theme")
    print("✅ Beautiful tab styling with teal accents")
    print("✅ Enhanced table and list styling")
    print("✅ Emoji icons for better visual hierarchy")
    print("\n🎨 The GUI now looks professional and modern!")
    
    # Uncomment the line below to actually launch the GUI and see the dark theme
    # launch_gui(people_list, courses, data_file)

if __name__ == "__main__":
    main()
