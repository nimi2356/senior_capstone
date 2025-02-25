import sys
import os
import glob
import pandas as pd

def process_network(network_dir, network_name, output_dir):
    """Processes all CSVs for a given network and extracts the top 50 NORP counts."""
    csv_files = glob.glob(os.path.join(network_dir, "*.csv"))
    all_top50 = []

    for csv_file in csv_files:
        filename = os.path.basename(csv_file)
        parts = filename.split('.')
        
        # Extract year from filename
        try:
            year = parts[2]  # Assuming the pattern "cleaned_<Network>.Text.<Year>.NORP_counts.csv"
        except IndexError:
            year = "UNKNOWN"
        
        # Read CSV and standardize column names
        df = pd.read_csv(csv_file)
        df.columns = ["NORP", "Count"]
        
        # Select top 50 entities
        df_top50 = df.nlargest(50, "Count").copy()
        df_top50["Network"] = network_name
        df_top50["Year"] = year
        
        all_top50.append(df_top50)

    if all_top50:
        return pd.concat(all_top50, ignore_index=True)
    return None

def main():
    if len(sys.argv) != 3:
        print(f"Usage: {sys.argv[0]} <input_root_dir> <output_dir>")
        sys.exit(1)
        
    input_root_dir = sys.argv[1]  # e.g., "extracted_norp_counts"
    output_dir = sys.argv[2]  # Where to save the results
    os.makedirs(output_dir, exist_ok=True)

    all_networks_data = []

    # Loop through each subdirectory (network name)
    for network_name in os.listdir(input_root_dir):
        network_dir = os.path.join(input_root_dir, network_name)
        
        if os.path.isdir(network_dir):  # Ensure it's a directory
            print(f"Processing: {network_name}")
            network_data = process_network(network_dir, network_name, output_dir)
            
            if network_data is not None:
                all_networks_data.append(network_data)

    # Combine results for all networks and save
    if all_networks_data:
        final_df = pd.concat(all_networks_data, ignore_index=True)
        out_csv_path = os.path.join(output_dir, "all_networks_top50.csv")
        final_df.to_csv(out_csv_path, index=False)
        print(f"Done! Results saved to: {out_csv_path}")
    else:
        print("No valid data found!")

if __name__ == "__main__":
    main()
