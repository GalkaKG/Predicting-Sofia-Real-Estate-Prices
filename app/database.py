import pandas as pd
import psycopg2
from psycopg2 import sql

def initialize_db():
    try:
        conn = psycopg2.connect(
            dbname="real_estate",
            user="postgres",
            password="postgres",
            host="db"
        )
        cursor = conn.cursor()
        cursor.execute('''
        CREATE TABLE IF NOT EXISTS properties (
            id SERIAL PRIMARY KEY,
            location TEXT,
            price REAL,
            price_per_m2 REAL,
            currency TEXT,
            apartment_type TEXT,
            date DATE
        )
        ''')
        conn.commit()
    except Exception as e:
        print(f"Error creating table: {e}")
    finally:
        conn.close()


def insert_new_data(data):
    conn = psycopg2.connect(
        dbname="real_estate",
        user="postgres",
        password="postgres",
        host="db"
    )
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO properties (location, price, price_per_m2, currency, apartment_type, date) VALUES (%s, %s, %s, %s, %s, %s)",
        (data['location'], data['price'], data['price_per_m2'], data['currency'], data['apartment_type'], data['date'])
    )
    conn.commit()
    conn.close()

def load_csv_and_insert():
    # Load the CSV file into a pandas DataFrame
    df = pd.read_csv('data/property_prices_combined.csv')

    # Connect to the PostgreSQL database
    conn = psycopg2.connect(
        dbname="real_estate",
        user="postgres",
        password="postgres",
        host="db"
    )
    cursor = conn.cursor()

    # Iterate over each row in the DataFrame and insert it into the database
    for index, row in df.iterrows():
        cursor.execute(
            "INSERT INTO properties (location, price, price_per_m2, currency, apartment_type, date) "
            "VALUES (%s, %s, %s, %s, %s, %s)",
            (row['Район'], row['Цена'], row['Цена / кв.м.'], row['Валута'], row['Тип Апартамент'], row['Дата'])
        )
    
    # Commit the transaction and close the connection
    conn.commit()
    conn.close()
    # Read CSV data into a pandas DataFrame
    df = pd.read_csv('data/property_prices_combined.csv')

    # Clean and transform data if necessary
    df = df.rename(columns={
        'Район': 'location',
        'Цена': 'price',
        'Цена / кв.м.': 'price_per_m2',
        'Валута': 'currency',
        'Тип Апартамент': 'apartment_type',
        'Дата': 'date'
    })

    # Convert date column to the appropriate format
    df['date'] = pd.to_datetime(df['date'], format='%Y-%m-%d').dt.date

    # Insert each row into the database
    for _, row in df.iterrows():
        data = {
            'location': row['location'],
            'price': row['price'],
            'price_per_m2': row['price_per_m2'],
            'currency': row['currency'],
            'apartment_type': row['apartment_type'],
            'date': row['date']
        }
        insert_new_data(data)

def fetch_data():
    conn = psycopg2.connect(
        dbname="real_estate",
        user="postgres",
        password="postgres",
        host="db"
    )
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM properties")
    rows = cursor.fetchall()
    conn.close()
    return rows
