input_string =("Enter a string: ")
modified_string = ""
vowels = "aeiouAEIOU"
for char in input_string:
    upper_char = char.upper()
    if upper_char in vowels :
        modified_string += "+"
    else :
        modified_string += upper_char
print("Chayawat tinna:",modified_string)
