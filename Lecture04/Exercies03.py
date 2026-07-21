columns = int(input("How many colums?:"))
for i in range(1,101):
    print(f"{i:>3}",end="")
    for j in range(columns,):
        if i % columns == 0:
            print()
