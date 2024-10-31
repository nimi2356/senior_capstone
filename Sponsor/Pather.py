import os
import pandas as pd

def go():
    # Add parameters
    scratch_dir = '../../scratch/alpine/nimi2356/raw_data'

    # List to store each file's info
    file_data = []

    # Traverse through directory and subdirectories
    for root, dirs, files in os.walk(scratch_dir):
        for file in files:
            if file.endswith('.txt'):
                file_path = os.path.join(root, file)
                file_size = os.path.getsize(file_path)  # Get the file size
                file_data.append({
                    'Name of document': file,
                    'Path to file': file_path.lstrip('./'), # Takes off the ../../
                    'File size': file_size
                })

    df = pd.DataFrame(file_data)
    df.to_csv("../../scratch/alpine/nimi2356/new_master.csv", index=False)
go()