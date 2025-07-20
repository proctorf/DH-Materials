#!/usr/bin/env python3
"""
Script to show the differences between original and cleaned dates
"""

import pandas as pd

def show_differences():
    """Show the specific changes made during date cleaning"""
    df = pd.read_csv('MarriagePaticipantsTable_Cleaned.csv')
    
    print("=== CHANGES MADE DURING DATE CLEANING ===\n")
    
    # Find rows where Date != Date_Cleaned
    changed_rows = df[df['Date'] != df['Date_Cleaned']]
    
    if len(changed_rows) == 0:
        print("No changes were needed - all dates were already consistent!")
        return
    
    print(f"Total rows with date changes: {len(changed_rows)}")
    print(f"Total citations affected: {changed_rows['Citation'].nunique()}")
    
    # Group by citation to show changes
    print("\n=== CITATION-BY-CITATION CHANGES ===")
    
    for citation in sorted(changed_rows['Citation'].unique()):
        citation_data = df[df['Citation'] == citation]
        original_dates = citation_data['Date'].unique()
        cleaned_date = citation_data['Date_Cleaned'].iloc[0]
        
        print(f"\nCitation {citation}:")
        print(f"  Original dates: {list(original_dates)}")
        print(f"  Standardized to: {cleaned_date}")
        
        # Show count of each original date
        date_counts = citation_data['Date'].value_counts()
        print(f"  Date frequency: {dict(date_counts)}")
        print(f"  Total records in citation: {len(citation_data)}")

def verify_consistency():
    """Verify that all citations now have consistent dates"""
    df = pd.read_csv('MarriagePaticipantsTable_Cleaned.csv')
    
    print("\n=== VERIFICATION OF CONSISTENCY ===")
    
    inconsistent = []
    for citation in df['Citation'].unique():
        citation_dates = df[df['Citation'] == citation]['Date_Cleaned'].unique()
        if len(citation_dates) > 1:
            inconsistent.append((citation, citation_dates))
    
    if inconsistent:
        print(f"⚠️  Found {len(inconsistent)} citations with inconsistent cleaned dates:")
        for citation, dates in inconsistent:
            print(f"  Citation {citation}: {list(dates)}")
    else:
        print("✅ SUCCESS: All citations have consistent dates in the Date_Cleaned column!")

if __name__ == "__main__":
    show_differences()
    verify_consistency()
