import os
import re
import argparse
import csv
import requests
from bs4 import BeautifulSoup

def extract_documents_and_save(soup, output_dir):
    # Find all <DOCUMENT> tags
    document_tags = soup.find_all('document')

    # Iterate through each <DOCUMENT> tag and save its content
    for i, document in enumerate(document_tags):
        document_content = re.sub(r'[^\x20-\x7E]', '', document.get_text(strip=True))
        
        # Construct the output filename
        file_name = f'document{i + 1}.txt'  # Names like document1.txt, document2.txt, etc.

        # Ensure unique filenames
        count = 1
        while os.path.exists(os.path.join(output_dir, file_name)):
            file_name = f'document{i + 1}_{count}.txt'
            count += 1
        
        output_file = os.path.join(output_dir, file_name)

        # Save the extracted document content to a new file
        with open(output_file, mode='w', encoding='utf-8') as outfile:
            outfile.write(document_content)

        print(f'Saved: {output_file}')

def process_file(file_path, output_dir):
    try:
        with open(file_path, 'r', encoding='utf-8') as infile:
            content = infile.read()
            soup = BeautifulSoup(content, 'html5lib')
            extract_documents_and_save(soup, output_dir)
    except FileNotFoundError:
        print(f"Error: The file {file_path} was not found.")
        return
    except PermissionError:
        print(f"Error: Permission denied when trying to access {file_path}.")
        return
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
        return

def main(args):
    if args.one_all == 1:
        #This section is for individually testing .txt files
        base_name = os.path.basename(args.file_path)
        name = os.path.splitext(base_name)[0]
        output_dir = os.path.join(args.directory_path, 'parsedTest')
        os.makedirs(output_dir, exist_ok=True)
        process_file(args.file_path, output_dir)
    else:
        with open(args.file_path, mode='r', newline='', encoding='utf-8') as infile:
            reader = csv.reader(infile)
            for row in reader:
                if row:  # Check if the row is not empty
                    split_elements = row[1].split('/')
    
                    # Ensure that split_elements has enough elements
                    if len(split_elements) == 7:
                        ident_CIK = split_elements[7].split('-')[-1].split('.')[0]
                        output_dir = os.path.join(args.directory_path)
                        dir_path = f'{output_dir}/parsed/{split_elements[3]}/{split_elements[4]}/{ident_CIK}/{row[1]}'
                        print(ident_CIK)
                        os.makedirs(dir_path, exist_ok=True)

                        file_name = row[1]  # Get the file name from the second column
                        #process_file(file_name, dir_path)
                    else:
                        print(f"Warning: Expected at least 3 elements, but got {len(split_elements)}: {split_elements}")

# Argument parsing
parser = argparse.ArgumentParser(description='Fetch scratch file directory path')
parser.add_argument('--file_path', type=str, required=True, help='The path to the text file or CSV file')
parser.add_argument('--directory_path', type=str, required=True, help='The path to the directory to store documents')
parser.add_argument('--one_all', type=int, required=True, help='1 to process a single file, 2 for all files from CSV')

args = parser.parse_args()

# Run the main function
main(args)
