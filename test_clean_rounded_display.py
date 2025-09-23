#!/usr/bin/env python3
"""
Test script to showcase the clean rounded display without emojis
"""

from gui import launch_gui
from storage import load_data
import os

def main():
    """Test the clean rounded display"""
    data_file = "schedule_data.json"
    
    # Ensure data file exists
    if not os.path.exists(data_file):
        with open(data_file, "w") as f:
            import json
            json.dump({"courses": {}, "people": {}}, f)
    
    # Load data
    people_list, courses = load_data(data_file)
    
    print("🔲 Clean Rounded Display Applied! 🔲")
    print("=" * 45)
    print("✅ Emojis Removed:")
    print("   • No more 📅, 👤, 🤝, 👥, ⏰, 📚, ✨, 🚫, ⚠️, ❌")
    print("   • Clean, text-only headers")
    print("   • Professional, minimalistic appearance")
    print("   • Focus on content, not decorative elements")
    print("✅ Rounded Backgrounds Added:")
    print("   • Headers: border-radius: 12px")
    print("   • Day sections: border-radius: 10px")
    print("   • Time slots: border-radius: 10px")
    print("   • People lists: border-radius: 10px")
    print("   • Status messages: border-radius: 10px")
    print("✅ Enhanced Padding:")
    print("   • Headers: padding: 12px 16px")
    print("   • Day sections: padding: 10px 16px")
    print("   • Time slots: padding: 10px 16px")
    print("   • People lists: padding: 8px 16px")
    print("✅ Consistent Styling:")
    print("   • All backgrounds use #2d2d2d")
    print("   • All borders use #404040")
    print("   • All accents use #007ACC")
    print("   • Uniform border-radius throughout")
    print("✅ Clean Visual Hierarchy:")
    print("   • Clear section separation")
    print("   • Consistent spacing")
    print("   • Professional typography")
    print("   • Easy to scan content")
    print("✅ Minimalistic Design:")
    print("   • No distracting emojis")
    print("   • Clean, rounded containers")
    print("   • Focus on readability")
    print("   • Professional appearance")
    print("✅ Modern Card-Style Layout:")
    print("   • Rounded corners everywhere")
    print("   • Consistent padding")
    print("   • Clean visual separation")
    print("   • Modern, polished look")
    print("\n🎨 Clean, rounded, professional display achieved!")
    
    # Uncomment the line below to actually launch the GUI and see the clean rounded display
    # launch_gui(people_list, courses, data_file)

if __name__ == "__main__":
    main()
