import tkinter as tk
from tkinter import ttk, messagebox, simpledialog
from schedule import common_free_times
from models import TimeSlot
from storage import *


class TimePickerFrame(ttk.Frame):
    """A simple time picker widget using spinboxes for hours and minutes"""

    def __init__(self, parent, initial_time="09:00", **kwargs):
        super().__init__(parent, **kwargs)

        # Parse initial time
        try:
            hour, minute = initial_time.split(":")
            self.hour = int(hour)
            self.minute = int(minute)
        except:
            self.hour = 9
            self.minute = 0

        # Create spinboxes
        self.hour_var = tk.StringVar(value=f"{self.hour:02d}")
        self.minute_var = tk.StringVar(value=f"{self.minute:02d}")

        # Hour spinbox
        self.hour_spin = ttk.Spinbox(
            self,
            from_=0,
            to=23,
            width=3,
            textvariable=self.hour_var,
            format="%02.0f",
            wrap=True,
        )
        self.hour_spin.pack(side="left")

        # Separator
        ttk.Label(self, text=":").pack(side="left")

        # Minute spinbox
        self.minute_spin = ttk.Spinbox(
            self,
            from_=0,
            to=59,
            width=3,
            textvariable=self.minute_var,
            format="%02.0f",
            wrap=True,
            increment=10,  # 10-minute increments
        )
        self.minute_spin.pack(side="left")

    def get_time(self):
        """Get the selected time as HH:MM string"""
        try:
            hour = int(self.hour_var.get())
            minute = int(self.minute_var.get())
            return f"{hour:02d}:{minute:02d}"
        except:
            return "09:00"

    def set_time(self, time_str):
        """Set the time from HH:MM string"""
        try:
            hour, minute = time_str.split(":")
            self.hour_var.set(f"{int(hour):02d}")
            self.minute_var.set(f"{int(minute):02d}")
        except:
            self.hour_var.set("09")
            self.minute_var.set("00")


class ScheduleManagerGUI:
    def __init__(self, people_list, data_file="schedule_data.json"):
        self.people_list = people_list
        self.data_file = data_file
        self.courses = load_courses(data_file)  # Load courses from file
        self.days = [
            "Monday",
            "Tuesday",
            "Wednesday",
            "Thursday",
            "Friday",
            "Saturday",
            "Sunday",
        ]

        # Create main window
        self.root = tk.Tk()
        self.root.title("Schedule Manager")
        self.root.geometry("1400x900")
        self.root.minsize(1200, 700)

        # Create notebook for tabs
        self.notebook = ttk.Notebook(self.root)
        self.notebook.pack(fill="both", expand=True, padx=10, pady=10)

        # Create tabs
        self.create_schedule_tab()
        self.create_people_tab()
        self.create_courses_tab()
        self.create_common_times_tab()

    def refresh_people_checkboxes(self):
        """Refresh the people selection checkboxes"""
        # Clear existing checkboxes
        for widget in self.people_checkboxes_frame.winfo_children():
            widget.destroy()

        self.people_check_vars.clear()

        # Add checkboxes for each person
        for i, person in enumerate(self.people_list):
            var = tk.BooleanVar(value=True)  # Default to selected
            self.people_check_vars[person.name] = var

            checkbox = ttk.Checkbutton(
                self.people_checkboxes_frame,
                text=f"👤 {person.name}",
                variable=var,
                command=self.update_selection_summary,
            )
            checkbox.grid(row=i, column=0, sticky="w", padx=5, pady=2)

        self.update_selection_summary()

        # Show initial results if people exist

        if self.people_list and not getattr(self, "_common_init_done", False):
            self.root.after(200, self.show_all_common_times_selected)
            self._common_init_done = True

    def select_all_people(self):
        """Select all people checkboxes"""
        for var in self.people_check_vars.values():
            var.set(True)
        self.update_selection_summary()

    def deselect_all_people(self):
        """Deselect all people checkboxes"""
        for var in self.people_check_vars.values():
            var.set(False)
        self.update_selection_summary()

    def update_selection_summary(self):
        """Update the selection summary label"""
        selected_count = sum(1 for var in self.people_check_vars.values() if var.get())
        total_count = len(self.people_check_vars)

        if selected_count == 0:
            self.selection_summary_label.config(
                text="❌ No people selected", foreground="red"
            )
        elif selected_count == total_count:
            self.selection_summary_label.config(
                text=f"✅ All {total_count} people selected", foreground="green"
            )
        else:
            self.selection_summary_label.config(
                text=f"🔹 {selected_count} of {total_count} people selected",
                foreground="blue",
            )

    def get_selected_people(self):
        """Get list of selected people objects"""
        selected_people = []
        for person in self.people_list:
            if (
                person.name in self.people_check_vars
                and self.people_check_vars[person.name].get()
            ):
                selected_people.append(person)
        return selected_people

    def find_common_times_selected(self):
        """Find common free times for selected people and selected day"""
        selected_people = self.get_selected_people()
        day = self.common_day_var.get()

        if not selected_people:
            self.results_text.delete("1.0", tk.END)
            self.results_text.insert(
                "1.0",
                "❌ No people selected. Please select at least one person to find common times.",
            )
            return

        if len(selected_people) == 1:
            # Show individual schedule for single person
            person = selected_people[0]
            self.results_text.delete("1.0", tk.END)

            result_text = f"👤 Individual Schedule for {person.name} on {day}\n"
            result_text += "=" * (len(person.name) + len(day) + 30) + "\n\n"

            # Get person's schedule for the day
            day_slots = []
            for course_slots in person.schedule:
                for slot in course_slots:
                    if slot.day == day:
                        day_slots.append((slot.start_time, slot.end_time))

            if day_slots:
                day_slots.sort()
                result_text += f"📚 Busy times on {day}:\n"
                for start, end in day_slots:
                    result_text += f"   🕐 {start} - {end}\n"

                # Show free times (simplified logic)
                result_text += f"\n🆓 Free times on {day}:\n"
                result_text += "   (Times not listed above are generally free)\n"
            else:
                result_text += f"🆓 {person.name} is completely free on {day}!\n"

            self.results_text.insert("1.0", result_text)
            return

        # Multiple people - find common times
        common_times = common_free_times(selected_people, day)

        self.results_text.delete("1.0", tk.END)

        result_text = f"🔍 Common free times for {day}\n"
        result_text += "=" * (len(day) + 25) + "\n\n"

        result_text += f"👥 Selected people ({len(selected_people)}):\n"
        for person in selected_people:
            result_text += f"  • {person.name}\n"
        result_text += "\n"

        if common_times:
            result_text += (
                f"✅ Found {len(common_times)} common free time period(s):\n\n"
            )
            total_minutes = 0
            for i, (start, end) in enumerate(common_times, 1):
                # Calculate duration
                start_parts = start.split(":")
                end_parts = end.split(":")
                start_minutes = int(start_parts[0]) * 60 + int(start_parts[1])
                end_minutes = int(end_parts[0]) * 60 + int(end_parts[1])
                duration = end_minutes - start_minutes
                total_minutes += duration

                result_text += f"  {i}. ⏰ {start} - {end} ({duration} minutes)\n"

            result_text += f"\n📊 Total common free time: {total_minutes} minutes ({total_minutes / 60:.1f} hours)"
        else:
            result_text += "❌ No common free times found for this day.\n"
            result_text += "\n💡 This means the selected people have conflicting schedules on this day.\n"
            result_text += "Try selecting fewer people or checking other days."

        self.results_text.insert("1.0", result_text)

    def show_all_common_times_selected(self):
        """Show common free times for all days with selected people"""
        selected_people = self.get_selected_people()

        if not selected_people:
            self.results_text.delete("1.0", tk.END)
            self.results_text.insert(
                "1.0",
                "❌ No people selected. Please select at least one person to find common times.",
            )
            return

        self.results_text.delete("1.0", tk.END)

        result_text = "📅 Common Free Times - Weekly Summary\n"
        result_text += "=" * 50 + "\n"
        result_text += (
            f"👥 Analyzing schedules for {len(selected_people)} selected people:\n"
        )
        for person in selected_people:
            result_text += f"  • {person.name}\n"
        result_text += "=" * 50 + "\n\n"

        total_common_slots = 0
        total_common_minutes = 0

        for day in self.days:
            if len(selected_people) == 1:
                # For single person, show their free/busy status
                person = selected_people[0]
                day_slots = []
                for course_slots in person.schedule:
                    for slot in course_slots:
                        if slot.day == day:
                            day_slots.append((slot.start_time, slot.end_time))

                result_text += f"📅 {day} - {person.name}:\n"
                if day_slots:
                    result_text += f"   📚 Has {len(day_slots)} scheduled time(s)\n"
                else:
                    result_text += "   🆓 Completely free\n"
            else:
                # Multiple people - find common times
                common_times = common_free_times(selected_people, day)
                result_text += f"📅 {day}:\n"

                if common_times:
                    total_common_slots += len(common_times)
                    day_minutes = 0
                    for start, end in common_times:
                        # Calculate duration
                        start_parts = start.split(":")
                        end_parts = end.split(":")
                        start_minutes = int(start_parts[0]) * 60 + int(start_parts[1])
                        end_minutes = int(end_parts[0]) * 60 + int(end_parts[1])
                        duration = end_minutes - start_minutes
                        day_minutes += duration
                        result_text += f"   ✅ {start} - {end} ({duration}min)\n"
                    total_common_minutes += day_minutes
                else:
                    result_text += "   ❌ No common free times\n"

            result_text += "\n"

        # Add summary
        if len(selected_people) > 1:
            result_text += "SUMMARY:\n"
            result_text += f"   • Total common time slots: {total_common_slots}\n"
            result_text += f"   • Total common time: {total_common_minutes} minutes ({total_common_minutes / 60:.1f} hours)\n"
            result_text += f"   • Days with common times: {sum(1 for day in self.days if common_free_times(selected_people, day))}\n"
            result_text += f"   • People analyzed: {len(selected_people)}\n"

            if total_common_slots == 0:
                result_text += "\nTips for finding common times:\n"
                result_text += "   • Try selecting fewer people\n"
                result_text += (
                    "   • Check if people have too many overlapping courses\n"
                )
                result_text += (
                    "   • Consider removing some courses or adjusting schedules\n"
                )
                result_text += "   • Try looking at weekend days (Saturday/Sunday)\n"

        self.results_text.insert("1.0", result_text)

        # Initialize displays

        self.refresh_schedule_view()
        self.refresh_people_list()
        self.refresh_courses_list()

    def refresh_all(self):
        """Refresh all displays"""
        self.refresh_schedule_view()
        self.refresh_people_list()
        self.refresh_courses_list()
        self.refresh_people_checkboxes()  # ADD this line

    def create_schedule_tab(self):
        """Create the main schedule viewing tab"""
        schedule_frame = ttk.Frame(self.notebook)
        self.notebook.add(schedule_frame, text="Schedules")

        # Create main container with scrolling
        main_container = ttk.Frame(schedule_frame)
        main_container.pack(fill="both", expand=True)

        # Create treeview for schedules
        columns = ["Person"] + self.days
        self.schedule_tree = ttk.Treeview(
            main_container, columns=columns, show="headings", height=15
        )

        # Configure columns
        self.schedule_tree.heading("Person", text="Person")
        self.schedule_tree.column("Person", width=120, minwidth=100)

        for day in self.days:
            self.schedule_tree.heading(day, text=day)
            self.schedule_tree.column(day, width=140, minwidth=120)

        # Add scrollbars
        v_scrollbar = ttk.Scrollbar(
            main_container, orient="vertical", command=self.schedule_tree.yview
        )
        h_scrollbar = ttk.Scrollbar(
            main_container, orient="horizontal", command=self.schedule_tree.xview
        )
        self.schedule_tree.configure(
            yscrollcommand=v_scrollbar.set, xscrollcommand=h_scrollbar.set
        )

        # Pack treeview and scrollbars
        self.schedule_tree.grid(row=0, column=0, sticky="nsew")
        v_scrollbar.grid(row=0, column=1, sticky="ns")
        h_scrollbar.grid(row=1, column=0, sticky="ew")

        # Configure grid weights
        main_container.grid_rowconfigure(0, weight=1)
        main_container.grid_columnconfigure(0, weight=1)

        # Add control buttons
        button_frame = ttk.Frame(schedule_frame)
        button_frame.pack(fill="x", pady=10)

        ttk.Button(
            button_frame, text="Refresh", command=self.refresh_schedule_view
        ).pack(side="left", padx=5)
        ttk.Button(button_frame, text="Save All Data", command=self.save_all_data).pack(
            side="left", padx=5
        )

        # Legend
        legend_frame = ttk.LabelFrame(button_frame, text="Legend", padding="5")
        legend_frame.pack(side="right", padx=5)
        ttk.Label(legend_frame, text="Course schedules | Free time").pack()

    def create_people_tab(self):
        """Create the people management tab"""
        people_frame = ttk.Frame(self.notebook)
        self.notebook.add(people_frame, text="Manage People")

        # Left side - People list
        left_frame = ttk.LabelFrame(people_frame, text="People", padding="10")
        left_frame.grid(row=0, column=0, sticky="nsew", padx=5, pady=5)

        # People listbox with scrollbar
        list_container = ttk.Frame(left_frame)
        list_container.pack(fill="both", expand=True)

        self.people_listbox = tk.Listbox(list_container, height=12, font=("Arial", 16))
        people_scroll = ttk.Scrollbar(
            list_container, orient="vertical", command=self.people_listbox.yview
        )
        self.people_listbox.configure(yscrollcommand=people_scroll.set)

        self.people_listbox.pack(side="left", fill="both", expand=True)
        people_scroll.pack(side="right", fill="y")

        # People management buttons
        people_btn_frame = ttk.Frame(left_frame)
        people_btn_frame.pack(fill="x", pady=10)

        ttk.Button(
            people_btn_frame, text="Add Person", command=self.add_person_dialog
        ).grid(row=0, column=0, padx=2, pady=2, sticky="ew")
        ttk.Button(
            people_btn_frame, text="Edit Name", command=self.edit_person_dialog
        ).grid(row=0, column=1, padx=2, pady=2, sticky="ew")
        ttk.Button(people_btn_frame, text="Delete", command=self.delete_person).grid(
            row=0, column=2, padx=2, pady=2, sticky="ew"
        )

        people_btn_frame.grid_columnconfigure(0, weight=1)
        people_btn_frame.grid_columnconfigure(1, weight=1)
        people_btn_frame.grid_columnconfigure(2, weight=1)

        # Right side - Schedule editing
        right_frame = ttk.LabelFrame(
            people_frame, text="Schedule Management", padding="10"
        )
        right_frame.grid(row=0, column=1, sticky="nsew", padx=5, pady=5)

        # Course assignment section
        course_section = ttk.LabelFrame(
            right_frame, text="Course Assignment", padding="10"
        )
        course_section.pack(fill="x", pady=5)

        course_btn_frame = ttk.Frame(course_section)
        course_btn_frame.pack(fill="x")

        ttk.Button(
            course_btn_frame, text="Assign Course", command=self.assign_course_dialog
        ).pack(side="left", padx=5)
        ttk.Button(
            course_btn_frame, text="Remove Course", command=self.remove_course_dialog
        ).pack(side="left", padx=5)

        # Individual time slot section
        slot_section = ttk.LabelFrame(
            right_frame, text="Add Individual Time Slot", padding="10"
        )
        slot_section.pack(fill="x", pady=5)

        # Time slot entry grid
        ttk.Label(slot_section, text="Day:").grid(row=0, column=0, sticky="w", pady=2)
        self.day_var = tk.StringVar(value="Monday")
        day_combo = ttk.Combobox(
            slot_section,
            textvariable=self.day_var,
            values=self.days,
            state="readonly",
            width=12,
        )
        day_combo.grid(row=0, column=1, sticky="w", padx=5, pady=2)

        ttk.Label(slot_section, text="Start:").grid(
            row=0, column=2, sticky="w", padx=(20, 5), pady=2
        )
        self.start_time_picker = TimePickerFrame(slot_section, initial_time="09:00")
        self.start_time_picker.grid(row=0, column=3, sticky="w", padx=5, pady=2)

        ttk.Label(slot_section, text="End:").grid(
            row=0, column=4, sticky="w", padx=(10, 5), pady=2
        )
        self.end_time_picker = TimePickerFrame(slot_section, initial_time="10:00")
        self.end_time_picker.grid(row=0, column=5, sticky="w", padx=5, pady=2)

        ttk.Button(slot_section, text="Add Slot", command=self.add_time_slot).grid(
            row=0, column=6, padx=10, pady=2
        )

        # Current schedule display
        schedule_section = ttk.LabelFrame(
            right_frame, text="Current Schedule", padding="10"
        )
        schedule_section.pack(fill="both", expand=True, pady=5)

        # Create text widget with scrollbar
        text_frame = ttk.Frame(schedule_section)
        text_frame.pack(fill="both", expand=True)

        self.schedule_text = tk.Text(
            text_frame, height=15, width=50, font=("Consolas", 16), wrap="word"
        )
        schedule_scroll = ttk.Scrollbar(
            text_frame, orient="vertical", command=self.schedule_text.yview
        )
        self.schedule_text.configure(yscrollcommand=schedule_scroll.set)

        self.schedule_text.pack(side="left", fill="both", expand=True)
        schedule_scroll.pack(side="right", fill="y")

        # Configure grid weights
        people_frame.grid_rowconfigure(0, weight=1)
        people_frame.grid_columnconfigure(0, weight=1)
        people_frame.grid_columnconfigure(1, weight=2)

        # Bind selection event
        self.people_listbox.bind("<<ListboxSelect>>", self.on_person_select)

    def create_courses_tab(self):
        """Create the courses management tab"""
        courses_frame = ttk.Frame(self.notebook)
        self.notebook.add(courses_frame, text="Manage Courses")

        # Left side - Course list
        left_frame = ttk.LabelFrame(courses_frame, text="Courses", padding="10")
        left_frame.grid(row=0, column=0, sticky="nsew", padx=5, pady=5)

        # Course listbox with scrollbar
        list_container = ttk.Frame(left_frame)
        list_container.pack(fill="both", expand=True)

        self.courses_listbox = tk.Listbox(list_container, height=12, font=("Arial", 16))
        courses_scroll = ttk.Scrollbar(
            list_container, orient="vertical", command=self.courses_listbox.yview
        )
        self.courses_listbox.configure(yscrollcommand=courses_scroll.set)

        self.courses_listbox.pack(side="left", fill="both", expand=True)
        courses_scroll.pack(side="right", fill="y")

        # Course management buttons
        course_btn_frame = ttk.Frame(left_frame)
        course_btn_frame.pack(fill="x", pady=10)

        ttk.Button(
            course_btn_frame, text="Add Course", command=self.add_course_dialog
        ).grid(row=0, column=0, padx=2, pady=2, sticky="ew")
        ttk.Button(
            course_btn_frame, text="Edit Name", command=self.edit_course_dialog
        ).grid(row=0, column=1, padx=2, pady=2, sticky="ew")
        ttk.Button(course_btn_frame, text="Delete", command=self.delete_course).grid(
            row=0, column=2, padx=2, pady=2, sticky="ew"
        )

        course_btn_frame.grid_columnconfigure(0, weight=1)
        course_btn_frame.grid_columnconfigure(1, weight=1)
        course_btn_frame.grid_columnconfigure(2, weight=1)

        # Right side - Course details and editing
        right_frame = ttk.LabelFrame(courses_frame, text="Course Details", padding="10")
        right_frame.grid(row=0, column=1, sticky="nsew", padx=5, pady=5)

        # Course name display
        self.course_name_label = ttk.Label(
            right_frame,
            text="Select a course to view details",
            font=("Arial", 16, "bold"),
            foreground="#3287a8",
        )
        self.course_name_label.pack(pady=10)

        # Time slot management section
        slot_mgmt_frame = ttk.LabelFrame(
            right_frame, text="Add Time Slot to Course", padding="10"
        )
        slot_mgmt_frame.pack(fill="x", pady=5)

        # Time slot entry
        entry_frame = ttk.Frame(slot_mgmt_frame)
        entry_frame.pack(fill="x")

        ttk.Label(entry_frame, text="Day:").grid(row=0, column=0, sticky="w", pady=2)
        self.course_day_var = tk.StringVar(value="Monday")
        course_day_combo = ttk.Combobox(
            entry_frame,
            textvariable=self.course_day_var,
            values=self.days,
            state="readonly",
            width=10,
        )
        course_day_combo.grid(row=0, column=1, sticky="w", padx=5, pady=2)

        ttk.Label(entry_frame, text="Start:").grid(
            row=0, column=2, sticky="w", padx=(20, 5), pady=2
        )
        self.course_start_picker = TimePickerFrame(entry_frame, initial_time="09:00")
        self.course_start_picker.grid(row=0, column=3, sticky="w", padx=5, pady=2)

        ttk.Label(entry_frame, text="End:").grid(
            row=0, column=4, sticky="w", padx=(10, 5), pady=2
        )
        self.course_end_picker = TimePickerFrame(entry_frame, initial_time="10:00")
        self.course_end_picker.grid(row=0, column=5, sticky="w", padx=5, pady=2)

        # Buttons for course time slot management
        btn_frame = ttk.Frame(slot_mgmt_frame)
        btn_frame.pack(fill="x", pady=5)

        ttk.Button(btn_frame, text="Add Slot", command=self.add_course_time_slot).pack(
            side="left", padx=5
        )
        ttk.Button(
            btn_frame, text="Remove Selected", command=self.remove_course_time_slot
        ).pack(side="left", padx=5)

        # Course schedule display
        schedule_frame = ttk.LabelFrame(
            right_frame, text="Course Schedule", padding="10"
        )
        schedule_frame.pack(fill="both", expand=True, pady=5)

        # Treeview for course time slots
        tree_container = ttk.Frame(schedule_frame)
        tree_container.pack(fill="both", expand=True)

        self.course_slots_tree = ttk.Treeview(
            tree_container, columns=("Day", "Start", "End"), show="headings", height=6
        )
        self.course_slots_tree.heading("Day", text="Day")
        self.course_slots_tree.heading("Start", text="Start Time")
        self.course_slots_tree.heading("End", text="End Time")
        self.course_slots_tree.column("Day", width=80, minwidth=70)
        self.course_slots_tree.column("Start", width=80, minwidth=70)
        self.course_slots_tree.column("End", width=80, minwidth=70)

        tree_scroll = ttk.Scrollbar(
            tree_container, orient="vertical", command=self.course_slots_tree.yview
        )
        self.course_slots_tree.configure(yscrollcommand=tree_scroll.set)

        self.course_slots_tree.pack(side="left", fill="both", expand=True)
        tree_scroll.pack(side="right", fill="y")

        # Enrolled students display
        enrolled_frame = ttk.LabelFrame(
            right_frame, text="Enrolled Students", padding="10"
        )
        enrolled_frame.pack(fill="both", expand=True, pady=5)

        enrolled_container = ttk.Frame(enrolled_frame)
        enrolled_container.pack(fill="both", expand=True)

        self.enrolled_text = tk.Text(
            enrolled_container, height=6, width=40, font=("Arial", 16), wrap="word"
        )
        enrolled_scroll = ttk.Scrollbar(
            enrolled_container, orient="vertical", command=self.enrolled_text.yview
        )
        self.enrolled_text.configure(yscrollcommand=enrolled_scroll.set)

        self.enrolled_text.pack(side="left", fill="both", expand=True)
        enrolled_scroll.pack(side="right", fill="y")

        # Configure grid weights
        courses_frame.grid_rowconfigure(0, weight=1)
        courses_frame.grid_columnconfigure(0, weight=1)
        courses_frame.grid_columnconfigure(1, weight=2)

        # Bind selection events
        self.courses_listbox.bind("<<ListboxSelect>>", self.on_course_select)

    def create_common_times_tab(self):
        """Create the common free times tab with people selection"""
        common_frame = ttk.Frame(self.notebook)
        self.notebook.add(common_frame, text="Common Times")

        # Main container with left and right panels
        main_container = ttk.Frame(common_frame)
        main_container.pack(fill="both", expand=True, padx=10, pady=10)

        # Left panel - People selection
        left_panel = ttk.LabelFrame(main_container, text="Select People", padding="10")
        left_panel.grid(row=0, column=0, sticky="nsew", padx=(0, 5))

        # Select All / Deselect All buttons
        select_buttons_frame = ttk.Frame(left_panel)
        select_buttons_frame.pack(fill="x", pady=(0, 10))

        ttk.Button(
            select_buttons_frame, text="Select All", command=self.select_all_people
        ).pack(side="left", padx=(0, 5))

        ttk.Button(
            select_buttons_frame, text="Deselect All", command=self.deselect_all_people
        ).pack(side="left", padx=5)

        # People selection with checkboxes
        self.people_selection_frame = ttk.Frame(left_panel)
        self.people_selection_frame.pack(fill="both", expand=True)

        # Scrollable frame for people checkboxes
        people_canvas = tk.Canvas(self.people_selection_frame, height=200)
        people_scrollbar = ttk.Scrollbar(
            self.people_selection_frame, orient="vertical", command=people_canvas.yview
        )
        self.people_checkboxes_frame = ttk.Frame(people_canvas)

        people_canvas.configure(yscrollcommand=people_scrollbar.set)
        people_canvas.create_window(
            (0, 0), window=self.people_checkboxes_frame, anchor="nw"
        )

        people_canvas.pack(side="left", fill="both", expand=True)
        people_scrollbar.pack(side="right", fill="y")

        # Update scroll region when frame changes
        def configure_scroll_region(event):
            people_canvas.configure(scrollregion=people_canvas.bbox("all"))

        self.people_checkboxes_frame.bind("<Configure>", configure_scroll_region)

        # Store checkbox variables
        self.people_check_vars = {}

        # Selection summary
        self.selection_summary_label = ttk.Label(
            left_panel, text="No people selected", font=("Arial", 9), foreground="gray"
        )
        self.selection_summary_label.pack(pady=(10, 0))

        # Right panel - Controls and Results
        right_panel = ttk.Frame(main_container)
        right_panel.grid(row=0, column=1, sticky="nsew", padx=(5, 0))

        # Controls frame
        controls_frame = ttk.LabelFrame(
            right_panel, text="Find Common Free Times", padding="15"
        )
        controls_frame.pack(fill="x", pady=(0, 10))

        # Control widgets
        control_row1 = ttk.Frame(controls_frame)
        control_row1.pack(fill="x", pady=(0, 10))

        ttk.Label(control_row1, text="Select Day:", font=("Arial", 10)).pack(
            side="left", padx=(0, 5)
        )
        self.common_day_var = tk.StringVar(value="Monday")
        day_combo = ttk.Combobox(
            control_row1,
            textvariable=self.common_day_var,
            values=self.days,
            state="readonly",
            width=12,
        )
        day_combo.pack(side="left", padx=5)

        # Action buttons
        control_row2 = ttk.Frame(controls_frame)
        control_row2.pack(fill="x")

        ttk.Button(
            control_row2,
            text="Find for Selected Day",
            command=self.find_common_times_selected,
        ).pack(side="left", padx=(0, 5))

        ttk.Button(
            control_row2,
            text="Show All Days",
            command=self.show_all_common_times_selected,
        ).pack(side="left", padx=5)

        ttk.Button(
            control_row2, text="Refresh", command=self.refresh_people_checkboxes
        ).pack(side="left", padx=5)

        # Results frame
        results_frame = ttk.LabelFrame(
            right_panel, text="Common Free Time Results", padding="10"
        )
        results_frame.pack(fill="both", expand=True)

        # Text widget for results
        text_container = ttk.Frame(results_frame)
        text_container.pack(fill="both", expand=True)

        self.results_text = tk.Text(text_container, wrap="word", font=("Consolas", 10))
        results_scroll = ttk.Scrollbar(
            text_container, orient="vertical", command=self.results_text.yview
        )
        self.results_text.configure(yscrollcommand=results_scroll.set)

        self.results_text.pack(side="left", fill="both", expand=True)
        results_scroll.pack(side="right", fill="y")

        # Configure grid weights
        main_container.grid_rowconfigure(0, weight=1)
        main_container.grid_columnconfigure(0, weight=1)
        main_container.grid_columnconfigure(1, weight=2)

        # Initialize people checkboxes
        self.root.after(100, self.refresh_people_checkboxes)

    def refresh_schedule_view(self):
        """Refresh the main schedule view"""
        # Clear existing items
        for item in self.schedule_tree.get_children():
            self.schedule_tree.delete(item)

        if not self.people_list:
            # Add a message if no people
            self.schedule_tree.insert(
                "", "end", values=["No people added yet"] + [""] * len(self.days)
            )
            return

        # Add each person's schedule
        for person in self.people_list:
            row_data = [person.name]

            for day in self.days:
                day_schedule = []
                for course_slots in person.schedule:
                    for slot in course_slots:
                        if slot.day == day:
                            day_schedule.append(f"{slot.start_time}-{slot.end_time}")

                if day_schedule:
                    row_data.append(", ".join(sorted(day_schedule)))
                else:
                    row_data.append("Free")

            self.schedule_tree.insert("", "end", values=row_data)

    def refresh_people_list(self):
        """Refresh the people listbox"""
        current_selection = None
        if self.people_listbox.curselection():
            current_selection = self.people_listbox.get(
                self.people_listbox.curselection()[0]
            )

        self.people_listbox.delete(0, tk.END)
        for person in self.people_list:
            self.people_listbox.insert(tk.END, person.name)

        # Restore selection if possible
        if current_selection:
            for i in range(self.people_listbox.size()):
                if self.people_listbox.get(i) == current_selection:
                    self.people_listbox.selection_set(i)
                    self.show_person_schedule(current_selection)
                    break

    def refresh_courses_list(self):
        """Refresh the courses listbox"""
        current_selection = None
        if self.courses_listbox.curselection():
            current_selection = self.courses_listbox.get(
                self.courses_listbox.curselection()[0]
            )

        self.courses_listbox.delete(0, tk.END)
        for course_name in sorted(self.courses.keys()):
            self.courses_listbox.insert(tk.END, course_name)

        # Restore selection if possible
        if current_selection and current_selection in self.courses:
            for i in range(self.courses_listbox.size()):
                if self.courses_listbox.get(i) == current_selection:
                    self.courses_listbox.selection_set(i)
                    self.show_course_details(current_selection)
                    break

    def on_person_select(self, event):
        """Handle person selection in listbox"""
        selection = self.people_listbox.curselection()
        if selection:
            person_name = self.people_listbox.get(selection[0])
            self.show_person_schedule(person_name)

    def on_course_select(self, event):
        """Handle course selection in listbox"""
        selection = self.courses_listbox.curselection()
        if selection:
            course_name = self.courses_listbox.get(selection[0])
            self.show_course_details(course_name)

    def show_person_schedule(self, person_name):
        """Show selected person's schedule in text widget"""
        self.schedule_text.delete("1.0", tk.END)

        person = next((p for p in self.people_list if p.name == person_name), None)
        if not person:
            return

        schedule_text = f"Schedule for {person_name}\n"
        schedule_text += "=" * (len(person_name) + 20) + "\n\n"

        # Group schedule by day
        schedule_by_day = {}
        course_names = {}  # Map course slots to course names

        # Find course names for each set of slots
        for course_name, course_slots in self.courses.items():
            for person_course in person.schedule:
                if person_course == course_slots:
                    course_names[id(person_course)] = course_name

        # Organize by day
        for course_slots in person.schedule:
            course_name = course_names.get(id(course_slots), "Individual Slots")
            for slot in course_slots:
                if slot.day not in schedule_by_day:
                    schedule_by_day[slot.day] = []
                schedule_by_day[slot.day].append(
                    {
                        "time": f"{slot.start_time} - {slot.end_time}",
                        "course": course_name,
                    }
                )

        # Display schedule
        for day in self.days:
            schedule_text += f"{day}:\n"
            if day in schedule_by_day:
                # Sort by start time
                day_slots = sorted(schedule_by_day[day], key=lambda x: x["time"])
                for slot_info in day_slots:
                    schedule_text += f"   {slot_info['time']} - {slot_info['course']}\n"
            else:
                schedule_text += "   Free\n"
            schedule_text += "\n"

        self.schedule_text.insert("1.0", schedule_text)

    def show_course_details(self, course_name):
        """Show selected course's details"""
        if course_name not in self.courses:
            return

        self.course_name_label.config(text=f"Course: {course_name}")

        # Clear and populate course slots tree
        for item in self.course_slots_tree.get_children():
            self.course_slots_tree.delete(item)

        course_slots = self.courses[course_name]
        for slot in sorted(
            course_slots, key=lambda x: (self.days.index(x.day), x.start_time)
        ):
            self.course_slots_tree.insert(
                "", "end", values=(slot.day, slot.start_time, slot.end_time)
            )

        # Show enrolled students
        self.enrolled_text.delete("1.0", tk.END)
        try:
            enrolled_people = get_people_in_course(
                self.people_list, self.courses, course_name
            )
            if enrolled_people:
                enrolled_text = f"Students enrolled in {course_name}:\n\n"
                for i, person_name in enumerate(enrolled_people, 1):
                    enrolled_text += f"{i}. {person_name}\n"
                enrolled_text += f"\nTotal: {len(enrolled_people)} students"
            else:
                enrolled_text = f"No students currently enrolled in {course_name}"

            self.enrolled_text.insert("1.0", enrolled_text)
        except Exception as e:
            self.enrolled_text.insert("1.0", f"Error loading enrollment: {str(e)}")

    # Person Management Methods
    def add_person_dialog(self):
        """Show dialog to add new person"""
        name = simpledialog.askstring("Add Person", "Enter person's name:")
        if name and name.strip():
            try:
                add_person(self.people_list, name.strip())
                self.refresh_all()
                self.save_all_data()
                messagebox.showinfo("Success", f"Added person: {name}")
            except ValueError as e:
                messagebox.showerror("Error", str(e))

    def edit_person_dialog(self):
        """Show dialog to edit person's name"""
        selection = self.people_listbox.curselection()
        if not selection:
            messagebox.showwarning("No Selection", "Please select a person to edit.")
            return

        old_name = self.people_listbox.get(selection[0])
        new_name = simpledialog.askstring(
            "Edit Person", f"Enter new name for {old_name}:", initialvalue=old_name
        )

        if new_name and new_name.strip() and new_name != old_name:
            person = next((p for p in self.people_list if p.name == old_name), None)
            if person:
                person.name = new_name.strip()
                self.refresh_all()
                self.save_all_data()
                messagebox.showinfo("Success", f"Renamed {old_name} to {new_name}")

    def delete_person(self):
        """Delete selected person"""
        selection = self.people_listbox.curselection()
        if not selection:
            messagebox.showwarning("No Selection", "Please select a person to delete.")
            return

        person_name = self.people_listbox.get(selection[0])

        if messagebox.askyesno(
            "Confirm Delete", f"Are you sure you want to delete {person_name}?"
        ):
            try:
                remove_person(self.people_list, person_name)
                self.refresh_all()
                self.schedule_text.delete("1.0", tk.END)
                self.save_all_data()
                messagebox.showinfo("Success", f"Deleted person: {person_name}")
            except ValueError as e:
                messagebox.showerror("Error", str(e))

    def add_time_slot(self):
        """Add individual time slot to selected person"""
        selection = self.people_listbox.curselection()
        if not selection:
            messagebox.showwarning("No Selection", "Please select a person first.")
            return

        person_name = self.people_listbox.get(selection[0])
        day = self.day_var.get()
        start_time = self.start_time_picker.get_time()
        end_time = self.end_time_picker.get_time()

        try:
            if not all([day, start_time, end_time]):
                raise ValueError("All fields must be filled")

            # Validate time format (basic check)
            if ":" not in start_time or ":" not in end_time:
                raise ValueError("Time must be in HH:MM format")

            # Create new time slot
            new_slot = TimeSlot(start_time, end_time, day)

            # Find the person and add the slot
            person = next((p for p in self.people_list if p.name == person_name), None)
            if person:
                # Add as a single-slot course
                person.schedule.append([new_slot])
                person.busy_time = person._create_busy_time_dict()

                self.show_person_schedule(person_name)
                self.refresh_schedule_view()
                self.save_all_data()
                messagebox.showinfo(
                    "Success", f"Added time slot: {day} {start_time}-{end_time}"
                )

        except Exception as e:
            messagebox.showerror("Error", f"Failed to add time slot: {str(e)}")

    def assign_course_dialog(self):
        """Show dialog to assign course to selected person"""
        selection = self.people_listbox.curselection()
        if not selection:
            messagebox.showwarning("No Selection", "Please select a person first.")
            return

        person_name = self.people_listbox.get(selection[0])

        if not self.courses:
            messagebox.showwarning(
                "No Courses", "No courses available. Please create courses first."
            )
            return

        # Create course selection dialog
        dialog = tk.Toplevel(self.root)
        dialog.title("Assign Course")
        dialog.geometry("400x600")
        dialog.transient(self.root)
        dialog.grab_set()
        dialog.resizable(True, True)

        # Center the dialog
        dialog.geometry(
            "+%d+%d" % (self.root.winfo_rootx() + 50, self.root.winfo_rooty() + 50)
        )

        main_frame = ttk.Frame(dialog, padding="20")
        main_frame.pack(fill="both", expand=True)

        ttk.Label(
            main_frame,
            text=f"Assign course to {person_name}:",
            font=("Arial", 16, "bold"),
        ).pack(pady=10)

        # Course selection
        list_frame = ttk.LabelFrame(main_frame, text="Available Courses", padding="10")
        list_frame.pack(fill="both", expand=True, pady=10)

        course_listbox = tk.Listbox(list_frame, font=("Arial", 16))
        course_scroll = ttk.Scrollbar(
            list_frame, orient="vertical", command=course_listbox.yview
        )
        course_listbox.configure(yscrollcommand=course_scroll.set)

        course_listbox.pack(side="left", fill="both", expand=True)
        course_scroll.pack(side="right", fill="y")

        # Populate with available courses
        available_courses = []
        person = next((p for p in self.people_list if p.name == person_name), None)
        if person:
            enrolled_course_ids = [id(course_slots) for course_slots in person.schedule]
            for course_name, course_slots in self.courses.items():
                if id(course_slots) not in enrolled_course_ids:
                    available_courses.append(course_name)
                    course_listbox.insert(tk.END, course_name)

        if not available_courses:
            course_listbox.insert(
                tk.END, "No available courses (already enrolled in all)"
            )
            course_listbox.config(state="disabled")

        # Course details display
        details_frame = ttk.LabelFrame(main_frame, text="Course Details", padding="10")
        details_frame.pack(fill="both", expand=False, pady=10)

        details_text = tk.Text(details_frame, height=8, wrap="word", font=("Arial", 16))
        details_scroll = ttk.Scrollbar(
            details_frame, orient="vertical", command=details_text.yview
        )
        details_text.configure(yscrollcommand=details_scroll.set)

        details_text.pack(side="left", fill="both", expand=True)
        details_scroll.pack(side="right", fill="y")

        def show_course_details_preview(event):
            selection = course_listbox.curselection()
            if selection and available_courses:
                course_name = course_listbox.get(selection[0])
                if course_name in self.courses:
                    course_slots = self.courses[course_name]
                    details = f"Course: {course_name}\n\n"
                    details += "Schedule:\n"
                    for slot in sorted(
                        course_slots,
                        key=lambda x: (self.days.index(x.day), x.start_time),
                    ):
                        details += (
                            f"  {slot.day}: {slot.start_time} - {slot.end_time}\n"
                        )

                    details_text.delete("1.0", tk.END)
                    details_text.insert("1.0", details)

        course_listbox.bind("<<ListboxSelect>>", show_course_details_preview)

        # Buttons
        button_frame = ttk.Frame(main_frame)
        button_frame.pack(fill="x", pady=10)

        def assign_selected():
            selection = course_listbox.curselection()
            if selection and available_courses:
                course_name = course_listbox.get(selection[0])
                if course_name in self.courses:
                    try:
                        assign_course_to_person(
                            self.people_list, person_name, self.courses, course_name
                        )
                        self.show_person_schedule(person_name)
                        self.refresh_schedule_view()
                        self.save_all_data()
                        messagebox.showinfo(
                            "Success", f"Assigned {course_name} to {person_name}"
                        )
                        # dialog.destroy()
                        course_listbox.delete(selection[0])
                    except ValueError as e:
                        messagebox.showerror("Error", str(e))
            else:
                messagebox.showwarning(
                    "No Selection", "Please select a course to assign."
                )

        ttk.Button(button_frame, text="Assign Course", command=assign_selected).pack(
            side="left", padx=5
        )
        ttk.Button(button_frame, text="Cancel", command=dialog.destroy).pack(
            side="right", padx=5
        )

    def remove_course_dialog(self):
        """Show dialog to remove course from selected person"""
        selection = self.people_listbox.curselection()
        if not selection:
            messagebox.showwarning("No Selection", "Please select a person first.")
            return

        person_name = self.people_listbox.get(selection[0])
        person = next((p for p in self.people_list if p.name == person_name), None)

        if not person or not person.schedule:
            messagebox.showwarning(
                "No Courses", f"{person_name} has no courses assigned."
            )
            return

        # Create course removal dialog
        dialog = tk.Toplevel(self.root)
        dialog.title("Remove Course")
        dialog.geometry("400x600")
        dialog.transient(self.root)
        dialog.grab_set()

        # Center the dialog
        dialog.geometry(
            "+%d+%d" % (self.root.winfo_rootx() + 50, self.root.winfo_rooty() + 50)
        )

        main_frame = ttk.Frame(dialog, padding="20")
        main_frame.pack(fill="both", expand=True)

        ttk.Label(
            main_frame,
            text=f"Remove course from {person_name}:",
            font=("Arial", 16, "bold"),
        ).pack(pady=10)

        list_frame = ttk.LabelFrame(main_frame, text="Enrolled Courses", padding="10")
        list_frame.pack(fill="both", expand=True, pady=10)

        course_listbox = tk.Listbox(list_frame, font=("Arial", 16))
        course_scroll = ttk.Scrollbar(
            list_frame, orient="vertical", command=course_listbox.yview
        )
        course_listbox.configure(yscrollcommand=course_scroll.set)

        course_listbox.pack(side="left", fill="both", expand=True)
        course_scroll.pack(side="right", fill="y")

        # Find courses this person is enrolled in
        person_courses = []
        for course_name, course_slots in self.courses.items():
            for person_course in person.schedule:
                if person_course == course_slots:
                    person_courses.append(course_name)
                    break

        for course_name in person_courses:
            course_listbox.insert(tk.END, course_name)

        if not person_courses:
            course_listbox.insert(tk.END, "No enrolled courses found")
            course_listbox.config(state="disabled")

        button_frame = ttk.Frame(main_frame)
        button_frame.pack(fill="x", pady=10)

        def remove_selected():
            selection = course_listbox.curselection()
            if selection and person_courses:
                course_name = course_listbox.get(selection[0])
                try:
                    remove_course_from_person(
                        self.people_list, person_name, self.courses, course_name
                    )
                    self.show_person_schedule(person_name)
                    self.refresh_schedule_view()
                    self.save_all_data()
                    messagebox.showinfo(
                        "Success", f"Removed {course_name} from {person_name}"
                    )
                # dialog.destroy()
                except ValueError as e:
                    messagebox.showerror("Error", str(e))
            else:
                messagebox.showwarning(
                    "No Selection", "Please select a course to remove."
                )

        ttk.Button(button_frame, text="Remove Course", command=remove_selected).pack(
            side="left", padx=5
        )
        ttk.Button(button_frame, text="Cancel", command=dialog.destroy).pack(
            side="right", padx=5
        )

    # Course Management Methods
    def add_course_dialog(self):
        """Show dialog to add new course"""
        course_name = simpledialog.askstring("Add Course", "Enter course name:")
        if course_name and course_name.strip():
            try:
                add_course(self.courses, course_name.strip(), [])
                self.refresh_courses_list()
                self.save_courses()
                messagebox.showinfo("Success", f"Added course: {course_name}")
            except ValueError as e:
                messagebox.showerror("Error", str(e))

    def edit_course_dialog(self):
        """Show dialog to edit course name"""
        selection = self.courses_listbox.curselection()
        if not selection:
            messagebox.showwarning("No Selection", "Please select a course to edit.")
            return

        old_name = self.courses_listbox.get(selection[0])
        new_name = simpledialog.askstring(
            "Edit Course", f"Enter new name for {old_name}:", initialvalue=old_name
        )

        if new_name and new_name.strip() and new_name != old_name:
            try:
                # Get the course slots
                course_slots = self.courses[old_name]
                # Remove old course
                remove_course(self.courses, old_name)
                # Add with new name
                add_course(self.courses, new_name.strip(), course_slots)

                self.refresh_all()
                self.save_all_data()
                messagebox.showinfo(
                    "Success", f"Renamed course from {old_name} to {new_name}"
                )
            except ValueError as e:
                messagebox.showerror("Error", str(e))

    def delete_course(self):
        """Delete selected course"""
        selection = self.courses_listbox.curselection()
        if not selection:
            messagebox.showwarning("No Selection", "Please select a course to delete.")
            return

        course_name = self.courses_listbox.get(selection[0])

        # Check if course is assigned to anyone
        try:
            enrolled_people = get_people_in_course(
                self.people_list, self.courses, course_name
            )
            if enrolled_people:
                if not messagebox.askyesno(
                    "Course In Use",
                    f"Course '{course_name}' is assigned to {len(enrolled_people)} people:\n"
                    + f"{', '.join(enrolled_people)}\n\n"
                    + "Deleting this course will remove it from all people. Continue?",
                ):
                    return
        except:
            pass

        if messagebox.askyesno(
            "Confirm Delete",
            f"Are you sure you want to delete course '{course_name}'?",
        ):
            try:
                course_slots = self.courses[course_name]

                # Remove course from all people first
                for person in self.people_list[:]:
                    person.schedule = [
                        course for course in person.schedule if course != course_slots
                    ]
                    person.busy_time = person._create_busy_time_dict()

                # Remove the course
                remove_course(self.courses, course_name)

                self.refresh_all()
                self.course_name_label.config(text="Select a course to view details")

                # Clear course details
                for item in self.course_slots_tree.get_children():
                    self.course_slots_tree.delete(item)
                self.enrolled_text.delete("1.0", tk.END)

                self.save_all_data()
                messagebox.showinfo("Success", f"Deleted course: {course_name}")
            except ValueError as e:
                messagebox.showerror("Error", str(e))

    def add_course_time_slot(self):
        """Add time slot to selected course"""
        selection = self.courses_listbox.curselection()
        if not selection:
            messagebox.showwarning("No Selection", "Please select a course first.")
            return

        course_name = self.courses_listbox.get(selection[0])
        day = self.course_day_var.get()
        start_time = self.course_start_picker.get_time()
        end_time = self.course_end_picker.get_time()

        try:
            if not all([day, start_time, end_time]):
                raise ValueError("All fields must be filled")

            # Validate time format
            if ":" not in start_time or ":" not in end_time:
                raise ValueError("Time must be in HH:MM format")

            # Create new time slot
            new_slot = TimeSlot(start_time, end_time, day)

            # Add to course
            self.courses[course_name].append(new_slot)

            # Update all people who have this course
            for person in self.people_list:
                for course_slots in person.schedule:
                    if course_slots == self.courses[course_name]:
                        person.busy_time = person._create_busy_time_dict()

            self.show_course_details(course_name)
            self.refresh_schedule_view()
            self.save_courses()
            messagebox.showinfo(
                "Success",
                f"Added time slot to {course_name}: {day} {start_time}-{end_time}",
            )

        except Exception as e:
            messagebox.showerror("Error", f"Failed to add time slot: {str(e)}")

    def remove_course_time_slot(self):
        """Remove selected time slot from course"""
        course_selection = self.courses_listbox.curselection()
        if not course_selection:
            messagebox.showwarning("No Selection", "Please select a course first.")
            return

        slot_selection = self.course_slots_tree.selection()
        if not slot_selection:
            messagebox.showwarning(
                "No Selection", "Please select a time slot to remove."
            )
            return

        course_name = self.courses_listbox.get(course_selection[0])
        slot_item = slot_selection[0]
        slot_values = self.course_slots_tree.item(slot_item)["values"]

        if messagebox.askyesno(
            "Confirm Remove",
            f"Remove {slot_values[0]} {slot_values[1]}-{slot_values[2]} from {course_name}?",
        ):
            try:
                # Find and remove the slot
                course_slots = self.courses[course_name]
                for i, slot in enumerate(course_slots):
                    if (
                        slot.day == slot_values[0]
                        and slot.start_time == slot_values[1]
                        and slot.end_time == slot_values[2]
                    ):
                        course_slots.pop(i)
                        break

                # Update all people who have this course
                for person in self.people_list:
                    for course_slots in person.schedule:
                        if course_slots == self.courses[course_name]:
                            person.busy_time = person._create_busy_time_dict()

                self.show_course_details(course_name)
                self.refresh_schedule_view()
                self.save_courses()
                messagebox.showinfo("Success", f"Removed time slot from {course_name}")

            except Exception as e:
                messagebox.showerror("Error", f"Failed to remove time slot: {str(e)}")

    # Common Times Methods
    def find_common_times(self):
        """Find common free times for selected day"""
        day = self.common_day_var.get()

        if not self.people_list:
            self.results_text.delete("1.0", tk.END)
            self.results_text.insert(
                "1.0", "No people added yet. Please add people first."
            )
            return

        common_times = common_free_times(self.people_list, day)

        self.results_text.delete("1.0", tk.END)

        result_text = f"Common free times for {day}\n"
        result_text += "=" * (len(day) + 25) + "\n\n"

        if common_times:
            result_text += f"Found {len(common_times)} common free time period(s):\n\n"
            for i, (start, end) in enumerate(common_times, 1):
                result_text += f"  {i}. {start} - {end}\n"
        else:
            result_text += "No common free times found for this day.\n"
            result_text += (
                "\nThis means all people have conflicting schedules on this day."
            )

        result_text += f"\nChecked schedules for {len(self.people_list)} people:\n"
        for person in self.people_list:
            result_text += f"  - {person.name}\n"

        self.results_text.insert("1.0", result_text)

    def show_all_common_times(self):
        """Show common free times for all days"""
        if not self.people_list:
            self.results_text.delete("1.0", tk.END)
            self.results_text.insert(
                "1.0",
                "No people added yet. Please add people first to find common times.",
            )
            return

        self.results_text.delete("1.0", tk.END)

        result_text = "Common Free Times - Weekly Summary\n"
        result_text += "=" * 50 + "\n"
        result_text += f"Analyzing schedules for {len(self.people_list)} people: "
        result_text += ", ".join([person.name for person in self.people_list])
        result_text += "\n" + "=" * 50 + "\n\n"

        total_common_slots = 0

        for day in self.days:
            common_times = common_free_times(self.people_list, day)
            result_text += f"{day}:\n"

            if common_times:
                total_common_slots += len(common_times)
                for i, (start, end) in enumerate(common_times, 1):
                    result_text += f"   {start} - {end}\n"
            else:
                result_text += "   No common free times\n"

            result_text += "\n"

        # Add summary
        result_text += "SUMMARY:\n"
        result_text += f"   - Total common time slots: {total_common_slots}\n"
        result_text += f"   - Days with common times: {sum(1 for day in self.days if common_free_times(self.people_list, day))}\n"
        result_text += f"   - People analyzed: {len(self.people_list)}\n"

        if total_common_slots == 0:
            result_text += "\nTips for finding common times:\n"
            result_text += "   - Check if people have too many overlapping courses\n"
            result_text += (
                "   - Consider removing some courses or adjusting schedules\n"
            )
            result_text += "   - Try looking at weekend days (Saturday/Sunday)\n"

        self.results_text.insert("1.0", result_text)

    # Save/Load Methods

    def save_courses(self):
        """Save courses data to file"""
        try:
            save_courses(self.courses, self.data_file)
        except Exception as e:
            messagebox.showerror("Save Error", f"Failed to save courses: {str(e)}")

    def save_all_data(self):
        """Save both people and courses data"""
        try:
            save_data(self.people_list, self.data_file)
            save_courses(self.courses, self.data_file)
        except Exception as e:
            messagebox.showerror("Save Error", f"Failed to save data: {str(e)}")

    def run(self):
        """Start the GUI main loop"""
        try:
            self.root.mainloop()
        except KeyboardInterrupt:
            self.root.quit()


def launch_gui(people_list, data_file="schedule_data.json"):
    """Launch the schedule manager GUI"""
    app = ScheduleManagerGUI(people_list, data_file)
    app.run()
