#!/usr/bin/env python3
"""
Script to analyze date patterns in the marriage data and clean them
"""

import pandas as pd
from collections import Counter

def analyze_dates():
    """Analyze the current date patterns in the dataset"""
    df = pd.read_csv('MarriagePaticipantsTable_Messy.csv')
    
    print("=== DATE ANALYSIS ===")
    print(f"Total records: {len(df)}")
    print(f"Unique citations: {df['Citation'].nunique()}")
    
    print("\n=== SAMPLE CITATIONS AND DATES ===")
    sample_data = df[['Citation', 'Date']].drop_duplicates().head(15)
    print(sample_data.to_string(index=False))
    
    print("\n=== DATE PATTERNS FOR FIRST FEW CITATIONS ===")
    for cit in sorted(df['Citation'].unique())[:5]:
        print(f"\nCitation {cit}:")
        date_counts = df[df['Citation']==cit]['Date'].value_counts()
        print(date_counts.to_string())
    
    return df

def clean_dates(df):
    """Clean dates by finding the most common date for each citation"""
    print("\n=== CLEANING DATES ===")
    
    # Create a new column for cleaned dates
    df['Date_Cleaned'] = df['Date']
    
    # Group by citation and find the most common date for each
    citation_groups = df.groupby('Citation')
    
    changes_made = 0
    total_citations = 0
    
    for citation, group in citation_groups:
        total_citations += 1
        date_counts = group['Date'].value_counts()
        
        if len(date_counts) > 1:  # If there are multiple dates for this citation
            most_common_date = date_counts.index[0]  # Get the most frequent date
            print(f"Citation {citation}: Multiple dates found, using '{most_common_date}'")
            print(f"  Date distribution: {dict(date_counts)}")
            
            # Update all rows for this citation to use the most common date
            df.loc[df['Citation'] == citation, 'Date_Cleaned'] = most_common_date
            changes_made += 1
    
    print(f"\nCleaning summary:")
    print(f"- Total citations processed: {total_citations}")
    print(f"- Citations with date inconsistencies: {changes_made}")
    print(f"- Citations with consistent dates: {total_citations - changes_made}")
    
    return df

def validate_cleaning(df):
    """Validate that each citation now has consistent dates"""
    print("\n=== VALIDATION ===")
    
    inconsistent_citations = []
    for citation in df['Citation'].unique():
        citation_dates = df[df['Citation'] == citation]['Date_Cleaned'].unique()
        if len(citation_dates) > 1:
            inconsistent_citations.append(citation)
    
    if inconsistent_citations:
        print(f"⚠️  WARNING: {len(inconsistent_citations)} citations still have inconsistent dates:")
        for cit in inconsistent_citations:
            print(f"  Citation {cit}")
    else:
        print("✅ SUCCESS: All citations now have consistent dates!")
    
    # Show before/after comparison for a few examples
    print("\n=== BEFORE/AFTER COMPARISON (First 10 rows) ===")
    comparison = df[['Citation', 'Date', 'Date_Cleaned']].head(10)
    print(comparison.to_string(index=False))

def save_cleaned_data(df):
    """Save the cleaned dataset"""
    output_file = 'MarriagePaticipantsTable_Cleaned.csv'
    df.to_csv(output_file, index=False)
    print(f"\n✅ Cleaned data saved to: {output_file}")
    
    # Show some statistics
    print(f"\nDataset statistics:")
    print(f"- Total rows: {len(df)}")
    print(f"- Date range: {df['Date_Cleaned'].min()} to {df['Date_Cleaned'].max()}")
    print(f"- Unique dates: {df['Date_Cleaned'].nunique()}")
    print(f"- Unique citations: {df['Citation'].nunique()}")

if __name__ == "__main__":
    # Analyze current data
    df = analyze_dates()
    
    # Clean the dates
    df_cleaned = clean_dates(df)
    
    # Validate the cleaning
    validate_cleaning(df_cleaned)
    
    # Save the cleaned data
    save_cleaned_data(df_cleaned)
