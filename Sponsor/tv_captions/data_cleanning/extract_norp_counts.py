import os
import glob
import sys
import json
import pandas as pd
from collections import Counter
import argparse

def extract_norp_counts_from_csv(file_path):
    """
    Reads a CSV file that contains a JSON dump of spaCy entity results
    in a column called 'entities', extracts all norps (NORP)
    and returns a Counter with their frequencies.
    """
    try:
        df = pd.read_csv(file_path)
    except Exception as e:
        print(f"Error reading {file_path}: {e}")
        return Counter()
    
    norp_counter = Counter()
    if 'entities' not in df.columns:
        print(f"File {file_path} does not contain an 'entities' column; skipping.")
        return norp_counter

    for idx, row in df.iterrows():
        try:
            # Parse the JSON string to get a list of entity dictionaries
            entities = json.loads(row['entities'])
        except json.JSONDecodeError as e:
            print(f"JSON decode error in {file_path} (row {idx}): {e}")
            continue

        for ent in entities:
            if ent.get('label') == 'NORP':
                norp_text = ent.get('text', '').strip()
                if norp_text:
                    norp_counter[norp_text] += 1
    return norp_counter

def process_files(input_dir, output_dir):
    """
    Recursively finds all CSV files in the input_dir, extracts norp counts,
    and writes a CSV file for each network/year combination to output_dir.
    The expected filename pattern is: <NETWORK>.Text.<YEAR>.<index>.csv
    """
    pattern = os.path.join(input_dir, '**', '*.csv')
    csv_files = glob.glob(pattern, recursive=True)
    print(f"Found {len(csv_files)} CSV files in {input_dir}")

    for file_path in csv_files:
        file_name = os.path.basename(file_path)
        # Expecting filename pattern like: Bloomberg.Text.2020.1.csv
        parts = file_name.split('.')
        if len(parts) < 5:
            print(f"Filename '{file_name}' does not match expected pattern; skipping.")
            continue
        network = parts[0]
        year = parts[2]
        print(f"Processing '{file_name}' (Network: {network}, Year: {year})")

        norp_counter = extract_norp_counts_from_csv(file_path)
        if not norp_counter:
            print(f"No norps found in '{file_name}'.")
            continue

        # Convert the Counter to a DataFrame
        df_counts = pd.DataFrame(list(norp_counter.items()), columns=['NORP', 'Count'])
        df_counts.sort_values(by='Count', ascending=False, inplace=True)

        # Create an output filename, e.g., Bloomberg.Text.2020.NORP_counts.csv
        output_filename = f"{network}.Text.{year}.NORP_counts.csv"
        output_path = os.path.join(output_dir, output_filename)
        df_counts.to_csv(output_path, index=False)
        print(f"Saved norp counts to '{output_path}'")

if __name__ == '__main__':
    if len(sys.argv) != 3:
        print("Usage: python clean_text.py <input_csv> <output_csv>")
        sys.exit(1)

    input_csv = sys.argv[1]
    output_csv = sys.argv[2]

    process_files(input_csv, output_csv)
    