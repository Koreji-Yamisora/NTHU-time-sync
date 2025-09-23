import json
import os
import base64
import hashlib
from cryptography.fernet import Fernet
from models import Person, TimeSlot
from datetime import datetime, timedelta
from zoneinfo import ZoneInfo
import re
import urllib.parse


TAIPEI = ZoneInfo("Asia/Taipei")
DAY_OFFSET = +1  # shift days manually

# Encryption key (in production, this should be more secure)
ENCRYPTION_KEY = b'schedule_manager_key_2024_secure_32bytes!'


def get_encryption_key():
    """Generate encryption key from the base key"""
    key = hashlib.sha256(ENCRYPTION_KEY).digest()
    return base64.urlsafe_b64encode(key)


def encrypt_json_data(data):
    """Encrypt JSON data"""
    try:
        key = get_encryption_key()
        fernet = Fernet(key)
        json_str = json.dumps(data, indent=2)
        encrypted_data = fernet.encrypt(json_str.encode())
        return base64.b64encode(encrypted_data).decode()
    except Exception as e:
        raise Exception(f"Encryption failed: {str(e)}")


def decrypt_json_data(encrypted_data):
    """Decrypt JSON data"""
    try:
        key = get_encryption_key()
        fernet = Fernet(key)
        encrypted_bytes = base64.b64decode(encrypted_data.encode())
        decrypted_data = fernet.decrypt(encrypted_bytes)
        return json.loads(decrypted_data.decode())
    except Exception as e:
        raise Exception(f"Decryption failed: {str(e)}")


def is_encrypted_json(filename):
    """Check if a JSON file is encrypted by trying to detect the format"""
    try:
        with open(filename, 'r') as f:
            content = f.read().strip()
            
        # Try to parse as regular JSON first
        json.loads(content)
        return False
    except:
        try:
            # Try to decrypt - if it works, it's encrypted
            decrypt_json_data(content)
            return True
        except:
            return False


def parse_ics_datetime(datetime_str):
    """Parse ICS datetime string to Python datetime object with manual day offset"""

    if datetime_str.endswith("Z"):
        dt = datetime.strptime(datetime_str[:-1], "%Y%m%dT%H%M%S")
        dt = dt.replace(tzinfo=ZoneInfo("UTC")).astimezone(TAIPEI)
        return dt + timedelta(days=DAY_OFFSET)

    raise ValueError(f"Unable to parse datetime: {datetime_str}")


def parse_ics_content(content):
    """Parse ICS content - use first line of description as course name"""

    events = []
    lines = content.split("\n")

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

            full_line = full_line.strip()

            colon_pos = full_line.find(":")
            if colon_pos > 0:
                property_name = full_line[:colon_pos]
                property_value = full_line[colon_pos + 1 :]

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

                    match = re.search(r"courses/([^\s]+)", full_line)
                    if match:
                        course_code = match.group(1)
                        course_code = urllib.parse.unquote(course_code).replace(" ", "")
                        current_event["course_code"] = course_code
                    else:
                        current_event["course_code"] = "Unknown"
        i += 1

    return events


def create_time_slot_from_event(event):
    """Create TimeSlot from single event with 24-hour format"""
    start_dt = event["start"]
    end_dt = event["end"]
    day_name = start_dt.strftime("%A")  # Monday, Tuesday, etc.

    # Format times in 24-hour format (HH:MM)
    start_time = start_dt.strftime("%H:%M")
    end_time = end_dt.strftime("%H:%M")

    return TimeSlot(start_time, end_time, day_name)


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
        name = event.get(
            "course_name", "imported Courses"
        )  # This uses description first line
        code = event.get("course_code", "Unknown Code")
        course_name = f"{name} ({code})"

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
    """Load people and courses from JSON file (handles both encrypted and plain JSON)"""
    if not os.path.exists(filename):
        return [], {}

    with open(filename, "r") as file:
        content = file.read().strip()
    
    # Try to determine if it's encrypted or plain JSON
    try:
        # First try to parse as plain JSON
        data = json.loads(content)
    except:
        try:
            # If that fails, try to decrypt
            data = decrypt_json_data(content)
        except Exception as e:
            raise Exception(f"Failed to load data: File is neither valid JSON nor encrypted data. Error: {str(e)}")

    # Load courses
    courses = {}
    for cname, slots in data.get("courses", {}).items():
        courses[cname] = [TimeSlot(*slot) for slot in slots]

    # Load people
    people = []
    for name, course_names in data.get("people", {}).items():
        # Get the actual course time slots for each course name
        person_courses = []
        for course_name in course_names:
            if course_name in courses:
                person_courses.append(courses[course_name])  # Keep as list of courses
        people.append(Person(name, person_courses))

    return people, courses


def save_data(people_list, courses, filename):
    """Save people and courses to JSON file"""
    # Convert courses to saveable format
    courses_data = {}
    for course_name, slots in courses.items():
        courses_data[course_name] = [
            (slot.start_time, slot.end_time, slot.day) for slot in slots
        ]

    # Create people data with course names
    people_data = {}
    for person in people_list:
        course_names = []
        for course_slots in person.schedule:
            # Find the course name that matches these slots
            for course_name, stored_slots in courses.items():
                if stored_slots == course_slots:
                    course_names.append(course_name)
                    break
        people_data[person.name] = course_names

    data = {"courses": courses_data, "people": people_data}

    with open(filename, "w") as file:
        json.dump(data, file, indent=2)


def save_data_encrypted(people_list, courses, filename):
    """Save people and courses to encrypted JSON file"""
    # Convert courses to saveable format
    courses_data = {}
    for course_name, slots in courses.items():
        courses_data[course_name] = [
            (slot.start_time, slot.end_time, slot.day) for slot in slots
        ]

    # Create people data with course names
    people_data = {}
    for person in people_list:
        course_names = []
        for course_slots in person.schedule:
            # Find the course name that matches these slots
            for course_name, stored_slots in courses.items():
                if stored_slots == course_slots:
                    course_names.append(course_name)
                    break
        people_data[person.name] = course_names

    data = {"courses": courses_data, "people": people_data}
    
    # Encrypt the data
    encrypted_data = encrypt_json_data(data)
    
    with open(filename, "w") as file:
        file.write(encrypted_data)


def export_data_plain(people_list, courses, filename):
    """Export people and courses to plain JSON file"""
    # Convert courses to saveable format
    courses_data = {}
    for course_name, slots in courses.items():
        courses_data[course_name] = [
            (slot.start_time, slot.end_time, slot.day) for slot in slots
        ]

    # Create people data with course names
    people_data = {}
    for person in people_list:
        course_names = []
        for course_slots in person.schedule:
            # Find the course name that matches these slots
            for course_name, stored_slots in courses.items():
                if stored_slots == course_slots:
                    course_names.append(course_name)
                    break
        people_data[person.name] = course_names

    data = {"courses": courses_data, "people": people_data}

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
    """Helper function to create a TimeSlot with 24-hour format validation"""
    # Validate 24-hour format (HH:MM)
    import re

    time_pattern = r"^([01]?[0-9]|2[0-3]):[0-5][0-9]$"

    if not re.match(time_pattern, start_time):
        raise ValueError(
            f"Invalid start_time format: {start_time}. Expected HH:MM (24-hour format)"
        )
    if not re.match(time_pattern, end_time):
        raise ValueError(
            f"Invalid end_time format: {end_time}. Expected HH:MM (24-hour format)"
        )

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
