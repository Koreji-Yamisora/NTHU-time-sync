#!/usr/bin/env python3
"""
Schedule Manager - A tool for managing schedules and finding common free times
"""

import os
import sys
import shutil
from storage import load_data, save_data, create_sample_data
from gui import launch_gui
from schedule import print_common_free_times


def get_data_file():
    """Return a path to save/load JSON outside the executable"""
    if getattr(sys, "frozen", False):
        # Running from PyInstaller executable
        base_path = os.path.dirname(sys.executable)
    else:
        # Running as normal Python script
        base_path = os.path.abspath(".")
    return os.path.join(base_path, "schedule_data.json")


def resource_path(relative_path):
    """Get absolute path to resource, works for PyInstaller"""
    base_path = getattr(sys, "_MEIPASS", os.path.abspath("."))
    return os.path.join(base_path, relative_path)


def main():
    """Main function to run the schedule manager"""
    data_file = get_data_file()
    if not os.path.exists(data_file):
        # Copy bundled default JSON to executable folder
        bundled_json = resource_path("schedule_data.json")
        shutil.copy(bundled_json, data_file)
    if getattr(sys, "frozen", False):
        people_list = load_data(data_file)
        launch_gui(people_list, data_file)
    else:
        print("Schedule Manager")
        print("=" * 50)

        # Load existing data or create sample data
        if os.path.exists(data_file):
            print(f"Loading data from {data_file}...")
            people_list = load_data(data_file)
            print(f"Loaded {len(people_list)} people.")
        else:
            print("No existing data found. Creating sample data...")
            people_list = create_sample_data()
            save_data(people_list, data_file)
            print(f"Created sample data with {len(people_list)} people.")
            print("Sample data saved to", data_file)

        # Show current people
        if people_list:
            print("\nCurrent people:")
            for person in people_list:
                print(f"  - {person.name}")

        # Ask user what they want to do
        while True:
            print("\nWhat would you like to do?")
            print("1. Launch GUI")
            print("2. Show common free times (console)")
            print("3. Show all schedules (console)")
            print("4. Exit")

            choice = input("Enter your choice (1-4): ").strip()

            if choice == "1":
                print("Launching GUI...")
                launch_gui(people_list, data_file)
                break

            elif choice == "2":
                show_common_times_console(people_list)

            elif choice == "3":
                show_all_schedules(people_list)

            elif choice == "4":
                print("Goodbye!")
                break

            else:
                print("Invalid choice. Please try again.")


def show_common_times_console(people_list):
    """Show common free times in console"""
    if not people_list:
        print("No people in the system.")
        return

    days = [
        "Monday",
        "Tuesday",
        "Wednesday",
        "Thursday",
        "Friday",
        "Saturday",
        "Sunday",
    ]

    print("\nCommon Free Times:")
    print("=" * 50)

    for day in days:
        print_common_free_times(people_list, day)


def show_all_schedules(people_list):
    """Show all individual schedules"""
    if not people_list:
        print("No people in the system.")
        return

    print("\nAll Schedules:")
    print("=" * 50)

    for person in people_list:
        print(f"\n{person.name}'s Schedule:")
        print("-" * (len(person.name) + 12))

        days = [
            "Monday",
            "Tuesday",
            "Wednesday",
            "Thursday",
            "Friday",
            "Saturday",
            "Sunday",
        ]

        for day in days:
            day_slots = []
            for course_slots in person.schedule:
                for slot in course_slots:
                    if slot.day == day:
                        day_slots.append(f"{slot.start_time}-{slot.end_time}")

            if day_slots:
                print(f"  {day:10}: {', '.join(day_slots)}")
            else:
                print(f"  {day:10}: Free")


if __name__ == "__main__":
    main()
