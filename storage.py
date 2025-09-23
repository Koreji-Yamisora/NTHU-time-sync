import json
import os
from models import Person, TimeSlot


def parse_ics_datetime(datetime_str):
    """Parse ICS datetime string to Python datetime object"""
    from datetime import datetime

    # Remove timezone info if present
    if datetime_str.endswith("Z"):
        datetime_str = datetime_str[:-1]

    # Handle different datetime formats
    formats_to_try = [
        "%Y%m%dT%H%M%S",  # 20231025T140000
        "%Y%m%d",  # 20231025 (date only)
    ]

    for fmt in formats_to_try:
        try:
            return datetime.strptime(datetime_str, fmt)
        except ValueError:
            continue

    # If no format works, try to parse manually
    if len(datetime_str) >= 8:
        try:
            year = int(datetime_str[:4])
            month = int(datetime_str[4:6])
            day = int(datetime_str[6:8])

            if len(datetime_str) >= 15:  # Has time component
                hour = int(datetime_str[9:11])
                minute = int(datetime_str[11:13])
                second = int(datetime_str[13:15]) if len(datetime_str) >= 15 else 0
                return datetime(year, month, day, hour, minute, second)
            else:
                return datetime(year, month, day, 9, 0)  # Default to 9 AM for date-only

        except (ValueError, IndexError):
            pass

    raise ValueError(f"Unable to parse datetime: {datetime_str}")


def parse_ics_content(content):
    """Parse ICS content - use first line of description as course name"""
    from datetime import datetime
    import re

    events = []
    lines = content.split("\n")
    lines = [line.strip() for line in lines]

    current_event = None
    in_event = False
    i = 0

    while i < len(lines):
        line = lines[i]

        if line == "BEGIN:VEVENT":
            in_event = True
            current_event = {}

        elif line == "END:VEVENT" and in_event:
            if current_event and "start" in current_event and "end" in current_event:
                # Ensure we have a course name, fallback to summary if no description
                if "course_name" not in current_event:
                    current_event["course_name"] = current_event.get(
                        "summary", "Imported Course"
                    )
                events.append(current_event)
            current_event = None
            in_event = False

        elif in_event and current_event is not None and ":" in line:
            # Handle multi-line folding
            full_line = line
            while i + 1 < len(lines) and (
                lines[i + 1].startswith(" ") or lines[i + 1].startswith("\t")
            ):
                i += 1
                full_line += lines[i][1:]

            colon_pos = full_line.find(":")
            if colon_pos > 0:
                property_name = full_line[:colon_pos]
                property_value = full_line[colon_pos + 1 :]

                # Handle parameters (like DTSTART;TZID=...)
                semicolon_pos = property_name.find(";")
                if semicolon_pos > 0:
                    property_name = property_name[:semicolon_pos]

                if property_name == "DTSTART":
                    current_event["start"] = parse_ics_datetime(property_value)
                elif property_name == "DTEND":
                    current_event["end"] = parse_ics_datetime(property_value)
                elif property_name == "SUMMARY":
                    # Store summary but don't use as course name yet
                    current_event["summary"] = (
                        property_value.replace("\\n", " ").replace("\\,", ",").strip()
                    )
                elif property_name == "DESCRIPTION":
                    # PRIORITY: Use first line of description as course name
                    description_lines = property_value.replace("\\n", "\n").split("\n")
                    first_line = description_lines[0].replace("\\,", ",").strip()

                    if first_line:
                        current_event["course_name"] = first_line

                    # Store full description for potential course code extraction
                    current_event["full_description"] = property_value

        i += 1

    return events


def extract_course_name_and_code(event):
    """Extract the best course name from an event, preferring description first line"""

    # Priority 1: First line of description (English name)
    if "course_name" in event:
        course_name = event["course_name"]

        # Try to also extract course code from full description if available
        if "full_description" in event:
            course_code = extract_course_code_from_description(
                event["full_description"]
            )
            if course_code:
                # You can choose format: "Course Name (CODE)" or just "Course Name"
                return f"{course_name} ({course_code})"
                # OR return just the English name: return course_name

        return course_name

    # Priority 2: Summary field
    if "summary" in event:
        return event["summary"]

    # Priority 3: Default fallback
    return "Imported Course"


def create_time_slot_from_event(event):
    """Create TimeSlot from single event"""
    start_dt = event["start"]
    end_dt = event["end"]
    day_name = start_dt.strftime("%A")  # Monday, Tuesday, etc.

    return TimeSlot(start_dt.strftime("%H:%M"), end_dt.strftime("%H:%M"), day_name)


def extract_course_code_from_description(description):
    """Extract course code from full description"""
    import re

    # Clean up the description
    cleaned = description.replace("\\n", "\n").replace("\\t", "\t")

    # Look for URL pattern with course code (your original logic)
    url_match = re.search(r"https://nthumods\.com/courses/([^\s\\]+)", cleaned)
    if url_match:
        url_part = url_match.group(1)
        import urllib.parse

        return urllib.parse.unquote(url_part)
    return None


def import_ics_file(filename, courses, person_name, people_list):
    """Import ICS file and create courses using description first line as course name"""
    with open(filename, "r", encoding="utf-8") as f:
        ics_content = f.read()

    events = parse_ics_content(ics_content)
    if not events:
        raise ValueError("No events found in ICS file")

    # Group events by course name (using description first line)
    courses_from_ics = {}
    for event in events:
        course_name = extract_course_name_and_code(
            event
        )  # This uses description first line

        if course_name not in courses_from_ics:
            courses_from_ics[course_name] = []

        time_slot = create_time_slot_from_event(event)
        courses_from_ics[course_name].append(time_slot)

    # Add courses and assign to person
    person = get_person(people_list, person_name)
    if not person:
        person = add_person(people_list, person_name, [])

    for course_name, time_slots in courses_from_ics.items():
        # Check if course already exists, if not create it
        if course_name not in courses:
            add_course(courses, course_name, time_slots)
        else:
            # If course exists, merge time slots
            existing_slots = courses[course_name]
            for slot in time_slots:
                if not any(
                    existing_slot.start_time == slot.start_time
                    and existing_slot.end_time == slot.end_time
                    and existing_slot.day == slot.day
                    for existing_slot in existing_slots
                ):
                    existing_slots.append(slot)

        # Assign course to person if not already assigned
        try:
            assign_course_to_person(people_list, person_name, courses, course_name)
        except ValueError:
            # Person already has this course
            pass


def load_data(filename):
    """Load people and courses from JSON file"""
    if not os.path.exists(filename):
        return []

    with open(filename, "r") as file:
        data = json.load(file)

    courses = {}
    for cname, slots in data.get("courses", {}).items():
        courses[cname] = [TimeSlot(*slot) for slot in slots]

    people = []
    for name, schedule in data.get("people", {}).items():
        people.append(
            Person(name, [courses[cname] for cname in schedule if cname in courses])
        )

    return people


def save_data(people_list, filename):
    """Save people and courses to JSON file"""
    # Extract all unique courses from all people
    all_courses = {}

    for person in people_list:
        for course_slots in person.schedule:
            # Create a unique course identifier based on the time slots
            course_key = f"course_{len(all_courses)}"
            slots_data = [
                (slot.start_time, slot.end_time, slot.day) for slot in course_slots
            ]

            # Check if this course already exists
            existing_key = None
            for key, existing_slots in all_courses.items():
                if existing_slots == slots_data:
                    existing_key = key
                    break

            if existing_key is None:
                all_courses[course_key] = slots_data

    # Create people data with course references
    people_data = {}
    for person in people_list:
        course_refs = []
        for course_slots in person.schedule:
            slots_data = [
                (slot.start_time, slot.end_time, slot.day) for slot in course_slots
            ]
            # Find the course key for this set of slots
            for key, existing_slots in all_courses.items():
                if existing_slots == slots_data:
                    course_refs.append(key)
                    break
        people_data[person.name] = course_refs

    data = {"courses": all_courses, "people": people_data}

    with open(filename, "w") as file:
        json.dump(data, file, indent=2)


def add_person(people_list, name, schedule=None):
    """Add a new person to the list"""
    if any(person.name == name for person in people_list):
        raise ValueError(f"Person with name '{name}' already exists")

    new_person = Person(name, schedule or [])
    people_list.append(new_person)
    return new_person


def remove_person(people_list, name):
    """Remove a person from the list"""
    for i, person in enumerate(people_list):
        if person.name == name:
            return people_list.pop(i)
    raise ValueError(f"Person with name '{name}' not found")


def update_person_schedule(people_list, name, new_schedule):
    """Update a person's schedule"""
    for person in people_list:
        if person.name == name:
            person.schedule = new_schedule
            person.busy_time = person._create_busy_time_dict()
            return person
    raise ValueError(f"Person with name '{name}' not found")


def get_person(people_list, name):
    """Get a person by name"""
    for person in people_list:
        if person.name == name:
            return person
    return None


def create_time_slot(start_time, end_time, day):
    """Helper function to create a TimeSlot"""
    return TimeSlot(start_time, end_time, day)


def load_courses(filename):
    """Load courses dictionary from JSON file"""
    if not os.path.exists(filename):
        return {}

    with open(filename, "r") as file:
        data = json.load(file)

    courses = {}
    for cname, slots in data.get("courses", {}).items():
        courses[cname] = [TimeSlot(*slot) for slot in slots]

    return courses


def save_courses(courses, filename):
    """Save courses to JSON file while preserving people data"""
    data = {"courses": {}, "people": {}}

    # Load existing data
    if os.path.exists(filename):
        with open(filename, "r") as file:
            existing_data = json.load(file)
            data["people"] = existing_data.get("people", {})

    # Convert courses to saveable format
    for course_name, slots in courses.items():
        data["courses"][course_name] = [
            (slot.start_time, slot.end_time, slot.day) for slot in slots
        ]

    with open(filename, "w") as file:
        json.dump(data, file, indent=2)


def add_course(courses, course_name, time_slots):
    """Add a new course with time slots"""
    if course_name in courses:
        raise ValueError(f"Course '{course_name}' already exists")

    courses[course_name] = time_slots
    return courses[course_name]


def remove_course(courses, course_name):
    """Remove a course"""
    if course_name not in courses:
        raise ValueError(f"Course '{course_name}' not found")

    return courses.pop(course_name)


def update_course(courses, course_name, new_time_slots):
    """Update a course's time slots"""
    if course_name not in courses:
        raise ValueError(f"Course '{course_name}' not found")

    courses[course_name] = new_time_slots
    return courses[course_name]


def get_course(courses, course_name):
    """Get a course by name"""
    return courses.get(course_name)


def assign_course_to_person(people_list, person_name, courses, course_name):
    """Assign a course to a person"""
    if course_name not in courses:
        raise ValueError(f"Course '{course_name}' not found")

    person = get_person(people_list, person_name)
    if not person:
        raise ValueError(f"Person '{person_name}' not found")

    # Check if person already has this course
    course_slots = courses[course_name]
    for existing_course in person.schedule:
        if existing_course == course_slots:
            raise ValueError(
                f"Person '{person_name}' is already enrolled in '{course_name}'"
            )

    person.schedule.append(course_slots)
    person.busy_time = person._create_busy_time_dict()
    return person


def remove_course_from_person(people_list, person_name, courses, course_name):
    """Remove a course from a person's schedule"""
    if course_name not in courses:
        raise ValueError(f"Course '{course_name}' not found")

    person = get_person(people_list, person_name)
    if not person:
        raise ValueError(f"Person '{person_name}' not found")

    course_slots = courses[course_name]

    # Find and remove the course from person's schedule
    for i, existing_course in enumerate(person.schedule):
        if existing_course == course_slots:
            person.schedule.pop(i)
            person.busy_time = person._create_busy_time_dict()
            return person

    raise ValueError(f"Person '{person_name}' is not enrolled in '{course_name}'")


def get_people_in_course(people_list, courses, course_name):
    """Get list of people enrolled in a specific course"""
    if course_name not in courses:
        raise ValueError(f"Course '{course_name}' not found")

    course_slots = courses[course_name]
    enrolled_people = []

    for person in people_list:
        for existing_course in person.schedule:
            if existing_course == course_slots:
                enrolled_people.append(person.name)
                break

    return enrolled_people


def create_sample_data():
    """Create sample data for testing"""
    # Create some sample time slots
    math_slots = [
        TimeSlot("09:00", "10:30", "Monday"),
        TimeSlot("09:00", "10:30", "Wednesday"),
        TimeSlot("09:00", "10:30", "Friday"),
    ]

    physics_slots = [
        TimeSlot("11:00", "12:30", "Tuesday"),
        TimeSlot("11:00", "12:30", "Thursday"),
    ]

    chemistry_slots = [
        TimeSlot("14:00", "15:30", "Monday"),
        TimeSlot("14:00", "15:30", "Wednesday"),
    ]

    # Create sample people
    people = [
        Person("Alice", [math_slots, physics_slots]),
        Person("Bob", [math_slots, chemistry_slots]),
        Person("Charlie", [physics_slots, chemistry_slots]),
    ]

    return people


def create_sample_courses():
    """Create sample courses for testing"""
    courses = {
        "Mathematics": [
            TimeSlot("09:00", "10:30", "Monday"),
            TimeSlot("09:00", "10:30", "Wednesday"),
            TimeSlot("09:00", "10:30", "Friday"),
        ],
        "Physics": [
            TimeSlot("11:00", "12:30", "Tuesday"),
            TimeSlot("11:00", "12:30", "Thursday"),
        ],
        "Chemistry": [
            TimeSlot("14:00", "15:30", "Monday"),
            TimeSlot("14:00", "15:30", "Wednesday"),
        ],
    }
    return courses
