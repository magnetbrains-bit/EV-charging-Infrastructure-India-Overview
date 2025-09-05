import pandas as pd
from sqlalchemy import create_engine, text
from sqlalchemy.exc import SQLAlchemyError

def load_data_to_sql():
    server_name = r'LAPTOP-8GKIQJMB\SQLEXPRESS'
    database_name = 'EV_India_Analysis'
    table_name = 'ChargingStations'
    csv_file_path = 'openchargemap_stations_clean.csv'
    chunk_size = 10000

    conn_str = (
        r'mssql+pyodbc://'
        f'{server_name}/{database_name}?'
        r'driver=ODBC+Driver+17+for+SQL+Server&'
        r'trusted_connection=yes'
    )
    
    engine = create_engine(conn_str)
    processed_ids = set()

    try:
        with engine.begin() as connection:
            print(f"Clearing existing data from table '{table_name}'...")
            connection.execute(text(f'TRUNCATE TABLE {table_name}'))
            print("Table cleared.")

        print("Reading CSV and loading data to SQL Server in chunks...")
        
        chunk_iterator = pd.read_csv(csv_file_path, chunksize=chunk_size, low_memory=False)
        
        for i, chunk in enumerate(chunk_iterator):
            print(f"Processing chunk {i+1}...")
            
            chunk.columns = chunk.columns.str.replace('.', '_', regex=False)
            
            # Step 1: Remove duplicates within the current chunk first.
            chunk.drop_duplicates(subset=['ID'], keep='first', inplace=True)
            
            # Step 2: Remove duplicates that have been seen in previous chunks.
            original_rows = len(chunk)
            chunk = chunk[~chunk['ID'].isin(processed_ids)]
            new_rows = len(chunk)
            
            if original_rows > new_rows:
                print(f"  -> Removed {original_rows - new_rows} duplicate IDs found in previous chunks.")
            
            if new_rows > 0:
                processed_ids.update(chunk['ID'])
                chunk.to_sql(table_name, engine, if_exists='append', index=False)

        print("\nData loading complete.")

    except SQLAlchemyError as e:
        print(f"A database error occurred: {e}")
    except FileNotFoundError:
        print(f"Error: The file '{csv_file_path}' was not found.")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")

if __name__ == '__main__':
    load_data_to_sql()