import struct
num_records = int(input("How many record do you wnant ro create?: "))
with open("records.bin","wb") as file:
    for _ in range(num_records):
        id_num = int(input("Enter ID number: "))
        name = input("Enter name: ")
        age = int(input("Enter age: "))
        gpa = float(input("Enter GPA: "))
        
        data = struct.pack('i20sif',id_num,name.encode(),age,gpa)
        file.write(data)
print(f"{num_records} records have been written to records.bin")