import pandas as pd
import requests
from bs4 import BeautifulSoup
import os
import argparse
import time

# This code pulls all quarters of all years from the Edgar database and then filters it, extracting CIK, Company Name, Form Type, Date Filed, and Filename to a csv. 
headers = {
    "User-Agent" : "Nicholas Miller (nimi2356@colorado.edu)"
}

qtrs = ["QTR1", "QTR2", "QTR3", "QTR4"]

#params: start-year, end-year

EDGAR_URL_BASE = 'https://www.sec.gov/Archives/'

error_data = {
    'CIK': [],
    'Company Name': [],
    'Form Type': [],
    'Date Filed': [],
    'Filename': [],
    'Year': [],
    'QTR': []
}

def transform_file(file) -> str:
    return file #BROKEN
    # soup = BeautifulSoup(file, 'html.parser')
    # return soup.getText() 

def go():
    #get params
    parser = argparse.ArgumentParser(description='Fetch start and end years.')

    # Add parameters
    parser.add_argument('--startyear', type=int, required=True, help='The start year (INCLUSIVE)')
    parser.add_argument('--endyear', type=int, required=False, help='The end year (EXCLUSIVE)')
    parser.add_argument('--basedir', type=int, require=False, help='Base directory for saving the files. Defaults to .')

    # Parse the arguments
    args = parser.parse_args()

    # Access the parameters
    start_year = args.startyear
    end_year = args.endyear
    if args.basedir is None:
        base_directory = '.'
    else:
        base_directory = args.basedir

    years = []
    
    if end_year is None:
        years.append(start_year)
    else:
        if end_year - start_year == 1:
            print(f'[WARNING] Only running for {start_year} because endyear argument is exclusive')
        assert(start_year < end_year)
        years = range(start_year, end_year)

    print(f'Running for {years}, saving @ base directory: {base_directory}')

    for year in years:
        for qtr in qtrs:
            file_count = 0
            print(f'Now downloading 10-Ks for: {year}, {qtr}')
            file_url = r"https://www.sec.gov/Archives/edgar/full-index/{}/{}/master.idx".format(year, qtr)
            content = requests.get(file_url, headers=headers).content.decode("latin-1")
            print(f'{content}')
            for line in content.splitlines():
                if "10-K" in line:
                    elements = line.split('|')
                    assert(len(elements) == 5)

                    try:
                        file_count += 1
                        if file_count % 9:
                            time.sleep(1)
                        #Try downloading form. Functionalize and add retries
                        form_url = EDGAR_URL_BASE + elements[4]
                        downloaded_file = requests.get(form_url, headers=headers).content.decode() #file is type string
                    except:
                        #Form failed to download
                        print(f'[ERROR] Form download failed. Year: {year}, Quarter: {qtr}, Info: {elements}')
                        error_data['CIK'].append(elements[0])
                        error_data['Company Name'].append(elements[1])
                        error_data['Form Type'].append(elements[2])
                        error_data['Date Filed'].append(elements[3])
                        error_data['Filename'].append(elements[4])
                        error_data['Year'].append(year)
                        error_data['QTR'].append(qtr)
                        continue

                    cleaned_file = transform_file(downloaded_file)
                    file_name = elements[4].split('/')[-1]
                    dir_path = f'{base_directory}/{year}/{qtr}/{elements[0][:3]}/{elements[0]}'
                    os.makedirs(dir_path, exist_ok=True)

                    with open(f'{dir_path}/{file_name}', 'w') as f:
                        f.write(cleaned_file)
            time.sleep(30)

    df = pd.DataFrame(error_data)
    df.to_csv("error_output.csv", index=False)

go()
