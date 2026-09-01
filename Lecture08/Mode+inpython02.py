def example_a_plus_mode():
    with open("example.txt", "a+") as file:
        file.seek(0)
        content = file.read()
        print("Currnent content of the file : ")
        print(content)
        
        file.write("Appending a new line at the end.\n")
        
        file.seek(0)
        updated_content = file.read()
        print("\nUpdated content of the file : ")
        print(updated_content)