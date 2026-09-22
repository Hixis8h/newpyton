import json

data = {"name" : "Alice" , "Age" : 25} 
json_str = json.dumps(data)
print(json_str)

parsed_data = json.load(json_str)

print(parsed_data)
print(parsed_data["name"])
print(parsed_data["Age"])

