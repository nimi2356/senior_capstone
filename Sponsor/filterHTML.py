import os
import argparse
import csv
import requests
from bs4 import BeautifulSoup

def extract_documents_and_save(soup, file_path, output_dir):
   # Extract content based on <TYPE> tags
    extracted_content = []

    # Read the content of the file
    with open(file_path, 'r', encoding='utf-8') as infile:
        for line in infile:
            if '<TYPE>' in line:
                extracted_text = line.split('<TYPE>', 1)[-1].strip()
                extracted_content.append(extracted_text)
    

    # Find all <DOCUMENT> tags
    document_tags = soup.find_all('document')

    # Iterate through each <DOCUMENT> tag and save its content
    for i, document in enumerate(document_tags):
        # Get the text content of the document without HTML tags
        document_content = document.get_text(strip=True)
        
        # Construct the output filename
        if i < len(extracted_content):
            base_name = extracted_content[i].replace('/', '_').replace('\\', '_')
            file_name = base_name + '.txt'

            # Ensure unique filenames
            count = 1
            while os.path.exists(os.path.join(output_dir, file_name)):
                file_name = f"{base_name}_{count}.txt"
                count += 1
            
            output_file = os.path.join(output_dir, file_name)

            # Save the extracted document content to a new file
            with open(output_file, mode='w', encoding='utf-8') as outfile:
                outfile.write(document_content)

            print(f'Saved: {output_file}')
        else:
            print(f'Warning: No corresponding <TYPE> for document {i + 1}')

def process_file(file_path, output_dir):
    try:
        with open(file_path, 'r', encoding='utf-8') as infile:
            content = infile.read() # Pass the content to BeautifulSoup
            soup = BeautifulSoup(content, 'html.parser')
    
            # Extract documents and save
            extract_documents_and_save(soup, file_path, output_dir)
    except FileNotFoundError:
        print(f"Error: The file {file_path} was not found.")
        return
    except PermissionError:
        print(f"Error: Permission denied when trying to access {file_path}.")
        return
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
        return
    with open(file_path, 'r', encoding='utf-8') as infile:
        content = infile.read()

def main(args):

    if args.one_all == 1:
         # Create output directory if it doesn't exist
        base_name = os.path.basename(args.file_path)

        # Remove the file extension
        name = os.path.splitext(base_name)[0]

        output_dir = os.path.join(args.directory_path, 'parsed_documents.' + name)
        os.makedirs(output_dir, exist_ok=True)
        process_file(args.file_path, output_dir)
    else:
        # Read the input CSV file
        with open(args.file_path, mode='r', newline='', encoding='utf-8') as infile:
            reader = csv.reader(infile)
            for row in reader:
                if row:  # Check if the row is not empty
                    base_name = os.path.basename(row[1])
                    name = os.path.splitext(base_name)[0]
                    output_dir = os.path.join(args.directory_path, 'parsed/'+ name.split('-')[0] + '/p' + base_name)
                    os.makedirs(output_dir, exist_ok=True)

                    file_name = '/' + row[1]  # Get the file name from the first column
                    process_file(file_name, output_dir)

# Argument parsing
parser = argparse.ArgumentParser(description='Fetch scratch file directory path')
parser.add_argument('--file_path', type=str, required=True, help='The path to the text file or CSV file')
parser.add_argument('--directory_path', type=str, required=True, help='The path to the directory to store documents')
parser.add_argument('--one_all', type=int, required=True, help='1 to process a single file, 2 for all files from CSV')

args = parser.parse_args()

# Run the main function
main(args)
