import pandas as pd
import requests
import os

# This code pulls all quarters of all years from the Edgar database and then filters it, extracting CIK, Company Name, Form Type, Date Filed, and Filename to a csv. 
headers = {
    "User-Agent" : "Nicholas Miller (nimi2356@colorado.edu)"
}
years = range(1993,2025)
qtrs = ["QTR1", "QTR2", "QTR3", "QTR4"]

data = {
    'CIK': [],
    'Company Name': [],
    'Form Type': [],
    'Date Filed': [],
    'Filename': []
}

for year in years:
    for qtr in qtrs:
        print(year, qtr)
        file_url = r"https://www.sec.gov/Archives/edgar/full-index/{}/{}/master.idx".format(year, qtr)
        content = requests.get(file_url, headers=headers).content.decode("latin-1")
        for line in content.splitlines():
            if "10-K" in line:
                elements = line.split('|')
                assert(len(elements) == 5)
                data['CIK'].append(elements[0])
                data['Company Name'].append(elements[1])
                data['Form Type'].append(elements[2])
                data['Date Filed'].append(elements[3])
                data['Filename'].append(elements[4])

df = pd.DataFrame(data)
df.to_csv("output.csv", index=False)


# This code builders out the directory tree for EDGAR data using CIK
def DirectoryTreeBuilder(df):
    base_dir = os.getcwd()  # Get current dir change to whatever

    for _, row in df.iterrows():
        CIK = str(row['CIK'])
        sec_url = row['Filename']
        
        level_1_dir = str(CIK)[:3]  
        level_1_path = os.path.join(base_dir, level_1_dir)
        os.makedirs(level_1_path, exist_ok=True)

        level_2_dir = str(CIK)[3:]
        level_2_path = os.path.join(level_1_path, level_2_dir)
        os.makedirs(level_2_path, exist_ok=True)

        response = requests.get(sec_url, headers=headers)
        file_path = os.path.join(level_2_path, f'{CIK}.txt')

        with open(file_path, 'wb') as f:
            f.write(response.content)

DirectoryTreeBuilder(df)