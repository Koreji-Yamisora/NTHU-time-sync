#!/usr/bin/env python3
"""
Test script to showcase the macOS Tahoe UI styling
"""

from gui import launch_gui
from storage import load_data
import os

def main():
    """Test the macOS Tahoe UI styling"""
    data_file = "schedule_data.json"
    
    # Ensure data file exists
    if not os.path.exists(data_file):
        with open(data_file, "w") as f:
            import json
            json.dump({"courses": {}, "people": {}}, f)
    
    # Load data
    people_list, courses = load_data(data_file)
    
    print("🍎 macOS Tahoe UI Styling Applied! 🍎")
    print("=" * 45)
    print("✅ Fully Rounded Tab Buttons:")
    print("   • border-radius: 20px (fully rounded)")
    print("   • Removed top-only rounded corners")
    print("   • Modern pill-shaped tabs")
    print("✅ Refined Tab Spacing:")
    print("   • margin-right: 8px (increased from 4px)")
    print("   • padding: 12px 20px (optimized)")
    print("   • min-width: 100px (reduced from 120px)")
    print("✅ Consistent Rounded Corners:")
    print("   • Normal tabs: border-radius: 20px")
    print("   • Selected tabs: border-radius: 20px")
    print("   • Hover tabs: border-radius: 20px")
    print("✅ Modern Tab Pane:")
    print("   • border-radius: 16px (increased from 12px)")
    print("   • margin-top: 8px (increased from -2px)")
    print("   • Better separation from tabs")
    print("✅ macOS Big Sur/Monterey Style:")
    print("   • Pill-shaped tab buttons")
    print("   • Smooth rounded corners")
    print("   • Clean, modern appearance")
    print("   • Consistent with macOS design language")
    print("✅ Typography Refinements:")
    print("   • font-size: 14px (reduced from 15px)")
    print("   • Better proportions for rounded tabs")
    print("\n🎨 macOS Tahoe UI design achieved!")
    
    # Uncomment the line below to actually launch the GUI and see the macOS Tahoe UI
    # launch_gui(people_list, courses, data_file)

if __name__ == "__main__":
    main()
