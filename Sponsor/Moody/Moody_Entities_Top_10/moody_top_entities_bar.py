import pandas as pd
import matplotlib.pyplot as plt
import argparse
import os

if __name__ == "__main__":

    #Gest the path for the csv file from the arguments passed
    parser = argparse.ArgumentParser(description="Bar chart of top entities")
    parser.add_argument("file_path", type=str, help="CSV file path")
    args = parser.parse_args()

    #Gets the data for the plot
    data = pd.read_csv(args.file_path)
    data['label'] = data['token'] + " (" + data['entity_type'] + ")"
    entity_counts = data.groupby('label').size().reset_index(name='count')
    top_entities = entity_counts.sort_values(by='count', ascending=False).head(10)

    #Creates the  bar chart and saves the plot
    plt.figure(figsize=(12, 6))
    plt.barh(top_entities['label'], top_entities['count'], color='skyblue')
    plt.xlabel("Total Mentions")
    plt.title(f"Top 10 {os.path.basename(args.file_path).split('.')[0].split('_')[-1]} Entities in Moody Documents")
    plt.gca().invert_yaxis()
    plt.tight_layout()
    output_file = os.path.splitext(args.file_path)[0] + "_top_entities_bar.png"
    plt.savefig(output_file)
    plt.close()

    print(f"Bar chart saved as {output_file}")