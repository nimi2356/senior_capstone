import pandas as pd
import spacy
import sys
import re
from collections import defaultdict

#Load the model to use and set the entities needed
nlp = spacy.load("en_core_web_sm")
ALLOWED_ENTITIES = {"ORG", "GPE", "PERSON", "LOC"}

#If arguments necessary are present, get the input csv
if len(sys.argv) < 2:
    print("Usage: python script.py <input_csv>")
    sys.exit(1)

input_csv = sys.argv[1]
input_df = pd.read_csv(input_csv)
entity_results = defaultdict(list)

#Clean and process text and extract the named entities
for idx, row in input_df.iterrows():
    text = str(row['text.all'])
    year = row['years.moodys']
    id_on = row['ids.all.seq']
    sentence_id = 0

    text = re.sub(r'\s+', ' ', text).strip()
    text = re.sub(r'(\w+)-\s+(\w+)', r'\1\2', text) 
    text = re.sub(r'(\b[A-Z][A-Z0-9& ]+)\s*:\s*', r'\n\1: ', text) 
    text = re.sub(r'(\d);(\d)', r'\1,\2', text) 
    text = re.sub(r'(\w)\s*;\s*(\w)', r'\1, \2', text)

    lines = text.split('\n')
    for line in lines:
        doc = nlp(line)
        for sent_idx, sent in enumerate(doc.sents):
            token_id = 0
            for ent in sent.ents:
                if ent.label_ in ALLOWED_ENTITIES and ent.text.strip():
                    entity_results[ent.label_].append({
                        'Year': year,
                        'ID.ON': id_on,
                        'sentence_id': sentence_id + sent_idx,
                        'token_id': token_id,
                        'token': ent.text.strip(),
                        'entity_type': ent.label_
                    })
                    token_id += 1
        sentence_id += len(list(doc.sents))

#Save entities to their own csv file
for entity_type, records in entity_results.items():
    output_df = pd.DataFrame(records)
    filename = f"output_{entity_type}.csv"
    output_df.to_csv(filename, index=False)
    print(f"Saved {len(records)} records to '{filename}'")