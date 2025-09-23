def to_minutes(time_str):
    """Convert time string (HH:MM) to minutes since midnight"""
    h, m = map(int, time_str.split(":"))
    return h * 60 + m


def to_time(minutes):
    """Convert minutes since midnight back to time string (HH:MM)"""
    return f"{minutes // 60:02d}:{minutes % 60:02d}"


def invert_busy(busy_times, day, start="09:00", end="20:00"):
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


def common_free_times(people_list, day, start="09:00", end="23:00"):
    """Find common free times for multiple Person objects on a given day"""
    all_free = []
    for person in people_list:
        free = invert_busy(list(person.busy_time.values()), day, start, end)
        all_free.append(free)

    if not all_free:
        return []

    # Intersect all free times
    common = all_free[0]
    for free in all_free[1:]:
        common = intersect_intervals(common, free)

    # Convert back to HH:MM
    return [(to_time(s), to_time(e)) for s, e in common]


def print_common_free_times(people_list, day):
    """Print common free times for a given day with participant names"""
    common = common_free_times(people_list, day)
    if common:
        print(f"{day}")
        print(" | ", end="")
        for start, end in common:
            print(f"{start} - {end}", end=" | ")
        print("\n")
    else:
        print(f"No common free time on {day}\n")
