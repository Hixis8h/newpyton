bool_list = [False, True , False]
numbers = [4,2,9,1,5,6]
any_true = any(bool_list)
print(f"Is any elemeant True? {any_true}")

all_true = all(bool_list)
print(f"Are all element True? {all_true}")

string = "hello"
char_list = list(string)
print(f"List of characters : {char_list}")

reversed_numbers = list(reversed(numbers))
print(f"Reversd list : {reversed_numbers}")

enumerate_numbers = list(enumerate(numbers))
print(f"Enumerated list : {enumerate_numbers}")