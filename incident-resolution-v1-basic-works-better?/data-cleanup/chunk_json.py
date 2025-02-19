import json


# Testing JSON chunker... 

def chunk_qa_data(input_path, chunk_size):
    # Load JSON data
    with open(input_path, 'r') as file:
        data = json.load(file)
    
    # Calculate the number of chunks
    total_qas = len(data)
    number_of_chunks = (total_qas + chunk_size - 1) // chunk_size
    
    # Create and save each chunk
    for i in range(number_of_chunks):
        chunk = data[i*chunk_size:(i+1)*chunk_size]
        with open(f'chunk_{i+1}.json', 'w') as file:
            json.dump(chunk, file, indent=4)
    
    print(f'Data has been chunked into {number_of_chunks} files.')

# Example usage
chunk_qa_data('./incident_data/qna.json', 25) 
