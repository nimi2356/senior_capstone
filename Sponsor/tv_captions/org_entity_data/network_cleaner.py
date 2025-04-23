import csv

def filter_networks(input_file, output_file, networks_to_exclude):
    # Convert network names to lowercase for case-insensitive comparison
    networks_lower = [network.lower() for network in networks_to_exclude]
    
    with open(input_file, 'r', newline='', encoding='utf-8') as infile, \
         open(output_file, 'w', newline='', encoding='utf-8') as outfile:
        
        reader = csv.reader(infile)
        writer = csv.writer(outfile)
        
        # Write header row to output file
        header = next(reader)
        writer.writerow(header)
        
        # Filter rows and write to output file
        for row in reader:
            if row and row[0].lower() not in networks_lower:
                writer.writerow(row)

if __name__ == "__main__":
    input_file = "all_networks_top50.csv"
    output_file = "all_networks_top_orgs_no_networks.csv"
    
    # Networks to exclude
    networks_to_exclude = ["CNBC", "MSNBC", "FBC", "Bloomberg", "CNN", "FoxNews", "Fox News"]
    
    filter_networks(input_file, output_file, networks_to_exclude)
    print(f"Filtered data saved to {output_file}")