#!/usr/bin/env python3
"""
Script to verify and display the date format conversions
"""

import pandas as pd

def verify_date_columns():
    """Verify the three date columns in the final dataset"""
    
    df = pd.read_csv('MarriagePaticipantsTable_Final.csv')
    
    print("=== DATE COLUMN COMPARISON ===")
    print(f"Dataset: {len(df)} rows, {len(df.columns)} columns\n")
    
    # Show the three date columns side by side
    date_comparison = df[['Citation', 'Date', 'Date_Cleaned', 'Date_ISO']].drop_duplicates().head(15)
    print("Sample of all three date formats:")
    print(date_comparison.to_string(index=False))
    
    print(f"\n=== SUMMARY STATISTICS ===")
    print(f"Original Date column - Unique values: {df['Date'].nunique()}")
    print(f"Cleaned Date column - Unique values: {df['Date_Cleaned'].nunique()}")
    print(f"ISO Date column - Unique values: {df['Date_ISO'].nunique()}")
    
    print(f"\n=== DATE RANGES ===")
    print(f"Original dates: {df['Date'].min()} to {df['Date'].max()}")
    print(f"Cleaned dates: {df['Date_Cleaned'].min()} to {df['Date_Cleaned'].max()}")
    print(f"ISO dates: {df['Date_ISO'].min()} to {df['Date_ISO'].max()}")
    
    # Check for any inconsistencies
    print(f"\n=== CONSISTENCY CHECK ===")
    # Count rows where Date != Date_Cleaned (should be the corrected ones)
    different_cleaned = len(df[df['Date'] != df['Date_Cleaned']])
    print(f"Rows where Date was corrected: {different_cleaned}")
    
    # All Date_Cleaned should have corresponding Date_ISO
    all_converted = len(df[df['Date_Cleaned'].notna() & df['Date_ISO'].notna()])
    print(f"Rows with both cleaned and ISO dates: {all_converted}")
    print(f"✅ All dates successfully converted!" if all_converted == len(df) else "⚠️ Some dates missing")

if __name__ == "__main__":
    verify_date_columns()
