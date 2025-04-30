import matplotlib.pyplot as plt
import argparse
import os
import pandas as pd


if __name__ == "__main__":
    #Get file from arguments
    parser = argparse.ArgumentParser(description="Visualize top named entities .")
    parser.add_argument("file_path", type=str, help="CSV file path")
    args = parser.parse_args()

    #Get the dats from the csv file
    df = pd.read_csv(args.file_path)
    entity_counts = df.groupby(['Year', 'token']).size().reset_index(name='count')
    top_entities = entity_counts.groupby('token')['count'].sum().nlargest(10).index
    filtered_df = entity_counts[entity_counts['token'].isin(top_entities)]

    #Create the plot
    plt.figure(figsize=(12, 6))
    for entity in filtered_df['token'].unique():
        subset = filtered_df[filtered_df['token'] == entity]
        plt.plot(subset['Year'], subset['count'], marker='o', label=entity)

   
    plt.xlabel("Year")
    plt.ylabel("Count")
    plt.title(f"Top 10 {os.path.basename(args.file_path).split('.')[0].split('_')[-1]} Entities Over Time")
    plt.legend()
    plt.grid(True)

    #Save the line plot
    output_file = os.path.splitext(args.file_path)[0] + "_entities_plot.png"
    plt.savefig(output_file)
    plt.close()

  
    print(f"Plot saved as {output_file}")