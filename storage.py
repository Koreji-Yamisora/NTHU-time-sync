import json
from models import Person, TimeSlot


def load_data(filename):
    with open(filename, "r") as file:
        data = json.load(file)

    courses = {}
    for cname, slots in data["courses"].items():
        courses[cname] = [TimeSlot(*slot) for slot in slots]

    people = []
    for name, schedule in data["people"].items():
        people.append(Person(name, [courses[cname] for cname in schedule]))

    return people
