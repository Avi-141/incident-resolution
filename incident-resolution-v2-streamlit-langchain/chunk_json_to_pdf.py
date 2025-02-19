import json
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas

# Use this file to break your dataset into chunks of pdfs (Optional)
# This is to preserve semantic context, and prevent the missing out the Q&A
def json_to_pdf(json_data, output_pdf_path):
    """Convert JSON data to a PDF file."""
    c = canvas.Canvas(output_pdf_path, pagesize=letter)
    width, height = letter
    
    # Initial position
    x_pos = 50
    y_pos = height - 50
    
    # Loop through the JSON data and write to PDF
    for i, entry in enumerate(json_data):
        entry_text = json.dumps(entry, indent=4)
        for line in entry_text.split('\n'):
            if y_pos < 50:  # Check if we need to add a new page
                c.showPage()
                y_pos = height - 50
            c.drawString(x_pos, y_pos, line)
            y_pos -= 12  # Move position down for the next line
            
        y_pos -= 24  # Add some space between entries

    c.save()

def chunk_json_to_pdfs(input_path, chunk_size):
    # Load JSON data
    with open(input_path, 'r') as file:
        data = json.load(file)
    
    # Calculate the number of chunks
    total_qas = len(data)
    number_of_chunks = (total_qas + chunk_size - 1) // chunk_size
    
    # Create and save each chunk as a PDF
    for i in range(number_of_chunks):
        chunk = data[i * chunk_size: (i + 1) * chunk_size]
        output_pdf_path = f'chunk_{i + 1}.pdf'
        json_to_pdf(chunk, output_pdf_path)
        print(f'Chunk {i + 1} saved as {output_pdf_path}')
    
    print(f'Data has been chunked into {number_of_chunks} PDF files.')

# Example usage
chunk_json_to_pdfs('../incident_data/qna.json', 25)
