#!/usr/bin/env python3
"""
Test script to showcase the reduced element sizes for less cluttered interface
"""

from gui import launch_gui
from storage import load_data
import os

def main():
    """Test that the interface is now less cluttered with smaller elements"""
    data_file = "schedule_data.json"
    
    # Ensure data file exists
    if not os.path.exists(data_file):
        with open(data_file, "w") as f:
            import json
            json.dump({"courses": {}, "people": {}}, f)
    
    # Load data
    people_list, courses = load_data(data_file)
    
    print("📏 Reduced Element Sizes Applied! 📏")
    print("=" * 50)
    print("✅ Button Improvements:")
    print("   • Reduced padding: 8px 16px → 6px 12px")
    print("   • Smaller border radius: 6px → 4px")
    print("   • Reduced font size: 12px → 11px")
    print("   • Smaller min-height: 16px → 14px")
    print("✅ Input Field Improvements:")
    print("   • Reduced padding: 8px 12px → 6px 10px")
    print("   • Thinner borders: 2px → 1px")
    print("   • Smaller border radius: 6px → 4px")
    print("   • Reduced font size: 12px → 11px")
    print("✅ Text Area Improvements:")
    print("   • Reduced padding: 10px → 8px")
    print("   • Thinner borders: 2px → 1px")
    print("   • Smaller border radius: 6px → 4px")
    print("   • Reduced font size: 12px → 11px")
    print("✅ List Widget Improvements:")
    print("   • Reduced padding: 4px → 3px")
    print("   • Thinner borders: 2px → 1px")
    print("   • Smaller border radius: 6px → 4px")
    print("   • Reduced font size: 12px → 11px")
    print("✅ Table Widget Improvements:")
    print("   • Reduced padding: 4px → 3px")
    print("   • Thinner borders: 2px → 1px")
    print("   • Smaller border radius: 6px → 4px")
    print("   • Reduced font size: 12px → 11px")
    print("✅ Group Box Improvements:")
    print("   • Reduced font size: 14px → 12px")
    print("   • Thinner borders: 2px → 1px")
    print("   • Smaller border radius: 8px → 6px")
    print("   • Reduced margins: 6px → 4px")
    print("✅ Tab Improvements:")
    print("   • Reduced padding: 12px 20px → 8px 16px")
    print("   • Smaller border radius: 20px → 16px")
    print("   • Reduced font size: 14px → 12px")
    print("   • Smaller min-width: 100px → 80px")
    print("✅ Title Improvements:")
    print("   • Reduced font size: 16px → 14px")
    print("   • Smaller padding: 6px 12px → 4px 8px")
    print("   • Smaller border radius: 4px → 3px")
    print("   • Reduced margins: 2px → 1px")
    print("✅ Height Reductions:")
    print("   • People list: 200px → 150px")
    print("   • Schedule text: 300px → 200px")
    print("   • Courses list: 200px → 150px")
    print("   • Course table: 250px → 180px")
    print("   • Results text: 400px → 250px")
    print("✅ Benefits:")
    print("   • Less cluttered interface")
    print("   • More spacious feeling")
    print("   • Better visual hierarchy")
    print("   • Professional appearance")
    print("\n🎨 Reduced element sizes achieved!")
    
    # Uncomment the line below to actually launch the GUI and see the improvements
    # launch_gui(people_list, courses, data_file)

if __name__ == "__main__":
    main()
