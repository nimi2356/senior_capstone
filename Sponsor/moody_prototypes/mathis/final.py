import pandas as pd
import spacy
import sys
import re
from collections import defaultdict


nlp = spacy.load("en_core_web_sm")

# Define allowed entity types
ALLOWED_ENTITIES = {"ORG", "GPE", "PERSON", "LOC"}

def clean_text(text):
    text = re.sub(r'\s+', ' ', text).strip()
    text = re.sub(r'(\w+)-\s+(\w+)', r'\1\2', text) # Resolve hyphenated
    text = re.sub(r'(\b[A-Z][A-Z0-9& ]+)\s*:\s*', r'\n\1: ', text) # Single out section headers
    text = re.sub(r'(\d);(\d)', r'\1,\2', text) # Resolve semicolons
    text = re.sub(r'(\w)\s*;\s*(\w)', r'\1, \2', text) # Resolve semicolons
    text = re.sub(r'\band\b', '&', text) # Replace 'and' with '&'

    return text


def looks_like_name(text):
    # Check for patterns that suggest a person's name
    # Matches patterns like "J. H. Post", "John Smith", "E. M. Bulkley"
    name_pattern = re.compile(r'^(?:[A-Z][.][ ])*[A-Z][a-zA-Z]+$|^[A-Z][a-zA-Z]+(?:[ ][A-Z][.])*(?:[ ][A-Z][a-zA-Z]+)+$')
    return bool(name_pattern.match(text))

def is_obvious_non_person(text):
    non_person_keywords = {
        'Sheet', 'Stock', 'Company', 'Co.', 'Reserve', 'Trust',
        'Balance', 'Bills', 'Stocks', 'Ratings', 'City', 'York',
        'Boston', 'Capital', 'United States', 'Key'
    }
    return any(keyword in text for keyword in non_person_keywords)

def correct_person_classifications(all_results):
    df = pd.DataFrame(all_results) if not isinstance(all_results, pd.DataFrame) else all_results.copy()
    df = df.sort_values(['Year', 'ID.ON', 'sentence_id', 'token_id'])
    
    window_size = 4
    
    for i in range(len(df)):
        if df.iloc[i]['entity_type'] != 'PERSON':
            current_text = df.iloc[i]['token']
            
            # if is_obvious_non_person(current_text):
            #     continue
                
            # if not looks_like_name(current_text):
            #     continue
            
            # Get window_size entries before and after current row
            start_idx = max(0, i - window_size)
            end_idx = min(len(df), i + window_size + 1)
            
            surrounding = df.iloc[start_idx:end_idx]
            
            person_count = sum(surrounding['entity_type'] == 'PERSON')
            
            # If at least 8 surrounding entries are PERSON, change current entry to PERSON
            if person_count >= 8:
                df.iloc[i, df.columns.get_loc('entity_type')] = 'PERSON'
    
    return df


def process_text(text, year, id_on):
    results = []
    sentence_id = 0
    
    # Clean the text first
    cleaned_text = clean_text(text)
    lines = cleaned_text.split("\n")

    for line in lines:
        doc = nlp(line)
        
        # Process
        # token_id -> for each processed token in that sample, give id
        # sentence_id -> for each processed sentence, it's length, given an id. sent_idx offsets
        for sent_idx, sent in enumerate(doc.sents):
            token_id = 0
            for ent in sent.ents:
                if ent.label_ in ALLOWED_ENTITIES:
                    results.append({'Year': year, 
                                        'ID.ON': id_on, 
                                            'sentence_id': sentence_id + sent_idx, 
                                                'token_id': token_id, 'token': ent.text.strip(),
                                                    'entity_type': ent.label_})
                    token_id += 1
            
        sentence_id += len(list(doc.sents))
    
    return results


def main(input_csv):
    input_df = pd.read_csv(input_csv)
    
    # Process CSV
    all_results = []
    for idx, row in input_df.iterrows():
        results = process_text(
            text=row['text.all'],
                year=row['years.moodys'],
                    id_on=row['ids.all.seq'])
                    
        all_results.extend(results)
    
    all_results = correct_person_classifications(all_results)

    output_df = pd.DataFrame(all_results)
    output_df.to_csv('output.csv', index=False)

    print("Processed {} documents. Results saved to 'output.csv'".format(len(input_df)))

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python script.py <input_csv>")
    else:
        main(sys.argv[1])



