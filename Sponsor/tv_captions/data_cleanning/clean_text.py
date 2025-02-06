import csv
import re

def clean_text(text):
    # remove any ">>"
    text = text.replace(">>", "")
    
    # remove everything starting from the "TOPICS:" 
    if "TOPICS:" in text:
        text = text.split("TOPICS:")[0]
    
    text = re.sub(
        r'\[\[TITLE\.[^]]+\]\](.*?)((</)?\[\[TITLE\.[^]]+\]\])',
        r'\1',
        text,
        flags=re.DOTALL
    )
    
    text = re.sub(
        r'\[\[TIME\.[^]]+\]\](.*?)\[\[TIME\.[^]]+\]\]',
        lambda m: "\n" + m.group(1).strip(),
        text,
        flags=re.DOTALL
    )
    
    return text

def process_csv(input_csv, output_csv):
    with open(input_csv, newline='', encoding='utf-8') as infile, \
         open(output_csv, 'w', newline='', encoding='utf-8') as outfile:
        
        reader = csv.reader(infile)
        writer = csv.writer(outfile)
        
        for row in reader:
            if len(row) < 3:
                continue
            
            # clean just the second and third row
            row[1] = clean_text(row[1])
            row[2] = clean_text(row[2])
            
            # get the first three columns
            writer.writerow(row[:3])
    
    print(f"Processing complete. Cleaned CSV saved as '{output_csv}'.")

if __name__ == '__main__':
    input_csv = input("Enter the path to the input CSV file: ").strip()
    output_csv = input("Enter the path to the output CSV file: ").strip()
    
    process_csv(input_csv, output_csv)
