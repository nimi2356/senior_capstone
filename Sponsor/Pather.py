import os
import argparse
import pandas as pd

# Place this file in your home directory and give it these arguments, replacing it with your identikey and years
# ../../scratch/alpine/identikey
# Will create a master file for your years in your home directory, which we will then bring together
# Input Args: --scratch_dir, --start_year, --end_year

def go():
    # Get our directory path
    parser = argparse.ArgumentParser(description='Fetch scratch directory path')

    # Add parameters
    parser.add_argument('--scratch_dir', type=str, required=True, help='The path from your home dir in alpine')
    parser.add_argument('--start_year', type=int, required=True, help='The start year (INCLUSIVE)')
    parser.add_argument('--end_year', type=int, required=False, help='The end year (EXCLUSIVE)')

    args = parser.parse_args()
    scratch_dir = args.scratch_dir
    start_year = args.start_year
    end_year = args.end_year

    # List to store each file's info
    file_data = []

    # Traverse through directory and subdirectories
    for root, dirs, files in os.walk(scratch_dir):
        for file in files:
            if file.endswith('.rtf'):
                file_path = os.path.join(root, file)
                file_size = os.path.getsize(file_path)  # Get the file size
                file_data.append({
                    'Name of document': file,
                    'Path to file': file_path,
                    'File size': file_size
                })
    df = pd.DataFrame(file_data)
    df.to_csv(f"{start_year}_{end_year}_master.csv", index=False)
go()