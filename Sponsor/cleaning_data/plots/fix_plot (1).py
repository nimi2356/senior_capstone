import os
import pandas as pd
import matplotlib.pyplot as plt

# Directory where your 10-K entity files are stored
base_directory = "/scratch/alpine/luel6939/new_parsed_data_1"

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

# Initialize a list to store the results
results = []

# Traverse the directory structure to process each entity report
for root, _, files in os.walk(base_directory):
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
                    results.append({'File': file, 'UniqueStatesCount': unique_states_count})
            except Exception as e:
                print(f"Error processing file {file_path}: {e}")

# Convert the results to a DataFrame
results_df = pd.DataFrame(results)

# Generate the histogram for geographical dispersion
plt.figure(figsize=(10, 6))
plt.hist(results_df['UniqueStatesCount'], bins=50, density=True, edgecolor='black', alpha=0.7)
plt.title("Histogram of Geographical Dispersion (Unique States per 10-K)", fontsize=14)
plt.xlabel("Number of State Names", fontsize=12)
plt.ylabel("Density", fontsize=12)
plt.grid(alpha=0.3)
plt.tight_layout()

# Save the histogram plot
plt.savefig("geographical_dispersion_per_filing_histogram.png")
plt.show()

# Save the results to a CSV for further analysis
results_df.to_csv("unique_states_per_filing_with_files.csv", index=False)
print("Histogram and detailed data saved.")
