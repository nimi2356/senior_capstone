import pandas as pd
import matplotlib.pyplot as plt

# Path to the combined CSV file
input_file = "unique_states_per_filing_with_files.csv"

# Read the updated CSV file
data = pd.read_csv(input_file, header=0, names=["File", "UniqueStatesCount"])

# Ensure UniqueStatesCount is numeric, replacing invalid values with NaN
data['UniqueStatesCount'] = pd.to_numeric(data['UniqueStatesCount'], errors='coerce')

# Print invalid rows for debugging
invalid_rows = data[pd.to_numeric(data['UniqueStatesCount'], errors='coerce').isna()]
print("Invalid rows causing issues:")
print(invalid_rows)

# Drop rows with missing or invalid values
data.dropna(subset=["File", "UniqueStatesCount"], inplace=True)

# Extract year from the file name
def extract_year(file_name):
    try:
        parts = file_name.split('-')
        if len(parts) < 2:  # Ensure there is at least one hyphen
            return None
        year_code = int(parts[1])  # Extract the year part
        if year_code >= 94:  # Years 94–99 -> 1994–1999
            return 1900 + year_code
        else:  # Years 00–24 -> 2000–2024
            return 2000 + year_code
    except (IndexError, ValueError, TypeError):  # Handle invalid file names
        return None

# Apply the extraction function to get the Year column
data['Year'] = data['File'].apply(extract_year)
data.dropna(subset=["Year"], inplace=True)

# Debug rows for 2003
data_2003 = data[data['Year'] == 2003]
print(f"Rows for 2003:\n{data_2003}")

# Convert Year to integer
data['Year'] = data['Year'].astype(int)

# Group by year and calculate the average number of unique states mentioned
yearly_data = data.groupby('Year')['UniqueStatesCount'].mean().reset_index()

# Debug: Display yearly data
print(yearly_data)

# Plot the data
plt.figure(figsize=(10, 6))
plt.plot(yearly_data['Year'], yearly_data['UniqueStatesCount'], marker='o', label='Average Unique States')
plt.title("Average Number of Unique States Mentioned Over Time (1994–2024)", fontsize=14)
plt.xlabel("Year", fontsize=12)
plt.ylabel("Average Unique States", fontsize=12)
plt.grid(alpha=0.3)
plt.legend()
plt.xticks(range(1994, 2025, 1), rotation=45)  # Show every 2 years for clarity
plt.tight_layout()

# Save the plot
plt.savefig("average_states_per_year_plot_debugged.png")
plt.show()

print("Updated plot saved as 'average_states_per_year_plot_debugged.png'")

