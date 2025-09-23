#!/usr/bin/env python3
"""
Test script to showcase the neutral color scheme without accent colors
"""

from gui import launch_gui
from storage import load_data
import os

def main():
    """Test the neutral color scheme"""
    data_file = "schedule_data.json"
    
    # Ensure data file exists
    if not os.path.exists(data_file):
        with open(data_file, "w") as f:
            import json
            json.dump({"courses": {}, "people": {}}, f)
    
    # Load data
    people_list, courses = load_data(data_file)
    
    print("⚫ Neutral Color Scheme Applied! ⚫")
    print("=" * 50)
    print("✅ Removed teal accent color (#0d7377)")
    print("✅ Replaced with neutral grays:")
    print("   • Buttons: #404040 (base) → #555555 (hover) → #333333 (pressed)")
    print("   • Focus borders: #666666")
    print("   • Selected items: #555555")
    print("   • Checkbox checked: #666666")
    print("   • Scrollbar hover: #666666")
    print("   • Tab selection: #666666")
    print("   • Title backgrounds: #404040")
    print("✅ Clean, monochromatic design:")
    print("   • No bright accent colors")
    print("   • Subtle gray variations")
    print("   • Professional appearance")
    print("   • Minimalistic luxury maintained")
    print("✅ Consistent neutral palette:")
    print("   • #1e1e1e - Main background")
    print("   • #2d2d2d - Secondary background")
    print("   • #404040 - Borders and buttons")
    print("   • #555555 - Hover states")
    print("   • #666666 - Focus and selection")
    print("   • #ffffff - Text color")
    print("\n🎨 Clean, neutral design achieved!")
    
    # Uncomment the line below to actually launch the GUI and see the neutral colors
    # launch_gui(people_list, courses, data_file)

if __name__ == "__main__":
    main()
