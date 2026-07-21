num_rows =int(input("How many rows?: "))
columns = int(input("How many colums?:"))
for i in range(num_rows):
    for j in range(columns):
        print("*",end="")
    print()
