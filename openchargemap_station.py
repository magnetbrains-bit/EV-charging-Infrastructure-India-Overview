import requests
import pandas as pd

API_KEY = '8f02756d-8c77-4e16-922a-61fd07147e40'
API_URL = 'https://api.openchargemap.io/v3/poi/'

def get_all_stations_india(api_key):
    all_stations = []
    start_index = 0
    max_results = 500

    session = requests.Session()
    session.headers.update({'User-Agent': 'EVInfrastructureAnalysisProject'})

    while True:
        params = {
            'output': 'json',
            'countrycode': 'IN',
            'maxresults': max_results,
            'startindex': start_index,
            'key': api_key
        }

        print(f"Fetching data from index {start_index}...")
        
        try:
            response = session.get(API_URL, params=params, timeout=30)
            response.raise_for_status()
            data = response.json()

            if not data:
                print("No more data to fetch.")
                break

            first_item_country = data[0].get('AddressInfo', {}).get('Country', {}).get('Title')
            print(f"  --> Data check: First item in this batch is from '{first_item_country}'")

            all_stations.extend(data)
            start_index += max_results
            
            if start_index > 200000:
                print("Stopping script at safety limit of 200,000 records.")
                break

        except requests.exceptions.RequestException as e:
            print(f"An error occurred: {e}")
            break

    return all_stations

if __name__ == '__main__':
    if API_KEY == 'your_open_charge_map_api_key_here':
        print("Please replace 'your_open_charge_map_api_key_here' with your actual API key.")
    else:
        stations = get_all_stations_india(API_KEY)
        
        if stations:
            df = pd.json_normalize(stations)
            
            print(f"\nSuccessfully downloaded data for {len(df)} charging points.")
            
            output_filename = 'openchargemap_stations.csv'
            df.to_csv(output_filename, index=False)
            
            print(f"Data saved to {output_filename}")
        else:
            print("Could not retrieve any station data. Please check your API key and connection.")