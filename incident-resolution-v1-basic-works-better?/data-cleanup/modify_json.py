import json

# Load the JSON data from the file
with open('./incident_data/output.json', 'r') as file:
    data = json.load(file)

# Transform the data
transformed_data = []
for item in data:
    transformed_item = {
        "Incident": item["Name"],
        "Question": item["Description"],
        "Answer": item.get("Resolution", "No resolution provided") 
    }
    transformed_data.append(transformed_item)

# Save the transformed data to a new JSON file
with open('output_file.json', 'w') as file:
    json.dump(transformed_data, file, indent=4)

print("New JSON file has been created with the required transformations.")
