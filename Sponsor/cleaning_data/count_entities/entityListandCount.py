import os
import spacy
import csv
import argparse
from collections import defaultdict, Counter
from multiprocessing import Pool
import multiprocessing

# Load SpaCy model globally
nlp = spacy.load('en_core_web_md')
nlp.max_length = 10_000_000  # Increase limit to handle very large documents

def process_file(file_path):
    """
    Processes a single text file to extract named entities (PERSON, ORG, GPE, LOC)
    with their line numbers and occurrences across files.
    """
    entity_data = []
    entity_counts = defaultdict(lambda: {'Count': 0, 'Documents': set()})

    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            text = f.read()

        doc = nlp(text)
        line_starts = [0] + [pos + 1 for pos, char in enumerate(text) if char == '\n']

        for ent in doc.ents:
            if ent.label_ in ['PERSON', 'ORG', 'GPE', 'LOC']:
                line_number = next(i + 1 for i, start in enumerate(line_starts) if start > ent.start_char) - 1
                entity_data.append({
                    'Entity': ent.text.strip(),
                    'Type': ent.label_,
                    'Line Number': line_number,
                    'Start Position': ent.start_char,
                    'End Position': ent.end_char,
                    'File': os.path.basename(file_path)
                })
                
                cleaned_entities = ent.text.strip().split()
                for entity in cleaned_entities:
                    key = (ent.label_, entity)
                    entity_counts[key]['Count'] += 1
                    entity_counts[key]['Documents'].add(os.path.basename(file_path))
                    
    except Exception as e:
        print(f"Error processing {file_path}: {e}")

    return entity_data, entity_counts

def aggregate_entity_counts(entity_counts_list):
    """
    Aggregates entity counts across all files.
    """
    aggregated_counts = defaultdict(lambda: {'Count': 0, 'Documents': set()})
    for entity_counts in entity_counts_list:
        for key, data in entity_counts.items():
            aggregated_counts[key]['Count'] += data['Count']
            aggregated_counts[key]['Documents'].update(data['Documents'])
    return aggregated_counts

def process_files_in_directory(directory):
    """
    Processes all text files in a given directory using multiprocessing.
    """
    txt_files = [os.path.join(directory, f) for f in os.listdir(directory) if f.endswith('.txt')]
    with Pool(multiprocessing.cpu_count()) as pool:
        results = pool.map(process_file, txt_files)

    entities_data = [data for file_data, _ in results for data in file_data]
    all_entity_counts = [count for _, count in results]
    aggregated_counts = aggregate_entity_counts(all_entity_counts)

    return entities_data, aggregated_counts

def write_to_csv(entities_data, output_file):
    """
    Writes entity details with line numbers to a CSV file.
    """
    with open(output_file, 'w', newline='', encoding='utf-8') as csvfile:
        fieldnames = ['Entity', 'Type', 'Line Number', 'Start Position', 'End Position', 'File']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        for entity_data in entities_data:
            writer.writerow(entity_data)

def write_count_summary(aggregated_counts, count_file):
    """
    Writes the entity count summary to a CSV file.
    """
    with open(count_file, 'w', newline='', encoding='utf-8') as csvfile:
        fieldnames = ['Type', 'Entity', 'Count', 'Documents']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        for (entity_type, entity), data in aggregated_counts.items():
            writer.writerow({
                'Type': entity_type,
                'Entity': entity,
                'Count': data['Count'],
                'Documents': ', '.join(data['Documents'])
            })

def find_and_process_txt_dirs(base_dir, start_range, end_range):
    """
    Finds and processes subdirectories containing .txt files within numeric directory ranges.
    """
    for root, subdirs, files in os.walk(base_dir):
        dir_name = os.path.basename(root)
        if dir_name.isdigit() and start_range <= int(dir_name) <= end_range:
            print(f"Processing directory: {root}")
            entities_data, aggregated_counts = process_files_in_directory(root)

            # Write results to CSV
            output_file = os.path.join(root, f"{dir_name}_entities.csv")
            count_file = os.path.join(root, f"{dir_name}_entity_counts.csv")
            write_to_csv(entities_data, output_file)
            write_count_summary(aggregated_counts, count_file)
            print(f"Entity details written to {output_file}")
            print(f"Entity count summary written to {count_file}")

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--input_dir', type=str, required=True, help='Parent directory with subdirectories containing text files')
    parser.add_argument('--start_range', type=int, required=True, help='Start of numeric directory range')
    parser.add_argument('--end_range', type=int, required=True, help='End of numeric directory range')
    args = parser.parse_args()

    find_and_process_txt_dirs(args.input_dir, args.start_range, args.end_range)
    print("Processing complete.")

if __name__ == '__main__':
    main()
