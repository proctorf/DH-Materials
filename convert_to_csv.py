#!/usr/bin/env python3
"""
Script to convert Excel file to CSV format
"""

import pandas as pd
import sys
import os

def convert_excel_to_csv(excel_file, csv_file=None):
    """
    Convert an Excel file to CSV format
    
    Args:
        excel_file (str): Path to the Excel file
        csv_file (str): Path for the output CSV file (optional)
    """
    try:
        # Read the Excel file
        print(f"Reading Excel file: {excel_file}")
        df = pd.read_excel(excel_file)
        
        # Generate CSV filename if not provided
        if csv_file is None:
            base_name = os.path.splitext(excel_file)[0]
            csv_file = f"{base_name}.csv"
        
        # Convert to CSV
        print(f"Converting to CSV: {csv_file}")
        df.to_csv(csv_file, index=False)
        
        print(f"✅ Successfully converted {excel_file} to {csv_file}")
        print(f"📊 Data shape: {df.shape[0]} rows, {df.shape[1]} columns")
        
        # Show first few rows as preview
        print("\n📋 Preview of the data:")
        print(df.head())
        
    except FileNotFoundError:
        print(f"❌ Error: File '{excel_file}' not found.")
        sys.exit(1)
    except Exception as e:
        print(f"❌ Error during conversion: {str(e)}")
        sys.exit(1)

if __name__ == "__main__":
    # Convert the MarriagePaticipantsTable_Messy.xlsx file
    excel_file = "MarriagePaticipantsTable_Messy.xlsx"
    convert_excel_to_csv(excel_file)
