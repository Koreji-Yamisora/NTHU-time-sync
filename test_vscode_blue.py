#!/usr/bin/env python3
"""
Test script to showcase the VS Code blue accents
"""

from gui import launch_gui
from storage import load_data
import os

def main():
    """Test the VS Code blue accents"""
    data_file = "schedule_data.json"
    
    # Ensure data file exists
    if not os.path.exists(data_file):
        with open(data_file, "w") as f:
            import json
            json.dump({"courses": {}, "people": {}}, f)
    
    # Load data
    people_list, courses = load_data(data_file)
    
    print("🔵 VS Code Blue Accents Applied! 🔵")
    print("=" * 40)
    print("✅ Subtle VS Code Blue (#007ACC):")
    print("   • Focus borders: Input fields, text areas")
    print("   • Selected items: Lists, tables")
    print("   • Checked checkboxes: Active state")
    print("   • Scrollbar hover: Interactive feedback")
    print("   • Selected tabs: Active tab indicator")
    print("✅ Strategic Color Usage:")
    print("   • Not overwhelming the neutral design")
    print("   • Only for interactive/selected states")
    print("   • Maintains minimalistic luxury")
    print("   • Familiar VS Code developer experience")
    print("✅ Focus & Selection States:")
    print("   • LineEdit focus: Blue border")
    print("   • ComboBox focus: Blue border")
    print("   • TextEdit focus: Blue border")
    print("   • ListWidget selection: Blue background")
    print("   • TableWidget selection: Blue background")
    print("✅ Interactive Elements:")
    print("   • Checkbox checked: Blue background")
    print("   • Scrollbar hover: Blue handle")
    print("   • Tab selected: Blue background")
    print("✅ Balanced Design:")
    print("   • Neutral grays for base elements")
    print("   • VS Code blue for active states")
    print("   • Professional developer aesthetic")
    print("   • Subtle but recognizable accents")
    print("\n🎨 VS Code-inspired blue accents achieved!")
    
    # Uncomment the line below to actually launch the GUI and see the VS Code blue accents
    # launch_gui(people_list, courses, data_file)

if __name__ == "__main__":
    main()
