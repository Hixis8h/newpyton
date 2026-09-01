with open("employee.txt", "r") as emp_file:
    lines = emp_file.read().splitlines()

for i in range(0, len(lines), 3):
    print(f"Name: {lines[i]}")
    print(f"ID: {lines[i + 1]}")
    print(f"Dept: {lines[i + 2]}")
    print()