# Master file joiner

import pandas as pd
import csv

def detect_delimiter(file_path):
    with open(file_path, 'r') as file:
        first_line = file.readline()
        # Use csv.Sniffer to detect the delimiter
        sniffer = csv.Sniffer()
        delimiter = sniffer.sniff(first_line).delimiter
        return delimiter

def combine_csv_files(file_paths, output_file, custom_header=None):
    combined_df = pd.DataFrame()

    for file in file_paths:
        print("Current Path: " + file)
        # Detect the delimiter for each file
        delimiter = detect_delimiter(file)
        df = pd.read_csv(file, delimiter=delimiter, header=0)
        combined_df = pd.concat([combined_df, df], ignore_index=True)

    # Save the combined DataFrame to the output CSV file
    combined_df.to_csv(output_file, index=False, header=custom_header)
    print(f"Combined file saved as {output_file}")

file_paths = [
    '../../scratch/alpine/mame5632/1993_1998_master.csv', # Max
    '../../scratch/alpine/joot9454/1998_2003_master.csv', # John
    '../../scratch/alpine/mafi7060/2003_2008_master.csv', # Mathis
    '../../scratch/alpine/luel6939/2008_2013_master.csv', # Luis
    '../../scratch/alpine/nimi2356/2013_2018_master.csv', # Nick
    '../../scratch/alpine/rera8642/2018_2025_master.csv'  # Reda
]

custom_header = ['Name of document', 'Path to file', 'File size']

combine_csv_files(file_paths, '../../scratch/alpine/nimi2356/1993_2025_master.csv', custom_header)