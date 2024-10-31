import os
import shutil
import sys

def copy_all_first3cik_files(src_dir, start_year, end_year, dest_dir):
    # Convert start and end year to integers
    start_year = int(start_year)
    end_year = int(end_year)
    
    # Ensure the destination directory is the specific raw_data directory
    dest_dir = os.path.join('../../scratch/alpine/nimi2356', 'raw_data')
    
    # Create the destination directory if it doesn't exist
    if not os.path.exists(dest_dir):
        os.makedirs(dest_dir)
    
    # Iterate over the range of years
    for year in range(start_year, end_year):
        year_dir = os.path.join(src_dir, str(year))
        
        # Check if the year directory exists
        if not os.path.exists(year_dir):
            print("Year directory {} does not exist, skipping.".format(year_dir))
            continue
        
        # Iterate over quarters
        for quarter in os.listdir(year_dir):
            quarter_dir = os.path.join(year_dir, quarter)
            
            # Ensure it is a directory
            if not os.path.isdir(quarter_dir):
                continue
            
            # Log progress for current year and quarter
            print("Currently working on year {} quarter {}".format(year, quarter))
            
            # Iterate over all first 3 cik directories
            for first3cik in os.listdir(quarter_dir):
                first3cik_dir = os.path.join(quarter_dir, first3cik)
                
                # Ensure it's a directory
                if not os.path.isdir(first3cik_dir):
                    continue
                
                # Now iterate over the full cik directories inside the first 3 cik directory
                for fullcik in os.listdir(first3cik_dir):
                    fullcik_dir = os.path.join(first3cik_dir, fullcik)
                    
                    # Ensure it is a directory
                    if not os.path.isdir(fullcik_dir):
                        continue
                    
                    # Destination path for the fullcik directory
                    dest_fullcik_dir = os.path.join(dest_dir, first3cik, fullcik)
                    
                    # Create the destination 'first3cik/fullcik' directory if it doesn't exist
                    if not os.path.exists(dest_fullcik_dir):
                        os.makedirs(dest_fullcik_dir)
                    
                    # Copy the files inside the 'fullcik' directory to the destination, merging without overwriting
                    for filename in os.listdir(fullcik_dir):
                        src_file = os.path.join(fullcik_dir, filename)
                        dest_file = os.path.join(dest_fullcik_dir, filename)
                        
                        # If the file doesn't already exist in the destination, copy it
                        if not os.path.exists(dest_file):
                            shutil.copy2(src_file, dest_file)
                        # Skip copying if the file already exists

if __name__ == "__main__":
    if len(sys.argv) != 4:
        print("Usage: python file.py <source_directory> <start_year> <end_year>")
        sys.exit(1)
    
    source_dir = sys.argv[1]
    start_year = sys.argv[2]
    end_year = sys.argv[3]
    destination_dir = os.path.join('../../scratch/alpine/nimi2356', "raw_data")
    
    copy_all_first3cik_files(source_dir, start_year, end_year, destination_dir)
