import pandas as pd

def refine_for_powerbi():
    input_filename = 'openchargemap_stations_clean.csv'
    output_filename = 'final_for_powerbi.csv'

    columns_to_keep = [
        'ID',
        'AddressInfo_Title',
        'AddressInfo_Town',
        'AddressInfo_StateOrProvince',
        'AddressInfo_Latitude',
        'AddressInfo_Longitude',
        'OperatorInfo_Title',
        'NumberOfPoints',
        'UsageType_Title',
        'UsageCost',
        'StatusType_Title',
        'DateLastStatusUpdate'
    ]

    try:
        print(f"Reading full dataset from '{input_filename}'...")
        df = pd.read_csv(input_filename, low_memory=False)

        # Step 1: RENAME the columns first (this was the missing step)
        df.columns = df.columns.str.replace('.', '_', regex=False)

        # Step 2: Now select the columns we want to keep
        print("Selecting key columns...")
        
        existing_columns_to_keep = [col for col in columns_to_keep if col in df.columns]
        df_refined = df[existing_columns_to_keep]

        df_refined.to_csv(output_filename, index=False)
        
        print(f"\nSuccess! Refined dataset with {len(df_refined.columns)} columns and {len(df_refined)} rows saved to '{output_filename}'.")

    except FileNotFoundError:
        print(f"Error: The input file '{input_filename}' was not found.")
    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == '__main__':
    refine_for_powerbi()