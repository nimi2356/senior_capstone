import os
import spacy
import csv
import argparse
from collections import Counter


def process_files(input_dir):
    """
    Processes all text files in the directory to extract named entities
    (PERSON, ORG, GPE, LOC) along with their line numbers.

    Returns a tuple of (entities_data, entity_counts):
    - entities_data: list of dictionaries with detailed information about each named entity.
    - entity_counts: Counter dictionary with each entity and its occurrence count.
    """
    nlp = spacy.load('en_core_web_md')
    entities_data = []
    entity_counts = Counter()

    for root, _, files in os.walk(input_dir):
        for filename in files:
            if filename.endswith('.txt'):
                file_path = os.path.join(root, filename)
                print(f"Processing {file_path}")
                try:
                    with open(file_path, 'r', encoding='utf-8') as f:
                        text = f.read()
                    
                    # Process with spaCy
                    doc = nlp(text)
                    
                    # Track line numbers based on character offsets
                    line_starts = [0] + [pos + 1 for pos, char in enumerate(text) if char == '\n']
                    
                    # Extract only named entities and store them in a list
                    for ent in doc.ents:
                        if ent.label_ in ['PERSON', 'ORG', 'GPE', 'LOC']:
                            # Find the line number by checking which line start is the most recent
                            line_number = next(i + 1 for i, start in enumerate(line_starts) if start > ent.start_char) - 1
                            entities_data.append({
                                'Entity': ent.text.strip(),
                                'Type': ent.label_,
                                'Line Number': line_number,
                                'Start Position': ent.start_char,
                                'End Position': ent.end_char,
                                'File': filename
                            })
                            # Update count for each entity
                            entity_counts[ent.text.strip()] += 1

                except Exception as e:
                    print(f"Error processing {file_path}: {e}")
                    continue

    return entities_data, entity_counts

def write_to_csv(entities_data, output_file):
    """
    Writes named entity details to a CSV file, including line numbers.
    """
    with open(output_file, 'w', newline='', encoding='utf-8') as csvfile:
        fieldnames = ['Entity', 'Type', 'Line Number', 'Start Position', 'End Position', 'File']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        
        for entity_data in entities_data:
            writer.writerow(entity_data)

def write_count_summary(entity_counts, count_file):
    """
    Writes the entity count summary to a CSV file.
    """
    with open(count_file, 'w', newline='', encoding='utf-8') as csvfile:
        fieldnames = ['Entity', 'Count']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        
        for entity, count in entity_counts.most_common():
            writer.writerow({'Entity': entity, 'Count': count})

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--input_dir', type=str, required=True)
    parser.add_argument('--output_file', type=str, required=True)
    parser.add_argument('--count_file', type=str, required=True, help="CSV file for entity count summary")
    args = parser.parse_args()

    entities_data, entity_counts = process_files(args.input_dir)
    write_to_csv(entities_data, args.output_file)
    write_count_summary(entity_counts, args.count_file)
    print(f"Entity details written to {args.output_file}")
    print(f"Entity count summary written to {args.count_file}")

if __name__ == '__main__':
    main()
