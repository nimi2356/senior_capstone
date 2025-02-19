from pathlib import Path
import os
import pandas as pd
import sys
import glob
import re
from html import unescape

# Global flag for whether to strip out just the text after [[TITLE.END]]
just_text = True

def clean_text(text):
    """
    Clean the text according to specified rules.
    """
    if not isinstance(text, str):
        return text
    
    if just_text:
        if "[[TITLE.END]]" in text:
            text = text.split("[[TITLE.END]]", 1)[1].strip()
    
    # Remove topic sections - check for both patterns
    if "TOPICS: TOPIC FREQUENCY" in text:
        text = text.split("TOPICS: TOPIC FREQUENCY")[0].strip()
    elif "TOPIC FREQUENCY" in text:
        text = text.split("TOPIC FREQUENCY")[0].strip()

    # Deal with start/end times
    text = re.sub(r'\[\[TIME\.START\]\].*?\[\[TIME\.END\]\]', '', text, flags=re.IGNORECASE)
    
    # Remove all other double brackets
    text = re.sub(r'\[\[.*?\]\]', '', text)
    
    # Remove HTML markup tags
    text = re.sub(r'<[^>]+>', '', text)
    
    # Unescape HTML entities
    text = unescape(text)
    
    # Add new lines before ">>" occurrences, ensuring they start at the beginning of the line
    text = re.sub(r'(?<!\n)>>', '\n', text)
    
    # Clean up multiple newlines and spaces
    text = re.sub(r'\n\s+', '\n', text)  # Remove spaces after newlines
    text = re.sub(r'\n{2,}', '\n', text)  # Reduce multiple newlines to a single newline
    text = re.sub(r' +', ' ', text)  # Reduce multiple spaces to a single space
    
    return text.strip()

def process_csv_file(file_path):
    """
    Process a single CSV file while maintaining structure but cleaning text content.
    """
    try:
        # Read the CSV file (assumes no header)
        df = pd.read_csv(file_path, header=None)

        if just_text:
            if len(df.columns) >= 3:
                df = df[[2]]  # Keep only the third column
            else:
                print(f"Warning: File {file_path} has fewer than 3 columns")
        
        # Create a copy of the dataframe for modification
        cleaned_df = df.copy()
        
        print(f"Debug: Shape of dataframe: {df.shape}")
        
        # Clean text in each cell
        for i in range(len(cleaned_df)):
            for j in range(len(cleaned_df.columns)):
                cleaned_df.iloc[i, j] = clean_text(cleaned_df.iloc[i, j])
            
            if i % 1000 == 0:
                print(f"Processed {i} rows...")
        
        return cleaned_df
        
    except Exception as e:
        print(f"Error processing file {file_path}: {str(e)}")
        raise

def process_year(input_base_path, output_base_path, year):
    """
    Process all CSV files for a given year and save each to an output file in a
    year-specific directory within the given output_base_path.
    """
    # Set up input and output paths using pathlib.Path
    year_input_path = Path(input_base_path) / str(year)
    year_output_path = Path(output_base_path) / str(year)
    
    # Create the output directory if it doesn't exist
    year_output_path.mkdir(parents=True, exist_ok=True)
    
    # Get all CSV files in the year directory
    csv_files = list(year_input_path.glob('*.csv'))
    
    print(f"\nProcessing {len(csv_files)} files for year {year}")
    print(f"Files found: {csv_files}")
    
    for csv_file in csv_files:
        try:
            print(f"\nProcessing file: {csv_file}")
            
            # Get original filename without path and extension
            filename = csv_file.stem
            
            # Process the file
            cleaned_df = process_csv_file(csv_file)
            
            if not cleaned_df.empty:
                # Create output filename
                output_file = year_output_path / f'cleaned_{filename}.csv'
                
                # Save to CSV
                cleaned_df.to_csv(output_file, index=False, header=False)
                
                print(f"Processed file: {csv_file}")
                print(f"Saved to: {output_file}")
                print(f"Shape: {cleaned_df.shape}") 
        except Exception as e:
            print(f"Error processing file {csv_file}: {str(e)}")

def main():
    if len(sys.argv) != 3:
        print("Usage: python script.py start_year end_year")
        sys.exit(1)
    
    try:
        start_year = int(sys.argv[1])
        end_year = int(sys.argv[2])
    except ValueError:
        print("Years must be integers")
        sys.exit(1)
        
    # Define your input and output base directories.
    # Input files remain in their original location.
    input_base_path = "/scratch/alpine/diga9728/TVarchive/Closed.Captions"
    # Processed output files will be saved under this directory:
    output_base_path = "/scratch/alpine/jasn7628/processed_output"
    
    # Create output base directory if it doesn't exist
    Path(output_base_path).mkdir(parents=True, exist_ok=True)
    
    # Process each year
    for year in range(start_year, end_year + 1):
        try:
            print(f"\nStarting processing for year {year}")
            process_year(input_base_path, output_base_path, year)
            print(f"\nCompleted processing for year {year}")
            
        except Exception as e:
            print(f"Error processing year {year}: {str(e)}")

if __name__ == "__main__":
    main()
