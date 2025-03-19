import os
import pandas as pd
import sys

# Ensure script is run with correct arguments
if len(sys.argv) != 3:
    print("Usage: python trading_map_script.py <input_directory> <output_directory>")
    sys.exit(1)

# Get directories from command-line arguments
input_dir = sys.argv[1]
output_dir = sys.argv[2]

# Trading symbols dictionary
trading_symbols = {
    'apple': 'AAPL', 'microsoft': 'MSFT', 'google': 'GOOG', 'alphabet': 'GOOG',
    'amazon': 'AMZN', 'ibm': 'IBM', 'intel': 'INTC', 'nvidia': 'NVDA', 'amd': 'AMD',
    'meta': 'META', 'facebook': 'META', 'twitter': 'TWTR', 'tesla': 'TSLA',
    'snap': 'SNAP', 'netflix': 'NFLX', 'oracle': 'ORCL', 'cisco': 'CSCO',
    'zoom': 'ZM', 'broadcom': 'AVGO', 'adobe': 'ADBE', 'salesforce': 'CRM',
    'paypal': 'PYPL', 'qualcomm': 'QCOM', 'micron': 'MU', 'ford': 'F',
    'general motors': 'GM', 'gm': 'GM', 'toyota': 'TM', 'honda': 'HMC',
    'nissan': 'NSANY', 'volkswagen': 'VWAGY', 'bmw': 'BMWYY', 'mercedes-benz': 'MBGYY',
    'ferrari': 'RACE', 'hyundai': 'HYMTF', 'jpmorgan': 'JPM', 'bank of america': 'BAC',
    'wells fargo': 'WFC', 'goldman sachs': 'GS', 'morgan stanley': 'MS',
    'citigroup': 'C', 'american express': 'AXP', 'visa': 'V', 'mastercard': 'MA',
    'square': 'SQ', 'charles schwab': 'SCHW', 'blackrock': 'BLK', 'bny mellon': 'BK',
    'american airlines': 'AAL', 'delta airlines': 'DAL', 'united airlines': 'UAL',
    'southwest airlines': 'LUV', 'alaska airlines': 'ALK', 'jetblue': 'JBLU',
    'ryanair': 'RYAAY', 'british airways': 'IAG.L', 'cathay pacific': 'CPCAY',
    'air canada': 'AC.TO', 'exxon': 'XOM', 'chevron': 'CVX', 'bp': 'BP', 'shell': 'SHEL',
    'total': 'TTE', 'conocophillips': 'COP', 'halliburton': 'HAL', 'baker hughes': 'BKR',
    'schlumberger': 'SLB', 'walmart': 'WMT', 'wal-mart': 'WMT', 'target': 'TGT',
    'costco': 'COST', 'mcdonalds': 'MCD', 'starbucks': 'SBUX', 'nike': 'NKE',
    'adidas': 'ADDYY', 'under armour': 'UA', 'lululemon': 'LULU', 'disney': 'DIS',
    'coca-cola': 'KO', 'pepsi': 'PEP', 'procter & gamble': 'PG', 'johnson & johnson': 'JNJ',
    'unilever': 'UL', 'nestle': 'NSRGY', 'verizon': 'VZ', 'at&t': 'T', 't-mobile': 'TMUS',
    'comcast': 'CMCSA', 'charter communications': 'CHTR', 'pfizer': 'PFE', 'moderna': 'MRNA',
    'astrazeneca': 'AZN', 'gilead sciences': 'GILD', 'merck': 'MRK',
    'bristol-myers squibb': 'BMY', 'eli lilly': 'LLY', 'novartis': 'NVS',
    'glaxosmithkline': 'GSK', 'biogen': 'BIIB', 'regeneron': 'REGN', 'boeing': 'BA',
    'airbus': 'EADSY', 'lockheed martin': 'LMT', 'raytheon': 'RTX',
    'general electric': 'GE', '3m': 'MMM', 'honeywell': 'HON', 'caterpillar': 'CAT',
    'deere': 'DE', 'dupont': 'DD', 'netflix': 'NFLX', 'disney': 'DIS',
    'warner bros discovery': 'WBD', 'comcast': 'CMCSA', 'viacomcbs': 'VIAC',
    'fox': 'FOX', 'news corp': 'NWSA', 'new york times': 'NYT', 'fedex': 'FDX',
    'ups': 'UPS', 'dhl': 'DPSGY', 'maersk': 'AMKBY', 'c.h. robinson': 'CHRW',
    'coinbase': 'COIN', 'robinhood': 'HOOD', 'block': 'SQ', 'nyse': 'ICE',
    'nasdaq': 'NDAQ', 's&p': 'SPY', 'dow jones': 'DJI', 'ftse': 'FTSE',
    'dax': 'DAX', 'nikkei': 'NIKKEI', 'hang seng': 'HSI', 'shanghai composite': '000001.SS',
    'wwe': 'WWE'
}

# Ensure the output directory exists
os.makedirs(output_dir, exist_ok=True)

# Walk through the input directory structure
for root, dirs, files in os.walk(input_dir):
    relative_path = os.path.relpath(root, input_dir)
    output_subdir = os.path.join(output_dir, relative_path)
    os.makedirs(output_subdir, exist_ok=True)

    for filename in files:
        if filename.endswith('.csv'):
            input_file = os.path.join(root, filename)
            output_file = os.path.join(output_subdir, filename)

            # Read the CSV file
            df = pd.read_csv(input_file)

            # Ensure column exists
            if 'Organization' not in df.columns:
                print(f"⚠ Skipping {input_file} (missing 'Organization' column)")
                continue

            # Handle NaN values and lowercase all organization names
            df['Organization'] = df['Organization'].fillna('').astype(str).str.lower()

            # Filter only organizations in the trading symbols list
            df = df[df['Organization'].isin(trading_symbols.keys())]

            # Map organization names to trading symbols
            df['TradingSymbol'] = df['Organization'].map(trading_symbols)

            # Save the updated CSV
            df.to_csv(output_file, index=False)

print(f"✅ Mapping complete. Updated CSVs are saved to: {output_dir}")
