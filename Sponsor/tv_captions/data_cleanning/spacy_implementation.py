import pandas as pd
import spacy
import json
import sys

if __name__ == '__main__':
    if len(sys.argv) != 3:
        print("Usage: python spacy_processing.py <input_csv> <output_csv>")
        sys.exit(1)

    input_csv = sys.argv[1]
    output_csv = sys.argv[2]

    df = pd.read_csv(input_csv)

    # Ensure at least three columns exist
    if len(df.columns) < 3:
        raise ValueError("CSV file must have at least three columns")

    # Load spaCy model
    nlp = spacy.load("en_core_web_sm")

    spacy_results = []

    for _, row in df.iterrows():
        col1 = row.iloc[0]  # First column (kept unchanged)
        col2 = row.iloc[1]  # Second column (kept unchanged)
        text_to_process = row.iloc[2]  # Third column (processed with spaCy)

        text_cleaned = text_to_process.replace("\n", " ")
        
        doc = nlp(str(text_cleaned))  # Ensure text is string

        # Extract named entities
        entities = [
            {
                "text": ent.text,
                "label": ent.label_,
                "start_char": ent.start_char,
                "end_char": ent.end_char
            }
            for ent in doc.ents
            if "\n" not in ent.text and ent.text != "\u266a" and ent.label != "TIME"
        ]

        spacy_results.append({
            "col1": col1,
            "col2": col2,
            "entities": json.dumps(entities)
        })

    # Save results to CSV
    spacy_df = pd.DataFrame(spacy_results)
    spacy_df.to_csv(output_csv, index=False)

    print(f"spaCy output has been saved to {output_csv}")
