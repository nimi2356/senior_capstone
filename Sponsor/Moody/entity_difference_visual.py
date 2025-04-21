import sys
import pandas as pd
import matplotlib.pyplot as plt

def plot_entity_difference(first_csv, second_csv, entity_type):
    valid_entities = {'ORG', 'GPE', 'PERSON', 'LOC'}
    if entity_type not in valid_entities:
        raise ValueError(f"Entity type must be one of {valid_entities}")

    def load_counts(csv_file):
        df = pd.read_csv(csv_file, low_memory=False)
        df.columns = df.columns.str.strip()
        df['Year'] = pd.to_numeric(df['Year'], errors='coerce').dropna().astype(int)
        df = df[df['entity_type'] == entity_type]


        return df.groupby('Year').size()

    # Our and Diego csv
    counts1 = load_counts(first_csv)
    counts2 = load_counts(second_csv)

    # Checking to see if both csv take into account the same years
    all_years = sorted(set(counts1.index) | set(counts2.index))
    c1 = counts1.reindex(all_years, fill_value=0)
    c2 = counts2.reindex(all_years, fill_value=0)

    diff = c1 - c2

    plt.figure(figsize=(10, 6))
    plt.plot(all_years, diff, marker='o')
    plt.title(f"Yearly difference in '{entity_type}' counts (Diego – Ours)")
    plt.xlabel("Year")
    plt.ylabel("Count Difference")
    plt.grid(True)
    plt.tight_layout()


    output_filename = f'test_diff.png'
    plt.savefig(output_filename)
    plt.close()
    print(f"Plot saved as {output_filename}")



if __name__ == "__main__":
    if len(sys.argv) != 4:
        print("Usage: python entity_visualization.py <first_csv> <second_csv> <entity_type>")
        sys.exit(1)

    _, first_csv_file, second_csv_file, entity_type = sys.argv
    plot_entity_difference(first_csv_file, second_csv_file, entity_type)
