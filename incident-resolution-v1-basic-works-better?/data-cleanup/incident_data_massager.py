import pandas as pd

def extract_and_save_data(excel_file, text_file):
    # Read the Excel file
    df = pd.read_excel(excel_file)
    df['Resolved by Change'] = df['Resolved by Change'].fillna('NA')
    # Select the required columns
    selected_columns = df[['Number', 'Description', 'Resolution Notes', 'Resolved by Change']]
    separator = "-" * 40  # creates a line of 40 dashes as a separator
    # Open the text file to write
    with open(text_file, 'w') as file:
        for _, row in selected_columns.iterrows():
            file.write(f"Name: {row['Number']}\n")
            file.write(f"Description: {row['Description']}\n")
            file.write(f"Resolution Notes: {row['Resolution Notes']}\n")
            file.write(f"CR ID: {row['Resolved by Change']}\n")
            file.write(separator + "\n\n")  # Add a separator line and a blank line for readability
# Example usage:
extract_and_save_data('./raw_data/Incidents.xlsx', 'Incidents.txt')
