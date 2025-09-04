# Group Free Time Scheduler

## Future Usage
```python
# Print individual schedules
print("Individual Schedules:")
for person in people_list:
    print(person)

# Find common free times for different days
days = ["monday", "tuesday", "wednesday", "thursday", "friday"]
print("\nCommon Free Times:")
for day in days:
    free_times = common_free_times(people_list, day)
    if free_times:
        print(f"{day.capitalize()}: {free_times}")
    else:
        print(f"{day.capitalize()}: No common free time")

# Example: Add a new course to Mo's schedule
print("\nAdding new course to Mo's schedule...")
coursez = [TimeSlot("11:00", "12:00", "wednesday")]
mo.schedule.append(coursez)
mo.busy_time = mo._create_busy_time_dict()  # Update busy_time

print("Updated schedules:")
for person in people_list:
    print(person)

print("\nUpdated common free times for Wednesday:")
free_times = common_free_times(people_list, "wednesday")
if free_times:
    print(f"Wednesday: {free_times}")
else:
    print("Wednesday: No common free time")
```
