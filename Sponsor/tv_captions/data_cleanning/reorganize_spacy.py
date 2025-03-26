#!/usr/bin/env python

import os
import sys
import json
import pandas as pd

def reorganize_and_expand_entities(
    source_root,
    target_root="/scratch/alpine/jasn7628/spacy_tv_final",
    years=range(2012, 2025),
    channels=("Bloomberg", "CNBC", "CNN", "FBC", "FoxNews", "MSNBC")
):
    print(f"\nSource root: {source_root}")
    print(f"Target root: {target_root}")
    print(f"Year range: {list(years)}\n")
    print(f"Channels: {channels}\n")

    os.makedirs(target_root, exist_ok=True)

    for year in years:
        year_str = str(year)
        year_dir = os.path.join(source_root, year_str)
        if not os.path.isdir(year_dir):
            print(f"[WARNING] Skipping {year_dir}, not a directory.\n")
            continue
        
        print(f"Processing directory: {year_dir}")

        csv_files = [f for f in os.listdir(year_dir) if f.lower().endswith(".csv")]
        if not csv_files:
            print(f"[INFO] No .csv files found in {year_dir}\n")
            continue
        
        for csv_file in csv_files:
            source_path = os.path.join(year_dir, csv_file)
            print(f"  Found CSV: {source_path}")

            try:
                df = pd.read_csv(source_path)
            except Exception as e:
                print(f"    [ERROR] Could not read {source_path}. Skipping. Error: {e}")
                continue
            
            if "entities" not in df.columns:
                print(f"    [WARNING] No 'entity' column in {source_path}. Skipping.\n")
                continue
            
            expanded_rows = []
            
            for idx, row in df.iterrows():
                entity_str = row["entities"]
    
                if not isinstance(entity_str, str):
                    continue
            
                try:
                    entities = json.loads(entity_str)
                except json.JSONDecodeError:
                 
                    continue
                
                
                if isinstance(entities, list):
                    for ent in entities:
                        new_row = row.to_dict()
                       
                        
                        new_row["text"] = ent.get("text", "")
                        new_row["label"] = ent.get("label", "")
                        new_row["start_char"] = ent.get("start_char", None)
                        new_row["end_char"] = ent.get("end_char", None)
                        
                        expanded_rows.append(new_row)
                else:
                    
                    continue
            
            if not expanded_rows:
                print(f"    [INFO] No valid entities parsed from {source_path}. No output written.\n")
                continue
            
            expanded_df = pd.DataFrame(expanded_rows)
            if "entities" in expanded_df.columns:
                expanded_df.drop(columns=["entities"], inplace=True)
          

            matched_channel = None
            filename_lower = csv_file.lower()
            for ch in channels:
                if ch.lower() in filename_lower:
                    matched_channel = ch
                    break
            if matched_channel is None:
                matched_channel = "Other"
            
            channel_dir = os.path.join(target_root, matched_channel)
            os.makedirs(channel_dir, exist_ok=True)
            
            output_path = os.path.join(channel_dir, csv_file)
            expanded_df.to_csv(output_path, index=False)
            print(f"    [SUCCESS] Wrote expanded CSV to: {output_path}\n")


def main():
    if len(sys.argv) < 2:
        print("ERROR: You must specify <input_dir>.\n")
        print(main.__doc__)
        sys.exit(1)
    
    input_dir = sys.argv[1]

    # Default values
    output_dir = "/scratch/alpine/jasn7628/spacy_tv_final"
    start_year = 2012
    end_year = 2024

    if len(sys.argv) >= 3:
        output_dir = sys.argv[2]
  


    reorganize_and_expand_entities(
        source_root=input_dir,
        target_root=output_dir,
        years=range(2012, 2025),
        channels=("Bloomberg", "CNBC", "CNN", "FBC", "FoxNews", "MSNBC")
    )

if __name__ == "__main__":
    main()
