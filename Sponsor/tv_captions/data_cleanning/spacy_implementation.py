import os
import sys
import glob
import json
import pandas as pd
import spacy
from concurrent.futures import ProcessPoolExecutor, as_completed

# Global variable for spaCy model in worker processes
nlp = None

def init_worker():
    """Initializer for each worker process: load the spaCy model once."""
    global nlp
    nlp = spacy.load("en_core_web_sm")

def process_single_csv(input_csv, output_csv):
    """
    Processes a single CSV file using spaCy.
    
    Reads the CSV (which must have at least 3 columns), cleans the text
    from the third column, extracts named entities (excluding ones that 
    contain newline characters, equal to '\u266a', or with label 'TIME'),
    and writes the result to the output CSV.
    """
    try:
        df = pd.read_csv(input_csv)
    except Exception as e:
        print(f"Error reading {input_csv}: {e}", file=sys.stderr)
        return

    # Ensure at least three columns exist
    if len(df.columns) < 1:
        print(f"File {input_csv} does not have at least one columns", file=sys.stderr)
        return

    spacy_results = []
    for _, row in df.iterrows():
        text_to_process = row.iloc[0]
        text_cleaned = str(text_to_process).replace("\n", " ")
        
        # Process the text with the preloaded global spaCy model
        doc = nlp(text_cleaned)
        entities = [
            {
                "text": ent.text,
                "label": ent.label_,
                "start_char": ent.start_char,
                "end_char": ent.end_char
            }
            for ent in doc.ents
            if "\n" not in ent.text and ent.text != "\u266a"
        ]
        
        spacy_results.append({
            "entities": json.dumps(entities)
        })
    
    # Save the processed results into a CSV file.
    spacy_df = pd.DataFrame(spacy_results)
    os.makedirs(os.path.dirname(output_csv), exist_ok=True)
    spacy_df.to_csv(output_csv, index=False)
    print(f"Processed {input_csv} -> {output_csv}")

def process_file(file_path, input_dir, output_dir):
    """
    Determines the output CSV path based on the relative path from the input directory,
    then processes the file.
    """
    # Preserve the directory structure:
    rel_path = os.path.relpath(file_path, input_dir)
    output_csv = os.path.join(output_dir, rel_path)
    process_single_csv(file_path, output_csv)

def main():

    input_dir = sys.argv[1]
    output_dir = sys.argv[2]
    num_workers = 8

    # Recursively find all CSV files in the input directory.
    csv_files = glob.glob(os.path.join(input_dir, '**', '*.csv'), recursive=True)
    print(f"Found {len(csv_files)} CSV files in '{input_dir}'")

    # Use ProcessPoolExecutor to process files in parallel.
    with ProcessPoolExecutor(max_workers=num_workers, initializer=init_worker) as executor:
        futures = []
        for file_path in csv_files:
            futures.append(executor.submit(process_file, file_path, input_dir, output_dir))
        
        # Optionally wait for all tasks to complete and catch any errors.
        for future in as_completed(futures):
            try:
                future.result()
            except Exception as e:
                print(f"Error processing file: {e}", file=sys.stderr)

if __name__ == '__main__':
    main()
