num_emps = int(input("How many employee records do you want to create? "))

with open("employee.txt", "w") as emp_file:
    for count in range(1, num_emps + 1):
        print("Enter data for employee #", count, sep="")
        name = input("Name: ")
        id_num = input("ID number: ")
        dept = input("Department: ")

        emp_file.write(f"Name: {name}\n")
        emp_file.write(f"ID: {id_num}\n")
        emp_file.write(f"Dept: {dept}\n")

        if count != num_emps:
            emp_file.write("\n")
        print()

print("Employee records written to employee.txt")