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
