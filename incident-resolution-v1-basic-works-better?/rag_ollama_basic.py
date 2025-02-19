import ollama # type: ignore
import time
import os
import json
import numpy as np # type: ignore
from numpy.linalg import norm # type: ignore


''' open a file and return paragraphs'''
def parse_file_separator(filename):
    with open(filename, 'r', encoding='utf-8-sig') as file:
        content = file.read()
        separator = "-" * 40
        '''Splitting the content by the separator line'''
        records = content.split(separator)
        paragraphs = []
        for record in records:
            '''Removing any extra whitespace and newlines'''
            cleaned_record = record.strip()
            if cleaned_record:
                paragraphs.append(cleaned_record)
        return paragraphs

def parse_file(filename, method="separator", chunk_size=1000, keywords=None, separator="-"*40):
    with open(filename, 'r', encoding='utf-8-sig') as file:
        content = file.read()

    paragraphs = []

    if method == "separator":
        records = content.split(separator)
        for record in records:
            cleaned_record = record.strip()
            if cleaned_record:
                paragraphs.append(cleaned_record)

    elif method == "fixed_length":
        paragraphs = [content[i:i+chunk_size].strip() for i in range(0, len(content), chunk_size)]

    elif method == "keywords" and keywords:
        current_chunk = []
        for line in content.splitlines():
            if any(keyword in line for keyword in keywords):
                if current_chunk:
                    combined_chunk = "\n".join(current_chunk).strip()
                    if "Description" in combined_chunk or "Problem Description" in combined_chunk:
                        paragraphs.append(combined_chunk)
                    current_chunk = []
            current_chunk.append(line)
        if current_chunk:
            combined_chunk = "\n".join(current_chunk).strip()
            if "Description" in combined_chunk or "Problem Description" in combined_chunk:
                paragraphs.append(combined_chunk)

    return paragraphs

def save_embeddings(filename, embeddings):
    '''Extract only the base filename without the path'''
    base_filename = os.path.basename(filename)
    # Create directory if it doesn't exist
    if not os.path.exists("embeddings"):
        os.makedirs("embeddings")
    # Dump embeddings to json
    with open(f"embeddings/{base_filename}.json", "w") as f:
        json.dump(embeddings, f)


def load_embeddings(filename):
    # check if file exists
    if not os.path.exists(f"embeddings/{filename}.json"):
        return False
    # load embeddings from json
    with open(f"embeddings/{filename}.json", "r") as f:
        return json.load(f)


def get_embeddings(filename, modelname, chunks):
    # check if embeddings are already saved
    if (embeddings := load_embeddings(filename)) is not False:
        return embeddings
    # get embeddings from ollama
    embeddings = [
        ollama.embeddings(model=modelname, prompt=chunk)["embedding"]
        for chunk in chunks
    ]
    # save embeddings
    save_embeddings(filename, embeddings)
    return embeddings


# find cosine similarity of every chunk to a given embedding
def find_most_similar(needle, haystack):
    needle_norm = norm(needle) # Embedding of the query.
    similarity_scores = [
        np.dot(needle, item) / (needle_norm * norm(item)) for item in haystack
    ]
    # haystack : List of embeddings to compare against
    # Return Sorted list of tuples with similarity scores and indices
    return sorted(zip(similarity_scores, range(len(haystack))), reverse=True)

def main():
    # Defines the role and behavior of the support agent
    SYSTEM_PROMPT = """You are a customer support agent. Your job is to answer any questions posed to you, based on the context provided. You are allowed to make an intelligent decision to club multiple answers together, but as points. Paraphrase the final answer to be more user friendly.
    If you're unsure, just say "I would suggest getting more details on this case.".
    Context:
    """
    # open file
    # Need to paste this cleanedup file in the folder below..
    filename = "./incident_data/final.txt"
    paragraphs = parse_file(
        filename,
        method="separator",
        keywords=["Issue Description:", "Problem Description:", "Resolution:"]
    )
    embeddings = get_embeddings(filename, "nomic-embed-text", paragraphs)

    # Prompts the user for input and generates responses based on the most similar chunks of context
    while True:
        prompt = input("What do you want to know? (Type 'exit' to quit) -> ")
        if prompt.lower() in ['exit', 'quit']:
            print("Exiting the assistant.")
            break

        # Generate embeddings for the new prompt
        prompt_embedding = ollama.embeddings(model="nomic-embed-text", prompt=prompt)["embedding"]
        most_similar_chunks = find_most_similar(prompt_embedding, embeddings)[:5]
        context_for_assistant = "\n".join(paragraphs[item[1]] for item in most_similar_chunks)
        response = ollama.chat(
            model="mistral",
            messages=[
                {"role": "system", "content": SYSTEM_PROMPT + context_for_assistant},
                {"role": "user", "content": prompt},
            ],
        )
        print("\n\n")
        print(response["message"]["content"])

if __name__ == "__main__":
    main()
