class TimeSlot:
    def __init__(self, start_time, end_time, day):
        self.start_time = start_time
        self.end_time = end_time
        self.day = day

    def __str__(self):
        return f'("{self.start_time}", "{self.end_time}", "{self.day}")'


class Person:
    def __init__(self, name, schedule=None):
        self.name = name
        self.schedule = schedule or []
        # Create busy_time dictionary for compatibility with existing functions
        self.busy_time = self._create_busy_time_dict()

    def _create_busy_time_dict(self):
        """Convert schedule to busy_time format expected by the functions"""
        busy_dict = {}
        counter = 0
        for course in self.schedule:
            for slot in course:
                busy_dict[counter] = (slot.start_time, slot.end_time, slot.day)
                counter += 1
        return busy_dict

    def __getitem__(self, key):
        if key == self.name:
            return self.schedule
        if hasattr(self, key):
            return getattr(self, key)

    def __setitem__(self, key, value):
        if key == self.name:
            self.schedule = value
            self.busy_time = (
                self._create_busy_time_dict()
            )  # Update busy_time when schedule changes
        elif hasattr(self, key):
            setattr(self, key, value)
        else:
            raise KeyError(f"No such key: {key}")

    def __str__(self):
        flat = [slot for group in self.schedule for slot in group]
        schdu = ", ".join(map(str, flat))
        return f"{self.name}: ({schdu})"


def to_minutes(time_str):
    """Convert time string (HH:MM) to minutes since midnight"""
    h, m = map(int, time_str.split(":"))
    return h * 60 + m


def to_time(minutes):
    """Convert minutes since midnight back to time string (HH:MM)"""
    return f"{minutes // 60:02d}:{minutes % 60:02d}"


def invert_busy(busy_times, day, start="09:00", end="18:00"):
    """Convert busy intervals into free intervals for a given day."""
    start_m, end_m = to_minutes(start), to_minutes(end)
    intervals = [t for t in busy_times if t[2] == day]  # filter by day
    intervals_m = [(to_minutes(s), to_minutes(e)) for s, e, d in intervals]
    intervals_m.sort()

    free = []
    current = start_m
    for s, e in intervals_m:
        if current < s:
            free.append((current, s))
        current = max(current, e)
    if current < end_m:
        free.append((current, end_m))
    return free


def intersect_intervals(list1, list2):
    """Intersect two lists of intervals"""
    i, j = 0, 0
    result = []
    while i < len(list1) and j < len(list2):
        start = max(list1[i][0], list2[j][0])
        end = min(list1[i][1], list2[j][1])
        if start < end:
            result.append((start, end))
        if list1[i][1] < list2[j][1]:
            i += 1
        else:
            j += 1
    return result


def common_free_times(people_list, day):
    """Find common free times for multiple Person objects on a given day"""
    all_free = []
    for person in people_list:
        free = invert_busy(list(person.busy_time.values()), day)
        all_free.append(free)

    if not all_free:
        return []

    # Intersect all free times
    common = all_free[0]
    for free in all_free[1:]:
        common = intersect_intervals(common, free)

    # Convert back to HH:MM
    return [(to_time(s), to_time(e)) for s, e in common]


# Example usage
if __name__ == "__main__":
    # Create time slots for courses
    coursex = [
        TimeSlot("9:00", "10:00", "monday"),
        TimeSlot("9:00", "10:00", "tuesday"),
    ]
    coursey = [TimeSlot("2:00", "3:00", "monday"), TimeSlot("9:00", "10:00", "tuesday")]

    # Create people with schedules
    mo = Person("mo", [coursex, coursey])
    joe = Person("joe", [coursex, coursey])
    people_list = [mo, joe]

    # Print individual schedules
    # print("Individual Schedules:")
    # for person in people_list:
    #     print(person)

    # Find common free times for different days
    # days = ["monday", "tuesday", "wednesday", "thursday", "friday"]
    # print("\nCommon Free Times:")
    # for day in days:
    #     free_times = common_free_times(people_list, day)
    #     if free_times:
    #         print(f"{day.capitalize()}: {free_times}")
    #     else:
    #         print(f"{day.capitalize()}: No common free time")
    #
    # # Example: Add a new course to Mo's schedule
    # print("\nAdding new course to Mo's schedule...")
    # coursez = [TimeSlot("11:00", "12:00", "wednesday")]
    # mo.schedule.append(coursez)
    # mo.busy_time = mo._create_busy_time_dict()  # Update busy_time
    #
    # print("Updated schedules:")
    # for person in people_list:
    #     print(person)
    #
    # print("\nUpdated common free times for Wednesday:")
    # free_times = common_free_times(people_list, "wednesday")
    # if free_times:
    #     print(f"Wednesday: {free_times}")
    # else:
    #     print("Wednesday: No common free time")
