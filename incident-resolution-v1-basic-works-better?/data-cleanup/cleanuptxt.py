import sys
import re
# Remove incident numbers from parsed data ---
def process_file(input_file, output_file):
    # Read entire file content
    with open(input_file, 'r') as f:
        content = f.read()
    
    # Split the file into blocks separated by blank lines
    blocks = content.strip().split("\n\n")
    processed_blocks = []
    
    for block in blocks:
        lines = block.splitlines()
        processed_lines = []
        resolution_lines = []
        
        for line in lines:
            # Skip any line that starts with "Name: INC"
            if re.match(r'^Name:\s*INC', line):
                continue
            
            # Replace "Description:" with "Issue Description:"
            if line.startswith("Description:"):
                line = "Issue Description:" + line[len("Description:"):]
            
            # If the line starts with "Resolution:", collect its content
            #if line.startswith("Resolution:"):
                # Remove the prefix and strip leading/trailing whitespace
                #resolution_lines.append(line[len("Resolution:"):].strip())
                #continue
            
            # For all other lines, keep them as is
            processed_lines.append(line)
        
        # If any resolution lines were found, combine them into a single Resolution: field
        #if resolution_lines:
            #combined_resolution = " ".join(resolution_lines)
            #processed_lines.append("Resolution: " + combined_resolution)
        
        processed_blocks.append("\n".join(processed_lines))
    
    # Join the processed blocks with a blank line separating each
    result = "\n\n".join(processed_blocks)
    
    # Write the result to the output file
    with open(output_file, 'w') as f:
        f.write(result)

if __name__ == '__main__':
    if len(sys.argv) != 3:
        print("Usage: python script.py <input_file.txt> <output_file.txt>")
    else:
        input_file = sys.argv[1]
        output_file = sys.argv[2]
        process_file(input_file, output_file)
        print(f"Processed file written to {output_file}")
