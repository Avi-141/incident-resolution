def format_and_clean_text(text_file, output_file):
    # Define the strings to be removed
    unwanted_strings = [
        "Resolution Notes: ############################",
        '#############################', 
        'Reach me by: Via Email',
        'Reach me by: Via IM',
        'I am ok to be contacted after hours: Yes',
        'I am ok to be contacted after hours: No',
        'CR No: No'
    ]

    # Read the existing text file
    with open(text_file, 'r') as file:
        lines = file.readlines()

    # Initialize a new list for the cleaned lines
    cleaned_lines = []

    # Process each line
    for line in lines:
        if any(unwanted in line for unwanted in unwanted_strings):
            continue  # Skip unwanted lines

        cleaned_lines.append(line)

        # Check and add new lines based on specific content
        if "Problem Description:" in line:
            cleaned_lines.append("\n")  # Add new line after 'Problem Description'
        if "Service Impacted:" in line:
            cleaned_lines.append("\n")  # Add new line before 'Service Impacted'
            cleaned_lines.append(line.replace("Service Impacted:", "Resolution:"))
            continue
        if "Resolution:" in line and "Service Impacted:" not in line:
            cleaned_lines.append("\n")  # Add new line after 'Resolution'
        if "CR ID:" in line:
            cleaned_lines.append("\n")  # Add new line before 'CR ID'

    # Write the cleaned lines to the output file
    with open(output_file, 'w') as file:
        file.writelines(cleaned_lines)

# Example usage:
format_and_clean_text('./incident_data/Incidents.txt', 'cleaned_Incidents.txt')

def format_and_add_description(text_file, output_file):
    # Recognized labels that should follow "Name:" if present
    labels = ["Description:", "Problem Description:", "Service Impacted:",
              "Resolution:", "CR ID:", "Resolution Notes:"]
    
    # Read the existing text file
    with open(text_file, 'r') as file:
        lines = file.readlines()

    # Initialize a new list for the formatted lines
    formatted_lines = []
    i = 0
    while i < len(lines):
        line = lines[i].strip()  # Remove any leading/trailing whitespace
        if "Name:" in line:
            formatted_lines.append(line + "\n")  # Add the line with "Name:"
            # Look ahead to check the next line
            if i + 1 < len(lines):
                next_line = lines[i + 1].strip()
                # If the next line does not start with any recognized label
                if not any(next_line.startswith(label) for label in labels):
                    # Insert "Description:" before the next line if it doesn't start with a label
                    formatted_lines.append("Description: " + next_line + "\n")
                    i += 1  # Increment to skip the next line as it's already handled
        else:
            formatted_lines.append(line + "\n")
        i += 1

    # Write the formatted lines to the output file
    with open(output_file, 'w') as file:
        file.writelines(formatted_lines)

# Example usage:
format_and_add_description('Incidents.txt', 'cleaned_Incidents.txt')
