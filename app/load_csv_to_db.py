import pandas as pd
from database import initialize_db, load_csv_and_insert

if __name__ == '__main__':
    # Ensure the CSV file exists in the expected directory
    csv_file_path = 'data/property_prices_combined.csv'

    try:
        # Attempt to load the CSV and insert data into the database
        print(f"Loading data from {csv_file_path} into the database...")
        initialize_db()
        load_csv_and_insert()
        print("Data loaded successfully!")
    except Exception as e:
        print(f"An error occurred: {e}")
