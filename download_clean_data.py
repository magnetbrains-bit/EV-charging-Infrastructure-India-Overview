import pandas as pd
import requests

API_KEY = 'your_open_charge_map_api_key_here'
API_URL = 'https://api.openchargemap.io/v3/poi/'

def get_clean_station_data(api_key):
    params = {
        'output': 'json',
        'countrycode': 'IN',
        'maxresults': 2000, # Get a sizable first batch
        'key': api_key
    }
    
    print("Requesting one batch of data from Open Charge Map...")
    try:
        response = requests.get(API_URL, params=params, timeout=30)
        response.raise_for_status()
        print("Data received.")
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"An error occurred: {e}")
        return None

if __name__ == '__main__':
    if API_KEY == 'your_open_charge_map_api_key_here':
        print("Please replace 'your_open_charge_map_api_key_here' with your actual API key.")
    else:
        stations = get_clean_station_data(API_KEY)
        if stations:
            df = pd.json_normalize(stations)
            
            # Drop any duplicates within this single batch just to be safe
            df.drop_duplicates(subset=['ID'], inplace=True)
            
            output_filename = 'openchargemap_stations_clean.csv'
            df.to_csv(output_filename, index=False)
            
            print(f"\nSuccessfully downloaded {len(df)} unique charging points.")
            print(f"Clean data saved to '{output_filename}'")
        else:
            print("Could not retrieve any station data.")