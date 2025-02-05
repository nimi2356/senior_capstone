import re
import pandas as pd
def html_filter(text):
    text_pass_time = re.sub(
        r'\[\[TIME\.START\]\]\s*(.*?)\s*\[\[TIME\.END\]\]',
        r'\n\1\n',
        text
    )

    text_pass_talk =  re.sub(r'\s*>>\s*', '\n', text_pass_time)


    cleaned_text = "\n".join(line.strip() for line in text_pass_talk.splitlines() if line.strip())
    return cleaned_text

if __name__ == '__main__':

    input_csv = "" #input csv
    output_csv = "cleaned_text.csv" #output

    df = pd.read_csv(input_csv)

    if "column containing articles" not in df.columns:
        raise ValueError("CSV file missing text column")
    
    df["cleaned_text"] = df['column containing articles'].apply(html_filter)

    df.to_csv(output_csv, index=False)

    print(f"Cleaned text has been saved to {output_csv}")