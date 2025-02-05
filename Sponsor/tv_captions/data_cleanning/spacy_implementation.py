import pandas as pd
import spacy
import json

if __name__ == '__main__':
    input_csv = "cleaned_text.csv"   # created by clean_text.py
    output_csv = "spacy_output.csv"    #  spaCy output

    df = pd.read_csv(input_csv)

    # check for the 'cleaned_text' column.
    if "cleaned_text" not in df.columns:
        raise ValueError("CSV file missing 'cleaned_text' column")

    nlp = spacy.load("en_core_web_sm")

    spacy_results = []

    for article_id, row in df.iterrows():
        cleaned_text = row["cleaned_text"]
        lines = cleaned_text.split("\n")
        for line_number, line in enumerate(lines, start=1):
            doc = nlp(line)

            # extract sentences detected by spaCy.
            sentences = [sent.text for sent in doc.sents]

            # Extract token-level details.
            tokens = []
            for token in doc:
                tokens.append({
                    "text": token.text,
                    "lemma": token.lemma_,
                    "pos": token.pos_,
                    "tag": token.tag_,
                    "dep": token.dep_,
                    "head": token.head.text
                })

            entities = []
            for ent in doc.ents:
                entities.append({
                    "text": ent.text,
                    "label": ent.label_,
                    "start_char": ent.start_char,
                    "end_char": ent.end_char
                })

            spacy_results.append({
                "article_id": article_id,
                "line_number": line_number,
                "text": line,
                "sentences": json.dumps(sentences),  
                "tokens": json.dumps(tokens),         
                "entities": json.dumps(entities)       
            })

    spacy_df = pd.DataFrame(spacy_results)
    spacy_df.to_csv(output_csv, index=False)

    print(f"spaCy output has been saved to {output_csv}")
