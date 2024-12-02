import os
import pandas as pd
import matplotlib.pyplot as plt

# Path to the existing CSV
output_csv = "unique_states_per_filing_with_files.csv"

# New directory to process
new_directory = "/scratch/alpine/rera8642/missing_parsed_data/new_parsed_data_1"  # Replace with your new directory path

# List of U.S. state names for filtering
state_names = [
    "Alabama", "Alaska", "Arizona", "Arkansas", "California", "Colorado", "Connecticut", 
    "Delaware", "Florida", "Georgia", "Hawaii", "Idaho", "Illinois", "Indiana", "Iowa", 
    "Kansas", "Kentucky", "Louisiana", "Maine", "Maryland", "Massachusetts", "Michigan", 
    "Minnesota", "Mississippi", "Missouri", "Montana", "Nebraska", "Nevada", "New Hampshire", 
    "New Jersey", "New Mexico", "New York", "North Carolina", "North Dakota", "Ohio", 
    "Oklahoma", "Oregon", "Pennsylvania", "Rhode Island", "South Carolina", "South Dakota", 
    "Tennessee", "Texas", "Utah", "Vermont", "Virginia", "Washington", "West Virginia", 
    "Wisconsin", "Wyoming"
]

# Initialize a list to store results for the new directory
new_results = []

# Process only the new directory
for root, _, files in os.walk(new_directory):
    for file in files:
        if file.startswith("entity_report_") and file.endswith(".csv"):
            file_path = os.path.join(root, file)
            try:
                # Read the entity report CSV
                data = pd.read_csv(file_path)

                # Filter for rows where Type is GPE and Entity is a valid state name
                if 'Type' in data.columns and 'Entity' in data.columns:
                    gpe_data = data[(data['Type'] == 'GPE') & (data['Entity'].isin(state_names))]

                    # Count the number of unique states mentioned in this 10-K
                    unique_states_count = gpe_data['Entity'].nunique()

                    # Store the file name and the unique state count
                    new_results.append({'File': file, 'UniqueStatesCount': unique_states_count})
            except Exception as e:
                print(f"Error processing file {file_path}: {e}")

# Convert the new results to a DataFrame
new_results_df = pd.DataFrame(new_results)

# If the existing CSV file exists, append to it
if os.path.exists(output_csv):
    existing_df = pd.read_csv(output_csv)

    # Append new results only if the files are not already present
    combined_df = pd.concat([existing_df, new_results_df], ignore_index=True)
else:
    # If no existing CSV, just save the new results
    combined_df = new_results_df

# Save the updated results to the CSV
combined_df.to_csv(output_csv, index=False)

# Generate the histogram for geographical dispersion
plt.figure(figsize=(10, 6))
plt.hist(combined_df['UniqueStatesCount'], bins=50, density=True, edgecolor='black', alpha=0.7)
plt.title("Histogram of Geographical Dispersion (Unique States per 10-K)", fontsize=14)
plt.xlabel("Number of State Names", fontsize=12)
plt.ylabel("Density", fontsize=12)
plt.grid(alpha=0.3)
plt.tight_layout()

# Save the histogram plot
plt.savefig("geographical_dispersion_per_filing_histogram_with_miss.png")
plt.show()

print("New files processed, and results appended to the existing CSV.")
