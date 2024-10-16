import os
import spacy
import csv
import argparse
from collections import Counter



def process_files(input_dir):
    """
    Processes all text files in the directory to extract named entities.

    Returns a dictionary with entity names as keys and counts as values.
    """
    nlp = spacy.load('en_core_web_md')
    entity_counts = Counter()

    for root, _, files in os.walk(input_dir):
        for filename in files:
            if filename.endswith('.txt'):
                file_path = os.path.join(root, filename)
                print(f"Processing {file_path}")
                try:
                    with open(file_path, 'r', encoding='utf-8') as f:
                        text = f.read()
                    #process with spaCy
                    doc = nlp(text)
                    # extract the entities and update the counts
                    entities = [ent.text.strip() for ent in doc.ents if ent.label_ in ['PERSON', 'ORG', 'GPE', 'LOC']]
                    entity_counts.update(entities)
                except Exception as e:
                    print(f"Error processing {file_path}: {e}")
                    continue

    return entity_counts

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
    args = parser.parse_args()

    entity_counts = process_files(args.input_dir)
    write_to_csv(entity_counts, args.output_file)
    print(f"Output written to {args.output_file}")

if __name__ == '__main__':
    main()
