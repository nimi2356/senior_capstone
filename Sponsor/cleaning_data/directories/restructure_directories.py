import os
import shutil
import argparse
from pathlib import Path
from datetime import datetime

def pad_cik(cik_str):
    """Pad a CIK number to 10 digits by adding leading zeros."""
    return str(cik_str).zfill(10)

def get_first_six(full_cik):
    """Get the first 6 digits of the padded CIK for the new directory structure."""
    return full_cik[:6]

def should_process_directory(dir_name, start_range, end_range):
    """Check if the directory name falls within the specified range."""
    try:
        dir_num = int(dir_name)
        return start_range <= dir_num <= end_range
    except ValueError:
        return False

def restructure_directories(source_base, dest_base, start_range, end_range):
    """
    Restructure the CIK directories from:
    source_base/first_3/partial_cik/contents
    to:
    dest_base/first_6/full_cik/contents
    
    Only process directories between start_range and end_range (inclusive)
    """
    start_time = datetime.now()
    files_processed = 0
    dirs_processed = 0
    
    # Create destination base directory if it doesn't exist
    dest_base = Path(dest_base)
    dest_base.mkdir(parents=True, exist_ok=True)
    
    # Walk through the source directory
    source_base = Path(source_base)
    
    print(f"Starting processing of directories between {start_range} and {end_range}")
    print(f"Start time: {start_time}")
    
    for first_3_dir in sorted(source_base.iterdir()):
        if not first_3_dir.is_dir():
            continue
            
        # Check if this directory falls within our range
        if not should_process_directory(first_3_dir.name, start_range, end_range):
            continue
            
        print(f"\nProcessing directory: {first_3_dir}")
        dirs_processed += 1
        
        # Process each CIK subdirectory
        for cik_dir in first_3_dir.iterdir():
            if not cik_dir.is_dir():
                continue
                
            # Get the original partial CIK from the directory name
            partial_cik = cik_dir.name
            
            # Pad the CIK to 10 digits
            full_cik = pad_cik(partial_cik)
            
            # Get the first 6 digits for the new structure
            first_6 = get_first_six(full_cik)
            
            # Create the new directory path
            new_dir = dest_base / first_6 / full_cik
            
            # Create the new directory structure
            new_dir.mkdir(parents=True, exist_ok=True)
            
            files_in_dir = 0
            try:
                # Copy only text files
                for item in cik_dir.iterdir():
                    if item.is_file() and item.suffix.lower() in ['.txt', '']:  # Include files without extension
                        shutil.copy2(item, new_dir)
                        files_in_dir += 1
                        files_processed += 1
                
                if files_in_dir > 0:
                    print(f"  Moved {files_in_dir} files from {cik_dir} to {new_dir}")
                    
                # Print progress every 1000 files
                if files_processed % 1000 == 0:
                    elapsed_time = datetime.now() - start_time
                    print(f"\nProgress update:")
                    print(f"Files processed: {files_processed}")
                    print(f"Time elapsed: {elapsed_time}")
                    print(f"Average speed: {files_processed / elapsed_time.total_seconds():.2f} files/second")
                    
            except Exception as e:
                print(f"Error processing {cik_dir}: {str(e)}")

    end_time = datetime.now()
    elapsed_time = end_time - start_time
    
    print("\nProcessing complete!")
    print(f"Start time: {start_time}")
    print(f"End time: {end_time}")
    print(f"Total time elapsed: {elapsed_time}")
    print(f"Total directories processed: {dirs_processed}")
    print(f"Total files processed: {files_processed}")
    if elapsed_time.total_seconds() > 0:
        print(f"Average processing speed: {files_processed / elapsed_time.total_seconds():.2f} files/second")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Restructure CIK directories within a specified range.')
    parser.add_argument('--start', type=int, required=True, help='Start of directory range (inclusive)')
    parser.add_argument('--end', type=int, required=True, help='End of directory range (inclusive)')
    parser.add_argument('--source', type=str, default="/scratch/alpine/nimi2356/raw_data", help='Source directory path')
    parser.add_argument('--dest', type=str, default="/scratch/alpine/nimi2356/new_raw_data", help='Destination directory path')
    
    args = parser.parse_args()
    
    # Validate ranges
    if args.start > args.end:
        print("Error: Start range must be less than or equal to end range")
        exit(1)
    
    # Run the restructuring
    restructure_directories(args.source, args.dest, args.start, args.end)