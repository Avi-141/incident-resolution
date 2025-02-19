import json

# Excel - JSON - Text 
input_file_path = './incident_data/qna.json'
output_file_path = './incident_data/qna.txt'

# Read the JSON data from the file
with open(input_file_path, 'r') as file:
    data = json.load(file)

# Extract Questions and Answers and format them
formatted_text = ""
for item in data:
    formatted_text += f"Q: {item['Question']}\nA: {item['Answer']}\n\n"

# Write the formatted text to a new text file
with open(output_file_path, 'w') as file:
    file.write(formatted_text)

print("Questions and answers have been written to the text file.")
