import spacy
from collections import defaultdict

nlp = spacy.load("en_core_web_sm")

def process_moodys_file(text):
    entity_counts = defaultdict(int)
    doc = nlp(text)
    
    for ent in doc.ents:
        if ent.label_ in ['PERSON', 'ORG', 'GPE', 'LOC']:
            entity_counts[(ent.text.strip(), ent.label_)] += 1
    
    return entity_counts

if __name__ == "__main__":
    input_file = "intermediate.txt"
    output_file = "output.txt"

    with open(input_file, "r", encoding="utf-8") as f:
        text = f.read()

    counts = process_moodys_file(text)

    with open(output_file, "w", encoding="utf-8") as f:
        for (entity, label), count in counts.items():
            f.write(f"{entity} {label} {count}\n")



# def custom_tokenizer(nlp):
#     infixes = nlp.Defaults.infixes + [r'(?<!\w)\.(?!\w)']  # Prevents breaking on periods in names
#     infix_re = spacy.util.compile_infix_regex(infixes)
#     return Tokenizer(nlp.vocab, infix_finditer=infix_re.finditer)

# nlp.tokenizer = custom_tokenizer(nlp)

# def process_moodys_file(text):
#     entity_counts = defaultdict(int)
#     doc = nlp(text)

#     for ent in doc.ents:
#         # Check if an ORG is actually a PERSON by looking for common patterns
#         if ent.label_ == "ORG":
#             tokens = [token.text for token in ent]
#             if len(tokens) <= 3 and all(token.istitle() for token in ent):  
#                 # If it's short and all words are capitalized, it's likely a name
#                 ent.label_ = "PERSON"

#         # Ensure we count corrected entities
#         if ent.label_ in ['PERSON', 'ORG', 'GPE', 'LOC']:
#             entity_counts[(ent.text.strip(), ent.label_)] += 1

#     return entity_counts
