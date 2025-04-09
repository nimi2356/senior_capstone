import sys
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

def plot_entity_counts(csv_file, entity_type):
    df = pd.read_csv(csv_file, low_memory=False)
    df.columns = df.columns.str.strip()

    # Convert the 'Year' column to numeric, set errors to NaN, drop rows with invalid years
    df['Year'] = pd.to_numeric(df['Year'], errors='coerce')
    df.dropna(subset=['Year'], inplace=True)
    df['Year'] = df['Year'].astype(int)
    
    valid_entities = {'ORG', 'GPE', 'PERSON', 'LOC'}
    if entity_type not in valid_entities:
        raise ValueError(f"Entity type must be one of {valid_entities}")


    filtered_df = df[df['entity_type'] == entity_type]
    if filtered_df.empty:
        print(f"No data found for entity type '{entity_type}' in file {csv_file}.")
        return

    
    yearly_counts = filtered_df.groupby('Year').size()
    
    
    # Fig
    plt.figure(figsize=(12, 6))
    sns.set_style("whitegrid")
    plt.plot(yearly_counts.index, yearly_counts.values, marker='o', linewidth=2)
    plt.title(f'Count of {entity_type} Entities Over Time', fontsize=14, pad=20)
    plt.xlabel('Year', fontsize=12)
    plt.ylabel(f'Number of {entity_type} Entities', fontsize=12)
    plt.xticks(rotation=45)
    
    # Add count to data points
    for x, y in zip(yearly_counts.index, yearly_counts.values):
        plt.annotate(str(y), (x, y), textcoords="offset points", xytext=(0,10), ha='center')
    
    plt.tight_layout()

    # Save just raw dogged the file name
    output_filename = f'DIEGO_{entity_type}_counts_over_time.png'
    plt.savefig(output_filename)
    plt.close()
    print(f"Plot saved as {output_filename}")



if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("Usage: python entity_visualization.py <input_csv> <entity_type>")
    else:
        csv_file = sys.argv[1]
        entity_type = sys.argv[2]
        plot_entity_counts(csv_file, entity_type)

