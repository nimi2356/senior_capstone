import os
import spacy
import csv
import argparse
from collections import Counter
from multiprocessing import Pool,cpu_count



def process_file(file_path):
    """
    Processes a single text file to extract named entities.
    Returns a Counter with entity counts.
    """
    nlp = spacy.load('en_core_web_md')
    entity_counts = Counter()
    
    print(f"Processing {file_path}")
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            text = f.read()
        # process with spaCy
        doc = nlp(text)
        # extract the entities and update the counts
        entities = [ent.text.strip() for ent in doc.ents if ent.label_ in ['PERSON', 'ORG', 'GPE', 'LOC']]
        entity_counts.update(entities)
    except Exception as e:
        print(f"Error processing {file_path}: {e}")
    
    return entity_counts

def process_files_in_parallel(input_dir, num_workers=None):
    """
    Process all text files in the directory using parallel workers.
    """
    # if num_workers is not provided, use the number of CPU cores available
    if num_workers is None:
        num_workers = cpu_count()

    all_txt_files = []
    
    # collect all .txt files
    for root, _, files in os.walk(input_dir):
        for filename in files:
            if filename.endswith('.txt'):
                all_txt_files.append(os.path.join(root, filename))
    
    # use a Pool to process files in parallel
    pool = Pool(processes=num_workers)
    results = pool.map(process_file, all_txt_files)
    pool.close()
    pool.join()

    # combine results from all workers
    combined_entity_counts = Counter()
    for result in results:
        combined_entity_counts.update(result)
    
    return combined_entity_counts

def write_to_csv(entity_counts, output_file):
    #write contents to csv file
    with open(output_file, 'w', newline='', encoding='utf-8') as csvfile:
        fieldnames = ['Entity', 'Count']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        for entity, count in entity_counts.most_common():
            writer.writerow({'Entity': entity, 'Count': count})

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--input_dir', type=str, required=True)
    parser.add_argument('--output_file', type=str, required=True)
    parser.add_argument('--num_workers', type=int, default=None, help='Number of parallel workers to use')  
    args = parser.parse_args()

    entity_counts = process_files_in_parallel(args.input_dir, args.num_workers)
    write_to_csv(entity_counts, args.output_file)
    print(f"Output written to {args.output_file}")

if __name__ == '__main__':
    main()
