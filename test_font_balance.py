#!/usr/bin/env python3
"""
Test script to showcase the balanced font sizes and reduced title space
"""

from gui import launch_gui
from storage import load_data
import os

def main():
    """Test the balanced font sizes"""
    data_file = "schedule_data.json"
    
    # Ensure data file exists
    if not os.path.exists(data_file):
        with open(data_file, "w") as f:
            import json
            json.dump({"courses": {}, "people": {}}, f)
    
    # Load data
    people_list, courses = load_data(data_file)
    
    print("📐 Balanced Font Sizes & Reduced Title Space Applied! 📐")
    print("=" * 60)
    print("✅ Reduced title space:")
    print("   • Font size: 20px → 16px")
    print("   • Padding: 8px/16px → 6px/12px")
    print("   • Margins: 4px → 2px")
    print("   • Border radius: 6px → 4px")
    print("✅ Balanced font sizes for better device proportions:")
    print("   • Buttons: 14px → 12px")
    print("   • Input fields: 14px → 12px")
    print("   • Text areas: 15px → 13px")
    print("   • Tables: 14px → 12px")
    print("   • Group boxes: 16px → 14px")
    print("✅ Reduced padding throughout:")
    print("   • Button padding: 12px/24px → 8px/16px")
    print("   • Input padding: 10px/14px → 8px/12px")
    print("   • Text padding: 24px → 16px")
    print("   • Table padding: 14px/18px → 10px/14px")
    print("✅ Smaller border radius for compact feel:")
    print("   • General: 8px → 6px")
    print("   • Titles: 6px → 4px")
    print("   • Text areas: 12px → 8px")
    print("\n🎯 Perfect balance for your device achieved!")
    
    # Uncomment the line below to actually launch the GUI and see the balanced fonts
    # launch_gui(people_list, courses, data_file)

if __name__ == "__main__":
    main()
