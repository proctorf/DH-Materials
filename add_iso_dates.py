#!/usr/bin/env python3
"""
Script to add a column with dates converted from dd.mm.yyyy to yyyy-mm-dd format
"""

import pandas as pd
from datetime import datetime

def convert_date_format(date_string):
    """
    Convert date from dd.mm.yyyy to yyyy-mm-dd format
    
    Args:
        date_string (str): Date in dd.mm.yyyy format
    
    Returns:
        str: Date in yyyy-mm-dd format
    """
    try:
        # Parse the date from dd.mm.yyyy format
        date_obj = datetime.strptime(date_string, '%d.%m.%Y')
        # Convert to yyyy-mm-dd format
        return date_obj.strftime('%Y-%m-%d')
    except (ValueError, TypeError) as e:
        print(f"Warning: Could not convert date '{date_string}': {e}")
        return date_string  # Return original if conversion fails

def add_iso_date_column():
    """Add a new column with ISO format dates (yyyy-mm-dd)"""
    
    # Read the cleaned CSV file
    print("Reading cleaned CSV file...")
    df = pd.read_csv('MarriagePaticipantsTable_Cleaned.csv')
    
    print(f"Original dataset: {len(df)} rows, {len(df.columns)} columns")
    
    # Convert the Date_Cleaned column to ISO format
    print("Converting dates from dd.mm.yyyy to yyyy-mm-dd format...")
    df['Date_ISO'] = df['Date_Cleaned'].apply(convert_date_format)
    
    # Show some examples of the conversion
    print("\n=== CONVERSION EXAMPLES ===")
    sample_data = df[['Date_Cleaned', 'Date_ISO']].drop_duplicates().head(10)
    print(sample_data.to_string(index=False))
    
    # Check for any conversion failures
    failed_conversions = df[df['Date_Cleaned'] == df['Date_ISO']]
    if len(failed_conversions) > 0:
        print(f"\n⚠️  Warning: {len(failed_conversions)} dates could not be converted")
        unique_failed = failed_conversions['Date_Cleaned'].unique()
        print(f"Failed dates: {list(unique_failed)}")
    else:
        print("\n✅ All dates converted successfully!")
    
    # Verify the date range
    print(f"\n=== DATE RANGE VERIFICATION ===")
    print(f"Original format range: {df['Date_Cleaned'].min()} to {df['Date_Cleaned'].max()}")
    print(f"ISO format range: {df['Date_ISO'].min()} to {df['Date_ISO'].max()}")
    print(f"Unique dates: {df['Date_ISO'].nunique()}")
    
    # Save the updated dataset
    output_file = 'MarriagePaticipantsTable_Final.csv'
    print(f"\nSaving updated dataset to {output_file}...")
    df.to_csv(output_file, index=False)
    
    print(f"✅ Successfully added Date_ISO column!")
    print(f"Final dataset: {len(df)} rows, {len(df.columns)} columns")
    
    # Show column summary
    print(f"\n=== COLUMN SUMMARY ===")
    date_columns = [col for col in df.columns if 'Date' in col]
    print(f"Date-related columns: {date_columns}")
    
    return df

if __name__ == "__main__":
    df_final = add_iso_date_column()
