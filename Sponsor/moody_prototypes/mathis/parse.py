import re

def clean_text(text):
    text = re.sub(r'\s+', ' ', text).strip()
    text = re.sub(r'(\b[A-Z][A-Z0-9& ]+)\s*:\s*', r'\n\1: ', text)
    text = re.sub(r'(\d);(\d)', r'\1,\2', text)
    text = re.sub(r'(\w)\s*;\s*(\w)', r'\1, \2', text)

    return text

with open("test.txt", "r", encoding="utf-8") as file:
    raw_text = file.read()

cleaned_text = clean_text(raw_text)

with open("intermediate.txt", "w", encoding="utf-8") as file:
    file.write(cleaned_text)

print("Text cleaned and saved to 'intermediate.txt'")
