import json
import os
from models import Person, TimeSlot


def import_ics_file(filename, courses, person, people_list):
    with open(filename, "r", encoding="utf-8") as f:
        ics = f.read()
    events = parse_ics_content(ics)
    for event in events:
        course_name = event.get("course_name", "Unnamed Course")
        add_course(courses, course_name, [create_time_slot_from_event(event)])
        add_person(people_list, person)
        assign_course_to_person(people_list, person, courses, course_name)


def create_time_slot_from_event(event):
    """Create TimeSlot from single event"""
    start_dt = event["start"]
    end_dt = event["end"]
    day_name = start_dt.strftime("%A")  # Monday, Tuesday, etc.

    return TimeSlot(start_dt.strftime("%H:%M"), end_dt.strftime("%H:%M"), day_name)


def parse_ics_content(content):
    """Parse ICS content - simple weekly schedule"""
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
            if current_event:
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

                if property_name == "DTSTART":
                    current_event["start"] = parse_ics_datetime(property_value)
                elif property_name == "DTEND":
                    current_event["end"] = parse_ics_datetime(property_value)
                elif property_name == "DESCRIPTION":
                    # Course name is first line of description

                    first_line = property_value.split("\\n")[0]
                    current_event["course_name"] = first_line
                    course_cod = course_code(property_value)
                    if course_cod:
                        current_event["course_code"] = course_code

        i += 1

    return events


def course_code(des):
    import re

    cled = des.replace("\n\t", "").replace("\t", "")
    url_match = re.search(r"https://nthumods\.com/courses/([^\s\\]+)", cled)
    if url_match:
        url_part = url_match.group(1)
        import urllib.parse

        return urllib.parse.unquote(url_part)


def parse_ics_datetime(datetime_str):
    """Generate TImeSlot"""
    from datetime import datetime

    if datetime_str.endwith("Z"):
        datetime_str = datetime_str[:-1]
    day = int(datetime_str[6:8])
    hour = int(datetime_str[9:11])
    minute = int(datetime_str[11:13])

    return datetime(day, hour, minute)


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
