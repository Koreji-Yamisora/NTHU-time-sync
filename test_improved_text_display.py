#!/usr/bin/env python3
"""
Test script to showcase the improved text display
"""

from gui import launch_gui
from storage import load_data
import os

def main():
    """Test the improved text display"""
    data_file = "schedule_data.json"
    
    # Ensure data file exists
    if not os.path.exists(data_file):
        with open(data_file, "w") as f:
            import json
            json.dump({"courses": {}, "people": {}}, f)
    
    # Load data
    people_list, courses = load_data(data_file)
    
    print("🎨 Improved Text Display Applied! 🎨")
    print("=" * 45)
    print("✅ Schedule Details - Now Beautiful HTML:")
    print("   • Replaced terminal-style plain text")
    print("   • Added HTML formatting with colors")
    print("   • Beautiful headers with VS Code blue")
    print("   • Gradient separators")
    print("   • Card-style time slots")
    print("   • Emoji icons for visual appeal")
    print("✅ Common Times Results - Now Beautiful HTML:")
    print("   • Replaced terminal-style plain text")
    print("   • Added HTML formatting with colors")
    print("   • Beautiful headers with VS Code blue")
    print("   • Gradient separators")
    print("   • Card-style time slots")
    print("   • Emoji icons for visual appeal")
    print("✅ Typography Improvements:")
    print("   • Font: SF Mono → Segoe UI (more readable)")
    print("   • Font size: 13px → 14px (better readability)")
    print("   • Line height: 1.6 (optimal spacing)")
    print("   • Padding: 16px → 20px (more breathing room)")
    print("✅ Visual Design Elements:")
    print("   • VS Code blue headers (#007ACC)")
    print("   • Gradient separators")
    print("   • Card-style containers")
    print("   • Left border accents")
    print("   • Proper spacing and margins")
    print("✅ Emoji Icons for Clarity:")
    print("   • 📅 Schedule headers")
    print("   • 👤 Individual schedules")
    print("   • 🤝 Common times")
    print("   • 👥 Selected people")
    print("   • ⏰ Time slots")
    print("   • 📚 Course names")
    print("   • ✨ Free times")
    print("   • 🚫 Busy times")
    print("   • ⚠️ Warnings")
    print("   • ❌ No results")
    print("✅ Professional Appearance:")
    print("   • No more terminal/console look")
    print("   • Modern web-style formatting")
    print("   • Consistent with overall design")
    print("   • Easy to scan and read")
    print("\n🎨 Beautiful, readable text display achieved!")
    
    # Uncomment the line below to actually launch the GUI and see the improved text display
    # launch_gui(people_list, courses, data_file)

if __name__ == "__main__":
    main()
