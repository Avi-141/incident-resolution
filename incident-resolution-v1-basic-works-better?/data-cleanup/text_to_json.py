import json

def parse_incidents(file_path):
    with open(file_path, 'r') as file:
        text = file.read()

    incidents = []
    current_incident = {}
    key = None

    # Split the text into lines
    lines = text.strip().split('\n')
    
    # Iterate through each line
    for line in lines:
        line = line.strip()
        if line.startswith('Name:'):
            # Start a new incident
            if current_incident:
                # Merge Resolution and Resolution Notes if both exist
                if 'Resolution' in current_incident and 'Resolution Notes' in current_incident:
                    current_incident['Resolution'] += " " + current_incident.pop('Resolution Notes')
                incidents.append(current_incident)
            current_incident = {'Name': line.split('Name: ')[1].strip()}
            key = None
        elif line.startswith('Description:'):
            key = 'Description'
            current_incident[key] = ""
        elif line.startswith('Problem Description:'):
            key = 'Problem Description'
            current_incident[key] = line.split('Problem Description:')[1].strip() if 'Problem Description:' in line else ""
        elif line.startswith('Service Impacted:'):
            key = 'Service Impacted'
            current_incident[key] = line.split('Service Impacted:')[1].strip() if 'Service Impacted:' in line else ""
        elif line.startswith('Resolution:'):
            if 'Resolution' in current_incident and key == 'Resolution':
                current_incident['Resolution'] += " " + (line.split('Resolution:')[1].strip() if 'Resolution:' in line else "")
            else:
                key = 'Resolution'
                current_incident[key] = line.split('Resolution:')[1].strip() if 'Resolution:' in line else ""
        elif line.startswith('CR ID:'):
            key = 'CR ID'
            current_incident[key] = line.split('CR ID:')[1].strip() if 'CR ID:' in line else ""
        elif line.startswith('Backend changes'):
            key = 'Backend changes'
            current_incident[key] = line.split('Backend changes(Y/N):')[1].strip() if 'Backend changes(Y/N):' in line else "No"
        elif line.startswith('Resolution Notes:'):
            if 'Resolution' in current_incident:
                current_incident['Resolution'] += " " + (line.split('Resolution Notes:')[1].strip() if 'Resolution Notes:' in line else "")
            else:
                key = 'Resolution Notes'
                current_incident[key] = line.split('Resolution Notes:')[1].strip() if 'Resolution Notes:' in line else ""
        elif line.startswith('----------------------------------------'):
            # Separator for incidents, append the current incident and reset
            if current_incident:
                # Merge Resolution and Resolution Notes if both exist
                if 'Resolution' in current_incident and 'Resolution Notes' in current_incident:
                    current_incident['Resolution'] += " " + current_incident.pop('Resolution Notes')
                incidents.append(current_incident)
                current_incident = {}
        elif key and line:  # Continuation of the last known key
            current_incident[key] += " " + line

    # Add the last incident if not already added
    if current_incident:
        if 'Resolution' in current_incident and 'Resolution Notes' in current_incident:
            current_incident['Resolution'] += " " + current_incident.pop('Resolution Notes')
        incidents.append(current_incident)

    return incidents

# Specify the path to your text file
file_path = './incident_data/cleaned_Incidents.txt'

# Parse the incidents from the text file
parsed_incidents = parse_incidents(file_path)

# Convert the parsed incidents to JSON format
json_output = json.dumps(parsed_incidents, indent=4)

# Print the JSON output
print(json_output)

# Optionally, save the JSON output to a file
with open('output.json', 'w') as json_file:
    json_file.write(json_output)
