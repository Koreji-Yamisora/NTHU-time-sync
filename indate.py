# Initialize empty dictionary to store data
class time_slot:
    def __init__(self, start_time, end_time, day):
        self.start_time = start_time
        self.end_time = end_time
        self.day = day

    def __str__(self):
        return f'("{self.start_time}", "{self.end_time}", "{self.day}")'


class people:
    def __init__(self, name, schedule=None):
        self.name = name
        self.schedule = schedule or []

    def __getitem__(self, key):
        if key == self.name:
            return self.schedule
        if hasattr(self, key):
            return getattr(self, key)

    def __setitem__(self, key, value):
        if key == self.name:
            self.schedule = value
        elif hasattr(self, key):
            setattr(self, key, value)
        else:
            raise KeyError(f"No such key: {key}")

    def __str__(self):
        flat = [slot for group in self.schedule for slot in group]
        schdu = ", ".join(map(str, flat))
        return f"{self.name}: ({schdu})"


coursex = [time_slot("9:00", "10:00", "monday"), time_slot("9:00", "10:00", "tuesday")]
coursey = [time_slot("2:00", "3:00", "monday"), time_slot("9:00", "10:00", "tuesday")]
names = (people("mo", (coursex, coursey)), people("joe", (coursex, coursey)))


# intergrate code below
def to_minutes(time_str):
    h, m = map(int, time_str.split(":"))
    return h * 60 + m


def to_time(minutes):
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


def common_free_times(schedules, day):
    """Find common free times for multiple Schedule objects on a given day"""
    all_free = []
    for sch in schedules:
        free = invert_busy(list(sch.busy_time.values()), day)
        all_free.append(free)

    if not all_free:
        return []

    # Intersect all free times
    common = all_free[0]
    for free in all_free[1:]:
        common = intersect_intervals(common, free)

    # Convert back to HH:MM
    return [(to_time(s), to_time(e)) for s, e in common]
