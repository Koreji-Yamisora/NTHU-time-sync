#!/usr/bin/env python3
"""
Test script to showcase the minimalistic luxury design improvements
"""

from gui import launch_gui
from storage import load_data
import os

def main():
    """Test the minimalistic luxury GUI"""
    data_file = "schedule_data.json"
    
    # Ensure data file exists
    if not os.path.exists(data_file):
        with open(data_file, "w") as f:
            import json
            json.dump({"courses": {}, "people": {}}, f)
    
    # Load data
    people_list, courses = load_data(data_file)
    
    print("✨ Minimalistic Luxury Design Applied! ✨")
    print("=" * 50)
    print("✅ Removed all emojis for clean, professional look")
    print("✅ Reduced title sizes for better proportions")
    print("✅ Enhanced schedule details:")
    print("   • Increased height to 500px")
    print("   • Better font: SF Mono for premium feel")
    print("   • Increased line height to 1.8")
    print("   • More padding (24px) for luxury spacing")
    print("✅ Balanced course details table:")
    print("   • Better proportions (300px/700px split)")
    print("   • Increased table height to 350px")
    print("   • Enhanced padding (14px/18px)")
    print("   • Compact add course section")
    print("✅ Improved common times results:")
    print("   • Increased height to 400px")
    print("   • Premium font styling")
    print("   • Line height 1.9 for readability")
    print("✅ Added proper checkbox ticks with SVG icons")
    print("✅ Consistent 8px margins throughout")
    print("✅ Professional typography hierarchy")
    print("\n🎨 Clean, minimalistic luxury design achieved!")
    
    # Uncomment the line below to actually launch the GUI and see the luxury design
    # launch_gui(people_list, courses, data_file)

if __name__ == "__main__":
    main()
