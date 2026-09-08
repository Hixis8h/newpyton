
attendance_week = [
    ["Alice","Bob","Charlie","David"],
    ["Alice","Charlie","David"],
    ["Alice","Bob","David"],
    ["Alice","David","Eve"],
    ["Bob","Charlie","David"]
]

attendance_sets = [set(day) for day in attendance_week]
print(attendance_week)

preset_every_day = set.intersection(*attendance_sets)
print("Preset every day: ",preset_every_day)

all_students = set.union(*attendance_sets)
absent_at_lease_one_day_ =all_students - preset_every_day
print("Abset at least one day: " , absent_at_lease_one_day_)

first_day_present = attendance_sets[0]
last_day_present = attendance_sets[-1]
first_day_but_not_last = list(first_day_present - last_day_present)

unique_students_count =len(all_students)
print("Total unique students: " ,unique_students_count)